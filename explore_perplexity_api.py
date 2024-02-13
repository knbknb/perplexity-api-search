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
import subprocess

from dotenv import load_dotenv

from bs4 import BeautifulSoup
import glob

def extract_json_from_html_report(report_file, json_outfile):
    with open(report_file, 'r') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    code_elements = soup.find_all('code')

    json_data = [code.get_text() for code in code_elements]  

    # Assuming JSON data is an array within the <code> elements
    with open(json_outfile, 'w') as f:
        json.dump(json_data, f)

# Example usage:
# extract_json_from_html_report("my_report.html", "extracted_data.json")

def enclose_filecontent_in_array(json_file):
    """
    Encloses a string containing JSON fragments (without commas) in an array,
    properly separated with commas.

    Args:
        json_file (str): The path to the file containing JSON fragments.
    """

    with open(json_file, 'r') as f:
        json_string = f.read()

    # Split the string into individual JSON fragments
    fragments = json_string.strip().split()

    # Wrap each fragment in quotes and add commas
    enclosed_fragments = [f'"{fragment}"' for fragment in fragments]

    # Join the fragments into an array string
    array_string = ", ".join(enclosed_fragments)

    # Add opening and closing brackets for the array
    valid_json = f"[ {array_string} ]"

    # Overwrite the file with the valid JSON
    with open(json_file, 'w') as f:
        f.write(valid_json)
    
    return json_file

# Example Usage
# enclose_filecontent_in_array("my_json_file.json")
        
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

# Example usage (assuming the JSON string is available)
#json_data = '{"data": [{"name": "Alice"}, {"model": "Example Model", "choices": [{"message": {"content": "This is a message"}}]}]}'
#write_json_output_to_stdout(json_data)


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

def finalize_json_files(slug):
    # ... (Steps 1-5 similar to your previous Python equivalents)
    # Remove existing files
    if os.path.exists(f"{slug}.json"):
        os.remove(f"{slug}.json")
    if os.path.exists("output.txt"):
        os.remove("output.txt")

    # Find JSON files matching the slug pattern
    json_files = glob.glob(f"json_extracted/*{slug}*.json")

    # Process each JSON file using jq command
    for json_file in json_files:
        subprocess.run(['jq', '-rs', '.', json_file], stdout=subprocess.PIPE, input=None)

    # Read the JSON file and extract the desired data
    with open(f"{slug}.json", 'r') as file:
        data = json.load(file)
        extracted_data = [item for sublist in data for item in sublist]

    # Write the extracted data to the output file
    with open(f"{slug}.txt", 'w') as file:
        for item in extracted_data:
            file.write(item)
            file.write('\n')

    #Flattens nested arrays in the JSON (jq '[.[].[]]' > "$outfile").
            
    # Question extraction
    #question = extract_question_from_json(slug)  # Assuming you add that part
    #write_question_to_file(slug, question)

    # Answer processing (using subprocess)
    with open("output.txt", 'w') as f:  # We'll temporarily store the text data
        subprocess.run(
            [
                'jq', '-r', 
                '.[]| ["<hr>## ", .[0].model, "<hr>\n\n", .[].choices[0].message.content, "\n\n"] | join(" ")',
                f'{slug}.json'
            ],
            stdout=subprocess.PIPE
        ) 
        subprocess.run(['pandoc', '-f', 'markdown', '-t', 'html'], input=f.read(), stdout=subprocess.PIPE)
        subprocess.run(['lynx', '-stdin', '-dump'], input="b", stdout=subprocess.PIPE)
        subprocess.run(['fmt'], input="b", stdout="f")

     # Append to final output file
    with open(f"final_output/{slug}.txt", 'a') as f:
        with open("output.txt", 'r') as tmp:
            f.write(tmp.read())

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
