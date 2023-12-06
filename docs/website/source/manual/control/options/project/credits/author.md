# Authors
{{ pp_meta.name }} allows you to centrally declare the authors of your project
and their roles, which are then used in various places,
including your package and its documentation.


## Setting
You can declare the core authors of your project, and optionally their roles,
via the `author` key of the `project/credits.yaml` file.

### Authors Roles
To assign roles to authors, you must first declare these roles under the `role` key
of the `author` object. The value of the `role` key must be an object,
where the keys are the IDs of the roles (to be assigned to authors),
and the values are objects with the following keys:

:title: ***string***

  The name of the role.

:description: ***string***

  A short description of the role.

:abbreviation: ***string***

  An abbreviation for the role.


::::{dropdown} Example

:::{code-block} yaml
:caption: 🗂 `project/credits.yaml`
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

::::


### Authors List
To declare the authors of your project, add a key `entries` to the `author` object,
where the value is an array of objects, each declaring a single author.
Each object has the following keys:

:username: ***string***

  The GitHub username of the author.

:roles: ***array***, ***optional***

  IDs of the roles assigned to the author.


::::{dropdown} Example

:::{code-block} yaml
:caption: 🗂 `./.meta/core/credits.yaml`
author:
  entries:
    - username: ${‎{ owner.username }}
      roles: [ concept, dev, maint ]
    - username: RepoDynamicsBot
      roles: [ maint ]
:::

::::


## Usage
The authors of your project are used in the following places:
- The `authors` metadata of your package,
  which is also displayed on the PyPI page of your package.
- The credits page of your project's website.
- The front page of your project's PDF documentation.
