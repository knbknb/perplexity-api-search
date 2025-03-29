<!-- markdownlint-disable MD001 MD022 MD026  -->
# Batch Prompting the Perplexity APIs with Python

#### In a Linux terminal, send your human-language query to Perplexity.ai's various LLM APIs  in a single loop.

#### See Python Script [`explore_perplexity_api.py`](explore_perplexity_api.py) - has fewer dependencies than the shell script [`explore_perplexity_api.sh`](explore_perplexity_api.sh).

#### The python script collects the API responses and puts them in a pretty textfile, for you to read and compare model outputs.

#### Example

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

This output can vary, depending on the models offered by Perplexity.ai. These models were available at the time of writing, Spring 2024:

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
```

And one year later, Spring 2025:  
(the models have changed, but the script still works):

```bash

Extracted answer from model llama-3.1-sonar-huge-128k-online into 'final_output/celentano-song--NoRole.tmp.txt'
Extracted answer from model llama-3.1-sonar-large-128k-online into 'final_output/celentano-song--NoRole.tmp.txt'
Extracted answer from model llama-3.1-sonar-small-128k-online into 'final_output/celentano-song--NoRole.tmp.txt'
Extracted answer from model r1-1776 into 'final_output/celentano-song--NoRole.tmp.txt'
Extracted answer from model sonar into 'final_output/celentano-song--NoRole.tmp.txt'
Extracted answer from model sonar into 'final_output/celentano-song--NoRole.tmp.txt'
Extracted answer from model sonar-deep-research into 'final_output/celentano-song--NoRole.tmp.txt'
Extracted answer from model sonar-pro into 'final_output/celentano-song--NoRole.tmp.txt'
Extracted answer from model sonar-pro into 'final_output/celentano-song--NoRole.tmp.txt'
Extracted answer from model sonar-reasoning into 'final_output/celentano-song--NoRole.tmp.txt'
Extracted answer from model sonar-reasoning-pro into 'final_output/celentano-song--NoRole.tmp.txt'

# ... Consolidating into final_output/celentano-song.txt not shown.
# done.
```

Today the above list of models supported by Perplexity might have changed again.

See the [Perplexity List of Models](https://docs.perplexity.ai/guides/model-cards).

### Final output file, 2024

All `*.tmp.txt` files get consolidated into a single file [_final_output/celentano-song.txt_](..//final_output/celentano-song.txt)

**Spring 2024: Many hallucinations, but some correct answers as well.**

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


--------------------------------------------------
```

All `*.tmp.txt` files were consolidated into a single file [_final_output/celentano-song.txt_](..//final_output/celentano-song--NoRole.md)

**Spring 2025: Mostly correct answers as well.**

```markdown

### llama-3.1-sonar-huge-128k-online:

The song by Adriano Celentano that features lyrics in fake English is titled
**"Prisencolinensinainciusol"**. It was released in 1972 and was designed to
mimic the sound of American English to non-English speakers, using nonsensical
gibberish instead of actual words[1][2][3].


### llama-3.1-sonar-large-128k-online:

The song by Adriano Celentano with lyrics in fake English is titled
**"Prisencolinensinainciusol"**. Released in 1972, the song is known for its
gibberish lyrics that are intended to mimic the sound of American English to
non-English speakers, despite having no actual meaning[1][3][4].


### llama-3.1-sonar-small-128k-online:

The song by Adriano Celentano that has lyrics in fake English is titled
"Prisencolinensinainciusol." This song was released in 1972 and was intended to
sound like American English to Italian listeners, despite its nonsensical and
deliberately unintelligible lyrics[1][3][5].


### r1-1776:

<think>
Okay, the user is asking about a song by Adriano Celentano that has lyrics in
fake English. Hmm, I remember that Adriano Celentano is an Italian artist,
right? He's been around for a while. The mention of fake English makes me think
of that one song that sounds like English but isn't actually using real words.
Let me try to recall... Was it from the 70s or 80s? I think the song was created
to mimic the sound of American English without any real meaning, just to show
how English sounds to non-speakers.
Wait, the title might be something like "Prisencolinensinainciusol." That sounds
familiar. Let me check that. Yes, the song is called
"Prisencolinensinainciusol," released in 1972. It's meant to resemble English
but is actually complete gibberish. Celentano wanted to critique the way people
often adopt foreign languages without understanding them. The song became quite
popular because of its unique concept and catchy rhythm.
I should confirm the spelling of the title. Sometimes it's written as
"Prisencolinensinainciusol" all together. Maybe the user has heard it before and
is trying to remember the name. Also, adding some context about why he made the
song could be helpful. Did Celentano have other similar songs? Not sure, but
this one is the most famous for that gimmick. Let me make sure there aren't
other contenders. I think another song of his with gibberish is "L'Unica
Chance," but the main one is Prisencolinensinainciusol. Yeah, that's the one. I
should also mention that it's a commentary on communication barriers. Alright,
that's probably the answer they're looking for.
</think>
The song by Adriano Celentano that features lyrics in nonsensical, fake English
is titled **"Prisencolinensinainciusol"**, released in 1972. Celentano created
it as a satirical commentary on language barriers and global communication,
mimicking the sound of American English while using entirely invented words. The
upbeat, rhythmic track became iconic for its clever parody of how English might
sound to non-speakers.


### sonar:

The song by Adriano Celentano with lyrics in fake English is titled
**"Prisencolinensinainciusol"**. Released in 1972, it was designed to mimic the
sound of American English to non-English speakers, particularly Italians. The
song features improvised, nonsensical lyrics that sound like English but are
actually gibberish, with only a couple of recognizable English words like "all"
and "right" throughout the song[1][2][3]. Despite its nonsensical nature,
"Prisencolinensinainciusol" became a hit in several European countries,
including Italy, France, Germany, and Belgium[4][5].


### sonar:

The song you're referring to is **"Prisencolinensinainciusol"** by Adriano
Celentano. It was released in 1972 and features lyrics that are intended to
mimic the sound of American English but are actually nonsensical gibberish, with
the exception of a few recognizable words like "all" and "right"[1][2]. The song
was a famous experiment to see how English sounds to non-native speakers and has
become a celebrated example of linguistic creativity in music.


### sonar-deep-research:

<think>
Okay, so the user is asking for the name of the song by Adriano Celentano that
has fake English lyrics. Let me start by recalling the search results provided.
First, looking at the search results, multiple sources mention Adriano Celentano
and a song from the 1970s with nonsense lyrics meant to mimic American English.
Source  directly states the song is "Prisencolinensinainciusol" from 1972.
That's a good lead. Let me check other sources to confirm.
Source [1] also mentions the same title, "Prisencolinensinainciusol", and
provides details about its release in 1972 and its popularity. Source [2], a
YouTube video, again references the same song title. Source [3] from News18
confirms the same information, noting it was a hit in the '70s.
Looking further, source [4] on Status-Q again mentions
"Prisencolinensinainciusol" as the song with gibberish lyrics intended to sound
like English. Source [5] from Actualized.org talks about Adriano Celentano
releasing a song with fake English lyrics in the '70s, which aligns with the
other sources. Source [6] is a YouTube video that reiterates the title and the
year 1972. Finally, source [7] gives the full title and explains the intent
behind the song.
All the sources consistently point to "Prisencolinensinainciusol" as the song in
question. Each source also confirms that the lyrics are nonsensical but designed
to imitate American English, supporting the user's query. No conflicting
information is present across the sources, so the answer is clear.
</think>
The song by Adriano Celentano featuring lyrics in fabricated English is
**"Prisencolinensinainciusol"**, released in 1972[1][3]. Designed to mimic the
sound of American English to Italian listeners, the track uses nonsensical
phonetic approximations of English words, with only "all right" being
intelligible[1][4].
Celentano aimed to critique communication barriers rather than create a novelty
hit, reflecting frustrations of misunderstanding through deliberately
unintelligible lyrics[1][7]. Despite its satirical origins, the song topped
charts across Europe and regained viral popularity in recent decades via YouTube
and media appearances[3][6]. Its title, stylized as
*"PRİSENCÓLİNENSİNÁİNCIÚSOL"* on the single cover, became iconic for blending
absurdist language with a critique of cultural trends[3][7].


### sonar-pro:

The song by Adriano Celentano with lyrics in fake English is called
"Prisencolinensinainciusol"[1][2][3]. This song was released in 1972 and became
a hit in Italy and other European countries[1][2]. The lyrics are intentionally
nonsensical gibberish meant to sound like American English to non-English
speakers, particularly Italians[1][3]. Celentano created this song to express
the idea of communication barriers and to show that Italians would enjoy any
song that sounded American[1][6]. Despite having no real meaning, the song
topped charts in several countries and has remained popular over the
decades[2][3].


### sonar-pro:

The song by Adriano Celentano that has lyrics in fake English is called
"Prisencolinensinainciusol"[1][3]. Released in 1972, this Italian pop song
features nonsensical lyrics designed to sound like American English to
non-English speakers, particularly Italians[1][3]. Despite containing mostly
gibberish words, the song became a hit not only in Italy but also in several
other European countries[1][3].


### sonar-reasoning:

<think>
Okay, let's tackle this query. The user is asking for the name of the song by
Adriano Celentano that has fake English lyrics. The search results provided
several sources, so I need to go through them to confirm the title.
Looking at the first search result, it mentions "Prisencolinensinainciusol" from
1972 as the song with nonsense lyrics that mimic American English. The second
result also refers to the same song, noting that only two English words are
present: "all" and "right." The third result from 2025 again confirms the song
title and explains that it's entirely gibberish designed to sound like English.
The fourth source from Now I Know in 2013 gives the same title and describes the
process of creating fake English. The fifth link is a YouTube video with the
song title in the URL and description. The sixth result on MetaFilter discusses
the song by title and artist.
All these sources consistently mention "Prisencolinensinainciusol" as the
correct title. No conflicting information is present. The song was released in
1972, became popular in Europe, and is known for its fake English lyrics aimed
at sounding like American English to Italian listeners. The artist's intention
was to explore communication barriers, which is also mentioned across multiple
sources.
I should structure the answer to clearly state the song's name, mention the
artist, and provide context about its creation and purpose. Including key points
like the year of release, the approach of mimicking English phonetics, and the
song's popularity would be useful. Citations from the search results should be
appropriately placed after relevant statements.
</think>
The Italian song by Adriano Celentano with fake English lyrics is titled
**"Prisencolinensinainciusol"** (often stylized with accent marks)[2][4].
Released in 1972, it features gibberish vocals designed to mimic the phonetic
rhythm and intonation of American English, rather than using actual words[2][3].
**Key Details**:
- **Creation**: Celentano ad-libbed nonsensical syllables to approximate the
sound of English, with only "all" and "right" being recognizable English
words[1][5].
- **Purpose**: Intended to highlight communication barriers, the song became a
linguistic experiment addressing frustration in cross-cultural
misunderstandings[2][3].
- **Impact**: The track topped charts in Italy, France, Belgium, and the
Netherlands, and gained renewed popularity in the 2000s through viral internet
content and television appearances[1][2][4].
Despite its gibberish nature, the song’s structure closely matches English
prosody (pacing and emphasis), creating the illusion of understandable
lyrics[2][5].


### sonar-reasoning-pro:

<think>
Okay, so the user is asking for the name of Adriano Celentano's song that has
fake English lyrics. Let me start by recalling that Adriano Celentano is an
Italian singer known for this particular song. From the search results provided,
there's a consistent mention of a song from the 1970s with nonsensical lyrics
meant to mimic American English.
Looking at the first search result, it mentions "Prisencolinensinainciusol" as
the 1972 song. The second result also confirms this title, noting that the
lyrics are mostly gibberish except for "all" and "right". Other sources like
[3], [4], and [5] all reference the same song title. There's a TikTok video in
[2] that also refers to the song by this name.
The key points here are the song's intent to mimic English sounds, its release
in the early '70s, and its popularity despite the gibberish lyrics. Results [3]
and [7] elaborate on Celentano's purpose: to explore communication barriers and
how English sounds to non-speakers. The song's structure uses American English
phonetics and rhythm, contributing to its realistic yet meaningless lyrics.
Multiple sources, including [6] and [8], reinforce the title
"Prisencolinensinainciusol" and its success in European charts. The song's
resurgence in popularity through platforms like YouTube and its use in TV shows
like Fargo is noted in [1] and [3].
I need to ensure that the song title is spelled correctly. From the sources,
variations include stylized versions with accents, but the standard spelling is
"Prisencolinensinainciusol". Each source consistently uses this title, so I can
be confident that's the correct answer. Additionally, the song's purpose and
impact are well-documented across the search results, which adds credibility to
the information.
</think>
The song by Adriano Celentano featuring intentionally nonsensical lyrics
designed to mimic American English is titled **"Prisencolinensinainciusol"**.
Released in 1972, this experimental track became a hit across Europe, topping
charts in Italy, France, Belgium, and the Netherlands[3][6].


### Key Details:

- **Concept**: The lyrics are gibberish but rhythmically imitate American
English phonetics and slang, with only "all right" being recognizable. Celentano
aimed to highlight communication barriers and how English sounds to
non-speakers[3][5][7].
- **Cultural Impact**: Despite its playful absurdity, the song resonated as a
critique of global communication breakdowns. It later gained renewed popularity
through memes, TV shows (*Fargo*, *Ted Lasso*), and a 2021 cover by Italian
artist Madame[1][3][7].
- **Legacy**: Praised for its innovative blend of funk, disco, and proto-rap
elements, the track remains a linguistic curiosity and a viral sensation decades
later[3][8][10].
For a firsthand experience, listen to the song’s[YouTube
performance](https://www.youtube.com/watch?v=81tDLcnKP5M), where Celentano’s
energetic delivery turns gibberish into a cultural statement[5][13].
https://www.youtube.com/watch?v=81tDLcnKP5M),
.
--------------------------------------------------
> Prompt: What is the name of the Song by Adriano Celentano     that has lyrics
in fake English language?
> Persona: Default Persona

```



## Alternatively, ....


For much simpler batch prompting via the command line, I recommend Simon Willison's [llm](https://github.com/simonw/llm) tool, `pip install llm`.

`llm "Where is Plutonia?"  # single query`  

Small batch:

    for loc in 'Literature' 'Computer Gaming'; do llm "Where is Plutonia in $loc?"; done

(Requires API keys for LLMs as well.)
