from dotenv import load_dotenv
from os import getenv
from gigachat import get_access_token


class BotSettings:
    bot_token: str
    gigachat_token: str
    model: str
    message_history: dict
    users: dict

    def __init__(self, model: str="GigaChat") -> None:
        load_dotenv()
        bt = getenv("BOT_TOKEN")
        if not bt:
            raise Exception("Failed to get bot token from env")
        self.bot_token = bt
        self.gigachat_token = get_access_token()
        self.model = model
        self.message_history = {}
        self.users = {}
    
