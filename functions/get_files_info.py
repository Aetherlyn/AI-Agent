import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_working_directory = os.path.abspath(working_directory)

        target_directory = os.path.normpath(os.path.join(absolute_working_directory, directory))
        
        # Will be True or False
        valid_target_directory = os.path.commonpath([absolute_working_directory, target_directory]) == absolute_working_directory

        if not valid_target_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'

        directory_content_list = os.listdir(target_directory)

        result_list = []
        for file in directory_content_list:
            item_path = os.path.join(target_directory, file)
            if os.path.isdir(item_path):
                is_path = "is_dir=True"
            else:
                is_path = "is_dir=False"
            
            file_size = f"file_size={os.path.getsize(item_path)} bytes"

            result = f" - {file}: {file_size}, {is_path}"
            
            result_list.append(result)

        return '\n'.join(result_list)           


    except Exception as e:
        return f"Error: {e}"