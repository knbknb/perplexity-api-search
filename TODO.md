<!-- markdownlint-disable MD001 -->
# TODO.md

### ~~Upload as Github Gist~~

~~Write a helper shellscript that uplaods each .txt output file to github, as a Gist.~~

- Done, see [upload_as_github_gist.sh](upload_as_github_gist.sh)

### The "find-assistant" script

##### (Under construction)

The [`find-assistant`](find-assistant) script is a simple script that will propose different custom instructions to pass to the AI system's "assistant" role.

Usage:

```bash
find-assistant Aristotle <enter>
```

Response:

The shell will turn into this:

![terminal window screenshot](resources/find-assistant-screenshot-terminalwindow-ann.png)

(1) Is your prompt after hitting `<enter>`  
(2) Shows a full expansion of the preview text shown in (1)

This will not be passed to the AI systems yet. It is just a potential future improvement to the script, to help you find  more focused results.

##### Prerequsites

These command line tools must be installed:

- `fzf`, the fuzzy finder
- `yq`, the YAML parser
- `jq`, the JSON parser
- `curl`, the HTTP client
