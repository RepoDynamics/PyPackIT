# Branch Types
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
  In addition, the meta content of the default branch is used as the source of truth for the entire repository.
  That is, other than some branch-specific meta contents and configurations
  (e.g., version-specific package metadata), all other configurations and data are read and applied
  from the default branch.
