
from flask import Flask, request, jsonify
from PiCarFunctions import PiCarFunctions


class PiCarRoutes:

     def __init__(self):
          self.picar = Flask(__name__)
          self._setup_routes()
          
          self.pf = PiCarFunctions()


     def _setup_routes(self):
          # ------------------------
          # LINE DETECTOR
          # ------------------------
          @self.picar.route('/picar/linedetector/get_data', methods=['GET'])
          def routes__linedetector__get_data(self):
               return self.pf.linedetector__get_data()

          @self.picar.route('/picar/linedetector/test', methods=['POST'])
          def routes__linedetector__test(self):
               self.pf.linedetector__test()


          # ------------------------
          # DISTANCE SENSOR
          # ------------------------
          @self.picar.route('/picar/distancesensor/get_data', methods=['GET'])
          def routes__distancesensor__get_data(self):
               return self.pf.distancesensor__get_data()

          @self.picar.route('/picar/distancesensor/is_obstacle_detected', methods=['GET'])
          def routes__distancesensor__is_obstacle_detected(self):
               return self.pf.distancesensor__is_obstacle_detected()

          @self.picar.route('/picar/distancesensor/test', methods=['POST'])
          def routes__distancesensor__test(self):
               self.pf.distancesensor__test()


          # ------------------------
          # PICAR CONTROLS
          # ------------------------

          ### ENGINES
          @self.picar.route('/picar/engines/forward', methods=['POST'])
          def routes__picarcontrols__forward(self):
               self.pf.picarcontrols__forward()

          @self.picar.route('/picar/engines/backward', methods=['POST'])
          def routes__picarcontrols__backward(self):
               self.pf.picarcontrols__backward()
          
          @self.picar.route('/picar/engines/set_wheels_speed/<speed>', methods=['POST'])  
          def routes__picarcontrols__set_wheels_speed(self , speed : int):
               self.pf.picarcontrols__set_wheels_speed(speed)

          @self.picar.route('/picar/engines/set_lw_speed/<speed>', methods=['POST'])
          def routes__picarcontrols__set_lw_speed(self, speed):
               self.pf.picarcontrols__set_lw_speed(speed)
          
          @self.picar.route('/picar/engines/set_rw_speed/<speed>', methods=['POST'])   
          def routes__picarcontrols__set_rw_speed(self, speed):
               self.pf.picarcontrols__set_rw_speed(speed)
          
          @self.picar.route('/picar/engines/stop', methods=['POST'])
          def routes__picarcontrols__stop(self):
               self.pf.picarcontrols__stop()
          
          @self.picar.route('/picar/engines/test', methods=['POST'])
          def routes__picarengine__test(self):
               self.pf.picarengine__test()

          ### STEERING
          @self.picar.route('/picar/steering/cali_left', methods=['POST'])  
          def routes__picarcontrols__steer_cali_left(self):
               self.pf.picarcontrols__steer_cali_left()

          @self.picar.route('/picar/steering/cali_right', methods=['POST'])
          def routes__picarcontrols__steer_cali_right(self):
               self.pf.picarcontrols__steer_cali_right()
          

          @self.picar.route('/picar/steering/steer/<angle>', methods=['POST'])
          def routes__picarcontrols__steer(self, angle):
               self.pf.picarcontrols__steer(angle)

          @self.picar.route('/picar/steering/reset_steer', methods=['POST'])
          def routes__picarcontrols__reset_steer(self):
               self.pf.picarcontrols__reset_steer()

          @self.picar.route('/picar/steering/test', methods=['POST'])
          def routes__picarsteering__test(self):
               self.pf.picarsteering__test()
                    
                    
     def begin_listening(self):
          # Démarre le serveur Flask
          self.picar.run(debug=True)
          

if __name__ == "__main__":
     
     webAPI = PiCarRoutes()  # Appelle __init__
     webAPI.begin_listening()
