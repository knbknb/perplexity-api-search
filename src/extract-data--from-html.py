# Dependencies installation (if not installed already)
# pip3 install beautifulsoup4

import os
import socket
import sys
import glob
from bs4 import BeautifulSoup
import json
from pprint import pprint

def extract_values_from_html(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract total run duration, total data received, and average response time
    timings_data_section = soup.find('h5', string="Timings and Data")
    if timings_data_section:
        timings_text = timings_data_section.find_parent('div').getText(",")
        timings_values = [item.strip() for item in timings_text.split(',') if item.strip()]
        # Assign values based on expected positions in the list
        total_run_duration = timings_values[timings_values.index('Total run duration:') + 1]
        total_data_received = timings_values[timings_values.index('Total data received:') + 1]
        average_response_time = timings_values[timings_values.index('Average response time:') + 1]

    else:
        total_run_duration = total_data_received = average_response_time = None
    
    # Extract date value from the <h5> tag
    date_section = soup.find('h5', class_="text-center")
    date_value = date_section.get_text(strip=True) if date_section else None
    
    # Extract the 'model' value from the <pre><code> section
    code_section = soup.find('code', class_='prettyPrint')
    if code_section:
        code_text = code_section.get_text()
        # Find the model value in the JSON-like string
        json_encoded = code_text.split('&quot;model&quot;: &quot;')[0].split('&quot;')[0]
        model_json = json.loads(json_encoded) if json_encoded else None
        model_value = model_json.get('model') if model_json else None
    else:
        model_value = None

    return {
        'Total Run Duration': total_run_duration,
        'Total Data Received': total_data_received,
        'Average Response Time': average_response_time,
        'Date': date_value,
        'Model': model_value
    }

def parse_html_files(directory, pattern):
    # Initialize a data table (list of dictionaries)
    data_table = []

    # Use glob to find files matching the pattern
    search_path = os.path.join(directory, pattern)
    matching_files = glob.glob(search_path)

    # Process each matching file
    for file_path in matching_files:
        with open(file_path, 'r') as html_file:
            html_content = html_file.read()
            extracted_data = extract_values_from_html(html_content)
            extracted_data['File Name'] = os.path.basename(file_path)  # Include file name for reference
            data_table.append(extracted_data)

    return data_table

def save_to_json(data, directory, filter_string):
    # Get hostname
    hostname = socket.gethostname()
    
    # Get directory name (basename)
    dirname = os.path.basename(directory)
    
    # Remove wildcard characters from filter_string
    filter_string_clean = filter_string.replace('*', '').replace('?', '')
    
    # Create the filename
    filename = f"{hostname}-{dirname}-{filter_string_clean}.json"
    
    # Save data to a JSON file
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    print(f"Data saved to {filename}")

def main():
    # Check if sufficient command-line arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python3 script_name.py <directory> <glob_pattern>")
        sys.exit(1)

    # Get the directory and glob pattern from command-line arguments
    directory = sys.argv[1]
    pattern = sys.argv[2]

    # Check if the directory exists
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        sys.exit(1)

    # Parse the HTML files and collect data
    data_table = parse_html_files(directory, pattern)

    # Check if any files were found with the glob pattern
    if not data_table:
        print(f"Error: No files found in directory '{directory}' matching pattern '{pattern}'.")
        sys.exit(1)

    # Output the data table (or further process it)
    for entry in data_table:
        print(entry)
    
    save_to_json(data_table, directory, pattern)

if __name__ == "__main__":
    main()
