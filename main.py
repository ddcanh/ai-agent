import os
from sqlite3 import paramstyle
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from config import MAX_MODEL_ITERATIONS
import sys


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    model_name = "gemini-2.0-flash-001"
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    client = genai.Client(api_key=api_key)

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )

    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )

    if len(sys.argv) < 2:
        print('Usage: uv run main.py "<prompt>"')
        sys.exit(1)
    
    verbose = "--verbose" in sys.argv

    user_prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    found_answer = False
    try_count = 1
    
    while not found_answer and try_count <= MAX_MODEL_ITERATIONS:
        try:

            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=config,
            )

            if response.text:
                # found_answer = True
                print(f'{response.text}')
                # break

            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)

            if not response.function_calls:
                break

            function_call_result = call_function(response.function_calls[0])

            if not function_call_result.parts[0].function_response.response:
                raise Exception("No function response found in function call result")
            elif verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    
            messages.append(types.Content(role="user", parts=function_call_result.parts))

            if verbose:
                for function_call_part in response.function_calls:
                    print(f'Calling function: {function_call_part.name}({function_call_part.args})')

            try_count += 1
            
        except Exception as error:
            print(f'error: {error}')
            break

    # print(response.text)
    # print(response.function_calls)
    
    # if verbose:
    #     print("User prompt:", user_prompt)
    #     print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    #     print("Response tokens:", response.usage_metadata.candidates_token_count)


# Run the main function
if __name__ == "__main__":
    main()