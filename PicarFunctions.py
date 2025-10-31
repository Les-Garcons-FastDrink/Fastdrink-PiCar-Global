from SunFounder_Line_Follower import Line_Follower
from picar import front_wheels
from picar import back_wheels
from utrasonic_module import Ultrasonic_Sensor
from
import time
import picar





class PiCarFunctions:
     
     def __init__()
          # ------------------------
          # COMPONENTS
          # ------------------------
          self.fw = front_wheels.Front_Wheels(db='config')
          self.bw = back_wheels.Back_Wheels(db='config')
          self.lf = Line_Follower.Line_Follower()
          self.us = Ultrasonic_Sensor()


          # ------------------------
          # SETUP
          # ------------------------
          self.picar.setup()
          self.fw.ready()
          self.bw.ready()
          
          
     # ------------------------
     # LINE FOLLOWER
     # ------------------------
     def linefollower__get_data(self):
          return.self.lf.read_digital()
     
     
     
     # ------------------------
     # PICAR CONTROLS
     # ------------------------
     def picarcontrols__forward(self):
          bw.left_wheel.forward()
          bw.right_wheel.forward()
          
     def picarcontrols__backward(self):
          self.bw.left_wheel.backward()
          self.bw.right_wheel.backward()
          
     def picarcontrols__set_wheels_speed(self, speed):
          self.picarcontrols__set_rw_speed(speed)
          self.picarcontrols__set_rw_speed(speed)
          
     def picarcontrols__set_lw_speed(self, speed):
          self.bw.left_wheel.speed = speed
          
     def picarcontrols__set_rw_speed(self, speed):
          self.bw.right_wheel.speed = speed
     