import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
#Loading in the API key
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
#If no key is found, then we raise a runtime error
if(api_key == None):
    raise RuntimeError("API key not found")
#Defining the gemini client we will use with our API key
client = genai.Client(api_key=api_key)

def main():
    #This is to handle command line arguments
    parser = argparse.ArgumentParser(description="Chat_request")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    requests = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(model = "gemini-2.5-flash", contents = requests)
    #If there is no response metadata, then it is likely that our API request failed
    if(response.usage_metadata == None):
        raise RuntimeError("Possible failed API request")
    #We then print the meta data to keep track of how many tokens we have used, as well as the response, if the verbose flag is enabled
    if(args.verbose):
        prompt_token = response.usage_metadata.prompt_token_count
        candidate_token = response.usage_metadata.candidates_token_count
        print(f"User prompt: {args.user_prompt}\nPrompt tokens: {prompt_token}\nResponse tokens: {candidate_token}\nResponse:\n{response.text}")
    else:
        print(f"{response.text}")
#We then call the main function to run
if __name__ == "__main__":
    main()