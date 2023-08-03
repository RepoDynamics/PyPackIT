import os


cache_hit = os.environ["CACHE-HIT"] == "true"
force_update = os.environ["FORCE_UPDATE"]

log = f"""#### Conditions
- {'✅' if force_update == "all" else ('❌' if force_update == "none" else '☑️')}  Force update ({force_update})
- {'✅' if cache_hit else '❌'}  Cache hit
#### Results
"""

if not cache_hit or force_update == "all":
    log += "- All metadata was recalculated from scratch."
elif force_update == "core":
    log += "- Core metadata was recalculated from scratch, while API metadata was loaded from cache."
elif force_update == "none":
    log += "- Metadata was loaded entirely from cache."
else:
    raise ValueError(f"Unknown force_update value: {force_update}")

with open("metadata_pretty.json") as f:
    metadata_text = f.read()

log = f"""<br>
<details><summary>🖥 Metadata</summary>

```json
{metadata_text}
```

</details>
"""

with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as fh:
    print(log, file=fh)
