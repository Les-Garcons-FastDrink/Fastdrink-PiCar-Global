import sys
import os

sys.path.insert(0, "/home/pi/Documents/SunFounder_PiCar/picar_local")
sys.path.append(os.path.abspath("./SunFounder_PiCar-S/example"))
sys.path.append(os.path.abspath("./SunFounder_PiCar"))

from SunFounder_Line_Follower import Line_Follower
from ultrasonic_module import Ultrasonic_Sensor
from picar_local import front_wheels, back_wheels
import numpy as np
from scipy import signal
print(front_wheels.__file__)
import time
import picar_local
import threading





class PiCarFunctions:

     def __init__(self):
          # ------------------------
          # COMPONENTS
          # ------------------------
          self.fw = front_wheels.Front_Wheels(db='/home/pi/Documents/SunFounder_PiCar/picar_local/config')
          self.bw = back_wheels.Back_Wheels(db='/home/pi/Documents/SunFounder_PiCar/picar_local/config')
          self.ld = Line_Follower.Line_Follower()
          self.ds = Ultrasonic_Sensor(17)

          # ------------------------
          # SETUP
          # ------------------------
          picar_local.setup()
          self.fw.ready()
          self.bw.ready()

          ### FILTER SETUP
          freq_echantillonage = 40
          freq_coupure_hz = 4
          freq_coupure_normalisee = freq_coupure_hz/(freq_echantillonage/2)
          butter_ordre = 2

          self.filter_b, self.filter_a = signal.butter(butter_ordre, freq_coupure_normalisee)

          # Initialiser le buffer de distance avec des lectures initiales
          self.distance_array = [self.ds.get_distance() for _ in range(3)]

          # Initialiser l'état du filtre (zi)
          self.filter_zi = signal.lfilter_zi(self.filter_b, self.filter_a) * self.distance_array[0]

          # ------------------------
          # SETTINGS
          # ------------------------
          self.distancesensor_treshold = 10
          self.acceleration_ns = 0.000000015
          self.current_speed = 0
          self.acceleration_start_delta_time = 0
          self.is_first_acceleration = True

          # ------------------------
          # THREADING
          # ------------------------
          self._running = False
          self._lock = threading.Lock()  # Pour protéger distance_array
          self.th1 = None

          # Démarrer le thread automatiquement
          self.__init_distancesensor_loop_thread__()

     def __del__(self):
          """Nettoyage à la destruction de l'objet"""
          self.stop_distance_sensor_thread()


     def __init_distancesensor_loop_thread__(self):
          self._running = True
          self.th1 = threading.Thread(target=self.__start_distancesensor_loop__, daemon=True)
          self.th1.start()

     def __start_distancesensor_loop__(self):
          """Boucle qui tourne en continu pour mettre à jour le capteur"""
          while self._running:
               self.distancesensor__set_filtered_data()
               time.sleep(0.025)  # 40 Hz

     def stop_distance_sensor_thread(self):
          """Arrête proprement le thread du capteur de distance"""
          self._running = False
          if self.th1 is not None:
               self.th1.join(timeout=1.0)

     # ------------------------
     # LINE FOLLOWER
     # ------------------------
     def linedetector__get_data(self):
          return self.ld.read_digital()

     def linedetector__test(self):
          while True:
               print(self.linedetector__get_data())
               print('')
               time.sleep(0.5)

     def linedetector__set_reference_white(self):
          self.ld.set_reference_white()

     def linedetector__set_reference_black(self):
          self.ld.set_reference_black()

     def linedetector__set_reference(self):
          self.ld.set_reference()

     def linedetector__get_reference(self):
          return self.ld.get_reference()

     def linedetector__get_reference_black(self):
          return self.ld.get_reference_black()

     def linedetector__get_reference_white(self):
          return self.ld.get_reference_white()

     # ------------------------
     # DISTANCE SENSOR
     # ------------------------

     def distancesensor__get_data(self):
          return self.ds.get_distance()

     def distancesensor__get_filtered_data(self):
          """Retourne la dernière valeur filtrée de manière thread-safe"""
          with self._lock:
               return self.distance_array[-1]

     def distancesensor__set_filtered_data(self):
          """Filtre la nouvelle mesure et met à jour le buffer"""
          distance = self.distancesensor__get_data()

          if distance == -1:  # Lecture invalide
               return

          # Filtrer avec maintien d'état
          filtered_distance, self.filter_zi = signal.lfilter(
               self.filter_b,
               self.filter_a,
               [distance],
               zi=self.filter_zi
          )

          # Mise à jour thread-safe du buffer
          with self._lock:
               self.distance_array.append(filtered_distance[0])
               self.distance_array.pop(0)


     def distancesensor__is_obstacle_detected(self):
          return self.distancesensor__get_filtered_data() < self.distancesensor_treshold


     def distancesensor__test(self):
          while True:
               distance = self.ds.get_distance()
               status = self.ds.less_than(self.distancesensor_treshold)
               if distance != -1:
                    print('distance', distance, 'cm')
               time.sleep(0.1)


     # ------------------------
     # PICAR CONTROLS
     # ------------------------

     ### ENGINES
     def picarcontrols__forward(self):
          self.bw.left_wheel.forward()
          self.bw.right_wheel.forward()


     def picarcontrols__backward(self):
          self.bw.left_wheel.backward()
          self.bw.right_wheel.backward()

     def picarcontrols__set_wheels_speed(self , speed : int):
          """
          Parameter
          ---------
               speed : int
                    Speed of engines. Must be an int from -100 to 100
          """

          #On détermine la vitesse après accélération
          if(self.is_first_acceleration):
               self.acceleration_start_delta_time = time.monotonic_ns()
               self.is_first_acceleration = False
          self.current_speed, self.acceleration_start_delta_time = self.picarcontrols__accelerate_to_speed(self.current_speed, speed, self.acceleration_start_delta_time)
          #On applique la nouvelle vitesse au bolide
          if(self.current_speed >= 0):
               self.picarcontrols__set_rw_speed(int(self.current_speed))
               self.picarcontrols__set_lw_speed(int(self.current_speed))
               self.picarcontrols__forward()
          elif(self.current_speed < 0):
               self.picarcontrols__set_rw_speed(-int(self.current_speed))
               self.picarcontrols__set_lw_speed(-int(self.current_speed))
               self.picarcontrols__backward()

     def picarcontrols__set_bi_wheels_speed(self , speed : int, angle : int):
          """
          Parameter
          ---------
               speed : int
                    Speed of engines. Must be an int from -100 to 100
               angle : int
                    Steering angle, in degrees. Must be an integer between -45 and 45 inclusive.
                    A value of 0 corresponds to the neutral position, where the wheels are perfectly straight.
          """

          # On détermine la vitesse après accélération
          if(self.is_first_acceleration):
               self.acceleration_start_delta_time = time.monotonic_ns()
               self.is_first_acceleration = False
          self.current_speed, self.acceleration_start_delta_time = self.picarcontrols__accelerate_to_speed(self.current_speed, speed, self.acceleration_start_delta_time)

          if(self.current_speed >= 0):
               if (angle > 0):
                    self.picarcontrols__set_rw_speed(int(self.current_speed))
                    self.picarcontrols__set_lw_speed(int(0.5*self.current_speed))
               else :
                    self.picarcontrols__set_rw_speed(int(0.5*self.current_speed))
                    self.picarcontrols__set_lw_speed(int(self.current_speed))
               self.picarcontrols__forward()
          elif(self.current_speed < 0):
               if (angle > 0):
                    self.picarcontrols__set_rw_speed(-int(self.current_speed))
                    self.picarcontrols__set_lw_speed(-int(0.5*self.current_speed))
               else :
                    self.picarcontrols__set_rw_speed(-int(0.5*self.current_speed))
                    self.picarcontrols__set_lw_speed(-int(self.current_speed))
               self.picarcontrols__backward()

     def picarcontrols__set_lw_speed(self, speed):
          self.bw.set_lw_speed(int(speed))

     def picarcontrols__set_rw_speed(self, speed):
          self.bw.set_rw_speed(int(speed))

     def picarcontrols__get_speed(self):
          return self.bw.left_wheel.speed, self.bw.right_wheel.speed

     def picarcontrols__stop(self):
          self.picarcontrols__set_wheels_speed(0)

     def picarcontrols__engines_cali_left(self):
          self.bw.calibration()
          self.bw.cali_left()
          self.bw.cali_ok()

     def picarcontrols__engines_cali_right(self):
          self.bw.calibration()
          self.bw.cali_right()
          self.bw.cali_ok()

     def picarcontrols__engines_get_calibration_values(self):
          return self.bw.get_calibration_values()

     def picarengine__test(self):
          DELAY = 0.01
          try:
               self.picarcontrols__forward()
               for i in range(0, 100):
                    self.picarcontrols__set_wheels_speed(i)
                    print("Forward, speed =", i)
                    time.sleep(DELAY)
               for i in range(100, 0, -1):
                    self.picarcontrols__set_wheels_speed(i)
                    print("Forward, speed =", i)
                    time.sleep(DELAY)

               self.picarcontrols__backward()
               for i in range(0, 100):
                    self.picarcontrols__set_wheels_speed(i)
                    print("Backward, speed =", i)
                    time.sleep(DELAY)
               for i in range(100, 0, -1):
                    self.picarcontrols__set_wheels_speed(i)
                    print("Backward, speed =", i)
                    time.sleep(DELAY)
          except KeyboardInterrupt:
               print("KeyboardInterrupt, motor stop")
               self.picarcontrols__set_wheels_speed(0)
          finally:
               print("Finished, motor stop")
               self.picarcontrols__set_wheels_speed(0)


     ### STEERING
     def picarcontrols__steer(self, angle : int):
          """
          Parameter
          ---------
               angle : int
                    Steering angle, in degrees. Must be an integer between -45 and 45 inclusive.
                    A value of 0 corresponds to the neutral position, where the wheels are perfectly straight.
          """
          angle = int(angle)
          angle *= -1
          angle += 90
          self.fw.turn(angle)

     def picarcontrols__steer_get_angle(self):
          return self.fw.get_angle()

     def picarcontrols__steer_get_offset(self):
          return self.fw.get_offset()

     def picarcontrols__reset_steer(self):
          self.fw.turn_straight()

     def picarcontrols__steer_cali_left(self):
          self.fw.calibration()
          self.fw.cali_left()
          self.fw.cali_ok()

     def picarcontrols__steer_cali_right(self):
          self.fw.calibration()
          self.fw.cali_right()
          self.fw.cali_ok()

     def picarsteering__test(self):
          print("turn_left")
          self.picarcontrols__steer(-45)
          time.sleep(1)
          print("turn_straight")
          self.picarcontrols__reset_steer()
          time.sleep(1)
          print("turn_right")
          self.picarcontrols__steer(45)
          time.sleep(1)
          print("turn_straight")
          self.picarcontrols__reset_steer()

     def picarcontrols__accelerate_to_speed(self, current_speed : float, target_speed : int, start_time : int):
          #start_time doit être en ns
          delta_speed = 0
          if (current_speed < target_speed):
               current_time = time.monotonic_ns()
               delta_speed = (current_time - start_time) * self.acceleration_ns
          else:
               current_time = time.monotonic_ns()
               delta_speed = (start_time - current_time) * self.acceleration_ns
          current_speed = current_speed + delta_speed
          end_time = time.monotonic_ns()
          return current_speed, end_time

     # Ending
     def picarcontrols__direct_stop(self):
          # Setting motors and steer to 0
          self.picarcontrols__set_rw_speed(0)
          self.picarcontrols__set_lw_speed(0)
          self.picarcontrols__steer(0)
          self.picarcontrols__forward()

          # Setting to 0 for acceleration
          self.is_first_acceleration = True
          self.current_speed = 0



if __name__ == "__main__":
    pf = PiCarFunctions()  # crée l’instance de la classe

    if len(sys.argv) < 2:
        print("Usage: python3 PiCarFunctions.py <method_name> [args...]")
        sys.exit(1)

    method_name = sys.argv[1]  # le nom de la méthode passée en argument
    args = sys.argv[2:]        # arguments supplémentaires



    # Vérifie si la méthode existe dans la classe
    if hasattr(pf, method_name):
        method = getattr(pf, method_name)
        # Appelle la méthode avec les arguments de la ligne de commande
        method(*args)
    else:
        print(f"Erreur : La méthode '{method_name}' n'existe pas dans PiCarFunctions")



