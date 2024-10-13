<!-- markdownlint-disable MD001 MD022 MD026  -->
# Batch Prompting the Perplexity API with Newman and Postman

```text
THIS IS OUTPUT FROM AN OLD DEPRECATED VERSION OF THE SCRIPT. Unmaintained. DO NOT USE.
```

#### Send your human-language query to Perplexity.ai's various AI systems/models, in a single loop.  
#### Collect the responses and put them in a pretty textfile.

See Shell Script [`explore_perplexity_api.sh`](../explore_perplexity_api.sh) - work in progress

You must also specify a command line argument  `--slug`. A slug is a prompt fragment for easy reference to the query and the output files.  If your slug is `sled-racing`, then see `final_output/sled-racing.txt`. Use simple words, no spaces.

The AI responses will be saved into a single textfile in the `final_output` directory.

**Important**: set this environment variable first, or the script will not run:

`export PERPLEXITY_API_KEY=pplx-....`

#### Example call:

##### (A question about a sport, Skeleton Bobsled Racing.)

Then run the script:

```bash
export PERPLEXITY_API_KEY=pplx-....
./explore_perplexity_api.sh --prompt "In which years became skeleton sled racing olympic?" \
  --slug "sled-racing"
```

##### Example output:

Shell output when running the script. (This is not the API response):

```text
Using prompt -p 'In which years became skeleton sleigh racing olympic?'

Using SLUG (prompt-fragment) --slug 'sleigh-racing'
Press enter to continue
codellama-34b-instruct: Saving into  queries/sleigh-racing--codellama-34b-instruct.json
llama-2-70b-chat:       Saving into  queries/sleigh-racing--llama-2-70b-chat.json
mistral-7b-instruct:    Saving into  queries/sleigh-racing--mistral-7b-instruct.json
pplx-7b-chat:           Saving into  queries/sleigh-racing--pplx-7b-chat.json
pplx-70b-chat:          Saving into  queries/sleigh-racing--pplx-70b-chat.json
pplx-7b-online:         Saving into  queries/sleigh-racing--pplx-7b-online.json
pplx-70b-online:        Saving into  queries/sleigh-racing--pplx-70b-online.json
```

Most of these "pplx-" models have been retired by Perplexity, and were replaced with better models called "sonar-". However the script will still run.

##### API response:

##### (Converted to pretty textfile:)

Various intermediate htmlfiles and jsonfiles are created, but the final output is a pretty textfile.

See `final_output/sled-racing.txt` (coming soon)

```text
     __________________________________________________________________

   ## codellama-34b-instruct
     __________________________________________________________________

   Skeleton sleigh racing has never been an Olympic sport. ## WRONG
     __________________________________________________________________

   ## llama-2-70b-chat
     __________________________________________________________________

   Skeleton sleigh racing, also known as skeleton bobsleigh, has been
   an Olympic sport for men since the 1924 Winter Olympics in Chamonix,
   France, and for women since the 2002 Winter Olympics in Salt Lake City,
   Utah, USA.  ## 1924-WRONG, 2002-CORRECT
     __________________________________________________________________

   ## mistral-7b-instruct
     __________________________________________________________________

   Skeleton sleigh racing became an Olympic sport in 2002 during the
   Winter Olympic Games held in Salt Lake City, USA.
     __________________________________________________________________

   ## pplx-70b-chat
     __________________________________________________________________

   Skeleton sleigh racing became an Olympic sport in 1924. 
   ## WRONG
     __________________________________________________________________

   ## pplx-70b-online
     __________________________________________________________________

   Skeleton sled racing, also known as skeleton, became an Olympic
   sport in 1928 and 1948, when the Winter Olympic Games were held in
   St. Moritz, Switzerland. The sport was then discontinued as an Olympic
   event until its permanent addition to the Winter Games in 2002.
   Skeleton is a winter sliding sport where competitors ride a small
   sled, known as a skeleton bobsled, down a frozen track while lying
   face down and head-first. ## CORRECT
     __________________________________________________________________

   ## pplx-7b-chat
     __________________________________________________________________

   Skeleton sleigh racing was first included as an Olympic sport  during the 1928 Winter Olympics in St. Moritz, Switzerland.  The event was
   originally intended to be a one-time showcase event, but due to its
   popularity, it was re-introduced as an official event at the 1948
   Winter Olympics in St. Moritz. Since then, skeleton sleigh racing has
   been a part of every Winter Olympics. So, the answer to your question
   is that skeleton sleigh racing became an Olympic sport in 1928 and
   has been included in every Winter Olympics since then.

   ## Sentence 1+2 - CORRECT, Sentece 3 - TOTALLY WRONG
     __________________________________________________________________

   ## pplx-7b-online
     __________________________________________________________________

   Skeleton racing, a winter sport where athletes ride a small sled called
   a skeleton bobsled head-first and face-down down a frozen track, has
   been featured in the Winter Olympics on two separate occasions. The
   sport first appeared at the 1928 Winter Olympics in St. Moritz and
   again at the 1948 Winter Olympics, also held in St. Moritz. However,
   it took until the 2002 Winter Olympics in Salt Lake City, Utah,
   for skeleton to become a permanent part of the Olympic Games. The
   International Olympic Committee (IOC) added the discipline to the
   2002 Salt Lake City Olympics, with both men’s and women’s events,
   and it has been held in each Winter Olympic competition since then.

   ## CORRECT (probably)
     __________________________________________________________________

     
     __________________________________________________________________

   ## mixtral-8x7b-instruct
     __________________________________________________________________

     Skeleton sled racing, also known simply as skeleton, has 
     been a part of the Olympic Winter Games since 2002. 
     It was first included as an official medal event in the 
     Winter Olympics during the Salt Lake City Games, which were 
     held in February of 2002. Since then, skeleton has been 
     contested in every Winter Olympics. In skeleton, athletes 
     race down an icy track on a small sled while lying face down 
     and head-first. The sport requires a combination of speed, 
     strength, and precision, and is known for its high speeds 
     and thrilling action. 
     I hope this helps! If you have any 
     other questions, just let me know.

     ## CORRECT (probably)
```
