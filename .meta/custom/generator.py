from pathlib import Path
from importlib.resources import files
from ruamel.yaml import YAML


def extract_defaults_from_schema(schema: str) -> str:
    def recursive_extract(properties, defaults):
        for key, defs in properties.items():
            if "default" not in defs:
                continue
            if "properties" in defs:
                defaults[key] = recursive_extract(defs["properties"], defs["default"])
            else:
                defaults[key] = defs["default"]
        return defaults
    schema = YAML(typ="safe").load(schema)
    if "properties" not in schema:
        out = schema["default"]
    else:
        out = recursive_extract(schema["properties"], schema["default"])
    return YAML(typ=["rt", "string"]).dumps(out, add_final_eol=True)


def schemas():
    path = files("repodynamics") / "_data" / "schema"
    filepaths = list(path.glob("**/*.yaml"))
    out = {}
    for filepath in filepaths:
        schema = filepath.read_text()
        schema_defaults = extract_defaults_from_schema(schema)
        entry = {"full": schema, "defaults": schema_defaults}
        rel_path = filepath.relative_to(path)
        name = rel_path.stem
        if rel_path.parent == Path("."):
            out[name] = entry
        else:
            sub_dict = out.setdefault(rel_path.parent.name, {})
            sub_dict[name] = entry
    return {"schema": out}


def run(metadata) -> dict:
    out = {}
    out |= schemas()
    return out

# run("")