<!-- markdownlint-disable MD001 -->
# Querying the Perplexity API with Newman and Postman

## Developer Notes

In a Terminal, using a Python script, send your human-language query to various AI systems/models, in a single loop.
Collect the responses an put them in a pretty textfile.

See Python Script [`explore_perplexity_api.py`](../explore_perplexity_api.py) - work in progress

## Prerequisites / Installation

##### Prerequsites - python script

For the Python script [explore_perplexity_api.py](../explore_perplexity_api.py), these command line tools must be installed:

- `node`, the JavaScript runtime
- `newman`, the Postman CLI, a `node` package

Use the Python script.

##### Prerequsites - shell script

There is an older, less powerful [shell script `explore_perlplexity_api.sh`](../explore_perplexity_api.sh)  in the `src/script-attic` directory. It is a prototype, and it is not maintained. It is not recommended to use it.

## Running exported Postman collection locally

Convenient and easy to control and customize- but requires exporting the collection and environment settings. No longer syncs with Postman.

##### Extract Postmand environment info into a local file

Run the following command

```bash
curl -sL "https://api.getpostman.com/environments/$envid?apikey=$apikey"
    
```

You environment info will be in a file like `perplexity-API-export-environment.json`

In the collection.json file, replace the `$pplx_api_key` with the actual key.

```bash
perl -pi -E "s/\$pplx_api_key/$pplx_api_key/g" Perplexity-API-for-newman.postman_collection.json
```

## Running an exported Postman collection from a file

Create a collection in Postman containing only a single HTTP request. In a shell script, send a query to various AI sysmtes/models in a single loop.

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
# needed for one-off export of collection and environment
export postman_apikey=PMAK-.............
export collid=137056-d7f808d2-27dd-4525-8869-a42de46af4cb
export envid=137056-ae5d3cc7-d7f7-450b-8737-c95a7b9e8f85
export pplx_api_key=pplx-........................

# extract the placeholder string for the api key  from the environment file, 
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

See Shell Script `explore_perlplexity_api`.
