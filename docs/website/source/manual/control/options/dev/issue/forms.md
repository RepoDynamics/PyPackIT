# Forms


## Setting

For more information on the syntax for issue forms,
see the corresponding [GitHub documentation](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms).
For details on different elements that can be added to the body of an issue form,
see the GitHub documentation on [syntax for GitHub's form schema](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema).


### ID

Each form must be given a unique ID,
which must start with an alphanumeric character,
and can only contain alphanumeric characters, underscores, and hyphens;
that is, it must match the following regular expression: `^[a-zA-Z0-9][a-zA-Z0-9_-]*$`.

The issue ID is used for two purposes:
- Referencing the issue in other parts of the control center
  (see [Issue Assignees](../maintainer/index.md#issue-assignees)).
- Generating the filename of the issue template's YAML file.

::::{dropdown} Example
:::{code-block} yaml
:caption: 🗂 `.meta/dev/issue.yaml`
forms:
  - id: app_bug_api
:::
::::


### Primary Type

Each form must be assigned a primary type,
which must match the key of one of the [primary type labels](../label/index.md#primary-types),
and consequently, the key of either one of the [primary action commit types](../commit/index.md#primary-action-types),
or one of the [primary custom commit types](../commit/index.md#primary-custom-types).

This is used to correlate each issue in the repository with a primary commit type:
{{ pp_meta.name }} automatically adds the corresponding primary type label
to each issue that is created using the form.
Subsequently, when a development branch is merged into a release branch,
{{ pp_meta.name }} first determines the corresponding issue of the branch from the branch name,
and then ascertains the corresponding primary commit type from the issue's primary type label,
in order to decide which actions to perform on the release branch.

::::{dropdown} Example
:::{code-block} yaml
:caption: 🗂 `.meta/dev/issue.yaml`
forms:
  - primary_type: release_patch
:::
::::


### Subtype

If two or more forms are assigned the same [primary type](#primary-type),
they must each define a unique subtype.
The subtype must match the key of one of the [subtype labels](../label/index.md#subtypes).
{{ pp_meta.name }} automatically adds the corresponding subtype label
to each issue that is created using the form,
and uses that with conjunction with the primary type label
to unambiguously identify the form that was used to create each issue in the repository.
It also helps maintainers and users
differentiate between issues with the same primary type.

::::{dropdown} Example
:::{code-block} yaml
:caption: 🗂 `.meta/dev/issue.yaml`
forms:
  - subtype: api
:::
::::


### Name

Each form must have a unique name,
which is what is displayed to the user on the template chooser interface
when creating a new issue on GitHub.

::::{dropdown} Example
:::{code-block} yaml
:caption: 🗂 `.meta/dev/issue.yaml`
forms:
  - name: 🖥 App 🐞 Bug Report 📱 API
:::
::::


### Description

In addition to a name, each form must also have a description,
which appears below its name on the template chooser interface.

::::{dropdown} Example
:::{code-block} yaml
:caption: 🗂 `.meta/dev/issue.yaml`
forms:
  - description: |
      Report a problem (e.g., errors and unexpected results) encountered
      while using the application's Python API.
:::
::::


### Labels

Optionally, a list of additional labels can be assigned to each form,
which are then automatically added to each issue that is created using the form.
Each assigned label must exactly match the full name of an existing label in the repository,
as defined in the [label configurations](../label/index.md).

Note that the [primary type](../label/index.md#primary-types), [subtype](../label/index.md#subtypes),
and [status](../label/index.md#statuses) labels are automatically added to each issue,
and do not need to be specified here.

::::{dropdown} Example
:::{code-block} yaml
:caption: 🗂 `.meta/dev/issue.yaml`
forms:
  - labels: [ first-custom-label, second-custom-label ]
:::
::::


### Projects

Optionally, a list of projects can be specified for each form,
in which case each issue created using the issue form
is automatically added to all specified projects.
Each project must be specified in the format `PROJECT-OWNER/PROJECT-NUMBER`,
where `PROJECT-OWNER` is the username or organization name of the project owner,
and `PROJECT-NUMBER` is the number of the project in the project owner's repository.

Note that for this to work, either your project's
[auto-add workflow](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/adding-items-automatically)
must be enabled, or the person opening the issue must have write permissions for the specified projects.

::::{dropdown} Example
:::{code-block} yaml
:caption: 🗂 `.meta/dev/issue.yaml`
forms:
  - projects: [ RepoDynamics/3, AAriam/1 ]
:::
::::


### Title

Optionally, a default title can be added to each form,
which will automatically pre-populate the title field
when a user creates a new issue using the form.

::::{dropdown} Example
:::{code-block} yaml
:caption: 🗂 `.meta/dev/issue.yaml`
forms:
  - title: "API Bug: "
:::
::::


### Body

Each form must have a body, defined as an array of form elements for requesting user input.
Each form element itself is defined as a set of key-value pairs
that determine the type of the element, the properties of the element,
and the constraints you want to apply to the element.
The rules and syntax are identical to that of the
[GitHub's form schema](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema),
with several additional options and constraints:

- Each form must have a `dropdown` element whose `id` is set to either `version` or `branch`,
  and whose `options` are an array of all the supported package versions (for version)
  or active release branches (for branch) in the repository.
  The `options` can be defined dynamically, by setting it equal to
  `${‎{ package.releases.package_versions }}` (for version) or
  `${‎{ package.releases.branch_names }}` (for branch).
  It makes sense to add version to forms that concern an issue with the package,
  and branch to forms for package-independent issues.
  When branch is set, {{ pp_meta.name }} parses the the user input
  and automatically adds the corresponding [branch labels](../label/index.md#branches)
  to each issue that is created using the form.
  Similarly, when version is set, {{ pp_meta.name }} determines the branch
  hosting each selected version, and automatically adds both
  [version labels](../label/index.md#versions) and branch labels to each issue.
  During the triage process, the maintainers can add or remove version/branch labels
  as needed; for example, the user may have selected only one version where they encountered the issue,
  but during the triage process, the maintainers may determine that the issue affects multiple versions.
  Subsequently, when the issue is labeled as [in development](../label/index.md#statuses),
  {{ pp_meta.name }} automatically creates a new development branch from each branch that is labeled.
- The value of the `label` key for each element that defines it (i.e., all but the `markdown` element)
  must be unique across all form elements.
  This is needed for the [post-processing](#post-processing) step,
  since the `label` is the only way to identify each element in the issue body after it has been created.
- You can specify an additional [`pre_process`](#pre-processing) key for each element.


### Pre-Processing

Some issue forms, or some elements of an issue form, may only need to be present
when certain conditions are met. Instead of you having to manually modify issue forms
each time one of these conditions changes, {{ pp_meta.name }} allows you to dynamically
define conditions for each form and each of its elements, so that they are automatically
added/removed according to the specified conditions. This is done by adding a `pre_process`
key either to the form itself, or to specific elements of the form. The value of the
`pre_process` key must be an object with one of the following keys:
- `if_any`: The form/element is only displayed if any of the specified values evaluate to `True`.
- `if_all`: The form/element is only displayed if all of the specified values evaluate to `True`.
- `if_none`: The form/element is only displayed if none of the specified values evaluate to `True`.
- `if_equal`: The form/element is only displayed if all of the specified values are equal.

For any of the above keys, the value must be an array, where the elements of the array
can have any type (e.g., string, integer, boolean, etc.). For boolean conditions
(i.e., `if_any`, `if_all`, and `if_none`), the value of each element is cast to a boolean
in Python, thus for example, `0`, `0.0`, `""`, `[]`, `{}`, and `null` all evaluate to `False`,
while any non-zero number, non-empty string, non-empty list, and non-empty dictionary evaluates to `True`.

For example, in {{ pp_meta.name }}'s default configurations, there are three separate issue forms
defined for reporting bugs in the package's API, GUI, and CLI. However, your package may only have
some of these interfaces, in which case it makes sense to only show the corresponding issue forms
when the corresponding interfaces are present. This is achieved by adding a condition to each form.

::::{dropdown} Examples
Display a form only if the package has a GUI interface:
:::{code-block} yaml
:caption: 🗂 `.meta/dev/issue.yaml`
forms:
  - pre_process:
      if_any: [ "${‎{ package.releases.gui_scripts }}" ]
:::
Display a form only if the package has a CLI interface:
:::{code-block} yaml
:caption: 🗂 `.meta/dev/issue.yaml`
forms:
  - pre_process:
      if_any: [ "${‎{ package.releases.cli_scripts }}" ]
:::
Display an element within a form only if the package has scripts:
:::{code-block} yaml
:caption: 🗂 `.meta/dev/issue.yaml`
forms:
  - body:
      - pre_process:
          if_any: [ "${‎{ package.releases.has_scripts }}" ]
:::
::::


### Post-Processing

{{ pp_meta.name }} allows you to define post-processing instructions for each form,
which are executed after an issue is created using the form.


#### Formatting the Issue Body

Issues that are created using GitHub's issue forms are visually not very appealing,
since GitHub simply creates a new `<h3>` heading for each form element,
and adds the user input underneath, without any formatting.
Moreover, there may be some elements that are only meant for the submission step,
and are not meant to be displayed in the issue body (e.g., checkboxes for agreeing with terms and conditions).
Therefore, {{ pp_meta.name }} allows you to define a template for the issue body,
which is used to reformat the issue body after the issue is created.
The template must be defined as a string representing valid Markdown and/or HTML syntax,
where the user input for each form element is referenced (similiar to Python strings)
using the syntax `{id}`, where `id` is the `id` of the corresponding form element.

::::{dropdown} Examples

:::{code-block} yaml
:caption: 🗂 `.meta/dev/issue.yaml`
forms:
  - post_process:
      body: |
        <h2>Bug Location</h2>

        <ul>
        <li><b>Package Version</b>: {version}</li>
        <li><b>Fully Qualified Name</b>: {api_entry}</li>
        </ul>

        <h2>System and Version Specifications</h2>

        <ul>
        <li><b>Operating System</b>: {os}</li>
        <li><b>Python Version</b>: {python_version}</li>
        <li><b>Package Manager</b>: {package_manager}</li>
        <li>
        <details>
        <summary><b>Environment</b></summary>

        ```
        {environment}
        ```

        </details>
        </li>
        </ul>

        <h2>Bug Summary</h2>

        {summary}

        <h2>Unit-Test / Minimal Reproducible Example (MRE)</h2>

        {code}

        <h2>Error Message</h2>

        {log}
:::
::::


#### Adding the Issue Creator as Assignee

You may want to ask the person who created an issue whether they would like to contribute
to the resolution of the issue, and if so, add them as an assignee to the issue.
{{ pp_meta.name }} allows you to do this automatically; first you need to add a `checkbox` element
to the form, which asks the user whether they would like to be added as an assignee.
Then, add a key `assign_creator` to the `post_process` object of the form, and under that,
add a key `if_checkbox` whose value must be an object with a key `id`,
specifying the `id` of the corresponding checkbox element.
If the checkbox element has multiple checkboxes,
you can also specify the `number` of the checkbox (starting from 1) that must be checked.
Also, if you have formulated the checkbox label in a way that the creator must be added as an assignee
if the checkbox is unchecked, you can set the `is_checked` key to `False`.

::::{dropdown} Example
:::{code-block} yaml
:caption: 🗂 `.meta/dev/issue.yaml`
forms:
  - body:
      - type: checkboxes
        id: collab
        attributes:
          label: |
            Thank you again for filling this bug report.
            If you are willing to collaborate on fixing the issue,
            please select the option below.
          options:
            - label: I am willing to work on the issue and submit a pull request.
              required: false
    post_process:
      assign_creator:
        if_checkbox:
          id: collab
          number: 1  # optional, default: 1
          is_checked: true  # optional, default: true
:::
::::
