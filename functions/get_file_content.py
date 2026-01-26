import os
from config import *
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)

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
