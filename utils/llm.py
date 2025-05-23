import asyncio
from openai import OpenAI
from utils.settings import OPENAI_API_KEY


async def ask_llm(prompt: str, llm_type: str = "openai", model: str = "o4-mini") -> str:
    if llm_type == "openai":
        client = OpenAI(api_key=OPENAI_API_KEY)
        # Simulate asynchronous behavior for the API call
        response = await asyncio.to_thread(client.responses.create,
                                           model=model,
                                           input=prompt)
        return response.output_text
    else:
        raise ValueError("Unsupported LLM type. Please use 'openai'.")

