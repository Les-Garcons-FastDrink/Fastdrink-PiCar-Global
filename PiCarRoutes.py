
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
from PiCarFunctions import PiCarFunctions


class PiCarRoutes:

     def __init__(self):
          self.picar = Flask(__name__)
          CORS(self.picar)
          self.pf = PiCarFunctions()
          self._setup_routes()
          


     def _setup_routes(self):
          
          @self.picar.route('/picar/ping', methods=['GET'])
          def routes__ping():
               return {"responseStatus" : 200}
          
          @self.picar.route('/picar/get_all_data', methods=['GET'])
          def routes__get_all_data():
               try:
                    # optional query param: ?filtered_data=true
                    q = request.args.get('filtered_data', 'false')
                    filtered_data = str(q).lower() in ('1', 'true', 'yes', 'y')

                    engine_power_left, engine_power_right = self.pf.picarcontrols__get_speed()
                    steer_data = self.pf.picarcontrols__steer_get_angle()
                    line_detector_data = self.pf.linedetector__get_data()
                    if filtered_data:
                         distance_sensor_data = self.pf.distancesensor__get_filtered_data()
                    else:
                         distance_sensor_data = self.pf.distancesensor__get_data()

                    return {
                         "response": {
                              "status": 200,
                              "data": {
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
                         "response": {
                              "status": 500,
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
               # linedetector__test is blocking (infinite loop). Run it in a background thread
               t = threading.Thread(target=self.pf.linedetector__test, daemon=True)
               t.start()
               return jsonify({"status": "started"}), 202
          
          @self.picar.route('/picar/linedetector/set_reference_white', methods=['PUT'])
          def routes__linedetector__set_reference_white():
               try :
                    self.pf.linedetector__set_reference_white()
                    return {"responseStatus" : 200}
               except :
                    return {"responseStatus" : 500}
                    
                    
          @self.picar.route('/picar/linedetector/set_reference_black', methods=['PUT'])
          def routes__linedetector__set_reference_black():
               try :
                    self.pf.linedetector__set_reference_black()
                    return {"responseStatus" : 200}
               except :
                    return {"responseStatus" : 500}

               
          @self.picar.route('/picar/linedetector/set_reference', methods=['PUT'])
          def routes__linedetector__set_reference():
               try :
                    self.pf.linedetector__set_reference()
                    return {"responseStatus" : 200}
               except :
                    return {"responseStatus" : 500}

               
          @self.picar.route('/picar/linedetector/get_reference', methods=['GET'])
          def routes__linedetector__get_reference():
               return self.pf.linedetector__get_reference()
          
          @self.picar.route('/picar/linedetector/get_reference_white', methods=['GET'])
          def routes__linedetector__get_reference_white():
               return self.pf.linedetector__get_reference_white()
          
          @self.picar.route('/picar/linedetector/get_reference_black', methods=['GET'])
          def routes__linedetector__get_reference_black():
               return self.pf.linedetector__get_reference_black()
               


          # ------------------------
          # DISTANCE SENSOR
          # ------------------------
          @self.picar.route('/picar/distancesensor/get_data', methods=['GET'])
          def routes__distancesensor__get_data():
               return self.pf.distancesensor__get_data()
          
          @self.picar.route('/picar/distancesensor/get_filtered_data', methods=['GET'])
          def routes__distancesensor__get_filtered_data():
               return self.pf.distancesensor__get_filtered_data()

          @self.picar.route('/picar/distancesensor/is_obstacle_detected', methods=['GET'])
          def routes__distancesensor__is_obstacle_detected():
               return self.pf.distancesensor__is_obstacle_detected()

          @self.picar.route('/picar/distancesensor/test', methods=['POST'])
          def routes__distancesensor__test():
               t = threading.Thread(target=self.pf.distancesensor__test, daemon=True)
               t.start()
               return jsonify({"status": "started"}), 202
          



          # ------------------------
          # PICAR CONTROLS
          # ------------------------

          ### ENGINES
          @self.picar.route('/picar/engines/forward', methods=['POST'])
          def routes__picarcontrols__forward():
               self.pf.picarcontrols__forward()
               return jsonify({"status": "ok"}), 200

          @self.picar.route('/picar/engines/backward', methods=['POST'])
          def routes__picarcontrols__backward():
               self.pf.picarcontrols__backward()
               return jsonify({"status": "ok"}), 200
          
          @self.picar.route('/picar/engines/set_wheels_speed/<speed>', methods=['POST'])  
          def routes__picarcontrols__set_wheels_speed(speed : int):
               self.pf.picarcontrols__set_wheels_speed(int(speed))
               return jsonify({"status": "ok", "speed": int(speed)}), 200

          @self.picar.route('/picar/engines/set_lw_speed/<speed>', methods=['POST'])
          def routes__picarcontrols__set_lw_speed(speed):
               self.pf.picarcontrols__set_lw_speed(int(speed))
               return jsonify({"status": "ok", "lw_speed": int(speed)}), 200
          
          @self.picar.route('/picar/engines/set_rw_speed/<speed>', methods=['POST'])   
          def routes__picarcontrols__set_rw_speed(speed):
               self.pf.picarcontrols__set_rw_speed(int(speed))
               return jsonify({"status": "ok", "rw_speed": int(speed)}), 200
          
          @self.picar.route('/picar/engines/stop', methods=['POST'])
          def routes__picarcontrols__stop():
               self.pf.picarcontrols__stop()
               return jsonify({"status": "ok"}), 200
          
          @self.picar.route('/picar/engines/test', methods=['POST'])
          def routes__picarengine__test():
               t = threading.Thread(target=self.pf.picarengine__test, daemon=True)
               t.start()
               return jsonify({"status": "started"}), 202
          
          @self.picar.route('/picar/engines/cali_left', methods=['POST'])  
          def routes__picarcontrols__engines_cali_left():
               self.pf.picarcontrols__engines_cali_left()
               return jsonify({"status": "ok"}), 200

          @self.picar.route('/picar/engines/cali_right', methods=['POST'])
          def routes__picarcontrols__engines_cali_right():
               self.pf.picarcontrols__engines_cali_right()
               return jsonify({"status": "ok"}), 200
          
          @self.picar.route('/picar/engines/engines_get_calibration_values')
          def routes__picarcontrols__engines_get_calibration_values():
               return self.pf.picarcontrols__engines_get_calibration_values()


          ### STEERING
          @self.picar.route('/picar/steering/cali_left', methods=['POST'])  
          def routes__picarcontrols__steer_cali_left():
               self.pf.picarcontrols__steer_cali_left()
               return jsonify({"status": "ok"}), 200

          @self.picar.route('/picar/steering/cali_right', methods=['POST'])
          def routes__picarcontrols__steer_cali_right():
               self.pf.picarcontrols__steer_cali_right()
               return jsonify({"status": "ok"}), 200
          

          @self.picar.route('/picar/steering/steer/<angle>', methods=['POST'])
          def routes__picarcontrols__steer(angle):
               
                  try:
                       self.pf.picarcontrols__steer(int(angle))
                  except ValueError:
                       self.pf.picarcontrols__steer(float(angle))
                  return jsonify({"status": "ok", "angle": angle}), 200

          @self.picar.route('/picar/steering/reset_steer', methods=['POST'])
          def routes__picarcontrols__reset_steer():
               self.pf.picarcontrols__reset_steer()
               return jsonify({"status": "ok"}), 200
          
          @self.picar.route('/picar/steering/get_steering_offset', methods=['GET'])
          def routes__picarcontrols__steer_get_offset():
               offset = self.pf.picarcontrols__steer_get_offset()
               return jsonify({
                    "response": {
                         "status": 200,
                         "data": {"offset": offset}
                    }
               }), 200

          @self.picar.route('/picar/steering/test', methods=['POST'])
          def routes__picarsteering__test():
               t = threading.Thread(target=self.pf.picarsteering__test, daemon=True)
               t.start()
               return jsonify({"status": "started"}), 202
          
         
                    
                    
     def begin_listening(self):
          # Démarre le serveur Flask
          self.picar.run(
               debug=True,
               use_reloader=False,
               host="0.0.0.0",
               port=5000,
               ssl_context=None  # désactiver HTTPS
          )
          

if __name__ == "__main__":
     
     webAPI = PiCarRoutes()  # Appelle __init__
     webAPI.begin_listening()
