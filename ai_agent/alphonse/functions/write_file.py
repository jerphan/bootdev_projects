import os
from google import genai
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the user specified content a file in the specified path from the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to write into, is relative to the working directory",
            ),
            "content" : types.Schema(
                type=types.Type.STRING,
                description="Content that should be written in the file specified by the file path relative to the working directory"
            ),
        },
        required = ["file_path"],
    ),
)

def write_file(working_directory, file_path, content):
    abs_path = os.path.abspath(working_directory)
    full_path = os.path.normpath(os.path.join(abs_path, file_path))
    #If the path is not a regular file, or cannot be found, we return an appropiate error message
    if os.path.isdir(full_path):
        return f"Error: Cannot write to \"{file_path}\" as it is a directory"
    #If the path is outside of the working directory, we return and appropiate error message
    if os.path.commonpath([abs_path, full_path]) != abs_path:
        return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
    os.makedirs(file_path, exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)
    return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
