import os

from google import genai
from google.genai import types

class GeminiClient:
    def __init__(self, api_key: str, model: str = 'gemini-2.5-flash'):
        self._client = genai.Client(api_key=api_key)
        self._model = model