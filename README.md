<!-- markdownlint-disable MD001 -->
# Querying the Perplexity API with Newman and Postman

See Shell Script `explore_perlplexity_api` - work in progress

## Prerequisites / Installation

The shell script controls newman and newman loads artifacts from Postman

On host "well", newman 6.0.0 is installed on Node 16 (use nvm to switch to 16)

```bash
nvm current
nvm use 16
npm i -g newman
npm install -g newman-reporter-htmlextra
```

## Running the collection remotely, and exporting the collection settings

A cool way to run a Postman collection via api.postman.com:

```bash
newman run https://api.getpostman.com/collections/XXXXX-XXXXX-XXXXX-XXXXX-XXXXX?apikey=YYYYY-YYYYY-YYYYY-YYYYY-YYYYY
```

This way the some JavaScript (for executing API requests and tests) is run from the terminal/node. This mode of execution keeps local files in sync with the Postman collection.

For the link above, the CollectionId can be found in the Postman GUI: by clicking on the collection and then click on the "i" info icon. That icon is on the folder collection info sidebar on the right.

The Postman API Key can be found by clicking on the user icon on the top right and then click on the "Settings" menu item. On the sidebar on the left, there is an entry API Key.

##### Some useful variables, keys and codesnippets

```bash
export postman_apikey=PMAK-.............
export collid=137056-d7f808d2-27dd-4525-8869-a42de46af4cb
export envid=137056-ae5d3cc7-d7f7-450b-8737-c95a7b9e8f85
export pplx_api_key=pplx-........................

# extract the api key from the environment file, 
environment_file=perplexity-API-export-environment.json
pplx_api_key=$(<  $environment_file jq -r '.environment.values[] | select(.key=="PERPLEXITY_API_KEY") | .value')
echo "PERPLEXITY_API_KEY=$pplx_api_key" >> .env
# optional
export perplexity_api_key=$(cat .env | grep PERPLEXITY_API_KEY | cut -d= -f2)
#now set as env variable, then run shellscript with that ENV variable
```

##### Run collection remotely, see results in terminal

```bash
# does not quite work
# permissions/sharing settings not set correctly
newman run https://api.getpostman.com/collections/137056-d7f808d2-27dd-4525-8869-a42de46af4cb?apikey=$apikey
```

## Running collection locally

More convenient and more control, but requires exporting the collection and environment settings. No longer syncs with Postman.

##### Extract environment info into a local file

and then run the following command

```bash
curl -sL "https://api.getpostman.com/environments/$envid?apikey=$apikey"
    
```

In the collection.json file, replace the `$pplx_api_key` with the actual key.

```bash
perl -pi -E "s/\$pplx_api_key/$pplx_api_key/g" Perplexity-API-for-newman.postman_collection.json
```

## Running the collection from a file

Create a collection in Postman containing only a single HTTP request. In a shell script, permute various endpoints in a loop.

See Shell Script `explore_perlplexity_api`.
