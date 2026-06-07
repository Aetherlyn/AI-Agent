import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:       
        absolute_working_directory = os.path.abspath(working_directory)

        target_directory = os.path.normpath(os.path.join(absolute_working_directory, file_path))
        
        # Will be True or False
        valid_target_directory = os.path.commonpath([absolute_working_directory, target_directory]) == absolute_working_directory

        if not valid_target_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_directory):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_directory), exist_ok=True)

        with open(target_directory, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        


    except Exception as e:
        return f"Error: {e}"