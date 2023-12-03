# Cache

You can define the amount of time to keep the cached data for the retrieved extensions,
and other data obtained through various web APIs,
such as GitHub repo/users data, software versions, publications etc.


## Setting

Cache retention time is configured through the `cache_retention_days` key,
which accepts an object with the following keys:

:api: ***integer***, ***default***: `1`

    Number of days to keep the cached data retrieved from web APIs,
    such as GitHub repo/users data, software versions, publications etc.

:extensions: ***integer***, ***default***: `1`

    Number of days to keep the cached extension files
    retrieved from other GitHub repositories.


## Usage

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
