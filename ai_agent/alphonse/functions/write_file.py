import os

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
