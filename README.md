<!-- markdownlint-disable MD001 MD022 MD026  -->
# Querying the Perplexity Web-APIs

... with a simple Python script.

#### In a Linux terminal, send your human-language query to Perplexity.ai's various LLM API endpoint paths.  

A spare-time project to explore the [Perplexity.ai API](https://blog.perplexity.ai/blog/introducing-pplx-online-llms).  This is a work in progress.

The goals are

- Make it easy to query the Perplexity.ai Web-API endpoints from the command line, and to compare the results of [~10 different models](https://docs.perplexity.ai/docs/model-cards) available. This means saving the API responses into a textfile, then reading and inspecting them. I'm not systematically benchmarking the models.  
- Demonstrate how to use a Postman collection `.json`-file (and Postman environment `.json`-file) from the command line (with the [Newman](https://www.npmjs.com/package/newman) CLI tool), thus exerting very fine-grained control over the API calls, and conserving the responses with lots of metadata (e.g., runtime duration).

## API Key required

Running the script requires an API key, available only to "Perplexity Pro" users. Thus running the script is not free of charge. You need to be a registered customer to use this script. See [Perplexity API Pricing](https://docs.perplexity.ai/docs/pricing) for more details.

I think there is a free 5$-per-month plan, which is the cheapest option. If your API usage is low, you might be able to use the API for free.

##### See

- Python Script [`explore_perplexity_api.py`](explore_perplexity_api.py)  
- [README-python.md](doc/README-python.md) for more details. 
- Shell Script [`explore_perplexity_api.sh`](explore_perplexity_api.sh) - first prototype .  
- [README-shell.md](doc/README-shell.md) for more details.

## Installation

See [INSTALL.md](doc/INSTALL.md) for more details.

## Future Work

- Make setting the "custom instruction" more flexible, and more interactive.
- ~~Finish the Python rewrite of this script.~~
- See [TODO.md](doc/TODO.md) for more details.
