# Branches

:::::{tab-set}
::::{tab-item} Info
- **Relative Path**: `{{ pp_meta.custom.meta[docname].path }}`
- **Pre-configured**: {{ pp_meta.custom.meta[docname].pre_config }}
::::
::::{tab-item} Schema
:::{code-block} yaml
{{ pp_meta.custom.meta[docname].schema_str }}
:::
::::
::::{tab-item} Default
:::{code-block} yaml
{{ pp_meta.custom.meta[docname].default_str }}
:::
::::
::::{tab-item} Example
:::{code-block} yaml
{{ pp_meta.custom.meta[docname].example_str }}
:::
::::
:::::

{{ pp_meta.name }} categorizes each branch of your repository into one of the following five types:
- **Release**: Release branches are the publication source for the different major versions of your package.
- **Pre-release**: Pre-release branches are transient branches that are
  the publication source for pre-release versions of your package, before they are merged into
  a release branch and published as a final release.
- **Development**: Development branches are created from a release branch,
  to apply and test changes before they are merged back into the release branch.
- **CI-pull-request**: CI-pull-request branches are created automatically by the CI/CD pipeline,
  to apply automatic updates to a branch and open a pull request for the changes.
- **Default**: The default (aka main) branch is a special case of a release branch,
  which always contains the latest version of your package.
  In addition, the `meta` content of the default branch is used as the source of truth for the entire repository.
  That is, other than some branch-specific meta contents and configurations
  (e.g., version-specific package metadata), all other configurations and data are read and applied
  from the default branch.

For each branch type,
you can specify its fullname (for default branch) or name prefix (for other branch types),
along with the branch protection rules that should be applied to it.
Changing these settings and pushing them to the remote repository's default branch will automatically
apply the corresponding changes to the entire repository, i.e., branch protection rules will be updated,
and all corresponding branches will be renamed.

All specifications are stored in the `dev/branch.yaml` file in the repository's `meta` directory.

## Default Branch
The settings for the default branch are specified under the `default` key.

:::{code-block} yaml
:caption: 🗂 `./.meta/dev/branch.yaml`
default:
  name: main
  protection_rules:
    allow_deletion: false
    allow_force_push: false
:::

## Branch Groups
For each branch group, you can specify its prefix and protection rules, under the
corresponding key in the `group` dictionary:

:::{code-block} yaml
:caption: 🗂 `./.meta/dev/branch.yaml`
group:
  ci_pull:
    prefix: ci-pull/
    protection_rules:
      allow_deletion: true
      allow_force_push: true
  dev:
    prefix: dev/
    protection_rules:
      allow_deletion: true
      allow_force_push: true
  pre_release:
    prefix: pre-release/v
    protection_rules:
      allow_deletion: false
      allow_force_push: false
  release:
    prefix: release/v
    protection_rules:
      allow_deletion: false
      allow_force_push: false
:::
