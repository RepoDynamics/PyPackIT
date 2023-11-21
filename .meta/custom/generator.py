from pathlib import Path
from importlib.resources import files
from ruamel.yaml import YAML


def extract_defaults_from_schema(schema: str) -> tuple[str, bool]:
    def recursive_extract(properties, defaults, all_have_defaults=True):
        for key, defs in properties.items():
            if "default" not in defs:
                all_have_defaults = False
                continue
            if "properties" in defs:
                default_vals, all_have_defaults = recursive_extract(defs["properties"], defs["default"])
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
    path = files("repodynamics") / "_data" / "schema"
    filepaths = list(path.glob("**/*.yaml"))
    out = {}
    for filepath in filepaths:
        schema = filepath.read_text()
        defaults, all_have_defaults = extract_defaults_from_schema(schema)
        entry = {"full": schema, "defaults": defaults, "all_have_defaults": all_have_defaults}
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