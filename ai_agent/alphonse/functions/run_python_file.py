import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(abs_path, file_path))
        #If the path is not a regular file, or cannot be found, we return an appropiate error message
        if not os.path.isfile(full_path):
            return f"Error: \"{file_path}\" does not exist"
        #If the path is outside of the working directory, we return and appropiate error message
        if os.path.commonpath([abs_path, full_path]) != abs_path:
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
        #If the file is not a python file, then we return an appropiate error message stating so
        if not full_path.endswith(".py"):
            return f"Error: \"{file_path}\" is not a Python file"
        #We then build the command lists to run, extending it if additional args were passed
        commands = ["python", full_path]
        if(args != None):
            commands.extend(args)
        completed_process = subprocess.run(commands, cwd = working_directory, capture_output = True, text = True, timeout = 30)
        #If the subprocess does not exit with a code of 0, then we print the exit code
        if(completed_process.returncode != 0):
            return f"Process exited with code {completed_process.returncode}"
        #If the subprocess does not have any output, then we return a string that reflects this
        if(completed_process.stdout == None or completed_process.stderr == None):
            return "No output was produced"
        #Otherwise we print the output of the subprocess
        return f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
