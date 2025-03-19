import pkgdata as _pkgdata
import pyserials as _ps


_data_dir_path = _pkgdata.get_package_path_from_caller(top_level=True) / "_data"


def get_package_datafile(path: str) -> str | dict | list:
    """
    Get a data file in the package's '_data' directory.

    Parameters
    ----------
    path : str
        The path of the data file relative to the package's '_data' directory.
    """
    full_path = _data_dir_path / path
    data = full_path.read_text()
    if full_path.suffix == ".yaml":
        return _ps.read.yaml_from_string(data=data, safe=True)
    return data
