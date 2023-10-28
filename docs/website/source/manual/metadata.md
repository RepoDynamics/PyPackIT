# Meta Content

## Core Metadata

### Project Introduction
- File: `core/intro.yaml`

#### `name`
Name of the project.
- Type: string
- Default: name of the repository after replacing hyphens with spaces

The name can only contain ASCII alphanumeric characters, spaces, periods (.), underscores (_) and hyphens (-).
Additionally, it must start and end with an alphanumeric character.

Example:
```yaml
name: PyPackIT
```

:::{note}
The package name is derived from the name of the project, via normalization[^name-normalization]:
The project name is lowercased, with all runs of spaces, periods (.), underscores (_) and hyphens (-)
replaced with a single hyphen.
That is why we enforce the restrictions of a valid non-normalized package name here,
otherwise the project name is only used in documents to refer to the project,
and so could have contained any unicode character.
:::
[^name-normalization]: [Python Packaging User Guide > PyPA specifications > Package name normalization](https://packaging.python.org/en/latest/specifications/name-normalization/)

#### `tagline`
A single-line tagline, slogan, or description of the project.
- Type: string
- Default: ""

Example:
```yaml
tagline: >-
  Python Projects Perfected: Innovate, Develop, and Deploy Effortlessly!
```

#### `description`
A long description of the project that can have multiple paragraphs, with Markdown or HTML formatting.
- Type: string
- Default: ""

Example:
```yaml
description: >-
  PyPackIT is a free and open-source toolkit
  <b>empowering the development of open-source Python projects on GitHub</b>.
  It is a <b>dynamic repository template</b> that provides a complete, professional, and
  robust infrastructure for your project, where the only thing missing is your code.
  With PyPackIT, you can solely focus on what truly matters:
  implementing your ideas and bringing your vision to life!
```

#### `keywords`
Keywords to describe the project.
- Type: list of strings
- Default: []

Each keyword must only contain 50 or less ASCII alphanumeric characters, spaces, and hyphens (-).
Additionally, it must start and end with an alphanumeric character.

Example:
```yaml
keywords:
  - python
  - github
  - packaging
  - template
  - dynamic repository
  - repository template
```

#### `keynotes`
A list of keynotes about the project.
- list of dictionaries
- Default: []

Each keynote is a dictionary with the following keys:
- `title`: string, required\
Title of the keynote.
- `description`: string, required\
Description of the keynote.


Example:
```yaml
keynotes:
  - title: Automation
    description: >-
      PyPackIT streamlines a remarkable portion of the process of creating,
      documenting, testing, publishing, and maintaining Python packages,
      making your project development a pleasant breeze!
  - title: Synchronization
    description: >-
      PyPackIT gathers all your project's key information and configuration in one place,
      and dynamically updates them throughout your repository, Python package, and documentation website.
  - title: Configuration
    description: >-
      PyPackIT elevates your project by providing full configuration for your repository,
      Python package, and documentation website, according to the latest guidelines and best practices.
  - title: Customization
    description: >-
      While carefully configured, PyPackIT is also fully customizable,
      allowing you to tailor every aspect of your development pipeline to your specific needs
```


### License and Copyright

- File: `core/license.yaml`
- Required: No

Example:
```yaml
license:
  id: gnu_agpl_v3+

copyright:
  year_start: 2023
  owner: John Doe
```

#### `license`
When this key is not provided, the [GNU AGPL v3.0+](https://choosealicense.com/licenses/agpl-3.0/) 
license (GNU Affero General Public License v3 or later) will be selected by default for your repository.
If you don't want to include a license in your project, set `license` to `null`:
```yaml
license: null
```
Otherwise, if you want to use one of the pre-defined licenses, set a single key, `id`, 
to one of the following values (case-insensitive):
- `GNU_AGPL_v3+`: [GNU Affero General Public License v3 or later](https://choosealicense.com/licenses/agpl-3.0/)
- `GNU_AGPL_v3`: [GNU Affero General Public License v3](https://choosealicense.com/licenses/agpl-3.0/)
- `GNU_GPL_v3+`: [GNU General Public License v3 or later](https://choosealicense.com/licenses/gpl-3.0/)
- `GNU_GPL_v3`: [GNU General Public License v3](https://choosealicense.com/licenses/gpl-3.0/)
- `MPL_v2`: Mozilla Public License 2.0
- `Apache_v2`: [Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)
- `MIT`: [MIT License](https://choosealicense.com/licenses/mit/)
- `BSD_2_Clause`: [BSD 2-Clause License](https://choosealicense.com/licenses/bsd-2-clause/)
- `BSD_3_Clause`: [BSD 3-Clause License](https://choosealicense.com/licenses/bsd-3-clause/)
- `BSL_v1`: [Boost Software License 1.0](https://choosealicense.com/licenses/bsl-1.0/)
- `Unlicense`: The Unlicense
For example, to use the MIT license:
```yaml
license:
  id: mit
```
If you want to use a custom license, set the following keys:
- `shortname`: The short name of the license
- `fullname`: The full name of the license
- `text`: The text of the license
- `notice`: The notice of the license
- `trove_classifier` (optional): If your license has a trove classifier, 
   and you want it to be automatically added to your package metadata, 
   set this to the full text of the license's trove classifier, e.g. `License :: OSI Approved :: BSD License`.
For example:
```yaml
license:
  shortname: MCL v1.0
  fullname: My Custom License 1.0
  text: |
                         My Custom License
                     Version 1.0, January 2024
               https://mywebsite.com/my-custom-license
    
    This is the full text of my custom license.
  notice: |
    Licensed under My Custom License, Version 1.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
       https://mywebsite.com/my-custom-license
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
```

#### `copyright`
By default, PyPackIT uses the creation date of your repository, 
and the name of the repository owner (set in their GitHub account),
to generate a copyright notice. The notice is of the form 
`{START-YEAR}–{CURRENT-YEAR} {OWNER-NAME}` (e.g. `2023–2024 John Doe`)
when the repository creation year is not the same as the current year,
and `{CURRENT-YEAR} {OWNER-NAME}` (e.g. `2024 John Doe`) otherwise.
You can customize this notice by setting the following keys:
- `year_start`: The start year of the project to use instead of the repository creation year
- `owner`: The name of the project owner to use instead of the repository owner name
Example:
```yaml
copyright:
  year_start: 2020
  owner: Jane Doe
```

### Project Credits

#### `author`

##### `author.role`
Example:
```yaml
author:
  role: Founder
```