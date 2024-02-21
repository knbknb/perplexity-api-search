#!/usr/bin/env python
# rewrite of the bash script explore_perplexity_api.sh

# TODO:
# ask the user for a prompt
# ask the user for a persona
# send the prompt to the API - get the responses from n=9 different AI models
#
# Keep the complete request and resonse metadata in json files (postman/newman doq this)
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
from utils import combine_json_files, prepare_environment_files, reformat_with_hyperlink_protection

def parse_arguments():
    parser = argparse.ArgumentParser(description='Explore Perplexity API')
    parser.add_argument('--prompt', required=True, help='Your question or task')
    parser.add_argument('--slug', required=True, help='Prompt slug')
    parser.add_argument('--persona', default="Default Persona", help='Persona')
    parser.add_argument('--persona-slug', help='Persona slug')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    return parser.parse_args()

def check_prerequisites(api_key, tools, directories):
        validator = Validator()
        validator.check_perplexity_api_key(api_key)
        validator.check_tools(tools)
        validator.check_directories(directories)

def main(api_key):
    args = parse_arguments()
    
    #(args.prompt, args.slug)
    directories = ['queries', 'json_extracted', 'newman', 'final_output']
    tools = ['newman']
    check_prerequisites(api_key, tools, directories)
    models = prepare_environment_files("perplexity-API-export-environment.json",
                                       "perplexity-API-export-environment-with-cleartext-key.json",
                                       api_key)
    
    model_processor = ModelProcessor()
    #models = models[0:2]
    model_processor.process_models(models, args, "Perplexity API export.postman_collection.json",
                   "perplexity-API-export-environment-with-cleartext-key.json",
                   "queries", "newman", "json_extracted")
    
    tmp_txt_file = combine_json_files("json_extracted", 
                        "final_output", args.prompt, args.slug)
    output_file = tmp_txt_file.replace(".tmp.txt", ".txt")
    reformat_with_hyperlink_protection(tmp_txt_file, output_file, max_width=80)
    
    try:
        os.remove(tmp_txt_file)
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    load_dotenv()
    main(os.getenv('PERPLEXITY_API_KEY'))
