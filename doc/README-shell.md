<!-- markdownlint-disable MD001 MD022 MD026  -->
# Shellscript
## Querying the Perplexity APIs with bash and newman

##### In a Linux terminal, send your human-language query to Perplexity.ai's various LLM APIs  in a single loop.

##### See Shell Script [`explore_perplexity_api.sh`](explore_perplexity_api.sh) - first prototype

##### The shell script collects the API responses and puts them in a pretty textfile, for you to read and compare model outputs.

You need to be a "perplexity pro" customer to use this script.  It requires an API key. Running the script is not free of charge. See [Perplexity API Pricing](https://docs.perplexity.ai/docs/pricing) for more details.

#### Prerequisites

Quite a few command line tools must be installed. For details, see [README-shell](README-shell.md).

- `node`, the JavaScript runtime
- `newman`, the Postman CLI, a `node` package
- `curl`, the HTTP client
- `jq`, the JSON parser
- `pandoc`, the document converter (for markdown to html)
- `lynx`, the commandline browser and HTML parser (for html to txt)
- `fmt`, the text formatter (for pretty text output)

All are free software.  
The large binary GUI App "Postman" should be installed, and you must know how to use it.  
Get it here: [Postman](https://getpostman.com), the GUI App. It is commercial, but it has a free tier/plan.

#### What script `explore_perlplexity_api.sh` does

Ask a query and get a pretty textfile with the responses from various AI systems/models, see [README-verbose.md](README-verbose.md) for more details.

The shell script [`explore_perlplexity_api.sh`](../explore_perplexity_api.sh) controls the NodeJS app `"newman"`, and newman loads artifacts exported from Postman.

On host "well", newman 6.0.0 is installed on Node 16 (use nvm to switch to 16). Attention: `npm` 10 does not work with Node 16.

```bash
nvm current
nvm use 16
npm i -g newman
npm install -g newman-reporter-htmlextra
```

#### Example call:

##### A question about a sport: Skeleton Bobsled Racing:  

> "In which years became skeleton sled racing olympic?"

```bash
# one-off: YOUR API KEY HERE
export PERPLEXITY_API_KEY=pplx-....
# ask a question, with a slug for easy reference
./explore_perplexity_api.sh --prompt "In which years became skeleton sled racing olympic?" \
  --slug "sled-racing"
```

This is a one-shot question, not a conversation.

##### Example output:

See [README-verbose.md](README-verbose.md) for more details.
