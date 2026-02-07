import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions.call_function import available_functions, call_function

#Loading in the API key
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
#If no key is found, then we raise a runtime error
if(api_key == None):
    raise RuntimeError("API key not found")
#Defining the gemini client we will use with our API key
client = genai.Client(api_key=api_key)

#Creating function to generate content from Gemini
def generate_content(client, requests, verbose):
    response = client.models.generate_content(
        model = "gemini-2.5-flash", 
        contents = requests,
        config = types.GenerateContentConfig(system_instruction = system_prompt, tools = [available_functions]))
    #If there are previous responses, we add them to the requests list so that the model can keep track of what it has previously done
    if (response.candidates):
        for candidate in response.candidates:
            requests.append(candidate)
    #If there is no response metadata, then it is likely that our API request failed
    if(response.usage_metadata == None):
        raise RuntimeError("Possible failed API request")
    #We then print the meta data to keep track of how many tokens we have used, as well as the response, if the verbose flag is enabled
    if(verbose):
        prompt_token = response.usage_metadata.prompt_token_count
        candidate_token = response.usage_metadata.candidates_token_count
        print(f"User prompt: {args.user_prompt}\nPrompt tokens: {prompt_token}\nResponse tokens: {candidate_token}\nResponse:\n{response.text}")
    else:
        print(f"{response.text}")
    function_results = []
    function_call_list = response.function_calls
    if(function_call_list == None):
        print(response.text)
        return
    for function_call in function_call_list:
        result = call_function(function_call, verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_results.append(result.parts[0])
    #We want the model to keep track of the function calls it has made, so we will also append those to the requests list
    requests.append(types.Content(role="user", parts=function_results))

def main():
    #This is to handle command line arguments
    parser = argparse.ArgumentParser(description="Chat_request")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    conversation_history = []
    #We then generate content through API calls to Gemini until it is able to complete the user given tasks, or if 20 requests have been made
    requests = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(5):
        generate_content(client, requests, args.verbose)
        
    
#We then call the main function to run
if __name__ == "__main__":
    main()
