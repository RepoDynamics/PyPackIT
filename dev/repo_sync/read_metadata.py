import importlib.util
import sys
import json

_name = "metadata"
_spec = importlib.util.spec_from_file_location(_name, "metadata/variables/__init__.py")
metadata = importlib.util.module_from_spec(_spec)
sys.modules[_name] = metadata
_spec.loader.exec_module(metadata)


def as_dict():
    dic = dict()
    for name in metadata.__dir__():
        if not name.startswith("_"):
            dic[name] = dict()
            module = getattr(metadata, name)
            for var_name in module.__dir__():
                if not var_name.startswith("_") and var_name.isupper():
                    dic[name][var_name] = getattr(module, var_name)
    return dic


def as_json_str():
    return json.dumps(as_dict())


if __name__ == "__main__":
    print(as_json_str())

