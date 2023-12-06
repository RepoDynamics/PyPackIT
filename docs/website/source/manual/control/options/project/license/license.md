# License
It is strongly recommended that you include a license in your project.


## Setting
In the control center files that are added to your repository
when you first install {{pp_meta.name}}, the license of your project
is set by default to the [GNU Affero General Public License v3 or later](https://choosealicense.com/licenses/agpl-3.0/).
You can change this default license by modifying the `license` key
under the `project/license.yaml` file.
There are two options for specifying the license of your project:
- [Specifying a pre-defined license](#pre-defined-licenses)
- [Declaring any other license](#other-licenses)

If you do not want to include a license in your project,
you can delete the `license` key in the `project/license.yaml` file,
or set it to `null`:

:::{code-block} yaml
:caption: 🗂 `project/license.yaml`
license: null
:::


### Pre-defined Licenses
To use one of the pre-defined licenses, set a single key, `id`,
to one of the following values (case-insensitive):
- `GNU_AGPL_v3+`: [GNU Affero General Public License v3 or later](https://choosealicense.com/licenses/agpl-3.0/)
- `GNU_AGPL_v3`: [GNU Affero General Public License v3](https://choosealicense.com/licenses/agpl-3.0/)
- `GNU_GPL_v3+`: [GNU General Public License v3 or later](https://choosealicense.com/licenses/gpl-3.0/)
- `GNU_GPL_v3`: [GNU General Public License v3](https://choosealicense.com/licenses/gpl-3.0/)
- `MPL_v2`: [Mozilla Public License 2.0](https://choosealicense.com/licenses/mpl-2.0/)
- `Apache_v2`: [Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)
- `MIT`: [MIT License](https://choosealicense.com/licenses/mit/)
- `BSD_2_Clause`: [BSD 2-Clause License](https://choosealicense.com/licenses/bsd-2-clause/)
- `BSD_3_Clause`: [BSD 3-Clause License](https://choosealicense.com/licenses/bsd-3-clause/)
- `BSL_v1`: [Boost Software License 1.0](https://choosealicense.com/licenses/bsl-1.0/)
- `Unlicense`: [The Unlicense](https://choosealicense.com/licenses/unlicense/)

For example, to use the MIT license:

:::{code-block} yaml
:caption: 🗂 `project/license.yaml`
license:
  id: mit
:::


### Other Licenses
If you want to use any other license not mentioned above, you must instead set the following keys
under the `license` key:

:shortname: ***string***

    The short name of the license

:fullname: ***string***

    The full name of the license

:text: ***string***

    The full text of the license

:notice: ***string***

    Short license notice

:trove_classifier: ***string***, ***optional***

    If your license has a trove classifier,
    and you want it to be automatically added to your package metadata,
    set this to the full text of the license's trove classifier, e.g. `License :: OSI Approved :: BSD License`.


::::{dropdown} Example

:::{code-block} yaml
:caption: 🗂 `project/license.yaml`

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
:::

::::


## Usage

When you select a pre-defined license by its `id`,
{{ pp_meta.name }} automatically retrieves all other information,
i.e., `shortname`, `fullname`, `text`, `notice`, and `trove_classifier`.
In addition to all these information being available for dynamic referencing throughout your project,
{{ pp_meta.name }} also uses them in several places:
- The license information is included in the license section of your documentation website.
- The license text is used to generate the `LICENSE` file in the root of your repository,
  so that GitHub can automatically detect and display the license of your project.
- The license file is also included in your package distribution and recognized by PyPI.
- The trove classifier of the license is added to the list of your package's trove classifiers,
  to help PyPI better categorize your package,
  so that users can find your package when searching for packages with a specific license.
- The license notice is added to the main docstring of your package.
