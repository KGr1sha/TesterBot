from dotenv import load_dotenv
from os import getenv

class BotSettings:
    bot_token: str
    gigachat_token: str
    model: str
    message_history: dict
    users: dict

    def __init__(self, gigatoken: str, model: str="GigaChat") -> None:
        load_dotenv()
        bt = getenv("BOT_TOKEN")
        if not bt:
            raise Exception("Failed to get bot token from env")
        self.bot_token = bt
        self.gigachat_token = gigatoken
        self.model = model
        self.message_history = {}
        self.users = {}
    
settings = None

def init_settings(gigatoken: str, gigamodel: str) -> None:
    global settings
    if settings is None:
        settings = BotSettings(gigatoken, gigamodel)
    else:
        raise Exception("Trying to create second bot settings instance")
