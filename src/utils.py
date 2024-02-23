from bs4 import BeautifulSoup
import json
import sys
import textwrap
import re
import os
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

def prepare_environment_files(environment_file, modif_environment_file, api_key):
    write_pm_env_file(environment_file, modif_environment_file, api_key)
    return extract_models(environment_file)


def reformat_txt_file(input_file, output_file, max_width=80):
    '''
    Reformat a text file to a maximum width
    '''
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            outfile.writelines(textwrap.fill(line, width=max_width) + '\n')

def reformat_with_hyperlink_protection(input_file, output_file, max_width=80):
    ''' 
    Reformat a text file to a maximum width, protecting hyperlinks and giving headlines more room
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
            skip = False
            for wrapped_line in wrapped_lines:
                for match in re.findall(headline_pattern, wrapped_line):
                    match = match.replace('>', '')
                    outfile.write('\n\n' + match + "\n\n")
                    skip = True
                if not skip:
                    outfile.write(wrapped_line + '\n')
                else: skip = False
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
        file.write(f"> Prompt: {prompt}\n\n")
        for item in extracted_data:
            if not 'choices' in item:
                continue
            print(f"Extracted answer from model {item['model']} into '{outfile_text}'")
            file.write(f"\n\n### {item['model']}: \n")
            file.write(f"{item['choices'][0]['message']['content']}\n")
        file.write(f"\n\n\n> Prompt: {prompt}\n")
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
