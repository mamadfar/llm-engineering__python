"""""
OpenAIInstance.py

This module initializes the OpenAI API client and provides methods for making responses and chat completions.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses import Response
from openai.types.chat import ChatCompletionMessageParam
from openai.types.responses import ResponseInputParam
from openai.types.shared_params import Reasoning


load_dotenv(override=True) #? override=True means that if the environment variable is already set, it will be overridden.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-6-luna"
REASONING: Reasoning = Reasoning(effort="none")

class OpenAI:
    def __init__(self):
        self.client = client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("OPENAI_API_KEY is not set")
            raise ValueError("OPENAI_API_KEY is not set")
        elif not api_key.startswith("sk-proj-"):
            print("OPENAI_API_KEY is not a valid API key")
            raise ValueError("OPENAI_API_KEY is not a valid API key")
        elif api_key.strip() != api_key:
            print("OPENAI_API_KEY contains whitespace")
            raise ValueError("OPENAI_API_KEY contains whitespace")
        else:
            print("OPENAI_API_KEY is set and valid")

    def responses(self, input: ResponseInputParam, model: str = MODEL, reasoning: Reasoning = REASONING) -> Response:
        return self.client.responses.create(model=model, reasoning=reasoning, input=input)

    def chat_completions(self, messages: list[ChatCompletionMessageParam], model: str = MODEL, **args):
        return self.client.chat.completions.create(model=model, messages=messages, **args)