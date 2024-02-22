<!-- markdownlint-disable MD001 MD022 MD026  -->
# Querying the Perplexity API

##### In a Linux terminal, send your human-language query to Perplexity.ai's various LLM API endpoint paths in a single command.  

A spare-time project to explore the [Perplexity.ai API](https://blog.perplexity.ai/blog/introducing-pplx-online-llms).  This is a work in progress.  
The goal is to make it easy to query the Perplexity.ai API endpoints from the command line, and to compare the results of [~10 different models](https://docs.perplexity.ai/docs/model-cards).
It also demonstrates how to use a Postman collection (and Postman environment file) from the command line, thus exerting very fine-grained control over the API calls.

Running the script is not free of charge. You need to be a paying customer to use this script. It requires an API key, available only to "Perplexity Pro" users. See [Perplexity API Pricing](https://docs.perplexity.ai/docs/pricing) for more details.

##### See

- Python Script [`explore_perplexity_api.py`](explore_perplexity_api.py) - rewrite of shell script .  
- [README-python.md](doc/README-python.md) for more details.  - has fewer dependencies than the shell script (which was a first implementation).
- Shell Script [`explore_perplexity_api.sh`](explore_perplexity_api.sh) - first prototype .  
- [README-shell.md](doc/README-shell.md) for more details.

## Installation

See [INSTALL.md](doc/INSTALL.md) for more details.

## Future Work

- Make setting the "custom instruction" more flexible, and more interactive.
- ~~Finish the Python rewrite of this script.~~
- See [TODO.md](doc/TODO.md) for more details.
