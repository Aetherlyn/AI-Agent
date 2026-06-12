import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments to pass to the Python file",
                items=types.Schema(type=types.Type.STRING)
            ),
        },
        required=["file_path"]
    ),
)

def run_python_file( working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:   
        
        absolute_working_directory = os.path.abspath(working_directory)

        target_directory = os.path.normpath(os.path.join(absolute_working_directory, file_path))
        
        # Will be True or False
        valid_target_directory = os.path.commonpath([absolute_working_directory, target_directory]) == absolute_working_directory

        if not valid_target_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_directory):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_directory]

        if args:
            command.extend(args)
        
        process = subprocess.run(command,
                                        cwd=absolute_working_directory,
                                        capture_output=True,
                                        text=True,
                                        timeout=30)
        
        output = []

        if process.returncode != 0:
            output.append(f"Process exited with code {process.returncode}")
        
        if not process.stdout and not process.stderr:
            output.append(f"No output produced")

        if process.stdout:
            output.append(f"STDOUT:{process.stdout}")

        if process.stderr:
            output.append(f"STDERR:{process.stderr}")

        return "\n".join(output)

    except Exception as e:
        return f"Error: {e}"