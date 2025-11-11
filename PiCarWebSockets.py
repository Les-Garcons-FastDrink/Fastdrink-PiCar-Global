import asyncio
import websockets
import json
from PiCarFunctions import PiCarFunctions

class PiCarWebSockets:
    def __init__(self):
        self.pf = PiCarFunctions()

    async def receive_and_send(self, websocket):
        print("Connection has been made!")

        # Each message
        try:
            async for message in websocket:
                # Receiving
                try:
                    data = json.loads(message)
                    steer_angle = data.get("steer_angle", 0)
                    engine_power = data.get("engine_power", 0)
                    print(f'Received engine_power: {engine_power} and steer_angle: {steer_angle}')
                except json.JSONDecodeError:
                    print(f'Received non-JSON: {message}')

                # Sending
                response = {
                    "distance_sensor": self.pf.distancesensor__get_data(),
                    "line_sensor": self.pf.linedetector__get_data()
                }

                await websocket.send(json.dumps(response))
                print(f'Sent: {response}')

        except websockets.exceptions.ConnectionClosed:
            print("Connection has been lost!")

    async def receive_and_send_handler(self):
        async with websockets.serve(self.receive_and_send, "0.0.0.0", 8765):
            print("WebSocket server running on ws://0.0.0.0:8765")
            await asyncio.Future()

if __name__ == "__main__":
    piCar_websockets = PiCarWebSockets()
    asyncio.run(piCar_websockets.receive_and_send_handler())
