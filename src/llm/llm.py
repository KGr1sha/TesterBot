class LLM:
    async def init_token(self) -> None:
        self.token = ""


    async def use(self, proompt: str, history: list = [], model: str = "") -> str:
        return "Not implemented."
