import asyncio
import json
import websockets

import config


async def echo(websocket, _):
    async for message in websocket:
        print(message)
        if message == "get":
            await websocket.send(json.dumps(data, sort_keys=True))
        else:
            values = message.split(" ")
            data[values[0]] = values[1:]

data = {}

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, config.HOST, config.SEND_PORT))
asyncio.get_event_loop().run_forever()
