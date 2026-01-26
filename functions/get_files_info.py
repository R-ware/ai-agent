import os

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        absolute_working_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_working_path, directory))
        valid_target_path = os.path.commonpath([absolute_working_path, target_path]) == absolute_working_path

        if not valid_target_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'
        
        items = os.listdir(target_path)
        files_info = []
        for item in items:
            item_size = os.path.getsize(os.path.join(target_path, item))
            is_dir = os.path.isdir(os.path.join(target_path, item))
            data = f"- {item}: file_size={item_size} bytes, is_dir={is_dir}"
            files_info.append(data)
            
    except Exception as e:
        return f"Error: {str(e)}"

    return "\n".join(files_info)