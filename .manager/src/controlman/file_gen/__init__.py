from pathlib import Path as _Path

import pyserials as _ps

from controlman import datatype as _dtype, const as _const
from controlman.file_gen.config import ConfigFileGenerator as _ConfigFileGenerator
from controlman.file_gen.forms import FormGenerator as _FormGenerator
from controlman.file_gen.python import PythonPackageFileGenerator as _PythonPackageFileGenerator


def generate(
    data: _ps.NestedDict,
    data_before: _ps.NestedDict,
    repo_path: _Path,
) -> list[_dtype.DynamicFile]:
    generated_files = []
    form_files = _FormGenerator(
        data=data,
        repo_path=repo_path,
    ).generate()
    generated_files.extend(form_files)
    config_files = _ConfigFileGenerator(
        data=data,
        data_before=data_before,
        repo_path=repo_path,
    ).generate()
    generated_files.extend(config_files)
    for key, value in data.items():
        if key.startswith("pypkg_"):
            package_files = _PythonPackageFileGenerator(
                data=data,
                data_before=data_before,
                repo_path=repo_path,
            ).generate(typ=key)
            generated_files.extend(package_files)
    out = []
    data_entry = {
        _dtype.DynamicFileType.CONFIG.value[0]: {"meta": _const.FILEPATH_METADATA},
    }
    for generated_file in generated_files:
        if generated_file.change is None:
            generated_file = _compare_file(generated_file, repo_path=repo_path)
        out.append(generated_file)
        if generated_file.change not in (
            _dtype.DynamicFileChangeType.DISABLED,
            _dtype.DynamicFileChangeType.REMOVED,
        ):
            type_dict = data_entry.setdefault(generated_file.type.value[0], {})
            if generated_file.subtype[0] in type_dict:
                raise RuntimeError(f"Duplicate dynamic file type and subtype: {generated_file.type.value[0]} {generated_file.subtype[0]}")
            type_dict[generated_file.subtype[0]] = generated_file.path
    data["project.file"] = data_entry
    metadata_file = _dtype.DynamicFile(
        type=_dtype.DynamicFileType.CONFIG,
        subtype=("meta", "Metadata"),
        content=_ps.write.to_json_string(data=data(), sort_keys=True, indent=3),
        path=_const.FILEPATH_METADATA,
        path_before=_const.FILEPATH_METADATA,
    )
    metadata_full = _compare_file(metadata_file, repo_path=repo_path)
    out.append(metadata_full)
    return out


def _compare_file(file: _dtype.DynamicFile, repo_path: _Path) -> _dtype.DynamicFile:
    path_before = file.path_before
    if path_before:
        path_before_abs = repo_path / path_before
        path_before_exists = path_before_abs.is_file()
        path_before = path_before if path_before_exists else None
    else:
        path_before_abs = None
        path_before_exists = False

    if file.content is None:
        typ = _dtype.DynamicFileChangeType.REMOVED if path_before_exists else _dtype.DynamicFileChangeType.DISABLED
    elif not file.path:
        typ = _dtype.DynamicFileChangeType.DISABLED
    elif not path_before_exists:
        typ = _dtype.DynamicFileChangeType.ADDED
    else:
        with open(path_before_abs) as f:
            content_before = f.read()
        contents_identical = file.content.strip() == content_before.strip()
        paths_identical = file.path == file.path_before
        change_type = {
            (True, True): _dtype.DynamicFileChangeType.UNCHANGED,
            (True, False): _dtype.DynamicFileChangeType.MOVED,
            (False, True): _dtype.DynamicFileChangeType.MODIFIED,
            (False, False): _dtype.DynamicFileChangeType.MOVED_MODIFIED,
        }
        typ = change_type[(contents_identical, paths_identical)]
    return _dtype.DynamicFile(
        type=file.type,
        subtype=file.subtype,
        content=file.content,
        path=file.path,
        path_before=path_before,
        change=typ,
        executable=file.executable,
    )
