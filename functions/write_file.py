import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write into the file",
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    try:
        absolute_working_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_working_path, file_path))
        valid_target_path = os.path.commonpath([absolute_working_path, target_path]) == absolute_working_path

        if not valid_target_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, 'w') as file:
            file.write(content)

    except Exception as e:
        return f'Error: {str(e)}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'