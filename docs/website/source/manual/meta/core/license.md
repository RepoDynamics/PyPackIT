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
