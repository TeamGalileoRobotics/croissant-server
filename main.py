import asyncio
import config
import json
import struct
import websockets


class Receiver:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, message, addr):
        ip = addr[0]
        print(str(message) + " from " + str(ip))
        data[ip] = struct.unpack("3f", message)


async def send(websocket, _):
    async for message in websocket:
        if message == "get":
            print("Sending data")
            await websocket.send(json.dumps(data))

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
# start_send()
# except KeyboardInterrupt:
#    pass
# finally:
#    print("Exiting...")
#    transport.close()
#    event_loop.close()
#    running_loop.close()
# TODO: Stop tasks
