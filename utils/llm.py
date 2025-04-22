from openai import OpenAI
from utils.settings import OPENAI_API_KEY


def ask_llm(llm_type: str, model: str, system_prompt: str, user_prompt: str) -> str:
    if llm_type == "openai":
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.responses.create(
            model=model,
            input=user_prompt
        )
        return response.output_text
    else:
        raise ValueError("Unsupported LLM type. Please use 'openai'.")

