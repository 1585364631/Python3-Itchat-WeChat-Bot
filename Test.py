import asyncio
import websockets


async def hello():
    async with websockets.connect("ws://47.106.68.150:9999") as websocket:
        await websocket.send("Hello world!")
        await websocket.recv()


asyncio.run(hello())
