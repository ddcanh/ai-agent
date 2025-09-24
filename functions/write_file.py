import os 
from google.genai import types

def write_file(working_directory, file_path, content):
  full_path = os.path.join(working_directory, file_path)
  abs_full_path = os.path.abspath(full_path)
  abs_working_directory= os.path.abspath(working_directory)
  if not abs_full_path.startswith(abs_working_directory):
    return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
  
  if not os.path.exists(abs_full_path):
    os.makedirs(os.path.dirname(abs_full_path), exist_ok=True)

  try:
    with open(abs_full_path, 'w') as file:
      file.write(content)
      return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
  except Exception as e:
    return f'Error: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write content to the file, create file if not exist, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)