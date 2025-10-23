from openai import OpenAI
from pydantic import BaseModel

from configurations.configs import get_chat_client_api_key, get_chat_base_url, get_chat_llm_model

client = OpenAI(
    api_key=get_chat_client_api_key(),
    base_url=get_chat_base_url()
)

current_chat = []
current_chat.append({"role": "user", "content": "hi"})

class ResponseSchema(BaseModel):
    response: str
    response_length: int
    further_question: str

result_response = client.responses.parse(
    model=get_chat_llm_model(),
    input=current_chat,
    text_format=ResponseSchema
)

print(result_response.choices[0].message.content)