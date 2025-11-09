import asyncio
import websockets
import json
from PiCarFunctions import PiCarFunctions

async def receivesAndSend(websocket):
    print("Connection has been made with GoDot!")

    try:
        async for message in websocket:
            print(f'Receiving: {message}')

            try:
                data = json.loads(message)
                velocity = data.get("velocity", 0)
                direction = data.get("direction", 0)
                print(f'Velocity: {velocity}, Direction: {direction}')
            except json.JSONDecodeError:
                print(f'Received non-JSON: {message}')

            response = {
                "distance": 100,
                "line_follower": [1, 0, 1, 0, 1]
            }
            await websocket.send(json.dumps(response))
            print(f'Sent: {response}')

    except websockets.exceptions.ConnectionClosed:
        print("Godot client disconnected")

async def main():
    async with websockets.serve(receivesAndSend, "0.0.0.0", 8765):
        print("WebSocket server running on ws://0.0.0.0:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())