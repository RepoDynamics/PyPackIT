import json
import datetime
import re
import argparse
import sys
from pathlib import Path
from typing import Optional, Literal

from ruamel.yaml import YAML
import trove_classifiers

import pylinks
from pypackit import versions


class _MetadataCache:

    def __init__(self, path_cache: str | Path, cache_expiration_days: int):
        self._exp_days = cache_expiration_days
        path = Path(path_cache)
        path.mkdir(parents=True, exist_ok=True)
        self.path_metadata_cache = path / 'metadata.yaml'
        if not self.path_metadata_cache.exists():
            self.cache = dict()
        else:
            self.cache = YAML(typ='safe').load(self.path_metadata_cache)
        return

    def user(self, username: str) -> dict:
        cached_user = self.cache.setdefault('user', dict()).setdefault(username, dict())
        timestamp = cached_user.get('timestamp')
        if timestamp and not self._is_expired(timestamp):
            return cached_user['data']
        cached_user['data'] = self._user_info(username=username)
        cached_user['timestamp'] = self.now
        with open(self.path_metadata_cache, 'w') as f:
            YAML(typ='safe').dump(self.cache, f)
        return cached_user['data']

    def repo(self, username, repo_name: str) -> dict:
        cached_repo = self.cache.setdefault('repo', dict())
        timestamp = cached_repo.get('timestamp')
        if timestamp and not self._is_expired(timestamp):
            return cached_repo['data']
        repo_info = pylinks.api.github.repo(username, repo_name).info
        repo_info.pop('owner')
        cached_repo['data'] = repo_info
        cached_repo['timestamp'] = self.now
        with open(self.path_metadata_cache, 'w') as f:
            YAML(typ='safe').dump(self.cache, f)
        return cached_repo['data']

    def python_versions(self):
        cached_version = self.cache.setdefault('python_versions', dict())
        timestamp = cached_version.get('timestamp')
        if timestamp and not self._is_expired(timestamp):
            return cached_version['data']
        vers = versions.semver_from_github_tags(
            github_username='python',
            github_repo_name='cpython',
            tag_prefix='v'
        )
        minors = sorted(set([v[:2] for v in vers if v[0] >= 3]))
        cached_version['data'] = minors
        cached_version['timestamp'] = self.now
        with open(self.path_metadata_cache, 'w') as f:
            YAML(typ='safe').dump(self.cache, f)
        return cached_version['data']

    @staticmethod
    def _user_info(username) -> dict:
        user = pylinks.api.github.user(username=username)
        info = user.info
        # Get website and social accounts
        info['external_urls'] = {'website': info['blog']}
        social_accounts = user.social_accounts
        for account in social_accounts:
            if account['provider'] == 'twitter':
                info['external_urls']['twitter'] = account['url']
            elif account['provider'] == 'linkedin':
                info['external_urls']['linkedin'] = account['url']
            else:
                for url, key in [
                    ('orchid\.org', 'orcid'),
                    ('researchgate\.net/profile', 'researchgate')
                ]:
                    match = re.compile(
                        '(?:https?://)?(?:www\.)?({}/[\w\-]+)'.format(url)
                    ).fullmatch(account['url'])
                    if match:
                        info['external_urls'][key] = f"https://{match.group(1)}"
                        break
                else:
                    other_urls = info['external_urls'].setdefault('others', list())
                    other_urls.append(account['url'])
        return info

    @property
    def now(self) -> str:
        return datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y.%m.%d-%H:%M:%S")

    def _is_expired(self, timestamp: str) -> bool:
        exp_date = (
            datetime.datetime.strptime(timestamp, "%Y.%m.%d-%H:%M:%S")
            + datetime.timedelta(days=self._exp_days)
        )
        return exp_date <= datetime.datetime.now()



class Metadata:

    def __init__(
            self,
            path_root: Optional[str | Path] = None,
            path_pathfile: Optional[str | Path] = None,
            path_cache: Optional[str | Path] = None,
    ):
        self.path_root = Path(path_root).resolve() if path_root else Path.cwd().resolve()
        if not path_pathfile:
            path_pathfile = self.path_root / 'meta' / 'metadata' / 'path.yaml'
        if not isinstance(path_pathfile, (str, Path)):
            raise TypeError(
                f"Argument 'path_pathfile' must be a string or a pathlib.Path object, "
                f"but got {type(path_pathfile)}."
            )
        if isinstance(path_pathfile, Path) or (
                isinstance(path_pathfile, str) and not path_pathfile.startswith('https://')
        ):
            path_pathfile = Path(path_pathfile).resolve()
            if not path_pathfile.exists():
                raise ValueError(f"Path '{path_pathfile}' does not exist.")
            if not path_pathfile.is_file():
                raise ValueError(f"Path '{path_pathfile}' is not a file.")
            paths = YAML(typ='safe').load(path_pathfile)
        else:
            raise NotImplementedError
        self.metadata = dict()
        self.metadata['path'] = paths
        self.metadata['path']['abs'] = self._get_absolute_paths()
        for section, filepath in self.metadata['path']['abs']['meta']['metadata'].items():
            path = Path(filepath)
            if not (path.exists() and path.is_file()):
                raise ValueError(f"Metadata file '{section}' does not exist in {filepath}.")
            self.metadata[section] = dict(YAML(typ='safe').load(path))
        self.metadata['config'] = dict()
        for section, filepath in self.metadata['path']['abs']['meta']['config'].items():
            path = Path(filepath)
            if not (path.exists() and path.is_file()):
                raise ValueError(f"Config file '{section}' does not exist in {filepath}.")
            self.metadata['config'][section] = dict(YAML(typ='safe').load(path))
        self._cache = _MetadataCache(
            path_cache=path_cache or self.metadata['path']['abs']['data']['cache'],
            cache_expiration_days=self.metadata['config']['repodynamics']['cache_expiration_days']
        )
        self.fill()
        return

    def json(self, write_to_file: bool = False, output_filepath: Optional[str] = None, **json_kwargs):
        if not write_to_file:
            return json.dumps(self.metadata, **json_kwargs)
        path = Path(output_filepath).resolve() if output_filepath else (
                self.metadata['path']['abs']['data']['local_output'] / 'metadata.json'
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.metadata, f, **json_kwargs)
        return

    def fill(self):
        self.add_project_copyright_year()
        self.add_project_authors()
        self.add_project_maintainers()
        self.add_project_repo()
        self.add_project_license()
        self.add_package_development_status()
        self.add_package_python_versions()
        self.add_package_operating_systems()
        self.add_urls()
        for classifier in self.metadata['project']['trove_classifiers']:
            if classifier not in trove_classifiers.classifiers:
                raise ValueError(f"Trove classifier '{classifier}' is not supported anymore.")
        return

    def add_project_copyright_year(self):
        start_year = int(self.metadata['project']['start_year'])
        current_year = datetime.date.today().year
        if start_year < 1970 or start_year > current_year:
            raise ValueError(
                f"Project's start year must be between 1970 and {datetime.date.today().year}, "
                f"but got {start_year}."
            )
        year_range = f"{start_year}{'' if start_year == current_year else f'–{current_year}'}"
        self.metadata['project']['copyright_year'] = year_range
        return

    def add_project_authors(self):
        self.metadata['project']['authors'] = [
            self._cache.user(author) for author in self.metadata['project']['authors']
        ]
        return

    def add_project_maintainers(self):
        maintainers = dict()
        # Sort maintainers based on the number of assigned issue types, discussion categories,
        # and pull request reviews, in that order.
        for idx, role in enumerate(['issues', 'discussions']):
            for people in self.metadata['maintainer'][role].values():
                for person in people:
                    entry = maintainers.setdefault(person, [0, 0, 0])
                    entry[idx] += 1
        for codeowner_entry in self.metadata['maintainer']['pull_requests']:
            for person in codeowner_entry['reviewers']:
                entry = maintainers.setdefault(person, [0, 0, 0])
                entry[2] += 1
        # Get maintainers' GitHub info sorted in a list based on ranking
        self.metadata['project']['maintainer'] = [
            self._cache.user(maintainer)
            for maintainer, _ in sorted(sorted(maintainers.items(), key=lambda i: i[1], reverse=True))
        ]
        return

    def add_project_repo(self):
        repo_fullname = self.metadata['project']['repo']['full_name']
        repo_name_components = repo_fullname.split("/")
        if len(repo_name_components) != 2:
            raise ValueError(
                f'project.repo.full_name must be in format username/repo-name, but got {repo_fullname}.'
            )
        username, repo_name = repo_name_components
        if not re.match(r'^[A-Za-z0-9_.-]+$', repo_name):
            raise ValueError(
                "Repository names can only contain alphanumeric characters, hyphens (-), underscores (_), "
                f"and periods (.), but got {repo_name}."
            )
        self.metadata['project']['repo'] = self._cache.repo(username=username, repo_name=repo_name)
        self.metadata['project']['owner'] = self._cache.user(username=username)
        if not self.metadata['project'].get('name'):
            self.metadata['project']['name'] = self.metadata['project']['repo']['name']
        if not re.match(
                r'^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$',
                self.metadata['project']['name'],
                flags=re.IGNORECASE
        ):
            raise ValueError(
                "Project name must only consist of alphanumeric characters, period (.), "
                "underscore (_) and hyphen (-), and can only start and end with an alphanumeric character, "
                f"but got {self.metadata['project']['name']}. "
                "See https://packaging.python.org/en/latest/specifications/name-normalization/ for more details."
            )
        self.metadata['package']['name'] = re.sub(r'[._-]+', '-', self.metadata['project']['name'].lower())
        return

    def add_project_license(self):
        name = {
            'gnu_agpl_v3+': (
                'GNU AGPL v3.0+',
                'GNU Affero General Public License v3.0 or later',
                'GNU Affero General Public License v3 or later (AGPLv3+)'
            ),
            'gnu_agpl_v3': (
                'GNU AGPL v3.0',
                'GNU Affero General Public License v3.0',
                'GNU Affero General Public License v3'
            ),
            'gnu_gpl_v3+': (
                'GNU GPL v3.0+',
                'GNU General Public License v3.0 or later',
                'GNU General Public License v3 or later (GPLv3+)'
            ),
            'gnu_gpl_v3': (
                'GNU GPL v3.0',
                'GNU General Public License v3.0',
                'GNU General Public License v3 (GPLv3)'
            ),
            'mozilla_v2': (
                'MPL v2.0',
                'Mozilla Public License 2.0',
                'Mozilla Public License 2.0 (MPL 2.0)',
            ),
            'apache_v2': (
                'Apache v2.0',
                'Apache License 2.0',
                'Apache Software License'
            ),
            'mit': (
                'MIT',
                'MIT License',
                'MIT License'
            ),
            'bsd_2_clause': (
                'BSD 2-Clause',
                'BSD 2-Clause License',
                'BSD License',
            ),
            'bsd_3_clause': (
                'BSD 3-Clause',
                'BSD 3-Clause License',
                'BSD License',
            ),
            'bsl_v1': (
                'BSL v1.0',
                'Boost Software License 1.0',
                'Boost Software License 1.0 (BSL-1.0)',
            ),
            'unlicense': (
                'Unlicense',
                'The Unlicense',
                'The Unlicense (Unlicense)',
            ),
        }
        license_id = self.metadata['project']['license']['id'].lower()
        if license_id not in name:
            raise ValueError(f"License ID '{license_id}' is not supported.")
        short, long, classifier = name[license_id]
        self.metadata['project']['license']['shortname'] = short
        self.metadata['project']['license']['fullname'] = long
        self.metadata['project']['trove_classifiers'].append(f"License :: OSI Approved :: {classifier}")
        return

    def add_package_development_status(self):
        phase = {
            1: "Planning",
            2: "Pre-Alpha",
            3: "Alpha",
            4: "Beta",
            5: "Production/Stable",
            6: "Mature",
            7: "Inactive",
        }
        status_code = self.metadata['package']['development_status']
        if isinstance(status_code, str):
            status_code = int(status_code)
        if status_code not in range(1, 8):
            raise ValueError("Project development status must be an integer between 1 and 7.")
        self.metadata['project']['trove_classifiers'].append(
            f"Development Status :: {status_code} - {phase[status_code]}"
        )
        return

    def add_package_python_versions(self):
        min_ver = self.metadata['package']['python_version_min']
        ver = tuple(map(int, min_ver.split('.')))
        if ver[0] != 3:
            raise ValueError(f"Minimum Python version must be 3.x, but got {min_ver}.")
        # Get a list of all Python versions that have been released to date.
        current_python_versions = self._cache.python_versions()
        vers = [
            '.'.join(map(str, v)) for v in sorted(
                set([tuple(v[:2]) for v in current_python_versions if v[0] == 3 and v[1] >= ver[1]])
            )
        ]
        if len(vers) == 0:
            raise ValueError(f"Minimum Python version is higher than latest release version.")
        self.metadata['package']['python_versions'] = vers
        self.metadata['package']['python_versions_cibuild'] = [ver.replace('.', '') for ver in vers]
        # Add trove classifiers
        classifiers = [
            "Programming Language :: Python :: {}".format(postfix) for postfix in ["3 :: Only"] + vers
        ]
        self.metadata['project']['trove_classifiers'].extend(classifiers)
        return

    def add_package_operating_systems(self):
        trove_classifiers_postfix = {
            'windows': 'Microsoft :: Windows',
            'macos': 'MacOS',
            'linux': 'POSIX :: Linux',
            'independent': 'OS Independent',
        }
        trove_classifier_template = "Operating System :: {}"
        github_os_matrix = []
        build_matrix = []
        for os in self.metadata['package']['operating_systems']:
            os_id = os['id'].lower()
            if os_id not in ['linux', 'macos', 'windows']:
                raise ValueError(
                    f"Operating system ID '{os_id}' is not supported. "
                    "Supported operating system IDs are 'linux', 'macos', and 'windows'."
                )
            self.metadata['project']['trove_classifiers'].append(
                trove_classifier_template.format(trove_classifiers_postfix[os_id])
            )
            github_runner = f"{os_id if os_id != 'linux' else 'ubuntu'}-latest"
            github_os_matrix.append(github_runner)
            if os['cibuilds']:
                for cibuild in os['cibuilds']:
                    build_matrix.append((github_runner, cibuild))
        self.metadata['package']['github_runners'] = github_os_matrix
        self.metadata['package']['build_matrix'] = build_matrix
        is_pure_python = False
        self.metadata['package']['is_pure_python'] = is_pure_python
        if is_pure_python:
            self.metadata['project']['trove_classifiers'].append(
                trove_classifier_template.format(trove_classifiers_postfix['independent'])
            )
        return

    def add_urls(self):
        urls = dict(github=dict(), website=dict())

        urls['github']['home'] = self.metadata['project']['repo']['html_url']

        # Main sections
        for key in ['issues', 'pulls', 'discussions', 'actions', 'releases', 'security']:
            urls['github'][key] = {'home': f"{urls['github']['home']}/{key}"}

        urls['github']['tree'] = (
            f"{self.metadata['project']['repo']['html_url']}/"
            f"tree/{self.metadata['project']['repo']['default_branch']}"
        )
        urls['github']['raw'] = (
            f"https://raw.githubusercontent.com/{self.metadata['project']['repo']['full_name']}/"
            f"{self.metadata['project']['repo']['default_branch']}"
        )

        # Issues
        urls['github']['issues']['template_chooser'] = f"{urls['github']['issues']['home']}/new/choose"
        urls['github']['issues']['new'] = {
            issue_type: f"{urls['github']['issues']['home']}/new?template={idx+1:02}_{issue_type}.yaml"
            for idx, issue_type in enumerate(
                [
                    'app_bug_setup',
                    'app_bug_api',
                    'app_request_enhancement',
                    'app_request_feature',
                    'app_request_change',
                    'docs_bug_content',
                    'docs_bug_site',
                    'docs_request_content',
                    'docs_request_feature',
                    'tests_bug',
                    'tests_request',
                    'devops_bug',
                    'devops_request',
                    'maintenance_request',
                ]
            )
        }

        # Security
        urls['github']['security']['policy'] = f"{urls['github']['security']['home']}/policy"
        urls['github']['security']['advisories'] = f"{urls['github']['security']['home']}/advisories"
        urls['github']['security']['new_advisory'] = f"{urls['github']['security']['advisories']}/new"

        urls['website'] = dict()
        urls['website']['home'] = (
            f"https://{self.metadata['website']['rtd_name']}.readthedocs.io/en/latest"
            if self.metadata['website'].get('rtd_name') else
            (
                f"https://{self.metadata['project']['owner']['login']}.github.io"
                f"""{"" if self.metadata['website']['is_gh_user_site'] else f"/{self.metadata['project']['github']['name']}"}"""
            )
        )

        urls['website']['base'] = urls['website']['home']  # TODO

        urls['announcement'] = (
            f"https://raw.githubusercontent.com/{self.metadata['project']['repo']['full_name']}/"
            f"{self.metadata['project']['repo']['default_branch']}/"
            f"{self.metadata['path']['docs']['website']['announcement']}"
        )
        urls['contributors'] = f"{urls['website']['home']}/about#contributors"
        urls['contributing'] = f"{urls['website']['home']}/contribute"
        urls['license'] = f"{urls['website']['home']}/license"
        urls['security_measures'] = f"{urls['website']['home']}/contribute/collaborate/maintain/security"


        urls['pypi'] = f"https://pypi.org/project/{self.metadata['package']['name']}/"
        self.metadata['url'] = urls
        return

    def _get_absolute_paths(self):
        def recursive(dic, new_dic):
            for key, val in dic.items():
                if isinstance(val, str):
                    new_dic[key] = str(self.path_root / val)
                else:
                    new_dic[key] = recursive(val, dict())
            return new_dic
        return recursive(self.metadata['path'], dict())


def metadata(
    path_root: Optional[str | Path] = None,
    path_pathfile: Optional[str | Path] = None,
    path_cache: Optional[str | Path] = None,
) -> dict:
    return Metadata(path_root=path_root, path_pathfile=path_pathfile, path_cache=path_cache).metadata


def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=str, help="Path to the root directory.", required=False)
    parser.add_argument('--pathfile', type=str, help="Path to the paths metadata file.", required=False)
    parser.add_argument('--cachefile', type=str, help="Path for the cache metadata file.", required=False)
    parser.add_argument('--output', type=str, help="Path for the output metadata file.", required=False)
    parser.add_argument('--output_pretty', type=str, help="Path for the pretty formatted output metadata file.", required=False)
    args = parser.parse_args()
    try:
        meta = Metadata(path_root=args.root, path_pathfile=args.pathfile, path_cache=args.cachefile)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    # print(meta.json())
    meta.json(write_to_file=True, output_filepath=args.output)
    meta.json(write_to_file=True, output_filepath=args.output_pretty, indent=4)
    return


if __name__ == '__main__':
    __main__()

