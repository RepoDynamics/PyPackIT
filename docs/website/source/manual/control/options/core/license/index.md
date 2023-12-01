# License and Copyright

:::::{tab-set}
::::{tab-item} Info
- **Relative Path**: `{{ pp_meta.custom.meta[docname].path }}`
- **Pre-configured**: {{ pp_meta.custom.meta[docname].pre_config }}
::::
::::{tab-item} Schema
:::{code-block} yaml
{{ pp_meta.custom.meta[docname].schema_str }}
:::
::::
::::{tab-item} Default
:::{code-block} yaml
{{ pp_meta.custom.meta[docname].default_str }}
:::
::::
::::{tab-item} Example
:::{code-block} yaml
{{ pp_meta.custom.meta[docname].example_str }}
:::
::::
:::::

All specifications related to the license and copyright of your project
are stored in the `core/license.yaml` file in the repository's `meta` directory.


## License
It is strongly recommended that you include a license in your project.
To do so, add a `license` key to the `core/license.yaml` file.
You have two options for specifying the license of your project:
- [Specify a pre-defined license](#pre-defined-licenses)
- [Declare any other license](#other-licenses)

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

For example, to use the GNU AGPL v3+ license:

:::{code-block} yaml
:caption: 🗂 `./.meta/core/license.yaml`
license:
  id: gnu_agpl_v3+
:::


### Other Licenses
If you want to use any other license not mentioned above, you must instead set the following keys:
- `shortname`: The short name of the license
- `fullname`: The full name of the license
- `text`: The full text of the license
- `notice`: Short license notice
- `trove_classifier` (optional): If your license has a trove classifier,
   and you want it to be automatically added to your package metadata,
   set this to the full text of the license's trove classifier, e.g. `License :: OSI Approved :: BSD License`.

:::{code-block} yaml
:caption: 🗂 `./.meta/core/license.yaml`
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


## Copyright
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
