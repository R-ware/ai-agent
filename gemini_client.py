import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

class GeminiClient:
    def __init__(self, api_key: str, model: str = 'gemini-2.5-flash'):
        self._client = genai.Client(api_key=api_key)
        self._model = model

    def count_tokens(self, messages: list[types.Content]) -> dict:
        response = self._client.models.count_tokens(
            model=self._model,
            contents=messages
        )
        if not response.usage_metadata:
            raise RuntimeError("Gemini API response missing usage_metadata; request may have failed.")
        usage = response.usage_metadata

        return {
            "prompt_tokens": usage.prompt_token_count,
            "response_tokens": usage.candidates_token_count
        }

    def generate_text(self, user_messages: list[types.Content], verbose: bool) -> str:
        response = self._client.models.generate_content(
            model=self._model,
            contents=user_messages,
        )

        if not response.usage_metadata:
            raise RuntimeError("Gemini API response missing usage_metadata; request may have failed.")

        return response.text