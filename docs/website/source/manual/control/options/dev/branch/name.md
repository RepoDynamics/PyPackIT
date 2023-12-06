# Names


## Setting
For each branch type,
you can specify its fullname (for default branch) or name prefix (for other branch types),
along with the branch protection rules that should be applied to it.
Changing these settings and pushing them to the remote repository's default branch will automatically
apply the corresponding changes to the entire repository, i.e., branch protection rules will be updated,
and all corresponding branches will be renamed.



### Default Branch
The settings for the default branch are specified under the `default` key.

:::{code-block} yaml
:caption: 🗂 `./.meta/dev/branch.yaml`
default:
  name: main
  protection_rules:
    allow_deletion: false
    allow_force_push: false
:::

### Branch Groups
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


## Usage
