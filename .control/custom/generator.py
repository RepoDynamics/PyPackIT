# Standard libraries
from importlib.resources import files

# Non-standard libraries
from repodynamics.path import RelativePath
from ruamel.yaml import YAML


def extract_defaults_from_schema(schema: str) -> tuple[str, bool]:
    def recursive_extract(properties, defaults, all_have_defaults=True):
        for key, defs in properties.items():
            if "default" not in defs:
                all_have_defaults = False
                continue
            if "properties" in defs:
                default_vals, all_have_defaults = recursive_extract(
                    defs["properties"],
                    defs["default"],
                )
                defaults[key] = default_vals
            else:
                defaults[key] = defs["default"]
        return defaults, all_have_defaults

    schema = YAML(typ="safe").load(schema)
    if "properties" not in schema:
        out = schema["default"]
        all_have_defaults = False
    else:
        out, all_have_defaults = recursive_extract(schema["properties"], schema["default"])
    return YAML(typ=["rt", "string"]).dumps(out, add_final_eol=True), all_have_defaults


def schemas():
    path_data = files("repodynamics") / "_data"
    path_schema = path_data / "schema"
    path_examples = path_data / "example"
    filepaths = list(path_schema.glob("**/*.yaml"))
    out = {}
    for filepath in filepaths:
        schema = filepath.read_text()
        defaults, all_have_defaults = extract_defaults_from_schema(schema)
        rel_path = filepath.relative_to(path_schema)
        path_example = path_examples / rel_path
        example_str = path_example.read_text() if path_example.exists() else ""
        docs_path = str(rel_path.with_suffix(""))
        if docs_path.startswith("package_python/"):
            docs_path = f"package/{docs_path.removeprefix('package_python/')}"
        # name = rel_path.stem
        # if rel_path.parent == Path("."):
        #     out[name] = entry
        # else:
        #     sub_dict = out.setdefault(rel_path.parent.name, {})
        #     sub_dict[name] = entry
        tabs = f""":::::{{tab-set}}
::::{{tab-item}} Info
- **Relative Filepath**{{sup}}`[1]`: `{rel_path}`
- **Pre-configured**: {all_have_defaults}

[1]: Filepath is relative to the root of the control center directory.
::::
::::{{tab-item}} Schema
:::{{code-block}} yaml
{schema}
:::
::::
::::{{tab-item}} Default
:::{{code-block}} yaml
{defaults}
:::
::::
::::{{tab-item}} Example
:::{{code-block}} yaml
{example_str}
:::
::::
:::::"""
        out[f"manual/control/options/{docs_path}/index"] = {
            "schema_str": schema,
            "default_str": defaults,
            "example_str": example_str,
            "pre_config": all_have_defaults,
            "path": str(rel_path),
            "tabs": tabs,
        }
    return {"meta": out}


def paths():
    return {
        "path": {
            name: f"./{rel_path}"
            for name, rel_path in RelativePath.__dict__.items()
            if not name.startswith("_")
        },
    }


def run(metadata) -> dict:
    out = {}
    out |= schemas()
    out |= paths()
    return out
