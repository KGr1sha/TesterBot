import requests
from dotenv import load_dotenv
from os import getenv
import uuid
import json


def get_access_token() -> str:
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
    response = requests.request("POST", auth_url, headers=headers, data=payload, verify=False)
    if response.status_code != 200:
        raise Exception(f"Bad response status code: {response.status_code}\n{response.text}")
    return response.json()['access_token']


def get_available_models(access_key: str) -> list:
    url = "https://gigachat.devices.sberbank.ru/api/v1/models"
    payload={}
    headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {access_key}'
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    if response.status_code != 200:
        raise Exception(f"Bad response status code: {response.status_code}\n{response.text}")
    return [model['id'] for model in response.json()['data']]


def use(access_token: str, model: str, message_history: list, proompt: str) -> str:
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

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    if response.status_code != 200:
        raise Exception(f"Bad response status code: {response.status_code}\n{response.text}")

    response_txt = response.json()["choices"][0]["message"]
    message_history.append(response_txt)
    return response_txt["content"]



if __name__ == '__main__':
    token = get_access_token()
    models = get_available_models(token)
    message_history = []
    response = use(
        token,
        models[0],
        message_history,
        "Привет, расскажи, что ты можешь."
    )
    print(response)


