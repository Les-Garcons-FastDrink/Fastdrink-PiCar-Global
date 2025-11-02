import sys
import os

sys.path.append(os.path.abspath("./SunFounder_PiCar-S/example"))
sys.path.append(os.path.abspath("./SunFounder_PiCar"))

from SunFounder_Line_Follower import Line_Follower
from ultrasonic_module import Ultrasonic_Sensor
from picar import front_wheels, back_wheels
import time
import picar





class PiCarFunctions:
     
     def __init__(self):
          # ------------------------
          # COMPONENTS
          # ------------------------
          self.fw = front_wheels.Front_Wheels(db='/home/pi/Documents/SunFounder_PiCar/picar/config')
          self.bw = back_wheels.Back_Wheels(db='/home/pi/Documents/SunFounder_PiCar/picar/config')
          self.ld = Line_Follower.Line_Follower()
          self.ds = Ultrasonic_Sensor(17)


          # ------------------------
          # SETUP
          # ------------------------
          picar.setup()
          self.fw.ready()
          self.bw.ready()
          
          # ------------------------
          # SETTINGS
          # ------------------------
          self.distancesensor_treshold = 10
          
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
     
     
     # ------------------------
     # DISTANCE SENSOR
     # ------------------------
     def distancesensor__get_data(self):
          return self.ds.get_distance()
     
     def distancesensor__is_obstacle_detected(self):
          if self.distancesensor__get_data() < self.distancesensor_treshold:
               return True
               
     
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
          self.bw.left_wheel.backward()
          self.bw.right_wheel.backward()

          
     def picarcontrols__backward(self):
          self.bw.left_wheel.forward()
          self.bw.right_wheel.forward()
          
     def picarcontrols__set_wheels_speed(self , speed : int):
          """
          Parameter
          ---------
               speed : int
                    Speed of engines. Must be an int from 0 to 100
          """
          
          self.picarcontrols__set_rw_speed(speed)
          self.picarcontrols__set_lw_speed(speed)
          
     def picarcontrols__set_lw_speed(self, speed):
          self.bw.left_wheel.speed = int(speed)
          
     def picarcontrols__set_rw_speed(self, speed):
          self.bw.right_wheel.speed = int(speed)
          
     def picarcontrols__stop(self):
          self.picarcontrols__set_wheels_speed(0)
          
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
     def picarcontrols__steer(self, angle):
          self.fw.turn(angle)
          
     def picarcontrols__reset_steer(self):
          self.fw.turn_straight()
     
     def picarsteering__test(self):
          try:
               while True:
                    print("turn_left")
                    self.picarcontrols__steer(-10)
                    time.sleep(1)
                    print("turn_straight")
                    self.picarcontrols__reset_steer()
                    time.sleep(1)
                    print("turn_right")
                    self.picarcontrols__steer(10)
                    time.sleep(1)
                    print("turn_straight")
                    self.picarcontrols__reset_steer()
                    time.sleep(1)
          except KeyboardInterrupt:
               self.picarcontrols__reset_steer()
          
          
          
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
          
          
          
     