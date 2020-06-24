import asyncio
import config
import json
import struct
import websockets


async def send(websocket, path):
    async for _ in websocket:
        await websocket.send(json.dumps(data))


async def receive(websocket, path):
    ip = websocket.remote_address[0]
    async for message in websocket:
        data[ip] = struct.unpack("3f", message)


data = {}

asyncio.get_event_loop().run_until_complete(
    websockets.serve(receive, "0.0.0.0", config.RECEIVE_PORT))
asyncio.get_event_loop().run_until_complete(
    websockets.serve(send, "0.0.0.0", config.SEND_PORT))
asyncio.get_event_loop().run_forever()
