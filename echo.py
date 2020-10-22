import asyncio
import websockets
import config

async def echo(websocket, path):
    async for message in websocket:
        print(message)
        await websocket.send(message)

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, "0.0.0.0", config.SEND_PORT))
asyncio.get_event_loop().run_forever()