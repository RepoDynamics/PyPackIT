# Inheritance and Templating

## Templating
To eliminate any redundancy and provide your project with a high degree of flexibility
and customization, {{ pp_meta.name }} allows for complex and recursive templating
within the entire control center, meaning that you can reference and reuse
any part of the control center's contents in all other places within the control center.

:::{admonition} Substitutions in Website Content
:class: seealso
The entire content of the control center is also made available to your documentation website,
and can be used for substitutions in your website's content.
See [Manual > Usage > Website > Substitutions](../../usage/website/substitutions.md) for more information.
:::


### Syntax

Substitutions are defined using the syntax `${‎{ PATH }}`
(the whitespace between `PATH` and the curly braces is optional and ignored),
where `PATH` is the full address to the control center's content you want to substitute,
as described in [Manual > Control Center > Outputs > Metadata File](../outputs/metadata.md).
You can use this syntax to substitute any key or value, or any part of a key or value
in any YAML or TOML file within the control center.
If you use this to substitute an entire value or array element, that value or element
will have the same type as the substituted value or element.
On the other hand, if you use this to substitute a part of a string,
the substituted part will also be converted to a string.
Substitutions are evaluated recursively, meaning that you can use substitutions
to reference a content that itself contains substitutions; you only need to make sure
not to create any circular references.


### Examples


## Inheritance


{{pp_meta.name}} allows you to dynamically inherit
some or all of the contents of your repository's control center from other repositories.
This is particularly useful when you are managing multiple repositories,
and want to share some common configurations and metadata between them.
Using extensions, you can make changes to the shared data in one place,
and have them automatically applied to all repositories that use them.

### Usage

During the processing of your repository's control center,
for each YAML or TOML file, {{pp_meta.name}} checks if there are any extensions defined for it.
If so, it will first look for [unexpired](/manual/control/options/config/cache.md)
cached copies of the extension files, and if not found,
it will fetch them from the GitHub servers and cache them for future use.
This is done both on local devices, and on the GitHub servers when running the workflows:
On local devices, the extension files are cached in the RepoDynamics cache directory
under the local directory of the repository, whereas on the GitHub servers,
they are cached in the GitHub Actions cache directory (not part of the repository files)
that can be accessed from the Actions tab of the repository.
Subsequently, the contents of the extension files are merged into the contents of the target file,
according to the extension settings.


## Data Retrieval

The `cache_retention_days.extensions` setting is used determine the expiration date
of each cached extension file,
as described in the section [Extensions](/manual/control/options/extensions/index.md#usage).
Similarly, {{ pp_meta.name }} maintains a cache file `api_cache.yaml`, containing all
the data retrieved from web APIs, such as GitHub repo/users data, software versions, publications etc.
This is done both on local devices, and on the GitHub servers when running the workflows:
On local devices, the file is stored in the RepoDynamics cache directory
under the local directory of the repository, whereas on the GitHub servers,
it is stored in the GitHub Actions cache directory (not part of the repository files)
and can be accessed from the Actions tab of the repository.
During the processing of your repository's control center,
for each piece of data that has to be retrieved from a web API,
{{pp_meta.name}} first checks if there is an unexpired entry for it in the `api_cache.yaml` file,
and if not, it will fetch it from the corresponding web API and cache it for future use.
