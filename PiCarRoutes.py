
from flask import Flask, request, jsonify
from PiCarFunctions import PiCarFunctions


class PiCarRoutes:

     def __init__(self):
          self.picar = Flask(__name__)
          self.pf = PiCarFunctions()
          self._setup_routes()
          


     def _setup_routes(self):
          
          @self.picar.route('/picar/ping', methods=['GET'])
          def routes__ping():
               return {"responseStatus" : 200}
          
          @self.picar.route('/picar/get_all_data', methods=['GET'])
          def routes__get_all_data():
               try :
                    
                    engine_power_left, engine_power_right = self.pf.picarcontrols__get_speed()
                    steer_data = self.pf.picarcontrols__steer_get_angle()
                    distance_sensor_data = self.pf.distancesensor__get_data()
                    line_detector_data = self.pf.linedetector__get_data()
                    
                    return {
                         "response": {
                              "status": 200,
                              "datas": {
                                   "engines": {
                                        "engine_power_left": engine_power_left,
                                        "engine_power_right": engine_power_right
                                   },
                                   "steering": steer_data,
                                   "distance_sensor": distance_sensor_data,
                                   "line_detector": line_detector_data
                              }
                         }
                    }
               except Exception as e:
                    print(f"[ERROR] /picar/get_all_data: {e}")
                    return {
                         "response" :
                         {
                              "status" : 500,
                              "error": str(e)
                         }
                    }

                    
               
               
          
          # ------------------------
          # LINE DETECTOR
          # ------------------------
          @self.picar.route('/picar/linedetector/get_data', methods=['GET'])
          def routes__linedetector__get_data():
               return self.pf.linedetector__get_data()

          @self.picar.route('/picar/linedetector/test', methods=['POST'])
          def routes__linedetector__test():
               self.pf.linedetector__test()


          # ------------------------
          # DISTANCE SENSOR
          # ------------------------
          @self.picar.route('/picar/distancesensor/get_data', methods=['GET'])
          def routes__distancesensor__get_data():
               return self.pf.distancesensor__get_data()

          @self.picar.route('/picar/distancesensor/is_obstacle_detected', methods=['GET'])
          def routes__distancesensor__is_obstacle_detected():
               return self.pf.distancesensor__is_obstacle_detected()

          @self.picar.route('/picar/distancesensor/test', methods=['POST'])
          def routes__distancesensor__test():
               self.pf.distancesensor__test()


          # ------------------------
          # PICAR CONTROLS
          # ------------------------

          ### ENGINES
          @self.picar.route('/picar/engines/forward', methods=['POST'])
          def routes__picarcontrols__forward():
               self.pf.picarcontrols__forward()

          @self.picar.route('/picar/engines/backward', methods=['POST'])
          def routes__picarcontrols__backward():
               self.pf.picarcontrols__backward()
          
          @self.picar.route('/picar/engines/set_wheels_speed/<speed>', methods=['POST'])  
          def routes__picarcontrols__set_wheels_speed(speed : int):
               self.pf.picarcontrols__set_wheels_speed(speed)

          @self.picar.route('/picar/engines/set_lw_speed/<speed>', methods=['POST'])
          def routes__picarcontrols__set_lw_speed(speed):
               self.pf.picarcontrols__set_lw_speed(speed)
          
          @self.picar.route('/picar/engines/set_rw_speed/<speed>', methods=['POST'])   
          def routes__picarcontrols__set_rw_speed(speed):
               self.pf.picarcontrols__set_rw_speed(speed)
          
          @self.picar.route('/picar/engines/stop', methods=['POST'])
          def routes__picarcontrols__stop():
               self.pf.picarcontrols__stop()
          
          @self.picar.route('/picar/engines/test', methods=['POST'])
          def routes__picarengine__test():
               self.pf.picarengine__test()

          ### STEERING
          @self.picar.route('/picar/steering/cali_left', methods=['POST'])  
          def routes__picarcontrols__steer_cali_left():
               self.pf.picarcontrols__steer_cali_left()

          @self.picar.route('/picar/steering/cali_right', methods=['POST'])
          def routes__picarcontrols__steer_cali_right():
               self.pf.picarcontrols__steer_cali_right()
          

          @self.picar.route('/picar/steering/steer/<angle>', methods=['POST'])
          def routes__picarcontrols__steer(angle):
               self.pf.picarcontrols__steer(angle)

          @self.picar.route('/picar/steering/reset_steer', methods=['POST'])
          def routes__picarcontrols__reset_steer():
               self.pf.picarcontrols__reset_steer()

          @self.picar.route('/picar/steering/test', methods=['POST'])
          def routes__picarsteering__test():
               self.pf.picarsteering__test()
          
         
                    
                    
     def begin_listening(self):
          # Démarre le serveur Flask
          self.picar.run(
               debug=True,
               host="0.0.0.0",
               port=5000,
               ssl_context='adhoc'
          )
          

if __name__ == "__main__":
     
     webAPI = PiCarRoutes()  # Appelle __init__
     webAPI.begin_listening()
