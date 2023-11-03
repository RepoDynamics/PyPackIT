## Repository Paths
Along with the `.github` directory, PyPackIT works with a few other directories in your repository. 
You can change the default paths of these directories by creating a `.path.json` file 
in the root of your repository. The JSON file must contain an object with a single key, `dir`, which
is an object containing the paths to the directories you want to change.

Default:

```json
{
   "dir": {
      "meta": ".meta",
      "source": "src",
      "local": ".local",
      "tests": "tests",
      "website": "docs/website"
   }
}
```
