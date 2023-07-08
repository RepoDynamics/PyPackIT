## Labels
Labels are managed automatically.
To add/modify/remove a label, modify the file ./github/config/labels.yaml.
Labels are then automatically synced by the workflow ./github/workflows/labels_sync.yaml,
using the [label-syncer](https://github.com/micnncim/action-label-syncer) action.

### Dev notes 
An alternative action to consider: https://github.com/marketplace/actions/issue-label-manager-action
this has the same functionalities, but uses a JSON file for declaring labels, instead of a YAML file.

Another alternative: https://github.com/marketplace/actions/github-labeler


## Labeling PRs
We use [multi-labeler](https://github.com/fuxingloh/multi-labeler), which has support for
conventional commits, filepaths, branch names, titles, bodies and more.

GitHubs own [labeler](https://github.com/actions/labeler) action can only label PRs based on
the paths of files being changed.

[release-drafter](https://github.com/release-drafter/release-drafter) also has a PR labeling tool called
[autolabeler](https://github.com/release-drafter/release-drafter#autolabeler), which can label PRs based on
regex matches on title or body of the PR, as well as on branch name.

Other ones with support for multiple conditions, but not for conventional commits: 
https://github.com/marketplace/actions/super-labeler
https://github.com/srvaroa/labeler
https://github.com/Resnovas/label-mastermind
https://github.com/Resnovas/smartcloud

Another one: https://github.com/marketplace/actions/auto-labeler
only matches regex on title or body of PRs.


## Configurations you have to set manually after creating a repository

### Automatically Deleting Branches after Merge
https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-the-automatic-deletion-of-branches
