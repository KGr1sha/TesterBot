from dotenv import load_dotenv
import os
import asyncio

from openai import AsyncOpenAI

from llm import LLM

class ChatGPT(LLM):
    async def init_token(self) -> None:
        load_dotenv()
        self.token = os.getenv("OPENAI_KEY")

    async def use(self, model, history, proompt) -> str:
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
        return str(completion.choices[0].message)


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


if __name__ == '__main__':
    asyncio.run(main())
