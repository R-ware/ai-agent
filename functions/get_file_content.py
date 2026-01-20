import os
from config import *

def get_file_content(working_directory, file_path):
    try:
        absolute_working_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_working_path, file_path))
        valid_target_path = os.path.commonpath([absolute_working_path, target_path]) == absolute_working_path

        if not valid_target_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
                
        with open(target_path, 'r') as file:
            content = file.read(MAX_CHARS)
            if file.read(1):
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            
    except Exception as e:
        return f"Error: {str(e)}"

    return content
