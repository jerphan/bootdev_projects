#List of functions available to the AI model
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.config import working_directory

available_functions = types.Tool(function_declarations = [schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file],)

#Mapping the functions in a dictionary so that the model may call upon the following functions
function_map = {
    "get_file_content" : get_file_content,
    "get_files_info" : get_files_info,
    "write_file" : write_file,
    "run_python_file" : run_python_file,
}

def call_function(function_call, verbose=False):
    if(verbose):
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_name = function_call.name or ""
    #Compares to see if the function that is being attempted to be used is in the previously defined map, if not then we return an error message
    if(function_name not in function_map):
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    #We then define the arguments for the function call, if any
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = working_directory
    result = function_map[function_name](**args)
    #We can then return the result of the function call
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )