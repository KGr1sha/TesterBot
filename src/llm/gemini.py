import asyncio
import os
from dotenv import load_dotenv

import google.generativeai as genai

from llm import LLM

class Gemini(LLM):
    async def init_token(self) -> None:
        load_dotenv()
        self.token = os.getenv("GEMINI_KEY")
        genai.configure(api_key=self.token)


    async def use(self, proompt: str, history: list = [], model="gemini-1.5-flash") -> str:
        model = genai.GenerativeModel(model)
        history.append({
            "role": "user",
            "parts": proompt 
        })
        chat = model.start_chat(history=history)
        response = await chat.send_message_async(proompt)
        history.append({
            "role": "model",
            "parts": response.text 
        })

        return response.text
        

async def main() -> None:
    chat = Gemini()
    await chat.init_token()
    response = await chat.use(
        proompt="Привет, расскажи, что ты можешь.",
    )
    print(response)


if __name__ == '__main__':
    asyncio.run(main())
