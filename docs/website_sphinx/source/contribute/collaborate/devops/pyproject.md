pyproject.toml file replaces setup.py.

It is written in [TOML](https://github.com/toml-lang/toml).

Python standard library has a module named [tomllib](https://docs.python.org/3/library/tomllib.html) 
for reading (but not writing) TOML files.
To write TOML files, other non-standard libraries such as
[toml](https://github.com/uiri/toml) and [tomli-W](https://github.com/hukkin/tomli-w) can be used.
However, these don't preserve the original style of a TOML file when modifying.
[TOML Kit](https://github.com/sdispater/tomlkit) is another alternative that also preserves styling,
and is used in this package to read, modify and write the pyproject.toml file.