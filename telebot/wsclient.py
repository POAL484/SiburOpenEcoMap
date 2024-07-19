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
            #что-то
        }
        self.to_recv = False
        self.to_recv_user_id = "123321"

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
                print("Але тут")
                if self.to_recv and not json.loads(msg)["op"] == "alert":
                    try: data = json.loads(msg)
                    except Exception: continue
                    print(f"Але 1 {data}")
                    if not data["op"] in self.end_points.keys():
                        self.to_recv = False
                        continue
                    print(f"Але 2 {data}")
                    asyncio.ensure_future(self.end_points[data["op"]](data, self.to_recv_user_id), loop=self.bot.loop)
                    self.to_recv = False
                else:
                    try: data = json.loads(msg)
                    except Exception: continue
                    if data["op"] != "alert": continue
                    print(data)
                    print(data["data"])
                    asyncio.ensure_future(self.end_points[data["op"]](data["data"], "_"), loop=self.bot.loop)

    def send_with_order(self, data, user_id, responce=True):
        thrd.Thread(target=self.send_ordered, args=(data, user_id, responce)).start()

    def send_ordered(self, data, user_id, responce):
        if isinstance(data, dict):
            try: data = json.dumps(data)
            except Exception: return
        while self.to_recv: pass
        self.to_recv = True
        self.to_recv_user_id = str(user_id)
        asyncio.ensure_future(self.ws.send(data), loop=self.loop)


    def run(self):
        while not self.bot.loop: pass
        asyncio.run(self.wbs_runner())