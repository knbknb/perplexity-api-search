import json
import os
import subprocess # for newman
from utils import extract_json_from_html_report, write_json_output_to_stdout
import re

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

    # add a function filter_models to filter the models based on the model_list:
    # if argument "model-type" is not provided, return all models
    # if model type is "small" return only the small models
    def filter_models(self, models, args):
        model_type = args.model_type

        if not model_type:
            return models
        elif model_type == "small":
            return [model for model in models if "small" in model]
        elif model_type == "online":
            # It is recommended to use only single-turn conversations 
            # and avoid system prompts for the online LLMs (sonar-small-online and sonar-medium-online).
            if args.persona:
                print("Warning: Online models ignore the custom instruction and are not recommended for multi-turn conversations")
                args.persona = "ignored-for-online-models"
            return [model for model in models if "online" in model]
        elif model_type == "instruct":
            return [model for model in models if "instruct" in model]
        elif model_type == "chat":
            # filter for 8x7b, 34B, 70B by using a regex 
            return [model for model in models if re.search(r'(chat)', model)]
        else:
            return models

    def process_models(self, models, args, collection_file, modif_environment_file, query_dir, html_outdir, json_outdir):
        # Filter the models based on the model_type argument
        filtered_models = self.filter_models(models, args) 
        for model in filtered_models:
            # Call the generate_prompt_json method using the modelprocessor instance
            prompt_json = self.generate_prompt_json(args.persona, args.prompt, model) 
            query_file, outfile_html = self.save_query_file(model, args.slug, args.persona_slug, prompt_json, collection_file, query_dir)
            self.execute_newman(query_file, modif_environment_file, outfile_html, html_outdir, args.prompt, model)
            self.process_report(outfile_html, html_outdir, json_outdir, args.slug, args.persona_slug, model, args.verbose)


    def generate_prompt_json(self, persona, prompt, model):
        custom_instruction = self.set_custom_instruction_fragment(persona, prompt)
        prompt_json = custom_instruction.copy()
        prompt_json["model"] = model
        return prompt_json


    def save_query_file(self, model, slug, persona_slug, prompt_json, collection_file, query_dir):
        outfile_json = f"{slug}--{persona_slug}--{model}.json"
        query_file = os.path.join(query_dir, outfile_json)
        with open(collection_file, 'r') as f:
            collection_data = json.load(f)
        collection_data['item'][0]['request']['body']['raw'] = json.dumps(prompt_json)
        collection_data['name'] = model
        with open(query_file, 'w') as f:
            json.dump(collection_data, f)
        print(f"{model}: Saving into {query_file}")
        return query_file, f"{slug}--{persona_slug}--{model}.html"


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
        #print(f"Executing: {' '.join(command)}")
        subprocess.run(command)


    def process_report(self, outfile_html, html_outdir, json_outdir, slug, persona_slug, model, verbose):
        report_file = os.path.join(html_outdir, outfile_html)
        if not os.path.exists(report_file):
            print(f"Skipping '{report_file}', file unavailable")
            return
        json_data = extract_json_from_html_report(report_file)
        json_outfile = os.path.join(json_outdir, f"{slug}--{persona_slug}--{model}.json")
        with open(json_outfile, 'w') as f:
            json.dump(json_data, f, indent=2)
        if verbose:
            write_json_output_to_stdout(json_outfile)


