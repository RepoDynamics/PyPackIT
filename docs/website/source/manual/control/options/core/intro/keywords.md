# Keywords
You can add a list of keywords to describe the project by adding a `keywords` key
to the `core/intro.yaml` file:

:::{code-block} yaml
:caption: 🗂 `./.meta/core/intro.yaml`
# Project keywords
keywords:
  - python
  - github
  - packaging
  - template
  - dynamic repository
  - repository template
:::

These keywords are used in the `keywords` metadata of your package,
and by default, the `topics` section of your GitHub repository, displayed under the `About` section.
While PyPA doesn't impose any restrictions on the keywords,
GitHub requires that each keyword only contains 50 or less ASCII alphanumeric characters and hyphens.
Additionally, it must start with an alphanumeric character.
You can define other keywords in the `dev/repo.yaml` file to be used for the GitHub repository topics instead.
If you do not do so, the keywords defined in the `core/intro.yaml` file will be used instead,
and any keyword that does not conform to the GitHub requirements
will be omitted from the GitHub repository topics.