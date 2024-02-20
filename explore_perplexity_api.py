#!/usr/bin/env python
# rewrite of the bash script explore_perplexity_api.sh

# ask the user for a prompt
# ask the user for a persona
# send the prompt to the API - get the responses from n=9 different AI models
#
# Keep the complete request and resonse metadata in json files (postman/newman doq this)
#
#
# Required dependencies:
# pip3 install argparse json os shutil subprocess

import argparse
import json
import os     
import sys    # For sys.exit()
import shutil # For shutil.which() / check_tools()
import subprocess # for newman
import textwrap
import re

from dotenv import load_dotenv

from bs4 import BeautifulSoup
import glob

def extract_json_from_html_report(report_file):
    """
    Extracts valid JSON data from HTML report files.

    Args:
        report_file (str): Path to the HTML report file.

    Returns:
        list: A list of valid JSON objects extracted from the report.
    """
    valid_json_data = []
    try:
        with open(report_file, 'r') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            code_elements = soup.find_all('code')
            for code in code_elements:
                try:
                    json_data = json.loads(code.get_text())
                    valid_json_data.append(json_data)
                except json.JSONDecodeError:
                    continue  # Skip non-JSON or malformed JSON
    except FileNotFoundError:
        print(f"File not found: {report_file}", file=sys.stderr)
    except Exception as e:
        print(f"Error processing file {report_file}: {e}", file=sys.stderr)
    return valid_json_data

def check_tools(tools):
    '''
    Checks if the required cli tools are available in the operating system.
    '''
    for tool in tools:
        if shutil.which(tool) is None:
            raise SystemExit(f"Tool {tool} could not be found. Needed for selecting and changing custom instructions.")

def check_arguments(prompt, slug):
    '''
    Checks if the required arguments are present. Exits the program if not.
    '''
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
    
    # TODO make persona optional

def check_directories(directories):
    '''
    Checks if the required directories are present. Creates them if not.
    '''
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def check_perplexity_api_key(perplexity_api_key):
    '''
    Checks if the PERPLEXITY_API_KEY environment variable is set. Exits the program if not.
    '''
    if not perplexity_api_key:
        raise ValueError('Please set the environment variable PERPLEXITY_API_KEY')
    
def write_json_output_to_stdout(json_string):
    """
    Extracts a specific JSON subelement and formats it for output.

    Args:
        json_string (str): The JSON string containing the data.

    Returns:
        str: The formatted output string.
    """

    try:
        # Load the JSON data
        data = json.loads(json_string)

        # Check if the data is empty
        if not data:
            return ""

        # Extract the desired subelement
        model = data[1]["model"]
        message = data[1]["choices"][0]["message"]["content"]

        # Format the output
        output = f"##### {model}\n\n{message}\n\n"

        # Print the formatted output (equivalent of writing to stdout)
        print(output)

    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error processing JSON: {e}")


def write_pm_env_file(json_infile, json_outfile, PERPLEXITY_API_KEY):
    '''
    Writes a new Postman environment file on the fly, to include the API key.
    '''
    with open(json_infile, "r") as f:
        data = json.load(f)
        data["environment"]["values"][0]["value"] = PERPLEXITY_API_KEY
    with open(json_outfile, "w") as f:
        json.dump(data, f)


def extract_models(environment_file):
    '''
    Extracts the Perplexity API model names from the environment file.
    '''
    with open(environment_file) as file:
        data = json.load(file)
        models = [value["value"] for value in data["environment"]["values"] if value["key"] == "model"]
    return models #[:1]

def set_custom_instruction_fragment(persona, prompt):
    '''
    Sets the custom instruction fragment for the Perplexity API. Persona and prompt are placeholders.
    '''
    custom_instruction = {
        "model": "MODEL",
        "messages": [
            {"role": "system", "content": persona},
            {"role": "user", "content": prompt}
        ]
    }
    return custom_instruction

def save_json_data(json_data, outfile):
    '''
    Writes the JSON data to a file.
    '''
    with open(outfile, 'w') as f:
        json.dump(json_data, f)

def reformat_txt_file(input_file, output_file, max_width=80):
    '''
    Reformat a text file to a maximum width
    '''
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            outfile.writelines(textwrap.fill(line, width=max_width) + '\n')

def reformat_with_hyperlink_protection(input_file, output_file, max_width=80):
    ''' 
    Reformat a text file to a maximum width, protecting hyperlinks and headlines
    '''
    hyperlink_pattern = r'https?://\S+'  # Simple URL pattern 
    headline_pattern = r'### .+$'  # 

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            wrapped_lines = textwrap.wrap(line, 
                               width=max_width, 
                               break_long_words=False,    # Protect long words in general                           
                               replace_whitespace=False,  # Important for URLs
                               break_on_hyphens=False)    # Prevent breaking at hyphens within URLs)                
                # outfile.write("\n\n" + match + '\n') 
            for wrapped_line in wrapped_lines:
                for match in re.findall(headline_pattern, wrapped_line):
                    outfile.write("\n\n")
                outfile.write(wrapped_line + '\n\n')
            # Re-insert original hyperlinks without breaks
            for match in re.findall(hyperlink_pattern, line):
                outfile.write(match + '\n') 

def save_txt_output(json_data, outfile_text, prompt):
    '''
    Extracts the message content from each JSON object and appends it to a text file.
    Returns the path to the output file.
    '''
    # Extract the message content from each JSON object
    extracted_data = [item for sublist in json_data for item in sublist]

    # Write the extracted data to the output file
    with open(outfile_text, 'w') as file:
        file.write(f"Prompt: {prompt}\n\n")
        for item in extracted_data:
            if not 'choices' in item:
                continue
            print(f"Extracted answer from model {item['model']} into '{outfile_text}'")
            file.write(f"\n\n### {item['model']}: \n")
            file.write(f"{item['choices'][0]['message']['content']}\n")
        file.write(f"\n\nPrompt: {prompt}\n")
    return outfile_text

def combine_json_files(subdir_in="json_extracted", subdir_out="final_output", prompt="", slug=""):
    '''
    Combines JSON files matching the slug pattern into a single JSON file.
    Returns the path to the output file.
    '''

    # Find JSON files matching the slug pattern
    json_files = glob.glob(os.path.join(subdir_in, f"*{slug}*.json"))

    json_data = []
    
    # Loop through each JSON file and load it .
    # Append all json files into one in-memory array.
    for json_file in json_files:
        with open(json_file) as f:
            data = json.load(f)
            json_data.append(data)

    outfile_temp = f"{slug}.tmp.txt"
    outfile_text = os.path.join(subdir_out, outfile_temp)
    
    # Write the combined JSON data to a new JSON file 
    #- for further processing at a much later time
    # optional:
    # outfile      = os.path.join(subdir_out, f"{slug}.json")
    # save_json_data(json_data, outfile)

    # Write the extracted data to a humanreadable text output file
    outfile_text = save_txt_output(json_data, outfile_text, prompt)
    return outfile_text


def parse_arguments():
    parser = argparse.ArgumentParser(description='Explore Perplexity API')
    parser.add_argument('--prompt', required=True, help='Your question or task')
    parser.add_argument('--slug', required=True, help='Prompt slug')
    parser.add_argument('--persona', default="Default Persona", help='Persona')
    parser.add_argument('--persona-slug', help='Persona slug')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    return parser.parse_args()


def check_prerequisites(api_key, tools, directories):
    check_perplexity_api_key(api_key)
    check_tools(tools)
    check_directories(directories)


def prepare_environment_files(environment_file, modif_environment_file, api_key):
    write_pm_env_file(environment_file, modif_environment_file, api_key)
    return extract_models(environment_file)


def process_models(models, args, collection_file, modif_environment_file, query_dir, html_outdir, json_outdir):
    for model in models:
        prompt_json = generate_prompt_json(args.persona, args.prompt, model)
        query_file, outfile_html = save_query_file(model, args.slug, prompt_json, collection_file, query_dir)
        execute_newman(query_file, modif_environment_file, outfile_html, html_outdir, args.prompt, model)
        process_report(outfile_html, html_outdir, json_outdir, args.slug, model, args.verbose)


def generate_prompt_json(persona, prompt, model):
    custom_instruction = set_custom_instruction_fragment(persona, prompt)
    prompt_json = custom_instruction.copy()
    prompt_json["model"] = model
    return prompt_json


def save_query_file(model, slug, prompt_json, collection_file, query_dir):
    outfile_json = f"{slug}--{model}.json"
    query_file = os.path.join(query_dir, outfile_json)
    with open(collection_file, 'r') as f:
        collection_data = json.load(f)
    collection_data['item'][0]['request']['body']['raw'] = json.dumps(prompt_json)
    collection_data['name'] = model
    with open(query_file, 'w') as f:
        json.dump(collection_data, f)
    print(f"{model}: Saving into {query_file}")
    return query_file, f"{slug}--{model}.html"


def execute_newman(query_file, modif_environment_file, outfile_html, html_outdir, prompt, model):
    report_file = os.path.join(html_outdir, outfile_html)
    command = [
        "newman",
        "run",
        query_file,
        "-e",
        modif_environment_file,
        "-r",
        "htmlextra",
        "--reporter-htmlextra-export",
        report_file,
        "--reporter-htmlextra-skipHeaders",
        "Authorization",
        "--reporter-htmlextra-browserTitle",
        f"{model}: {prompt}",
        "--reporter-htmlextra-title",
        f"{model}: {prompt}"
    ]
    subprocess.run(command)


def process_report(outfile_html, html_outdir, json_outdir, slug, model, verbose):
    report_file = os.path.join(html_outdir, outfile_html)
    if not os.path.exists(report_file):
        print(f"Skipping '{report_file}', file unavailable")
        return
    json_data = extract_json_from_html_report(report_file)
    json_outfile = os.path.join(json_outdir, f"{slug}--{model}.json")
    with open(json_outfile, 'w') as f:
        json.dump(json_data, f, indent=2)
    if verbose:
        write_json_output_to_stdout(json_outfile)


def main(api_key):
    args = parse_arguments()
    directories = ['queries', 'json_extracted', 'newman', 'final_output']
    tools = ['newman']
    check_prerequisites(api_key, tools, directories)
    models = prepare_environment_files("perplexity-API-export-environment.json",
                                       "perplexity-API-export-environment-with-cleartext-key.json",
                                       api_key)
    models = models[2:4]
    process_models(models, args, "Perplexity API export.postman_collection.json",
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
