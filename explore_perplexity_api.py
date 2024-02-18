#!/usr/bin/env python
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
import sys    # For sys.exit()
import shutil # For shutil.which() / check_tools()
import subprocess # for newman
import textwrap
import re

from dotenv import load_dotenv

from bs4 import BeautifulSoup
import glob

def extract_json_from_html_report(report_file):
    with open(report_file, 'r') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    code_elements = soup.find_all('code')

    valid_json_data = []
    for code in code_elements:
        code_text = code.get_text()

        # Attempt to parse JSON
        try:
            json_data = json.loads(code_text)
            valid_json_data.append(json_data)
        except json.JSONDecodeError:
            # Handle cases where the code text is not valid JSON 
            pass 
    return valid_json_data
    #return [code.get_text() for code in code_elements]  

# Example usage:
# data = extract_json_from_html_report("my_report.html", "extracted_data.json")

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
    
#def write_json_output_to_stdout_gpt(json_outfile):
#    if not os.path.isfile(json_outfile) or os.path.getsize(json_outfile) == 0:
#        print("ERROR: {} is empty (?)".format(json_outfile))
#    else:
#        with open(json_outfile, 'r') as file:
#            data = json.load(file)
#            # Process and print data as needed
#            pretty_data = json.dumps(data, indent=4)
#            print(pretty_data)

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
    Modifies the environment file to include the API key.
    '''
    with open(json_infile, "r") as f:
        data = json.load(f)
        data["environment"]["values"][0]["value"] = PERPLEXITY_API_KEY
    with open(json_outfile, "w") as f:
        json.dump(data, f)


def extract_models(environment_file):
    '''
    Extracts the models from the environment file.
    '''
    with open(environment_file) as file:
        data = json.load(file)
        models = [value["value"] for value in data["environment"]["values"] if value["key"] == "model"]
    return models #[:1]

def set_custom_instruction_fragment(persona, prompt):
    custom_instruction = {
        "model": "MODEL",
        "messages": [
            {"role": "system", "content": persona},
            {"role": "user", "content": prompt}
        ]
    }
    return json.dumps(custom_instruction)

def save_json_data(json_data, outfile):
    with open(outfile, 'w') as f:
        json.dump(json_data, f)

def reformat_txt_file(input_file, output_file, max_width=80):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            outfile.writelines(textwrap.fill(line, width=max_width) + '\n')

def reformat_with_hyperlink_protection(input_file, output_file, max_width=80):
    hyperlink_pattern = r'https?://\S+'  # Simple URL pattern 
    headline_pattern = r'### '  # 

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            wrapped_lines = textwrap.wrap(line, 
                               width=max_width, 
                               break_long_words=False,    # Protect long words in general                           
                               replace_whitespace=False,  # Important for URLs
                               break_on_hyphens=False)    # Prevent breaking at hyphens within URLs)

            for wrapped_line in wrapped_lines:
                outfile.write(wrapped_line + '\n')
            # Re-insert original hyperlinks without breaks
            for match in re.findall(hyperlink_pattern, line):
                outfile.write(match + '\n') 
            for match in re.findall(headline_pattern, line):
                outfile.write("\n\n" + match + '\n') 

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
            print(f"Extracted answer from model {item['model']} into '{outfile_text}'")
            file.write(f"\n### {item['model']}: \n")
            file.write(f"{item['choices'][0]['message']['content']}\n")
        file.write(f"\nPrompt: {prompt}\n")
    return outfile_text

def combine_json_files(slug, subdir_in="json_extracted", subdir_out="final_output", prompt=""):
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
    #outfile      = os.path.join(subdir_out, f"{slug}.json")
    # optional:
    # save_json_data(json_data, outfile)

    # Write the extracted data to a humanreadable text output file
    outfile_text = save_txt_output(json_data, outfile_text, prompt)
    return outfile_text


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
    #PSLUG   = args.persona_slug
    VERBOSE = args.verbose

    directories = ['queries', 'json_extracted', 'newman', 'final_output']
    tools = ['newman']

    # Check for required tools
    check_perplexity_api_key(api_key)
    check_tools(tools)
    check_arguments(PROMPT, SLUG)
    check_directories(directories)
    
    write_pm_env_file(environment_file, modif_environment_file, os.getenv('PERPLEXITY_API_KEY'))
    models = extract_models(environment_file)
    print(f"Using models: {models}")
    # unserialize this JSON string into a Python object
    custom_instruction = json.loads(set_custom_instruction_fragment(PERSONA, PROMPT))
    
    for model in models:
        # Update template using the current model
        prompt_json = custom_instruction.copy()
        prompt_json["model"] = model
        # Construct file paths
        outfile_json = f"{SLUG}--{model}.json"
        outfile_html = f"{SLUG}--{model}.html"
        query_file = os.path.join(query_dir, outfile_json)
        # Process collection file: edit 1 nested item in-place
        with open(collection_file, 'r') as f:
            collection_data = json.load(f)
        collection_data['item'][0]['request']['body']['raw'] = prompt_json 
        collection_data['name'] = model
        # Save output into the query file
        with open(query_file, 'w') as f:
            json.dump(collection_data, f)
        print(f"{model}: Saving into {query_file}")
      
        report_file =  f"{html_outdir}/{outfile_html}"
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
            f"{model}: {PROMPT}",
            "--reporter-htmlextra-title",
            f"{model}: {PROMPT}" 
        ]
        subprocess.run(command)
        
        # Print or process the results as required
        file_name = os.path.basename(query_file)
        base_name = os.path.splitext(file_name)[0]
        json_outfile = os.path.join(json_outdir, f"{base_name}.json")
        # report_file is newman/SLUG--MODEL.html
        if not os.path.exists(report_file):
            print(f"Skipping '{report_file}', file unavailable")
            continue  # Assuming this code is within a loop
        # Extract JSON from HTML report
        # Assuming JSON data is an array within the <code> elements
        json_data = extract_json_from_html_report(report_file) 
        # json-outfile is json_extracted/SLUG--MODEL.json
        with open(json_outfile, 'w') as f:
            print(f"Saving extracted response JSON into '{json_outfile}'\n")
            json.dump(json_data, f, indent=2)

        
        # User feedback depending on verbosity 
        if VERBOSE:  
            write_json_output_to_stdout(json_outfile)
    
    tmp_txt_file = combine_json_files(SLUG, subdir_in="json_extracted", 
                        subdir_out="final_output", 
                        prompt=PROMPT)
    output_file = tmp_txt_file.replace(".tmp.txt", ".txt")
    reformat_with_hyperlink_protection(tmp_txt_file, output_file, max_width=80)
    
    try:
        os.remove(tmp_txt_file)
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    load_dotenv()
    api_key=os.getenv('PERPLEXITY_API_KEY')    
    main(api_key)
