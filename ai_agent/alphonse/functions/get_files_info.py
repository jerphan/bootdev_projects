import os

def get_size_path(path_to_check):
    if os.path.isfile(path_to_check):
        return os.path.getsize(path_to_check)
    size = 0
    for entry in os.listdir(path_to_check):
        full_entry = os.path.join(path_to_check, entry)
        size += get_size_path(full_entry)
    return size

def get_files_info(working_directory, directory="."):
    abs_path = os.path.abspath(working_directory)
    full_path = os.path.normpath(os.path.join(abs_path, directory))
    valid_check = os.path.commonpath([abs_path, full_path]) == abs_path
    if not os.path.isdir(full_path):
        return f"{directory} is not a directory"
    if os.path.commonpath([abs_path, full_path]) != abs_path:
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
    list_of_content = os.listdir(full_path)
    if not list_of_content:
        return "No contents in directory"
    table = f"Result for \'{directory}\' directory:"
    try:
        for paths in list_of_content:
            item_path = os.path.join(full_path, paths)
            if(os.path.isfile(item_path)):
                table+= f"\n- {paths}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
            if(os.path.isdir(item_path)):
                table+= f"\n- {paths}: file_size={get_size_path(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
        return table
    except Exception as e:
        return f"Error: {e}"