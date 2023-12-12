#!/usr/bin/env bash
# Use Postman and Newman (Postman CLI) to explore the Perplexity API.
# Requires obscure command-line tools newman, xidel, and jq version 1.7

## Command line arguments
## You must set a short prompt fragment, e.g. "user-acceptance-testing" (omit whitespace),
## and a longer prompt with the actual question or task

# example usage:
# . ./explore_perplexity_api.sh --prompt "translate this into emojis: 'you and me'" --slug "emojis-you-me"
PRSLUG="prompt-slug"
PROMPT="your question or task"
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --prompt)
            PROMPT=$2
            shift
            ;;
        --slug)
            PRSLUG=$2
            shift
            ;;
        *)
            echo '. ./explore_perplexity_api.sh --prompt "translate this into emojis: 'you and me'" --slug "emojis-you-me"'
            echo "Invalid option: $1" >&2
            exit 1
            ;;
    esac
    shift
done

#shift $((OPTIND-1))
# Check if PROMPT is empty
if [ -z "$PROMPT" ]; then
    echo "Missing required argument: --prompt PROMPT" >&2
    exit 1
else 
    echo "Using prompt --prompt '$PROMPT'"
fi

# Check if PRSLUG is empty
if [ -z "$PRSLUG" ]; then
    echo "Missing required argument: -prompt '...'" >&2
    exit 1
else
    echo "Using PRSLUG (prompt-fragment) --slug '$PRSLUG'"
fi
read -p "Press enter to continue"
mkdir -p queries json_extracted newman json_all
# works
# manual prerequisite one-off task: extract Postman environment info into a .json file
collection_file="Perplexity API export.postman_collection.json"
environment_file="perplexity-API-export-environment.json"
# this file should NOT be checked into git - contains the API key
modif_environment_file="perplexity-API-export-environment-with-cleartext-key.json"

html_outdir=newman
json_outdir=json_extracted
query_dir="queries"

# write API key to environment file
<"$environment_file" jq --arg PERPLEXITY_API_KEY "$PERPLEXITY_API_KEY" '.environment.values[0].value |= $PERPLEXITY_API_KEY' > "$modif_environment_file"

models=$(< $environment_file jq -r '.environment.values[] | select(.key=="model") | .value ')

# if ENV variable is not set, exit with error
: "${PERPLEXITY_API_KEY:?Need to set/export env var PERPLEXITY_API_KEY non-empty}"

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


# uses jq -rs to wrap everything into an enclosing array
enclose_filecontent_in_array() {
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
        local slug="$1"
        cat <<EOF
# now run this to see the results, extracted from the json files
< json_all/*$slug*.json jq -r ' .[]| ["###### ", .[0].model, .[].choices[0].message.content, "\n\n"] | join("        ")' \ 
 | pandoc -f markdown -t html | lynx -stdin -dump > json_all/$slug.txt
or
fmt json_all/*$slug*.json  
    
EOF
}

for model in $models; do
    # use jq to replace the MODEL in the custom_instruction
    prompt_json=$(echo "$custom_instruction" | jq --arg MODEL "$model" '.model |= $MODEL')
    # use jq to replace the PROMPT in the custom_instruction
    #echo "$prompt_json" 
   
    query_file="$query_dir/$PRSLUG--$model.json"
    #echo "Writing $query_file"    
    <"$collection_file" jq --arg RAW "$prompt_json" --arg NAME "$model" '.item[0].request.body.raw |= $RAW | .name |= $NAME' > "$query_file"
      
   #
   #report="newman/$PRSLUG--$model---$(date +%Y-%m-%d-%H-%M-%S).html"
   report="newman/$PRSLUG--$model.html"

   echo "$model: Running collection $query_file"
   newman run "$query_file" -e "$modif_environment_file" \
       -r htmlextra \
       --reporter-htmlextra-export "$report" \
       --reporter-htmlextra-skipHeaders "Authorization" \
       --reporter-htmlextra-browserTitle "$model: $prompt" \
       --reporter-htmlextra-title "$model: $prompt"


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
   enclose_filecontent_in_array "$json_outfile"
   ## inform user
   write_json_output_to_stdout "$json_outfile"

done

# json to html to pretty printed text
finalize_json_files() {
    local slug="$1"
    local outfile="json_all/$slug.json"

    rm "$outfile" 2>/dev/null
    ls -1 json_extracted/*"$slug"*.json | xargs -i bash -c "jq -rs < \"{}\"  >> $outfile"
    enclose_filecontent_in_array "$outfile"
    cp "$outfile" "$outfile.json"
    # requires jq 1.7
    < "$outfile.json" jq '[.[].[]]' > "$outfile"
    rm "$outfile.json"
    < "$outfile" jq -r '.[]| ["<hr>## ", .[0].model, "<hr>\n\n", .[].choices[0].message.content, "\n\n"] | join(" ")' \
    | pandoc -f markdown -t html | lynx -stdin -dump | fmt > "json_all/$slug.txt"
}

finalize_json_files "$PRSLUG"
##display_all_results "$PRSLUG"

