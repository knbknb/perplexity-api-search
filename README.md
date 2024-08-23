<!-- markdownlint-disable MD001 MD022 MD026  -->
# Batch Prompting the Perplexity Web-APIs

... with Python + Postman/Newman.  
A command-line script that will create _very_ verbose output with many details of the API requests and responses.

It is more a learning tool than a practical one.  
I wanted to script Postman with Newman, and Newman with Python.

#### In a Linux terminal, send your human-language queries to Perplexity.ai's various LLMs.  

A spare-time project to explore the [Perplexity.ai API endpoint paths](https://blog.perplexity.ai/blog/introducing-pplx-online-llms) and try a mix of different promts and models.

```bash
./explore_perplexity_api.py --slug celentano-song \
  --prompt "What is the name of the Song by Adriano Celentano \
                                     which has lyrics in fake English language?" 
```

- You need to have a Perplexity API key. Set it in the environment variable `PERPLEXITY_API_KEY`.
- You need to have "Newman" installed. It is a command-line tool for running Postman collections.

See [INSTALL.md](./doc/INSTALL.md) -- [README-python.md](./doc/README-python.md) -- [README-verbose](./doc/README-verbose.md) -- [TODO.md](./doc/TODO.md) for more details.

## License

Use it as you like.

## Note

For simpler batch prompting via the command line, I recommend Simon Willison's [llm](https://github.com/simonw/llm) tool, `pip install llm`.

`llm "Where is Plutonia?"`  
`for loc in 'Literature' 'Computer Gaming'; do llm "Where is Plutonia in $loc?"; done`

(Requires API keys for LLMs as well.)
