from pathlib import Path
import json
import re


class JSONLoader:

    def __init__(self, filepath):
        self._data = self._read(filepath)
        self.dir_path = Path(filepath).parent
        return

    def fill(self):
        filled = {}
        for key, val in self._data.items():
            filled[key] = self.recursive_subst(val)
        return filled

    def recursive_subst(self, value):
        if isinstance(value, str):
            match_whole_str = re.match(r'{{{([^{}]*)}}}$', value)
            if match_whole_str:
                return self.substitute_val(match_whole_str.group(1))
            return re.sub(r'{{{(.*?)}}}', lambda x: str(self.substitute_val(x.group(1))), value)
        if isinstance(value, list):
            return [self.recursive_subst(elem) for elem in value]
        if isinstance(value, dict):
            news = {}
            for key, val in value.items():
                news[self.recursive_subst(key)] = self.recursive_subst(val)
            return news
            # return {self.recursive_subst(key): self.recursive_subst(val) for key, val in value.items()}
        return value

    def substitute_val(self, match):
        filename, *address = match.strip().split(".")
        parsed_address = []
        for add in address:
            name = re.match(r'^([^[]+)', add).group()
            indices = re.findall(r'\[([^\]]+)\]', add)
            parsed_address.append(name)
            parsed_ind = []
            for idx in indices:
                if not ":" in idx:
                    parsed_ind.append(int(idx))
                else:
                    slice_ = [int(i) if i else None for i in idx.split(":")]
                    parsed_ind.append(slice(*slice_))
            parsed_address.extend(parsed_ind)
        if not filename:
            target = self.retrieve_address(address=parsed_address)
            return self.recursive_subst(value=target)
        new_file = self.get_sibling(name=filename)
        target = new_file.retrieve_address(address=parsed_address)
        return new_file.recursive_subst(value=target)

    def retrieve_address(self, address):

        def recursive_retrieve(obj, add):
            if len(add) == 0:
                return obj
            curr_add = add.pop(0)
            try:
                next_layer = obj[curr_add]
            except (TypeError, KeyError, IndexError) as e:
                try:
                    next_layer = self.recursive_subst(obj)[curr_add]
                except (TypeError, KeyError, IndexError) as e2:
                    raise KeyError(f"Object '{obj}' has no element '{curr_add}'") from e
            return recursive_retrieve(next_layer, add)

        return recursive_retrieve(self._data, add=address)

    def path_sibling(self, name):
        return self.dir_path / f'{name}.json'

    def get_sibling(self, name):
        return JSONLoader(filepath=self.path_sibling(name))

    @staticmethod
    def _read(filepath):
        path = Path(filepath)
        if not path.exists():
            raise ValueError()
        if not path.is_file():
            raise ValueError()
        with open(path) as f:
            data = json.load(f)
        return data


def read(filepath):
    return JSONLoader(filepath=filepath).fill()
