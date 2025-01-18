(manual-branching)=
# Branching


- **Main Branch**:
  A special release branch that always contains the latest final release of the library,
  while its control center settings are used as the source of truth
  for all non-version-specific project configurations.
- **Development Branches**:
  Automatically created from target release branches,
  providing an isolated environment to integrate new changes
  before merging back into target branches and deploying to production.
  Each change can be implemented in a separate development branch,
  enabling the simultaneous development of multiple orthogonal features and release candidates.
- **Prerelease Branches**:
  Automatically created from development branches for publishing
  new package versions as a prereleases.
  They facilitate the implementation and documentation of modifications
  during the prerelease period, before the final product is merged into a release branch.
- **Release Branches**:
  Each contain the latest release of an earlier major version of the library.
  They are automatically created from the main branch
  each time a backward-incompatible change is about to be merged.
  This enables proof-of-concept software libraries to rapidly evolve into mature products,
  while all major versions are automatically preserved for long-term maintenance and support.






|{{ ccc.name }}| categorizes each branch of your repository into one of the following five types:
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


(branch-protection-rules)=
## Protection Rules
