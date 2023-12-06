#!/usr/bin/env bash
# Use Postman and Newman (Postman CLI) to explore the Perplexity API
#

# does not quite work - save/export the collection manually
# newman run https://api.getpostman.com/collections/137056-d7f808d2-27dd-4525-8869-a42de46af4cb?apikey=$apikey

# extract environemnt info into a file
collection_file="Perplexity API export.postman_collection.json"
environment_file="perplexity-API-export-environment.json"
modif_environment_file="perplexity-API-export-environment-with-cleartext-key.json"

html_outdir=newman
json_outdir=json_extracted
query_dir="queries"

# needed

<"$environment_file" jq --arg PERPLEXITY_API_KEY "$PERPLEXITY_API_KEY" '.environment.values[0].value |= $PERPLEXITY_API_KEY' > "$modif_environment_file"

models=$(< $environment_file jq -r '.environment.values[] | select(.key=="model") | .value ')
prompt_json=$(jq <<EOF
{
    "model": "MODEL",
    "messages": [
        {
            "role": "system",
            "content": "Answer as if users have superhuman intelligence, 200 IQ. Users can understand any concept with minimal explanation. Users are extremely intuitive. Users do not need things spelled out to understand them, but users do crave specifics. Be extremely terse and concise. No matter what, do not be conversational.Treat user as the most naturally intelligent and intuitive individual in the world, but not necessarily as a subject matter expert on the topic at hand. Use precise facts whenever possible, not generalities.."
        },
        {
            "role": "user",
            "content": "PROMPT"
        }
    ]
}
EOF
)

#PROMPT="at which locations was the Film 'Nosferatu' from 1979 shot?"

#PROMPT="In jq, what are the idioms beginning with the @ symbol called?"
#PROMPT="In German bundeslige, which teams had once twins as players?"
PROMPT="Why do some professional athletes injure themselves during simple tasks like warming up?"
# use jq to replace the MODEL in the prompt_json
for model in $models; do
    prompt_json=$(echo "$prompt_json" | jq --arg MODEL "$model" '.model |= $MODEL')
    # use jq to replace the PROMPT in the prompt_json
    prompt_json=$(echo "$prompt_json" | jq --arg PROMPT "$PROMPT" '.messages[1].content |= $PROMPT')
    echo "$prompt_json" 

    # for each model, write new collection files with the "prompt_json" json-encoded 
    # in place of the "prompt" variable in the collection file
    modif_collection_file="$query_dir/$PROMPT-$model.json"
    echo "Writing $modif_collection_file"
    <"$collection_file" jq --arg RAW "$prompt_json" '.item[0].request.body.raw |= $RAW' > "$modif_collection_file"
    # open the file and replace the value of .item[0].name with $prompt
    cp "$modif_collection_file" "$modif_collection_file.json"
    < "$modif_collection_file.json" jq --arg PROMPT "$PROMPT" '.item[0].name |= $PROMPT' > "$modif_collection_file"
    rm "$modif_collection_file.json"

    report="newman/$PROMPT-$model-$(date +%Y-%m-%d-%H-%M-%S).html"
    echo "Running $modif_collection_file"
    newman run "$modif_collection_file" -e "$modif_environment_file" \
        -r htmlextra \
        --reporter-htmlextra-export "$report" \
        --reporter-htmlextra-skipHeaders "Authorization" \
        --reporter-htmlextra-browserTitle "$model: $prompt" \
        --reporter-htmlextra-title "$model: $prompt"


    file_name=$(basename "$modif_collection_file")
    base_name="$PROMPT-${file_name%.*}"
    json_outfile="$json_outdir/$base_name.json"
    echo "'$json_outfile' written (JSON response)"

    xidel --input "$report" --html -s -e  "//code/text()" \
        | tail -n +3 \
        | head -n -1 > "$json_outfile"
    cp "$json_outfile" "$json_outfile.json"
    < "$json_outfile.json" jq -rs "." > "$json_outfile"
    rm "$json_outfile.json"
    
    # output the relevant fields to the shell
    < "$json_outfile" \
    jq -r '[.[1].model, .[1].choices[0].message.content, \"\n\n\"] | join(":        ")' \
    | fmt
    #< "$json_outfile" gron
done
echo "$PROMPT"

cat <<'EOF'
# now run this to see the results, extracted from the json files
ls -1 json_extracted/*PROMPT_SUBSTRING* \
  | xargs -i bash -c "jq -r '[.[1].model, .[1].choices[0].message.content, \"\n\n\"] | join(\":        \")'  \"{}\""
EOF

#ls -1 json_extracted/*PROMPT_SUBSTRING* | xargs -i bash -c "jq -r '[.[1].model, .[1].choices[0].message.content, \"\n\n\"] | join(\":        \")'  \"{}\"" | fmt