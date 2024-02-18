<!-- markdownlint-disable MD001 MD022 MD026  -->
# Querying the Perplexity APIs with Python

##### In a Linux terminal, send your human-language query to Perplexity.ai's various LLM APIs  in a single loop.

##### See Python Script [`explore_perplexity_api.py`](explore_perplexity_api.py) - has fewer dependencies than the shell script.

##### The python script collects the API responses and puts them in a pretty textfile, for you to read and compare model outputs.

## Example call:

```bash
./explore_perplexity_api.py --prompt "What is the name of the Song by Adriano Celentano which has lyrics in fake English language?" --slug celentano-song
```

### Output

### On the command line

```bash
...

Extracted answer from model mixtral-8x7b-instruct into 'final_output/celentano-song.tmp.txt'
Extracted answer from model codellama-70b-instruct into 'final_output/celentano-song.tmp.txt'
Extracted answer from model llama-2-70b-chat into 'final_output/celentano-song.tmp.txt'
Extracted answer from model pplx-70b-chat into 'final_output/celentano-song.tmp.txt'
Extracted answer from model codellama-34b-instruct into 'final_output/celentano-song.tmp.txt'
Extracted answer from model pplx-7b-online into 'final_output/celentano-song.tmp.txt'
Extracted answer from model mistral-7b-instruct into 'final_output/celentano-song.tmp.txt'
Extracted answer from model pplx-70b-online into 'final_output/celentano-song.tmp.txt'
Extracted answer from model pplx-7b-chat into 'final_output/celentano-song.tmp.txt'
```
