import shutil # For shutil.which() / check_tools()
import sys    # For sys.exit(
import os     

class Validator:
    def __init__(self):
        pass

    def check_tools(self, tools):
        '''
        Checks if the required cli tools are available in the operating system.
        '''
        for tool in tools:
            if shutil.which(tool) is None:
                raise SystemExit(f"Tool {tool} could not be found. Needed for selecting and changing custom instructions.")

    def check_arguments(self, prompt, slug):
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

    def check_directories(self, directories):
        '''
        Checks if the required directories are present. Creates them if not.
        '''
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def check_perplexity_api_key(self, perplexity_api_key):
        '''
        Checks if the PERPLEXITY_API_KEY environment variable is set. Exits the program if not.
        '''
        if not perplexity_api_key:
            raise ValueError('Please set the environment variable PERPLEXITY_API_KEY')
        
    