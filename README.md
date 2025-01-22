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
- in 2023-2024 there were ~10 models available via the Perplexity API.  
  Those were rather diverse.
- in 2025, the ~5 current models are kind of similar.

```

### Batch Prompting the Perplexity Web-APIs

In 2024, the [Perplexity API endpoints](https://docs.perplexity.ai/docs/model-cards)   were actually just "wrappers" or fine-tuned variants of Meta's important family of models, the [Llama models](https://github.com/meta-llama/). So those models were worth exploring via the Perplexity API. I know that there are many other ways to interact with the Llama models, but I 
wanted to try this one.

A command-line script that will create _very_ verbose output with many details of the API requests and responses. The output is saved in a markdown textfile in `final_output/` directory.

#### In a Linux terminal, send your human-language queries to Perplexity.ai's variants of Meta-Llama LLMs.  

A spare-time project to explore the [Perplexity.ai API endpoint paths](https://blog.perplexity.ai/blog/introducing-pplx-online-llms) and try a mix of different prompts and models.

```bash
./explore_perplexity_api.py --slug celentano-song \
  --prompt "What is the name of the Song by Adriano Celentano \
    that has lyrics in fake English language?" 
```

#### This command will send your prompt to all the models available via the Perplexity API (n = 5 in early 2025), and save the consolidated responses in a markdown textfile.


- You need to have a Perplexity API key. Set it in the environment variable `PERPLEXITY_API_KEY` in an `.env`.
- You need to have "Newman" installed. It is a command-line tool for running Postman collections. Python class `model_processor.py` calls this.

See [INSTALL.md](./doc/INSTALL.md) -- [README-python.md](./doc/README-python.md) -- [README-verbose](./doc/README-verbose.md) -- [TODO.md](./doc/TODO.md) for more details.

## License

Use it as you like.

