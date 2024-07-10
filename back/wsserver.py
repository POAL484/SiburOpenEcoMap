import websockets as wbs
from websockets.server import serve
import asyncio
import json

# 20 - timeout
# 21 - auth failed
# 22 - invalid format
# 23 - op not found
# 24 - Not enough fields
# 25 - drone not found
# 26 - probe taken

TOKEN = json.load(open("wbs_token.json"))["token"]

async def resp(ws: wbs.client.WebSocketClientProtocol, status: bool, info: any, code: int):
    await ws.send(json.dump({
        "status": "ok" if status else "err",
        "info": info,
        "code": str(code)
    }))

async def empty(ws: wbs.client.WebSocketClientProtocol, data: dict): pass

class Server:
    def __init__(self, db, port=3333):
        self.port = port
        self.db = db

        self.end_points = {
            "drone": empty,
            "set_probe": empty,
            "super_data": empty,
        }

    async def new_connection(self, ws: wbs.client.WebSocketClientProtocol):
        try:
            async with asyncio.timeout(30):
                msg = await ws.recv()
        except TimeoutError:
            await resp(ws, False, "Timeout", 20)
            return
        if not msg == TOKEN:
            await resp(ws, False, "Auth Failed", 21)
        await resp(ws, True, "Auth success", 10)
        async for msg in ws:
            try: json.loads(msg)
            except Exception:
                await resp(ws, False, "Is not json format", 22)
                continue
            req = json.loads(msg)
            if ( not "op" in req.keys() ) or ( not "data" in req.keys() ):
                await resp(ws, False, "Not op or not data in req", 22)
                continue
            if not req["op"] in self.end_points.keys():
                await resp(ws, False, "This end point not found", 23)
                continue
            await self.end_points[req["op"]](ws, req["data"])

    async def _start_server(self):
        async with serve(self.new_connection, "0.0.0.0", self.port) as self.ws_server:
            await asyncio.Future()

    def run_server(self):
        asyncio.run(self._start_server())