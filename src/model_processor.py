import json
import os
import subprocess # for newman
from utils import extract_json_from_html_report, write_json_output_to_stdout

class ModelProcessor:
    def __init__(self):
        pass

    def set_custom_instruction_fragment(self, persona, prompt):
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

    def save_json_data(self, json_data, outfile):
        '''
        Writes the JSON data to a file.
        '''
        with open(outfile, 'w') as f:
            json.dump(json_data, f)


    
    def process_models(self, models, args, collection_file, modif_environment_file, query_dir, html_outdir, json_outdir):
        for model in models:
            prompt_json = self.generate_prompt_json(args.persona, args.prompt, model) # Call the generate_prompt_json method using the modelprocessor instance
            query_file, outfile_html = self.save_query_file(model, args.slug, prompt_json, collection_file, query_dir)
            self.execute_newman(query_file, modif_environment_file, outfile_html, html_outdir, args.prompt, model)
            self.process_report(outfile_html, html_outdir, json_outdir, args.slug, model, args.verbose)


    def generate_prompt_json(self, persona, prompt, model):
        custom_instruction = self.set_custom_instruction_fragment(persona, prompt)
        prompt_json = custom_instruction.copy()
        prompt_json["model"] = model
        return prompt_json


    def save_query_file(self, model, slug, prompt_json, collection_file, query_dir):
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


    def execute_newman(self, query_file, modif_environment_file, outfile_html, html_outdir, prompt, model):
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


    def process_report(self, outfile_html, html_outdir, json_outdir, slug, model, verbose):
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


