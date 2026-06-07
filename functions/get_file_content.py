import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:   
        
        absolute_working_directory = os.path.abspath(working_directory)

        target_directory = os.path.normpath(os.path.join(absolute_working_directory, file_path))
        
        # Will be True or False
        valid_target_directory = os.path.commonpath([absolute_working_directory, target_directory]) == absolute_working_directory

        if not valid_target_directory:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_directory):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_directory, "r") as file:
            file_contents = file.read(MAX_CHARS)
            if file.read(1):
                file_contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return file_contents

    except Exception as e:
        return f"Error: {e}"