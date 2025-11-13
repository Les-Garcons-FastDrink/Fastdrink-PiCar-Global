import sys
import os
from PiCarFunctions import PiCarFunctions
import time


class Benchmark:

     THRESHOLD_DISTANCE = 0 #(m)

     def __init__(self):
          self.pf = PiCarFunctions()
          self.pf.fw.calibration()
          self.THRESHOLD_DISTANCE




     def _initialize_benchmark(self):
          """Initialise le benchmark : position, direction, données."""
          initial_distance = self.pf.distancesensor__get_data()
          if not (initial_distance > 0):
               print("Error with the distance sensor")
               return -1

          self.pf.picarcontrols__reset_steer()

          data_speed = []
          data_distance = []
          data_time = []

          self.pf.picarcontrols__forward()
          start_time = time.time()

          return initial_distance, data_speed, data_distance, data_time, start_time




     def _collect_data_point(self, speed, start_time, data_speed, data_distance, data_time):
          """Collecte un point de données et vérifie la condition d'arrêt."""
          distance = self.pf.distancesensor__get_data()

          if distance < self.THRESHOLD_DISTANCE:
               return False  # Arrêter le benchmark

          current_time = time.time() - start_time
          data_speed.append(int(speed))
          data_distance.append(float(distance))
          data_time.append(float(current_time))
          print(float(distance))

          return True  # Continuer le benchmark




     def _finalize_benchmark(self, filename, data_speed, data_distance, data_time,
                           initial_distance, write_to_file):
          """Finalise le benchmark : arrêt, sauvegarde, repositionnement."""
          self.pf.picarcontrols__stop()

          if write_to_file:
               self.write_benchmark_data_to_file(filename, data_speed, data_distance, data_time)

          # self.replace_piCar_at_distance_x(initial_distance)














     def run_all_benchmark(self, write_to_file=False):
          """Execute tous les benchmarks avec des vitesses de 10 à 100."""

          print("Running all benchmark \n")

          self.sleep_before_run()

          for speed in range(20, 100, 10):
               self.run_benchmark_constant_speed(speed, 0.1, write_to_file)

          for incr in range(1, 31, 5):
               self.run_benchmark_speed(0, 100, 0.1, incr, 5, write_to_file)

          # variance de la distance
          for n in range(0, 2):  # 0, 1, 2, 3
               i = 1.5 + n * 0.2
               self.run_benchmark_distance_sensor(distance=i, time_delta_data=0.05,  write_to_file=write_to_file)

          # variance du delta echantillonage
          for n in range(0, 10):  # 0.01 à 0.5 par pas de 0.05
               dt = 0.01 + n * 0.05
               self.replace_piCar_at_distance_x(i)
               self.run_benchmark_distance_sensor(distance=0.5,time_delta_data=dt, write_to_file=write_to_file)






     def run_benchmark_constant_speed(self, speed: int, interval=0.1, write_to_file=False):
          """
          Fait avancer la voiture à vitesse constante et prend une mesure toutes les `interval` secondes.
          """

          print(f"Running constant speed benchmark at speed {speed}\n")

          self.sleep_before_run()

          initial_distance, data_speed, data_distance, data_time, start_time = self._initialize_benchmark()
          self.pf.picarcontrols__set_wheels_speed(speed)

          while True:
               if not self._collect_data_point(speed, start_time, data_speed, data_distance, data_time):
                    break
               time.sleep(interval)

          filename = f"benchmark__speed_constant_{int(speed)}"
          self._finalize_benchmark(filename, data_speed, data_distance, data_time,
                                 initial_distance, write_to_file)


     def run_benchmark_speed(
          self,
          initial_speed=0,
          final_speed=100,
          time_delta_data=0.05,
          speed_increment=5,
          iter_delta_speed_increment=5,
          write_to_file=False
     ):

          print(f"Running acceleration benchmark with speed incrementation of {speed_increment} each {time_delta_data} sec\n")

          self.sleep_before_run()
          initial_distance, data_speed, data_distance, data_time, start_time = self._initialize_benchmark()

          speed = initial_speed
          iteration_count = 0

          while True:
               self.pf.picarcontrols__set_wheels_speed(speed)

               if not self._collect_data_point(speed, start_time, data_speed, data_distance, data_time):
                    break

               iteration_count += 1

               if (iteration_count % iter_delta_speed_increment) == 0 and speed < final_speed:
                    speed += iter_delta_speed_increment

               time.sleep(time_delta_data)

          filename = f"benchmark__speed_acceleration_increment_{speed_increment}"
          self._finalize_benchmark(filename, data_speed, data_distance, data_time,
                                 initial_distance, write_to_file)


     def run_benchmark_distance_sensor(
          self,
          distance=1,
          time_delta_data=0.05,
          nb_of_datas=200,
          write_to_file=False
     ):
          print(f"Running distance sensor benchmark, while stationnary at {distance}m and with delta time {time_delta_data} sec\n")
          distance = float(distance)
          time_delta_tata = float(time_delta_data)
          nb_of_datas = int(nb_of_datas)
          self.sleep_before_run()
          initial_distance, data_speed, data_distance, data_time, start_time = self._initialize_benchmark()

          # self.replace_piCar_at_distance_x(distance)

          iteration_count=0

          THRESHOLD_DISTANCE = 0
          while iteration_count < nb_of_datas:

               if not self._collect_data_point(0, start_time, data_speed, data_distance, data_time):
                    break

               iteration_count += 1

               time.sleep(float(time_delta_data))

          filename = f"benchmark__distance_sensor_{distance}m_tdelta_{time_delta_data}"
          self._finalize_benchmark(filename, data_speed, data_distance, data_time,
                                 initial_distance, write_to_file)




     #--------------------
     # BENCHMARK UTILS
     #--------------------


     def write_benchmark_data_to_file(self, filename, data_speed, data_distance, data_time):

          folder = "/home/pi/Documents/benchmarks"
          with open(f"{folder}/{filename}.txt", "w+") as f:
               f.write("time\tdistance\tspeed\n")  # entêtes
               for t, d, s in zip(data_time, data_distance, data_speed):
                    f.write(f"{t}\t{d}\t{s}\n")






     def sleep_before_run(self):

          sleep_delta : int = 5
          for i in range(sleep_delta):
               print(sleep_delta-i)
               time.sleep(1)



     def replace_piCar_at_distance_x(self, x):

          print(f"Replacing PiCar at distance {x}")
          speed = 40

          self.pf.picarcontrols__set_wheels_speed(speed)
          while True:
               distance = self.pf.distancesensor__get_data()

               if distance > (x-0.05) and distance < (x+0.05):
                    self.pf.picarcontrols__stop()
                    print("Replacement done")
                    return

               if distance > x :
                    self.pf.picarcontrols__forward()
                    continue

               self.pf.picarcontrols__backward()









if __name__ == "__main__":
     try :

          bm = Benchmark()  # crée l’instance de la classe

          if len(sys.argv) < 2:
               print("Usage: python3 benchmark.py <method_name> [args...]")
               sys.exit(1)

          method_name = sys.argv[1]  # le nom de la méthode passée en argument
          args = sys.argv[2:]        # arguments supplémentaires

          # Vérifie si la méthode existe dans la classe
          if hasattr(bm, method_name):
               method = getattr(bm, method_name)
               # Appelle la méthode avec les arguments de la ligne de commande
               method(*args)
          else:
               print(f"Erreur : La méthode '{method_name}' n'existe pas dans BenchMark")

     except KeyboardInterrupt:
          print("KeyboardInterrupt, motor stop")
          bm.pf.picarcontrols__stop()
