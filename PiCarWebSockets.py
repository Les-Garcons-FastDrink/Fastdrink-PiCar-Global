import asyncio
import websockets
import json
from PiCarFunctions import PiCarFunctions
from IniConfig import IniConfig

class PiCarWebSockets:
    def __init__(self, config_path = "./FastDrink-Godot-Headless/config.ini"):
        self.pf = PiCarFunctions()
        self.pf.picarcontrols__set_lw_speed(0)
        self.pf.picarcontrols__set_rw_speed(0)
        self.conf = IniConfig(config_path)
        self.conf_max_speed_limit = self.conf["CONF_MAX_SPEED_LIMIT"]
        self.conf_use_biwheels = self.conf["CONF_USE_BIWHEELS"]
        

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
                    end = data.get("end", 0)

                    if end:
                        self.pf.picarcontrols__direct_stop()
                    else:
                        self.pf.picarcontrols__steer(steer_angle)
                        
                        engine_power = int(self.conf_max_speed_limit*engine_power)
                        if not self.conf_use_biwheels :
                            self.pf.picarcontrols__set_wheels_speed(engine_power)
                        else :
                            self.pf.picarcontrols__set_bi_wheels_speed(engine_power, steer_angle)
                            
                except json.JSONDecodeError:
                    print(f'Received non-JSON: {message}')
                except websockets.exceptions.ConnectionClosed:
                    print("Connection has been lost!")

                # Sending
                response = {
                    "distance_sensor": self.pf.distancesensor__get_filtered_data(),
                    "line_sensor": self.pf.linedetector__get_data(),
                    "car_speed": int(self.pf.current_speed)
                }

                await websocket.send(json.dumps(response))

        except websockets.exceptions.ConnectionClosed:
            print("Connection has been lost!")
            self.pf.picarcontrols__direct_stop()

    async def receive_and_send_handler(self):
        async with websockets.serve(self.receive_and_send, "0.0.0.0", 8765):
            print("WebSocket server running on ws://0.0.0.0:8765")
            await asyncio.Future()

if __name__ == "__main__":
    piCar_websockets = PiCarWebSockets()
    asyncio.run(piCar_websockets.receive_and_send_handler())
