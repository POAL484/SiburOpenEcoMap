import websockets as wbs
import asyncio
import json

#from bot import SiburOpenEcoMap

DEVELOPER_TELEGRAM_ID = "1130674897"

class WsClient:
    def __init__(self, bot: any, host="ws://localhost:3333"):
        self.auth_token = json.load(open("wbs_token.json"))["token"]
        self.host = host
        self.bot = bot

        self.to_recv = [False, lambda wsc: print(end="")]

    async def wbs_runner(self):
        print("oaoao")
        async for ws in wbs.connect(self.host):
            print("Websockets connected")
            await ws.send(self.auth_token)
            msg = json.loads(await ws.recv())
            if msg["code"] == "21":
                self.bot.loop.run_until_complete(
                    self.bot.send_message(DEVELOPER_TELEGRAM_ID, "Аутификаци не удалась(((")
                )
                print("123123\n\n\n123123")
                return
            for msg in ws:
                if self.to_recv[0]:
                    self.to_recv[1](self)
                    self.to_recv = [False, lambda wsc: print(end="")]
                else:
                    pass

    def run(self):
        while not self.bot.loop: pass
        asyncio.run(self.wbs_runner())