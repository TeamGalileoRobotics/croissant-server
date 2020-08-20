import asyncio
import config
import json
import struct
import websockets


async def send(websocket, _):
    async for message in websocket:
        if message == "get":
            print("Sending data")
            await websocket.send(json.dumps(data))


async def receive(reader, writer):
    peer = writer.get_extra_info("peername")[0]
    while not reader.at_eof():
        message = await reader.read(12)
        print(str(message) + " from " + str(peer))
        data[peer] = struct.unpack("3f", message)


data = {}

loop = asyncio.get_event_loop()
loop.run_until_complete(websockets.serve(send, config.HOST, config.SEND_PORT))
receiver = asyncio.start_server(receive, config.HOST, config.RECEIVE_PORT, loop=loop)
loop.run_until_complete(receiver)
loop.run_forever()

# TODO: Exit gracefully
