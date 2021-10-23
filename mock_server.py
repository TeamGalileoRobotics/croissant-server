import asyncio
import json
import websockets
import time

import config


async def echo(websocket, _):
    async for message in websocket:
        now = time.time()
        print(message)
        if message == "get":
            global data
            data = {k: v for k, v in data.items()
                    if now - last_seen[k] < config.TIMEOUT}
            await websocket.send(json.dumps(data, sort_keys=True))
        else:
            values = message.split(" ")
            id = values[0]
            last_seen[id] = now
            data[id] = [float(v) for v in values[1:]]

data = {}
last_seen = {}

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, config.HOST, config.SEND_PORT))
asyncio.get_event_loop().run_forever()
