# Development Cycle

Every change in the repository is initiated by opening an issue.
Each issue form is linked to a specific primary commit type.
In addition, each issue form has a field where the person submitting the issue can specify
the package versions (for package-related issues) or the branches (for non-package-related issues)
the issue is related to.
When an issue is submitted, {{ pp_meta.name }} will carry out the following tasks:
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
