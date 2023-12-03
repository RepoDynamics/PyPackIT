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
