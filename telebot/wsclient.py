import websockets as wbs
import asyncio
import json
import threading as thrd

class SiburOpenEcoMap: pass

#from bot import SiburOpenEcoMap

DEVELOPER_TELEGRAM_ID = "1130674897"

class WsClient:
    def __init__(self, bot: SiburOpenEcoMap, host="ws://localhost:3333"):
        self.auth_token = json.load(open("wbs_token.json"))["token"]
        self.host = host
        self.bot = bot

        self.loop = None
        self.ws = None

        self.end_points = {
            "drone": ""
        }
        self.to_recv = False

    async def wbs_runner(self):
        self.loop = asyncio.get_running_loop()
        print("Trying to connect to websockets... ", end='')
        async for ws in wbs.connect(self.host):
            print("Websockets connected")
            await ws.send(self.auth_token)
            msg = json.loads(await ws.recv())
            if msg["code"] == "21":
                asyncio.ensure_future(
                    self.bot.send_message(DEVELOPER_TELEGRAM_ID, "Аутификация не удалась((("), loop=self.bot.loop
                )
                print("Authication failed")
                return
            print("Autification success")
            self.ws = ws
            async for msg in ws:
                if self.to_recv:
                    data = json.loads(msg)
                    if not data["op"] in self.end_points.keys(): continue
                    asyncio.ensure_future(self.end_points[data["op"]](data), loop=self.bot.loop)
                    self.to_recv = False
                else:
                    pass

    def send_with_order(self, data):
        thrd.Thread(target=self.send_ordered, args=(data,)).start()

    def send_ordered(self, data):
        if isinstance(data, dict):
            try: data = json.dumps(data)
            except Exception: return
        while self.to_recv: pass
        self.to_recv = True
        asyncio.ensure_future(self.ws.send(data), loop=self.loop)


    def run(self):
        while not self.bot.loop: pass
        asyncio.run(self.wbs_runner())