import asyncio
import config
import json
import struct
import websockets
import time

last = time.time()


class Receiver:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, message, addr):
        global last

        ip = addr[0]
        print(f"Message from {ip}, time since last {(time.time() - last)*1000:.2f}ms")
        last = time.time()
        data[ip] = struct.unpack("3f", message)


async def send(websocket, _):
    async for message in websocket:
        if message == "get":
            print("Sending data")
            await websocket.send(json.dumps(data, sort_keys=True))

data = {}


# try:
def main():
    loop = asyncio.get_event_loop()

    udpsock = loop.create_datagram_endpoint(
        lambda: Receiver(),
        local_addr=(config.HOST, config.RECEIVE_PORT))
    loop.run_until_complete(udpsock)
    loop.run_until_complete(websockets.serve(
        send, config.HOST, config.SEND_PORT))
    loop.run_forever()


asyncio.run(main())
