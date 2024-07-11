import websockets as wbs
import asyncio
import json

from bot import SiburOpenEcoMap

DEVELOPER_TELEGRAM_ID = "1130674897"

class WsClient:
    def __init__(self, bot: SiburOpenEcoMap, host="ws://localhost:3333"):
        self.auth_token = json.load(open("wbs_token.json"))["token"]
        self.host = host
        self.bot = bot

    async def wbs_runner(self):
        async for ws in wbs.connect(self.host):
            await ws.send(self.auth_token)
            msg = json.loads(await ws.recv())
            if msg["code"] == "21":
                pass

    def run(self):
        asyncio.run(self.wbs_runner())