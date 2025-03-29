<!-- markdownlint-disable MD001 MD022 MD026  -->
# Perplexity.ai API exploration

#### The code in this repo represents more a personal learning tool than a practical one.  

##### Send out 5-10 prompts at once, collect the LLM responses in a textfile.

```text
Danger: Obsolescence ahead!

The Perplexity.ai REST APIs get redesigned every few months. Same for the models and documentation.

- in 2023-2024 there were ~10 models available via the Perplexity API .  
  Those were rather diverse, from different vendors (Meta, Mistral,...).
- in 2025, the ~5 current models are kind of similar, built by Perplexity independently.  
  Maybe based on DeepSeek's open-source/openweights LLMs, but not sure.

Besides, 
this repo implements an  incredibly awkward and convoluted way to interact with the Perplexity API.

```

### Batch Prompting the Perplexity Web-APIs

A command-line script that will create _very_ verbose output with many details of the API requests and responses. The output is saved in a markdown textfile in `final_output/` directory.

#### In a Linux terminal, send your human-language queries to Perplexity.ai's LLMs.  

A spare-time project to explore the Perplexity.ai API endpoint paths and try a mix of different prompts and models.

```bash
./explore_perplexity_api.py --slug celentano-song \
  --prompt "What is the name of the Song by Adriano Celentano \
    that has lyrics in fake English language?" 
```

[See results](doc/README-python.md).

- This command will send your prompt to all the models available via the Perplexity API (n = ~5 in early 2025), and save the consolidated responses in a markdown textfile.
- You need to have a Perplexity API key. Set it in the environment variable `PERPLEXITY_API_KEY` in an `.env` (see `.env-example` file).
- You need to have "Newman" installed. It is a command-line tool for running Postman collections. Python class `model_processor.py` calls this. This tool collects the API responses, lots of details about the API requests and responses, and saves them in a markdown textfile.

See [INSTALL.md](./doc/INSTALL.md) -- [README-python.md](./doc/README-python.md) -- [README-verbose](./doc/README-verbose.md) -- [TODO.md](./doc/TODO.md) for more details.

Perplexity BlogPosts:

- 2023[Perplexity.ai API endpoint paths](https://blog.perplexity.ai/blog/introducing-pplx-online-llms)
- 2025 [Updated models, available via API](https://www.perplexity.ai/hub/blog/new-sonar-search-modes-outperform-openai-in-cost-and-performance)

## License

Use it as you like.

