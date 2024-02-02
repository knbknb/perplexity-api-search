#!/usr/bin/env python
# UNDER CONSTRUCTION
# rewrite of the bash script explore_perplexity_api.sh

# ask the user for a prompt
# ask the user for a persona
# send the prompt to the API - get the responses from n=7 different AI models
#
# Keep the complete request and resonse metadata in json files (postman/newman doq this)
#
#
# Required dependencies:
# pip3 install argparse json os shutil subprocess

import argparse
import json
import os
import sys  # For sys.exit()
import shutil
#import subprocess
from dotenv import load_dotenv


def check_tools(tools):
    for tool in tools:
        if shutil.which(tool) is None:
            raise SystemExit(f"Tool {tool} could not be found. Needed for selecting and changing custom instructions.")

def check_arguments(prompt, slug):
    if not prompt:
        print("Missing required argument: --prompt PROMPT", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"Using prompt --prompt '{prompt}'")

    if not slug:
        print("Missing required argument: --slug SLUG", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"Using SLUG (prompt-fragment) --slug '{slug}'")

def check_directories(directories):
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def check_perplexity_api_key(perplexity_api_key):
    if not perplexity_api_key:
        raise ValueError('Please set the environment variable PERPLEXITY_API_KEY')
    
def write_json_output_to_stdout(json_outfile):
    if not os.path.isfile(json_outfile) or os.path.getsize(json_outfile) == 0:
        print("ERROR: {} is empty (?)".format(json_outfile))
    else:
        with open(json_outfile, 'r') as file:
            data = json.load(file)
            # Process and print data as needed
            pretty_data = json.dumps(data, indent=4)
            print(pretty_data)


def write_pm_env_file(json_infile, json_outfile, PERPLEXITY_API_KEY):
    
    with open(json_infile, "r") as f:
        data = json.load(f)
        # Process and print data as needed
        #pretty_data = json.dumps(data, indent=4)
        #print(pretty_data)
        data["environment"]["values"][0]["value"] = PERPLEXITY_API_KEY
    with open(json_outfile, "w") as f:
        json.dump(data, f)
    #shutil.rmtree(json_infile)

def extract_models(environment_file):
    with open(environment_file) as file:
        data = json.load(file)
        models = [value["value"] for value in data["environment"]["values"] if value["key"] == "model"]
    return models

def set_custom_instruction_fragment(persona, prompt):
    custom_instruction = {
        "model": "MODEL",
        "messages": [
            {"role": "system", "content": persona},
            {"role": "user", "content": prompt}
        ]
    }
    return json.dumps(custom_instruction)

def main(api_key):
    collection_file  = "Perplexity API export.postman_collection.json"
    environment_file = "perplexity-API-export-environment.json"
    # this file should NOT be checked into git - contains the API key
    modif_environment_file = "perplexity-API-export-environment-with-cleartext-key.json"

    html_outdir = "newman"
    json_outdir = "json_extracted"
    query_dir   = "queries"

    parser = argparse.ArgumentParser(description='Explore Perplexity API')
    parser.add_argument('--prompt', required=True, help='Your question or task')
    parser.add_argument('--slug',   required=True, help='Prompt slug')
    parser.add_argument('--persona', default="Default Persona", help='Persona')
    parser.add_argument('--persona-slug',                       help='Persona slug')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()

    SLUG    = args.slug
    PROMPT  = args.prompt
    PERSONA = args.persona
    PSLUG   = args.persona_slug
    VERBOSE = args.verbose

    directories = ['queries', 'json_extracted', 'newman', 'final_output']
    tools = ['curl', 'jq', 'yq', 'fzf', 'fold', 'tput']

    # Check for required tools
    check_perplexity_api_key(api_key)
    check_tools(tools)
    check_arguments(PROMPT, SLUG)
    check_directories(directories)
    
    write_pm_env_file(environment_file, modif_environment_file, os.getenv('PERPLEXITY_API_KEY'))
    #models=$(< $environment_file jq -r '.environment.values[] | select(.key=="model") | .value ')
    models = extract_models(environment_file)
    print(f"Using models: {models}")
    set_custom_instruction_fragment(PERSONA, PROMPT)

    # todo: merge custom instruction fragment into environment file
    # todo: loop over models
    # process the model responses (json files) into a single json file and/or html file (report)
    # merge the json files into a single text file

    # Use subprocess.run or similar to execute shell commands
    # For example:
    #result = subprocess.run(['your_command_here'], stdout=subprocess.PIPE)

    # Print or process the results as required

if __name__ == "__main__":
    load_dotenv()
    api_key=os.getenv('PERPLEXITY_API_KEY')    
    main(api_key)
