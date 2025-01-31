from openai import OpenAI


class BaseAgent:
    def __init__(self, client, base_model: str="gpt-3.5-turbo"):
        self.chat_agent = client
        self.base_model = base_model

    def infer(self, messages: list[dict]):
        response = self.chat_agent.chat.completions.create(
            model=self.base_model,
            messages=messages,
            stream=False
        )
        
        resp = response.choices[0].message.content
        total_tokens = response.usage.total_tokens

        return resp, total_tokens



