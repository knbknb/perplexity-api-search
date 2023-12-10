<!-- markdownlint-disable MD001 -->
# Querying the Perplexity API with Newman and Postman

In a shell script, send you human-language query to various AI systems/models, in a single loop.
Collect the responses an put them in a pretty textfile.

See Shell Script `explore_perlplexity_api` - work in progress

example call:

```bash
export PERPLEXITY_API_KEY=pplx-....
./explore_perplexity_api.sh --prompt "In which years became skeleton sled racing olympic?" --slug "sled-racing"
```

example output:

```text
Using prompt -p 'In which years became skeleton sleigh racing olympic?'
Using SLUG (prompt-fragment) --slug 'sleigh-racing'
Press enter to continue
codellama-34b-instruct: Running collection queries/sleigh-racing--codellama-34b-instruct.json
llama-2-70b-chat:       Running collection queries/sleigh-racing--llama-2-70b-chat.json
mistral-7b-instruct:    Running collection queries/sleigh-racing--mistral-7b-instruct.json
pplx-7b-chat:           Running collection queries/sleigh-racing--pplx-7b-chat.json
pplx-70b-chat:          Running collection queries/sleigh-racing--pplx-70b-chat.json
pplx-7b-online:         Running collection queries/sleigh-racing--pplx-7b-online.json
pplx-70b-online:        Running collection queries/sleigh-racing--pplx-70b-online.json
```
