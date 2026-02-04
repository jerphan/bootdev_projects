import os

MAX_CHAR_TO_READ = 10000

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads the content in the file, up to a maximum of {MAX_CHAR_TO_READ} characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "content": types.Schema(
                type=types.Type.STRING,
                description="Returns the content in string form, found in the file path relative to the working directory, if the file at the path is a regular file",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    abs_path = os.path.abspath(working_directory)
    full_path = os.path.normpath(os.path.join(abs_path, file_path))
    #If the path is not a regular file, or cannot be found, we return an appropiate error message
    if not os.path.isfile(full_path):
        return f"Error: File not found or is not a regular file: \"{file_path}\""
    #If the path is outside of the working directory, we return and appropiate error message
    if os.path.commonpath([abs_path, full_path]) != abs_path:
        return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
    #Opening file to read
    with open(full_path, "r") as f:
        file_content = f.read(MAX_CHAR_TO_READ)
    #If file is larger than max chars, we make a note that it was truncated
        if f.read(1):
            file_content += f"[...File \"{file_path}\" truncated at {MAX_CHAR_TO_READ} characters]"
    return file_content
    
