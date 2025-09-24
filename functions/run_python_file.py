import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
  full_path = os.path.join(working_directory, file_path)
  abs_full_path = os.path.abspath(full_path)
  abs_working_directory= os.path.abspath(working_directory)
  if not abs_full_path.startswith(abs_working_directory):
    return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

  if not os.path.exists(abs_full_path):
    return f'Error: File "{file_path}" not found.'

  if not file_path.endswith(".py"):
    return f'Error: "{file_path}" is not a Python file.'

  try:
    completed_process = subprocess.run(
      ["python", abs_full_path] + args,
      check=True,
      text=True,
      capture_output=True,
      timeout=30
    )

    result = f'STDOUT: {completed_process.stdout} STDERR: {completed_process.stderr}' 
    if completed_process.returncode != 0:
      result += f'Process exited with code {completed_process.returncode}'
    return result
  except subprocess.CalledProcessError as error:
    return f"Error: executing Python file: {error}"

schema_run_python_file= types.FunctionDeclaration(
    name="run_python_file",
    description="execute python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The arguments when executing the file.",
                items=types.Schema(
                  type=types.Type.STRING
                )
            ),
        },
    ),
)