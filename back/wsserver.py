import websockets as wbs
from websockets.server import serve
import asyncio

class Server:
    def __init__(self, db, port=3333):
        self.port = port
        self.db = db

    async def new_connection(self, ws: wbs.client.ClientConnection):
        return
    
    

    async def _start_server(self):
        async with serve(self.new_connection, "0.0.0.0", self.port) as self.ws_server:
            await asyncio.Future()

    def run_server(self):
        asyncio.run(self._start_server())