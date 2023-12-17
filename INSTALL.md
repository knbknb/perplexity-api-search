<!-- markdownlint-disable MD001 -->
# Querying the Perplexity API with Newman and Postman

## Developer Notes

In a Terminal, using a shell script, send your human-language query to various AI systems/models, in a single loop.
Collect the responses an put them in a pretty textfile.

See Shell Script [`explore_perlplexity_api.sh`](explore_perplexity_api.sh) - work in progress

## Prerequisites / Installation


##### Prerequsites

These command line tools must be installed:

- `node`, the JavaScript runtime
- `newman`, the Postman CLI, a `node` package
- `curl`, the HTTP client
- `jq`, the JSON parser
- `pandoc`, the document converter (for markdown to html)
- `lynx`, the commandline browser and HTML parser (for html to txt)
- `fmt`, the text formatter (for pretty text output)

This large binary GUI App should be installed, and you must know how to use it:

[Postman](https://getpostman.com), the GUI

All are free software.

#### What it does

Ask a query and get a pretty textfile with the responses from various AI systems/models, see [README-verbose.md](README-verbose.md) for more details.

The shell script [`explore_perlplexity_api.sh`](./explore_perplexity_api.sh) controls the NodeJS app `"newman"`, and newman loads artifacts exported from Postman.

On host "well", newman 6.0.0 is installed on Node 16 (use nvm to switch to 16)

```bash
nvm current
nvm use 16
npm i -g newman
npm install -g newman-reporter-htmlextra
```

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

See Shell Script `explore_perlplexity_api`.
