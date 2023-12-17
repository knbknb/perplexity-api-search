<!-- markdownlint-disable MD001 MD022 MD026  -->
# Querying the Perplexity API

##### In a Linux terminal, send your human-language query to Perplexity.ai's various AI systems/models, in a single loop.  
##### Collect the responses and put them in a pretty textfile.

See Shell Script [`explore_perlplexity_api.sh`](explore_perplexity_api.sh) - work in progress

#### Example call:

##### (A question about a sport: Skeleton Bobsled Racing.)

```bash
# one-off: YOUR API KEY HERE
export PERPLEXITY_API_KEY=pplx-....
# ask a question, with a slug for easy reference
./explore_perplexity_api.sh --prompt "In which years became skeleton sled racing olympic?" \
  --slug "sled-racing"
```

##### Example output:

See [README-verbose.md](README-verbose.md) for more details.

## Installation

See [INSTALL.md](INSTALL.md) for more details.

## Future Work

See [TODO.md](TODO.md) for more details.
