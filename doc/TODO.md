<!-- markdownlint-disable MD001 -->
# TODO.md

### ~~Upload as Github Gist~~

~~Write a helper shellscript that uplaods each .txt output file to github, as a Gist, for sharing.~~
    - Done, see [upload_as_github_gist.sh](./upload_as_github_gist.sh). Rarely used in practice

### The "find-prompt" script

Used in practice, because it is easy to use and maintain.
Provide a selection of "personas" to the user, and let them choose one. The script will then pass the chosen persona as an additional argument to the AI system.

The script is called "`find-prompt`", because the repository I've forked it from is called "[awesome-chatgpt-prompts]([https://](https://github.com/f/awesome-chatgpt-prompts))",  misleadingly. Few prompts, n~140, but more focused on chatbot-like prompts.

More importantly,

- I am using **[my own fork of that repo](https://github.com/knbknb/awesome-chatgpt-prompts/tree/knb-2024)**, to make it easier to maintain and update the list of custom instructions.
- Personas are **grouped by topic or category**, e.g. "IT", "Business", "Comm. and Lang.", etc.


Usage:

```bash
find-prompt Aristotle <enter>
```

Response:

The shell will turn into this:

![terminal window screenshot](../resources/find-assistant-screenshot-terminalwindow-ann.png)

(1) Is your prompt after hitting `<enter>`  
(2) Shows a full expansion of the preview text shown in (1)

This will not be passed to the AI systems yet. It is just a potential future improvement to the script, to help you find  more focused results.

### The "find-assistant" script

Second approach.

Rich in emojis 👩‍🏫+ , but not used in practice.

##### (Under construction)

The [`find-assistant`](../src/find-assistant) script is a simple script that will propose different custom instructions to pass to the AI system's "assistant" role. Forked from [awesome-assistants](https://github.com/awesome-assistants/awesome-assistants/blob/main/assistants.yml) repo. About n=260 custom instructions.  
I am using [my own fork of that repo](https://github.com/knbknb/awesome-assistants), to make it easier to maintain and update the list of custom instructions.

##### Prerequsites

These command line tools must be installed:

- `curl`, as HTTP client
- `fzf`, the fuzzy finder
- `yq`, the YAML parser
- `jq`, the JSON parser
