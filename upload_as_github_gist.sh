#!/usr/bin/env bash

# write a program to upload a file to github gist
# - files are txt files in subdirectory json_all
# - use curl to upload the file
# - use an enironment variable for the github token
# - as gist filename use the filename of the .txt file
# - as description use line containing "content:" of each respective .txt file

# - use a for loop to iterate over all files

# if ENV variable is not set, exit with error
: "${GITHUB_TOKEN:?Need to set/export env var GITHUB_TOKEN non-empty. Check .git/config for github token.}"

# get list of all github gists, and write name into array
# - get json array of gistnames
gist_names_json_array=$(curl -sL -X GET -H "Authorization: token $GITHUB_TOKEN"     https://api.github.com/gists | jq -s  'map(.[0], .[].files | keys) | flatten ')
gist_names=$(echo $gist_names_json_array | jq -r '.[]')

# get list of all files in subdirectory json_all
for file in json_all/*.txt; do
    # get filename without path
    filename=$(basename "$file")
    # get file modification date of $file

    mdate=$(stat -c %y "$file" | cut -d' ' -f1)
    # get description from line containing "content:"
    description=$(head -1 "$file" | grep '"content":'  | sed 's/"content": //g' | sed 's/[#"]//g')
    description="Perplexity-API, $mdate: $description"
    # get content from file, convert $content to json string
    content=$( jq -Rs . < "$file")
    
    # if $filename is not in array of $gistnames, then upload file
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

