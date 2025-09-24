from google.genai import types
from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .write_file import write_file
from .run_python_file import run_python_file
from config import WORKING_DIRECTORY

def call_function(function_call_part: types.FunctionCall, verbose=False):
  if verbose:
    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
  else:
    print(f" - Calling function: {function_call_part.name}")

  functions_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
  }

  function_name = function_call_part.name
  
  if function_name not in functions_map:
    return types.Content(
      role="tool",
      parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
        )
      ],
    )
    
  function_impl = functions_map[function_name]
  function_result = function_impl(working_directory=WORKING_DIRECTORY, **function_call_part.args)
  
  return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
  )
  
