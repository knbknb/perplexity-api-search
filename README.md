<!-- markdownlint-disable MD001 MD022 MD026  -->
# Obsolete - (Perplexity.ai API redesigned)

##### Send out 5-10 prompts at once, collect the LLM responses in a textfile.

```text
Code in repo is obsolete in 2025  
Perplexity.ai API was redesigned and rebranded.

Besides, 
- the code in this repo was more a personal learning tool than a practical one.  
- this repo implements an  incredibly awkward  
  and convoluted way to interact with the Perplexity API.
- in 2023-2024 there were ~10 models available via the Perplexity API .  
  Those were rather diverse, from different vendors.
- in 2025, the ~5 current models are kind of similar, built by Perplexity independently.  
  Maybe based on DeepSeek's open-source/openweights LLMs, but not sure.

```

### Batch Prompting the Perplexity Web-APIs


A command-line script that will create _very_ verbose output with many details of the API requests and responses. The output is saved in a markdown textfile in `final_output/` directory.

#### In a Linux terminal, send your human-language queries to Perplexity.ai's variants of Meta-Llama LLMs.  

A spare-time project to explore the [Perplexity.ai API endpoint paths](https://blog.perplexity.ai/blog/introducing-pplx-online-llms) and try a mix of different prompts and models.

```bash
./explore_perplexity_api.py --slug celentano-song \
  --prompt "What is the name of the Song by Adriano Celentano \
    that has lyrics in fake English language?" 
```

[See results](doc/README-python.md).

#### This command will send your prompt to all the models available via the Perplexity API (n = ~5 in early 2025), and save the consolidated responses in a markdown textfile.


- You need to have a Perplexity API key. Set it in the environment variable `PERPLEXITY_API_KEY` in an `.env`.
- You need to have "Newman" installed. It is a command-line tool for running Postman collections. Python class `model_processor.py` calls this.

See [INSTALL.md](./doc/INSTALL.md) -- [README-python.md](./doc/README-python.md) -- [README-verbose](./doc/README-verbose.md) -- [TODO.md](./doc/TODO.md) for more details.

## License

Use it as you like.

