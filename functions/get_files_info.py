import os
from google.genai import types


def get_files_info(working_directory, directory="."):
  full_path = os.path.join(working_directory, directory)
  abs_full_path = os.path.abspath(full_path)
  abs_working_directory= os.path.abspath(working_directory)

  if not abs_full_path.startswith(abs_working_directory):
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
  
  if not os.path.isdir(abs_full_path):
    return f'Error: "{directory}" is not a directory'
  
  try:
    files_info = []
    entries = os.listdir(full_path)
    for name in entries:
      file_path = os.path.join(abs_full_path, name)
      file_size = 0
      is_dir = os.path.isdir(file_path)
      file_size = os.path.getsize(file_path) 
      files_info.append(f"- {name}: file_size={file_size}, is_dir={is_dir}")
    
    return "\n".join(files_info)

  except OSError as e:
    print(f"Error: {e}")

  
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)