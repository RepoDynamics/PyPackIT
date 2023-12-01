# Authors
You can declare the core authors of your project, and optionally their roles,
by adding an `author` key to the `core/credits.yaml` file.

## Authors Roles
To assign roles to authors, you must first declare these roles under the `role` key
of the `author` object. The value of the `role` key must be an object,
where the keys are the IDs of the roles (to be assigned to authors),
and the values are objects containing the following keys:
- `title`: The name of the role.
- `description`: A short description of the role.
- `abbreviation`: An abbreviation for the role.

Example:
:::{code-block} yaml
:caption: 🗂 `./.meta/core/credits.yaml`
author:
  role:
    concept:
      title: Conceptualization
      description: Development of the initial idea for the project.
      abbreviation: CNCPT
    dev:
      title: Software Development
      description: Implementation of the project.
      abbreviation: DEV
    maint:
      title: Maintenance
      description: Maintenance of the project.
      abbreviation: MAINT
:::


## Authors List
To declare the authors of your project, add a key `entries` to the `author` object,
where the value is an array of objects, each declaring a single author.
Each object must contain a key `username` with the GitHub username of the author,
and optionally a key `roles` with the IDs of the roles assigned to the author.

Example:
:::{code-block} yaml
:caption: 🗂 `./.meta/core/credits.yaml`
author:
  entries:
    - username: ${‎{ owner.username }}
      roles: [ concept, dev, maint ]
    - username: RepoDynamicsBot
      roles: [ maint ]
:::

