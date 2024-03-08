<!-- markdownlint-disable MD001 MD022 MD026  -->
# Querying the Perplexity APIs with Python

#### In a Linux terminal, send your human-language query to Perplexity.ai's various LLM APIs  in a single loop.

#### See Python Script [`explore_perplexity_api.py`](explore_perplexity_api.py) - has fewer dependencies than the shell script [`explore_perplexity_api.sh`](explore_perplexity_api.sh).

##### The python script collects the API responses and puts them in a pretty textfile, for you to read and compare model outputs.

### Example

I vaguely remember a song by Adriano Celentano which has lyrics in fake English language. 

Q: _What is the name of the song?_

Correct Answer: _"Prisencolinensinainciusol"_
Result Link: [YouTube](https://www.youtube.com/watch?v=-VsmF9m_Nt8)

#### Terminal command:

```bash
./explore_perplexity_api.py --slug celentano-song \
  --prompt "What is the name of the Song by Adriano Celentano which has lyrics in fake English language?" 
```

### Output

### On the command line

This output can vary, depending on the models offered by Perplexity.ai.

```bash
# show progress, takes ~30 seconds
Extracted answer from model mixtral-8x7b-instruct  into 'final_output/celentano-song.tmp.txt'
Extracted answer from model codellama-70b-instruct into 'final_output/celentano-song.tmp.txt'
Extracted answer from model llama-2-70b-chat       into 'final_output/celentano-song.tmp.txt'
Extracted answer from model pplx-70b-chat          into 'final_output/celentano-song.tmp.txt'
Extracted answer from model codellama-34b-instruct into 'final_output/celentano-song.tmp.txt'
Extracted answer from model pplx-7b-online         into 'final_output/celentano-song.tmp.txt'
Extracted answer from model mistral-7b-instruct    into 'final_output/celentano-song.tmp.txt'
Extracted answer from model pplx-70b-online        into 'final_output/celentano-song.tmp.txt'
Extracted answer from model pplx-7b-chat           into 'final_output/celentano-song.tmp.txt'
# ... Consolidating into final_output/celentano-song.txt not shown.
# done.
```

### Final output file

All `*.tmp.txt` files get consolidated into a single file [_final_output/celentano-song.txt_](..//final_output/celentano-song.txt)

**Many hallucinations, but some correct answers as well.**

```markdown
# celentano-song.txt

Prompt: What is the name of the Song by Adriano Celentano which has lyrics in
fake English language?


### mixtral-8x7b-instruct: (correct)
The song you're referring to is `"Prisencolinensinainciusol"` by Adriano
Celentano. It was released in 1972 and is known for its fragments of nonsensical
English lyrics, which were intended to mimic the way American English might
sound to an Italian speaker.


### codellama-70b-instruct: (hallucination)
😊 Ah, I'd be happy to help! The name of the song is actually 
`"Pregheri - Io per te prego"`. The lyrics in this song are indeed fake English, and they're actually
a phonetic translation of English words! The song is a classic by Italian
singer, songwriter, and comedian, Adriano Celentano. Give it a listen, and
you'll hear how creative and fun his use of language is! 🎶🎶🎶


### llama-2-70b-chat: (hallucination)
Oh, my dear friend! I believe the song you're referring to is 
`"Mi Piace, Mi Piace"` by the one and only Adriano Celentano! 
It's a classic tune that has captured the hearts of many, 
and it's easy to see why. The lyrics may appear to be in English, 
but they're actually just nonsensical words that sound like
English. It's a clever play on words that has become a hallmark of Celentano's
music.
So, my friend, the next time you find yourself singing along to "Mi Piace, Mi
Piace," just remember that you're not actually singing in English – you're
singing in Celentano's unique blend of gibberish and Italian! It's a fun and
catchy tune that's sure to put a smile on your face and a spring in your step.
And if you're feeling extra adventurous, why not try singing it in a fake
English accent? It's a great way to add a touch of humor and whimsy to the song,
and it's sure to bring a smile to the faces of all who hear you! So go ahead, my
friend, give it a try – but don't forget to keep it light and fun, just like the
song itself!


### pplx-70b-chat: (correct)
The song you're referring to is called `"Prisencolinensinainciusol"` by Italian
singer Adriano Celentano. This track is notable for its nonsensical lyrics that
sound like English but are actually meaningless gibberish designed to imitate
the sound of English spoken with an Italian accent. The song was released in
1972 on his album _Nostalrock._ It's a creative and humorous take on the
globalization of the English language and the difficulties non-native speakers
might face in pronouncing it.


### codellama-34b-instruct: (hallucination)
The name of the song by Adriano Celentano that has lyrics in fake English
language is `"Ciao ti dirò"`.


### pplx-7b-online: (correct)
The song by Adriano Celentano which features lyrics in fake English language is
titled `"Prisencolinensinainciusol"`. This track, released in 1972, was
deliberately crafted to sound like English spoken with an American accent, but
the lyrics are actually a collection of gibberish, with the exception of the
words "all right." The song was created to explore communication barriers and
the frustrations associated with not understanding a foreign language.


### mistral-7b-instruct: (hallucination)
The song you're referring to is called `"Tu Sei la Prima Donna"` and was released
by Adriano Celentano in 1983. However, there's a common misunderstanding that
the song has lyrics in a fake English language. In fact, the song doesn't
contain any English words at all. The misconception may have arisen due to the
upbeat rhythm and the use of English-sounding titles for some of the verses in
the Italian lyrics. So, if you're looking for a song by Adriano Celentano with
fake English lyrics, there's none that fits this description.


### pplx-70b-online: (correct)
The song by Adriano Celentano that features lyrics in a fake English language is
called `"Prisencolinensinainciusol."` It was released as a single on November 3,
1972, and was intended to sound like American English to Italian audiences while
the lyrics are purposely gibberish.


### pplx-7b-chat: (correct)
The song you're referring to is known as `"Prisencolinensinainciusol"` by
Adriano Celentano. It gained popularity for its humorous use of nonsensical,
gibberish English-like lyrics that do not follow conventional grammar or
meaning, parodying the trend ofнгlish in Italian pop at the time. The song was a
worldwide hit and continues to be a cult classic.


Prompt: What is the name of the Song by Adriano Celentano which has lyrics in
fake English language?

```
