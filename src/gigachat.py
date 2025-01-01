import asyncio
from dotenv import load_dotenv
from os import getenv
import uuid
import json
from aiohttp import ClientSession


async def get_access_token() -> str:
    rq_uid = str(uuid.uuid4())
    load_dotenv()
    AUTH_KEY = getenv("GIGACHAT_AUTH_KEY")
    auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload={
      'scope': 'GIGACHAT_API_PERS'
    }

    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json',
      'RqUID': rq_uid,
      'Authorization': f'Basic {AUTH_KEY}'
    }
    async with ClientSession() as session:
        async with session.post(auth_url, headers=headers, data=payload, ssl=False) as resp:
            if resp.status != 200:
                raise Exception(f"Bad response status code: {resp.status}\n{resp.text}")
            json = await resp.json()
            return json["access_token"]


async def get_available_models(access_key: str) -> list:
    url = "https://gigachat.devices.sberbank.ru/api/v1/models"
    payload={}
    headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {access_key}'
    }

    async with ClientSession() as session:
        async with session.get(url, headers=headers, data=payload, ssl=False) as response:
            if response.status != 200:
                raise Exception(f"Bad response status code: {response.status}\n{response.text}")
            json = await response.json()
            return [model['id'] for model in json['data']]


async def use(access_token: str, model: str, message_history: list, proompt: str) -> str:
    message_history.append({
        "role": "user",
        "content": proompt,
    })
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    payload = json.dumps({
        "model": model,
        "messages": message_history,
        "temperature": 0.5,
        "top_p": 0.1, #Контроль разнообразия ответов
        "n": 1, #Кол-во возвращаемых ответов
        "stream": False, #Потоковая передача ответа
        "max_tokens": 512, #Максимальное количество токенов в ответе
        "repetition_penalty": 1, #Штраф за повторения
        "update_interval": 0 #Интервал обновления (для потоковой передачи)
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    async with ClientSession() as session:
        async with session.post(url, headers=headers, data=payload, ssl=False) as response:
            if response.status != 200:
                raise Exception(f"Bad response status code: {response.status}\n{response.text}")

            response_txt = (await response.json())["choices"][0]["message"]
            message_history.append(response_txt)
            return response_txt["content"]



async def main() -> None:
    token = await get_access_token()
    models = await get_available_models(token)
    print(models)

    message_history = []
    response = await use(
        token,
        models[0],
        message_history,
        "Привет, расскажи, что ты можешь."
    )
    print(response)


if __name__ == '__main__':
    asyncio.run(main())

