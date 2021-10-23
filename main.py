import asyncio
import json
import struct
import websockets
import time

import config


class Receiver:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, message, addr):
        ip = addr[0]
        print(f"Message from {ip}")
        # Split and store values
        data[ip] = struct.unpack("3f", message)
        # Store timestamp of most recent message
        last_seen[ip] = time.time()


async def send(websocket, _):
    async for message in websocket:
        if message == "get":
            print("Sending data")
            # Remove data for nodes that stopped sending input
            global data
            data = {k: v for k, v in data.items()
                    if time.time() - last_seen[k] < config.TIMEOUT}
            # Send JSON-formatted data sorted by ip
            await websocket.send(json.dumps(data, sort_keys=True))

data = {}
last_seen = {}


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
