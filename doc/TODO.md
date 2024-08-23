<!-- markdownlint-disable MD001 -->
# TODO.md

### ~~Upload as Github Gist~~

~~Write a helper shellscript that uplaods each .txt output file to github, as a Gist, for sharing.~~
    - Done, see [upload_as_github_gist.sh](./upload_as_github_gist.sh). Rarely used in practice

### The "find-persona" script

~~Used in practice, because it is easy to use and maintain.Provide a selection of "personas" to the user, and let them choose one. The script will then pass the chosen persona as an additional argument to the AI system.~~

The script is called "`src/find-persona`".

More importantly,

- I am using **[my repo](https://github.com/knbknb/ai-system-personas)**, to make it easier to maintain and update a list of custom instructions.
- Personas are **grouped by topic or category**, e.g. "IT", "Business", "Health", "Comm.+L ang.", etc.

Usage:

```bash
src/find-persona Aristotle <enter>
```

Response:

The shell will turn into something similar to this:
The output of your selection can be passed to any AI systems GUI or API.

![terminal window screenshot](../resources/find-assistant-screenshot-terminalwindow-ann.png)

(1) Is your prompt after hitting `<enter>`  
(2) Shows a full expansion of the preview text shown in (1)

##### Prerequsites

These command line tools must be installed:

- `curl`, as HTTP client
- `fzf`, the fuzzy finder
- `yq`, the YAML parser
- `jq`, the JSON parser
