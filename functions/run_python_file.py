import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="List of arguments to pass to the Python file",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the Python file to execute, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        absolute_working_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_working_path, file_path))
        valid_target_path = os.path.commonpath([absolute_working_path, target_path]) == absolute_working_path

        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ['python', target_path]
        if args:
            command.extend(args)
        
        completed_process = subprocess.run(
            command,
            cwd=absolute_working_path,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if completed_process.returncode != 0:
            base =  f'Process exited with code {completed_process.returncode}'
        else:
            base = ""
        
        stdout = completed_process.stdout or ""
        stderr = completed_process.stderr or ""

        if not stdout.strip() and not stderr.strip():
            if base:
                return base
            return 'No output produced'
        
        parts = []
        if base:
            parts.append(base)
        if stdout:
            parts.append(f'STDOUT: {stdout}')
        if stderr:
            parts.append(f'STDERR: {stderr}')

        return '\n'.join(parts)

    except Exception as e:
        return f'Error: executing Python file: {e}'