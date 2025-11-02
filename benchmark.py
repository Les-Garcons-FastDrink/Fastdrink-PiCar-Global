from PiCarFunctions import PiCarFunctions



class Benchmark:


     def __init__(self):
          self.pf = PiCarFunctions()

     def run_all_benchmark(self):
          pass
     
     def run_benchmark_constant_speed(self, speed):
          self.pf.picarcontrols__reset_steer()
          self.pf.picarcontrols__set_wheels_speed(speed)
          
          
          self.pf.picarcontrols__forward()
          
     
     

          
          



     def write_output_to_file(speed):
          filename = f"bechmark_speed_{speed}.txt"
          
          with open(filename, 'w'):
               pass
               






if __name__ == "__main__":
     bm = Benchmark()
     
     bm.run_all_benchmark()