import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
  full_path = os.path.join(working_directory, file_path)
  abs_full_path = os.path.abspath(full_path)
  abs_working_directory= os.path.abspath(working_directory)
  if not abs_full_path.startswith(abs_working_directory):
    return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
  
  if not os.path.isfile(abs_full_path):
    return f'Error: File not found or is not a regular file: "{file_path}"'

  try:
    with open(abs_full_path, 'r') as file:
      file_content_string = file.read(MAX_CHARS + 1)
      if len(file_content_string) < MAX_CHARS + 1:
        return file_content_string
      else:
        return file_content_string[:MAX_CHARS] + f'...File "{file_path}" truncated at 10000 characters'
  except Exception as e:
    return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file, max characters from config: MAX_CHARS, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read content, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)