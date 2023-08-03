import os


cache_hit = os.environ["CACHE-HIT"] == "true"
force_update = os.environ["FORCE_UPDATE"]

log = f"""
- {'✅' if force_update == "all" else ('❌' if force_update == "none" else '☑️')}  Force update (input: {force_update})
- {'✅' if cache_hit else '❌'}  Cache hit
"""
if not cache_hit or force_update == "all":
    log += "- ➡️ Updated all metadata"
elif force_update == "core":
    log += "- ➡️ Updated core metadata but loaded API metadata from cache"
elif force_update == "none":
    log += "- ➡️ Loaded all metadata from cache"
else:
    raise ValueError(f"Unknown force_update value: {force_update}")

with open("metadata_pretty.json") as f:
    metadata_text = f.read()

log += f"""<br>
<details><summary>🖥 Metadata</summary><br>

```json
{metadata_text}
```

</details>
"""

with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as fh:
    print(log, file=fh)
