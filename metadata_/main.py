
project = {
    "name": "template_package"
}


license: [
        "GNU Affero General Public License v3 or later (AGPLv3+)",
        "GNU Affero General Public License v3",
        "GNU General Public License v3 or later (GPLv3+)",
        "GNU General Public License v3 (GPLv3)",
        "GNU Lesser General Public License v3 or later (LGPLv3+)",
        "GNU Lesser General Public License v3 (LGPLv3)",
        "MIT License",
        "Boost Software License 1.0 (BSL-1.0)",
        "BSD License",
        "The Unlicense (Unlicense)"
    ]

{

    "repo_name": "{{ cookiecutter.project_name.replace(' ', '-') }}",
    "package_name": "{{ cookiecutter.repo_name.replace('-', '_').lower() }}",
    "first_module_name": "{{ cookiecutter.package_name }}",
    "pypi_username": "{{ cookiecutter.github_username }}",

}