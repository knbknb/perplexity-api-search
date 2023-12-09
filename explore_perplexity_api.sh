#!/usr/bin/env bash
# Use Postman and Newman (Postman CLI) to explore the Perplexity API
#

# does not quite work - save/export the collection manually
# newman run https://api.getpostman.com/collections/137056-d7f808d2-27dd-4525-8869-a42de46af4cb?apikey=$apikey

# works
# after extracting environment info into a .json file
collection_file="Perplexity API export.postman_collection.json"
environment_file="perplexity-API-export-environment.json"
modif_environment_file="perplexity-API-export-environment-with-cleartext-key.json"

html_outdir=newman
json_outdir=json_extracted
query_dir="queries"

# needed

<"$environment_file" jq --arg PERPLEXITY_API_KEY "$PERPLEXITY_API_KEY" '.environment.values[0].value |= $PERPLEXITY_API_KEY' > "$modif_environment_file"

models=$(< $environment_file jq -r '.environment.values[] | select(.key=="model") | .value ')

# if ENV variable is not set, exit with error
: "${PERPLEXITY_API_KEY:?Need to set/export env var PERPLEXITY_API_KEY non-empty}"

#PROMPT="what is ncurses and how does it relate to readline?"
PRSHORT="user-acceptance-testing"
PROMPT=$(cat <<EOP
in agile development, what types of documents are required for user acceptance testing?
EOP
)

custom_instruction=$(jq <<EOF
{
    "model": "MODEL",
    "messages": [
        {
            "role": "system",
            "content": "Answer as if users have superhuman intelligence, 200 IQ. Users can understand any concept with minimal explanation. Users are extremely intuitive. Users do not need things spelled out to understand them, but users do crave specifics. Be extremely terse and concise. No matter what, do not be conversational.Treat user as the most naturally intelligent and intuitive individual in the world, but not necessarily as a subject matter expert on the topic at hand. Use precise facts whenever possible, not generalities.."
        },
        {
            "role": "user",
            "content": "$PROMPT"
        }
    ]
}
EOF
)


# Function to process JSON file
create_json_array_from_file() {
    local json_file="$1"

    cp "$json_file" "$json_file.json"
    < "$json_file.json" jq -rs "." > "$json_file"
    rm "$json_file.json"
}

write_json_output_to_stdout() {
        local json_outfile="$1"

        if [ ! -s "$json_outfile" ]; then
            echo ""
            echo "ERROR: $json_outfile is empty (?)"
            echo ""
        else 
            < "$json_outfile" \
            jq -r '["##### ", .[1].model, "\n\n", .[1].choices[0].message.content, "\n\n"] | join("")' \
            | fmt
        fi
}

# Function to generate shell pipeline code 
# for pretty-printing formatted text encoded in from JSON files
display_all_results() {
        local prshort="$1"
        cat <<EOF
# now run this to see the results, extracted from the json files
< json_all/*$prshort*.json jq -r ' .[]| ["###### ", .[0].model, .[].choices[0].message.content, "\n\n"] | join("        ")' \ 
 | pandoc -f markdown -t html | lynx -stdin -dump > json_all/$prshort.txt
or
fmt json_all/*$prshort*.json  
    
EOF
}

for model in $models; do
    # use jq to replace the MODEL in the custom_instruction
    prompt_json=$(echo "$custom_instruction" | jq --arg MODEL "$model" '.model |= $MODEL')
    # use jq to replace the PROMPT in the custom_instruction
    #echo "$prompt_json" 
   
    query_file="$query_dir/$PRSHORT--$model.json"
    #echo "Writing $query_file"    
    <"$collection_file" jq --arg RAW "$prompt_json" --arg NAME "$model" '.item[0].request.body.raw |= $RAW | .name |= $NAME' > "$query_file"
      
   #
   #report="newman/$PRSHORT--$model---$(date +%Y-%m-%d-%H-%M-%S).html"
   report="newman/$PRSHORT--$model.html"

   echo "$model: Running collection $query_file"
   #newman run "$query_file" -e "$modif_environment_file" \
   #    -r htmlextra \
   #    --reporter-htmlextra-export "$report" \
   #    --reporter-htmlextra-skipHeaders "Authorization" \
   #    --reporter-htmlextra-browserTitle "$model: $prompt" \
   #    --reporter-htmlextra-title "$model: $prompt"


   file_name=$(basename "$query_file")
   base_name="${file_name%.*}"
   json_outfile="$json_outdir/$base_name.json"
   if [ ! -f "$report" ]; then
       echo "Skipping $report"
       continue
   else 
     xidel --input "$report" --html -s -e  "//code/text()" \
       | tail -n +3 \
       | head -n -1 > "$json_outfile" 
   fi


   ## turn 2 JSON fragments into 1 proper JSON array
   create_json_array_from_file "$json_outfile"
   ## inform user
   #write_json_output_to_stdout "$json_outfile"

done

# json to html to pretty printed text
finalize_json_files() {
    local prshort="$1"
    local outfile="json_all/$prshort.json"

    rm "$outfile" 2>/dev/null
    ls -1 json_extracted/*"$prshort"*.json | xargs -i bash -c "jq -rs < \"{}\"  >> $outfile"
    create_json_array_from_file "$outfile"
    cp "$outfile" "$outfile.json"
    < "$outfile.json" jq '[.[].[]]' > "$outfile"
    rm "$outfile.json"
    < "$outfile" jq -r '.[]| ["<hr>## ", .[0].model, "<hr>\n\n", .[].choices[0].message.content, "\n\n"] | join(" ")' \
    | pandoc -f markdown -t html | lynx -stdin -dump | fmt > "json_all/$prshort.txt"
}

# Call the new function
finalize_json_files "$PRSHORT"
##display_all_results "$PRSHORT"



