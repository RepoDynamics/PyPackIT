# Quickstart

This quickstart guide demonstrates a simple iteration cycle with |{{ ccc.name }}|.
In general, every change in the project starts by opening an issue ticket:

1. To [open a new issue ticket](){.user-link-repo-issues-choose},
   click on the {bdg-success}`New issue` button in the [Issues](){.user-link-repo-issues}
   section of the repository.
2. Select the appropriate issue type from the list, and click on the {bdg-success}`Get started` button.
3. Fill in the issue form with relevant information, and click on the {bdg-success}`Submit new issue` button.

Under the repository's [Actions](){.user-link-repo-actions} tab,
you will see that a new workflow run has been started to process the submitted issue ticket.
This will automatically add all relevant labels to the issue, assign it to specified team members,
and generate a development protocol. Once finished, the submitted ticket will be replaced
with the generated protocol.

It is now the job of the assigned team members to triage the submitted ticket and
devise a plan:

4. Add relevant triage documentation under the specified section in the development protocol.
5. Depending on the triage decision, change the status label of ticket.
   If you do not plan to implement the issue, change its label to one of `rejected`, `duplicate`, or `invalid`.
   This will automatically close the issue. Otherwise, change the label to `planning`.
   You will see that the old status label is automatically removed, and the Status section
   of the protocol is updated to reflect the current progress.
6. When the issue is ready for implementation, change the status label to `implementation`

Another workflow run will be triggered, performing the following automated tasks:
- A development branch is created from each affected base branch, and a new ongoing changelog entry is added
  with data from the development protocol and the issue ticket.
- For each development branch, a draft pull request is created with an added implementation protocol,
  and labeled and assigned to specified team members accordingly.

It is now the job of the assigned team members to devise an implementation tasklist:

7. Edit the pull request protocol to add tasks under the specified section.
8. Start implementing the changes in the created development branch.
9. When a specified task is finished, commit the changes with a commit message matching the respective task in the tasklist.

The pull request protocol is automatically updated to reflect the progress in the development branch.
When all tasks are complete, |{{ ccc.name }}| automatically un-drafts the pull request
and assigns specified team members to review the pull request.
For every push to the development branch, CI pipelines are run and their results are shown
on the pull request page. After approvals by reviewers, the status label of the pull request
can be changed to one of `alpha release`, `beta release`, `release candidate`, or `final release`.
|{{ ccc.name }}| will then automatically merge the pull request into the base branch
and publish a new release.


<!--

Every change in the repository is initiated by opening an issue.
Each issue form is linked to a specific primary commit type.
In addition, each issue form has a field where the person submitting the issue can specify
the package versions (for package-related issues) or the branches (for non-package-related issues)
the issue is related to.
When an issue is submitted, |{{ ccc.name }}| will carry out the following tasks:
1. Add a type label to the issue, specifying the primary commit type.
2. Add a subtype label to the issue, if specified in the issue form.
3. Add branch labels to the issue, specifying the target branches according to the user specification
   in the issue form. If the issue form specifies the target package versions instead of target branches,
   version labels are added in addition to the corresponding branch labels,
   which are automatically detected from the specified versions.
4. Add a `triage` status label, indicating that the issue is awaiting triage.
5. Post process the issue body according to the specifications in the issue form, if specified.
6. Add assignees to the issue, if specified.

After an issue is opened, the assignees (or any other maintainer of the project) must triage the issue
and then change its status label from `triage` to one of the following:
- `invalid`: The issue is not valid. Adding this label will automatically close the issue with
  the `not_planned` state reason.
- `duplicate`: The issue is a duplicate of another issue. Adding this label will automatically close
  the issue with the `not_planned` state reason.
- `rejected`: The issue is valid and not a duplicate, but the proposed changes are not accepted.
  Adding this label will automatically close the issue with the `not_planned` state reason.
- `discuss`: The issue requires more discussion before it can be planned.
  Adding this label will signal to other maintainers to join the discussion.
- `need_volunteer`: The issue is valid and accepted, but no one is available to work on it.
  Adding this label will signal to other maintainers and outside collaborators that the issue is ready
  to be worked on by a volunteer.
- `queued`: The issue is accepted and has a volunteer, but is not yet ready to be worked on.
  Adding this label will signal to other maintainers and outside collaborators that the issue is being
  worked on, and that they should not start working on it.
- `in_dev`: The issue is accepted and being worked on.

When the issue is accepted and ready to be worked on, its status label must be changed to `in_dev`.
Before doing so, the maintainer must make sure that the branch labels of the issue are correct (i.e.,
the user specification in the issue form is consistent with the actual target branches of the issue),
and add or delete branch labels as necessary.

Changing the status label of an issue to `in_dev` will then automatically carry out the following tasks:
1. Create a new development branch from each of the issue's

-->
