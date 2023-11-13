## Repository Paths
Along with the `.github` directory, PyPackIT works with a few other directories in your repository.

To change the meta directory, create a file at `.github/.repodynamics_meta_path.txt`
and put the path to your meta directory (relative to the root of repository) in it; for example:
```
some_directory/my_custom_meta_directory
```
All other paths can be configured in the `paths.yaml` file in the meta directory.
The file must contain an object with a single key `path`, which itself must contain an object with the
single key `dir`. Within the `dir` object, you can define alternative paths for the source directory,
tests directory, website directory, and local directory. You can add extra keys under `path.dir.local.cache`
and `path.dir.local.report` to use.

Default:

```yaml
path:
  dir:
    source: src
    tests: tests
    website: docs/website
    local:
      root: .local
      cache:
        root: cache
        repodynamics: repodynamics
        coverage: coverage
        mypy: mypy
        pylint: pylint
        pytest: pytest
        ruff: ruff
      report:
        root: report
        repodynamics: repodynamics
        coverage: coverage
        mypy: mypy
        pylint: pylint
        pytest: pytest
        ruff: ruff
```
