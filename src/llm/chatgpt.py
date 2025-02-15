from dotenv import load_dotenv
import os
import asyncio

from openai import AsyncOpenAI

from llm import LLM

class ChatGPT(LLM):
    async def init_token(self) -> None:
        load_dotenv()
        self.token = os.getenv("OPENAI_KEY")

    async def use(self, proompt: str, history: list = [], model: str = "") -> str:
        if not self.token:
            raise Exception("Need to init token first")

        client = AsyncOpenAI(api_key=self.token)
        history.append(
            {"role": "user", "content": proompt}
        )
        completion = await client.chat.completions.create(
            model=model,
            messages=history 
        )
        response_text = completion.choices[0].message
        history.append(
            {"role": "user", "content": response_text}
        )
        return str(response_text)


async def main() -> None:
    chat = ChatGPT()
    await chat.init_token()
    message_history = []
    response = await chat.use(
        "gpt-4o-mini",
        message_history,
        "Привет, расскажи, что ты можешь."
    )
    print(response)

from openai import OpenAI
if __name__ == '__main__':
    load_dotenv()
    client = OpenAI()
    completion = client.chat.completions.create(
        model="chatgpt-4o-latest",
        store=True,
        messages=[
            {"role": "user", "content": "write a haiku about ai"}
        ]
    )
    print(completion.choices[0].message)
