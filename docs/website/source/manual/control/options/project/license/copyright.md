# Copyright
By default, PyPackIT uses the creation date of your repository,
and the name of the repository owner (set in their GitHub account),
to generate a copyright notice, which is used in README files and on your website.
The notice is of the form `{START-YEAR}–{CURRENT-YEAR} {OWNER-NAME}` (e.g. `2023–2024 John Doe`)
when the repository creation year is not the same as the current year,
and `{CURRENT-YEAR} {OWNER-NAME}` (e.g. `2024 John Doe`) otherwise.
You can customize this notice by setting the following keys under the `copyright` key:
- `year_start`: The start year of the project to use instead of the repository creation year.
- `owner`: The name of the project owner to use instead of the repository owner name.

:::{code-block} yaml
:caption: 🗂 `./.meta/core/license.yaml`
copyright:
  year_start: 2020
  owner: Jane Doe
:::
