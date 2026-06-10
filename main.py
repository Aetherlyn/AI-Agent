import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")

def main():
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages: list[types.Content] = [ types.Content(role="user", parts=[types.Part(text=args.user_prompt)]) ]

    response = client.models.generate_content(
        model = 'gemini-2.5-flash', 
        contents = messages,
        config = types.GenerateContentConfig(tools=[available_functions], 
                                             system_instruction=system_prompt
                                             ),
    )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    
    if response.function_calls:
        for function in response.function_calls:
            print(f"Calling function: {function.name}({function.args})")
    else:
        if args.verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
       
        print(f"Response:\n{response.text}")

if __name__ == "__main__":
    main()
