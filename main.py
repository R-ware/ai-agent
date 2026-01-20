import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response missing usage_metadata; request may have failed.")
    
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)



def main():
    parser = argparse.ArgumentParser(description="Gemini Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set.")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    verbose = args.verbose

    if verbose:
        print(f"User prompt: {args.user_prompt}")

    generate_content(client, messages, verbose)


if __name__ == "__main__":
    main()