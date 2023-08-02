import os
import json

context = json.loads(os.environ["GH_CONTEXT"], strict=False)
_ = context.pop("token")
payload = context.pop("event")
context_sorted = dict(sorted(context.items()))
payload_sorted = dict(sorted(payload.items()))
summary = f"""<details><summary>🖥 GitHub context</summary>

```json
{json.dumps(context_sorted, indent=4)}
```

</details><details><summary>🖥 Event payload</summary>

```json
{json.dumps(payload_sorted, indent=4)}
```

</details>
"""
with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as fh:
    print(summary, file=fh)
