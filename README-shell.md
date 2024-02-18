<!-- markdownlint-disable MD001 MD022 MD026  -->
# Querying the Perplexity APIs

##### In a Linux terminal, send your human-language query to Perplexity.ai's various LLM APIs  in a single loop.

##### See Shell Script [`explore_perplexity_api.sh`](explore_perplexity_api.sh) - first prototype

##### The shell script collects the API responses and puts them in a pretty textfile, for you to read and compare model outputs.

You need to be a "perplexity pro" customer to use this script.  It requires an API key. Running the script is not free of charge. See [Perplexity API Pricing](https://docs.perplexity.ai/docs/pricing) for more details.

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

