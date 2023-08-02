import os
import json

# with open(os.environ["GROUPS"]) as f:
#     groups = json.load(f)
# with open(os.environ["ALL"]) as f:
#     all_files = json.load(f)

groups = json.loads(os.environ["GROUPS"], strict=False)
all_files = dict(sorted(json.loads(os.environ["ALL"], strict=False).items()))
sep_groups = dict()

for item_name, val in groups.items():
    group_name, attr = item_name.split("_", 1)
    group = sep_groups.setdefault(group_name, dict())
    group[attr] = val
group_summary_str = ""

for group_name, group_attrs in sep_groups.items():
    sep_groups[group_name] = dict(sorted(group_attrs.items()))
    group_summary_str += (
        f"- {'✅' if group_attrs['any_modified'] == 'true' else '❌'}  {group_name}\n"
    )

all_groups = {"all": all_files} | sep_groups
file_list = "\n".join(sorted(all_files["all_changed_and_modified_files"].split()))

with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
    print(f"json={json.dumps(all_groups)}", file=fh)

summary = f"""#### Modified Categories
{group_summary_str}

<details><summary>🖥 Changed Files</summary>

```bash
{file_list}
```

</details>

<details><summary>🖥 Details</summary>

```json
{json.dumps(all_groups, indent=4)}
```

</details>
"""

with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as fh:
    print(summary, file=fh)
