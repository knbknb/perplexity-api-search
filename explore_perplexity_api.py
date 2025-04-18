#!/usr/bin/env python
# rewrite of the bash script explore_perplexity_api.sh

# TODO:
# ask the user for a prompt
# ask the user for a persona
# send the prompt to the API - get the responses from n=9 different AI models
#
# Keep the complete request and response metadata in json files (postman/newman do this)
#
#
# Required dependencies:
# - pip3 install argparse json os shutil subprocess sys dotenv bs4 
# - newman node binary must be installed and in the PATH
import sys
import os     
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

import argparse
from dotenv import load_dotenv

from validator import Validator
from model_processor import ModelProcessor
from utils import combine_json_files, write_pm_env_file, reformat_with_hyperlink_protection

def parse_arguments():
    parser = argparse.ArgumentParser(description='Explore Perplexity API')
    parser.add_argument('--prompt', required=True, help='Your question or task')
    parser.add_argument('--slug', required=True, help='Prompt slug')
    parser.add_argument('--persona', default="Default Persona", help='Persona')
    parser.add_argument('--persona-slug', help='Persona slug', default="NoRole")
    parser.add_argument('--model', help='Model to use (filter by this string)')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    return parser.parse_args()

def check_prerequisites(api_key, tools, directories):
        validator = Validator()
        validator.check_perplexity_api_key(api_key) # api key set?
        validator.check_tools(tools)                # cli tools installed?
        validator.check_directories(directories)    # local subdirectories exist?

def get_model_list(modellist_url=None):
    if not modellist_url:
        raise ValueError("Model list URL is required.")
    from bs4 import BeautifulSoup
    import requests
    response = requests.get(modellist_url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch model list from {modellist_url}. Status code: {response.status_code}")
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first and second tables
    card_headers = soup.find_all('h2', attrs={'contenteditable': 'false'})
    card_headers_clean = [h.get_text().strip() for h in card_headers]
    
    model_names = [header for header in card_headers_clean]

    return model_names

def main(api_key):
    args = parse_arguments()
    
    #(args.prompt, args.slug)
    directories = ['queries', 'json_extracted', 'newman', 'final_output']
    tools = ['newman']
    models = get_model_list(modellist_url=os.getenv('PERPLEXITY_MODELCARD_URL'))
    print (f"Models: {models}")
    check_prerequisites(api_key, tools, directories)
    write_pm_env_file(models, "postman/perplexity-API-export-environment.json",
                                       "postman/perplexity-API-export-environment-with-cleartext-key.json",
                                       api_key)
    model_processor = ModelProcessor()
    model_processor.process_models(models, args, "postman/Perplexity API export.postman_collection.json",
                   "postman/perplexity-API-export-environment-with-cleartext-key.json",
                   "queries", "newman", "json_extracted")
    
    tmp_txt_file = combine_json_files("json_extracted", 
                        "final_output", args.prompt, args.slug, args.persona, args.persona_slug)
    output_file = tmp_txt_file.replace(".tmp.txt", ".md")
    # reformats and also renames the file
    reformat_with_hyperlink_protection(tmp_txt_file, output_file, max_width=80)
    print (f"Output file: {output_file}")

    try:
        os.remove(tmp_txt_file)
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    load_dotenv()
    main(os.getenv('PERPLEXITY_API_KEY'))
