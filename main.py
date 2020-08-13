import asyncio
import config
import json
import struct
import websockets
import socket


async def send(websocket, path):
    async for _ in websocket:
        await websocket.send(json.dumps(data))

async def receive(reader, writer):
    message = await reader.read(1024)
    peer = writer.get_extra_info("peername")
    data[peer] = struct.unpack("3f", message)
    writer.close()

data = {}

loop = asyncio.get_event_loop()
loop.run_until_complete(websockets.serve(send, config.HOST, config.RECEIVE_PORT))
receiver = asyncio.start_server(receive, config.HOST, config.RECEIVE_PORT, loop=loop)
loop.run_until_complete(receiver)
loop.run_forever()

# TODO: Exit gracefully