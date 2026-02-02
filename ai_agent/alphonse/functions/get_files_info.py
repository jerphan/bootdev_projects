def get_files_info(working_directory, directory="."):
    if(not(os.path.isdir(directory))):
        raise RuntimeError(f"{directory} is not a directory")
    abs_path = working_directory.os.path.abs_path()
    full_path = os.path.normpath(os.path.join(abs_path, directory))
    valid_check = os.path.commonpath([abs_path, full_path]) == abs_path
    if(not(valid_check)):
        raise RuntimeError(f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory")
    table = ""
    for items in full_path.os.list:
        