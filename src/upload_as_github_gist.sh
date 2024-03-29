#!/usr/bin/env bash
# knb 20240101
# Shellscript to upload a bunch of textfiles to gist.github.com
# - files are txt files in subdirectory final_output
# - use curl to upload the file
# - use an environment variable for the github token, must be set on command line first
# - as gist filename use the filename of the .txt file
# - as description use line containing "content:" of each respective .txt file
# - use a for loop to iterate over all files

# if ENV variable is not set, exit with error
: "${GITHUB_TOKEN:?Need to set/export env var GITHUB_TOKEN non-empty. Check .git/config for github token.}"

# get list of all github gists, and write name into array
# - get json array of gistnames, turn into bash array
gist_names_json_array=$(curl -sL -X GET -H "Authorization: token $GITHUB_TOKEN"     https://api.github.com/gists | jq -s  'map(.[0], .[].files | keys) | flatten ')
gist_names=$(echo $gist_names_json_array | jq -r '.[]') 
# if gist_names is empty, stop
if [ ${#gist_names} -eq 0 ]; then
    echo "List 'gist_names' from github.com is empty, cannot continue"
    exit 1
fi
# if $filename is not in array of $gistnames, then upload file.
for file in final_output/*.txt; do
    filename=$(basename "$file")
    # get file modification date of $file, make it part of "Description:"
    # - get description from line containing "content:"
    # - get content from file, convert $content to json string
    mdate=$(stat -c %y "$file" | cut -d' ' -f1)
    description=$(head -1 "$file" | grep '"content":'  | sed 's/"content": //g' | sed 's/[#"]//g')
    description="Perplexity-API, $mdate: $description"
    content=$( jq -Rs . < "$file")
    
    if [[ ! " ${gist_names[@]}" =~ "${filename}" ]]; then
        echo "uploading $filename"
        # upload file to github gist
        curl -X POST -H "Authorization: token $GITHUB_TOKEN" \
          -d '{"description": "'"$description"'", "public": true, "files": {"'"$filename"'": {"content": '"$content"'}}}' \
          https://api.github.com/gists
    else
        echo "skipping '$filename', Gist already exists"
        continue
    fi
    
done

