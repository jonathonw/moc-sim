#!/usr/bin/env python

import Processes

class MealyT(Processes.MealyProcess):
  def __init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal):
    Processes.MealyProcess.__init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)

class ZipT(Processes.ZipProcess):
  pass

class UnzipT(Processes.UnzipProcess):
  pass

class SourceT(Processes.SourceProcess):
  pass

class InitT(Processes.InitProcess):
  pass

def fireProcess(process):
  if process.preFire():
    process.fire()
    process.postFire()
  else:
    print "Precondition not met"

def main():
  # MealyT process test
  print "MealyT"
  partitionFunction = "return 3"
  outputFunction = "return [(x[0] + x[2] + w)]"
  nextStateFunction = "return x[1]"
  initialState = 0
  
  inputSignal = range(9)
  outputSignal = []
  
  process = MealyT(partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)
  print "InputSignal:", inputSignal
  fireProcess(process)
  fireProcess(process)
  fireProcess(process)

  print "OutputSignal:", outputSignal
  
  # ZipT process test
  print "ZipT"
  
  inputSignal1 = range(9)
  inputSignal2 = range(10,19)
  outputSignal = []
  
  process = ZipT(2, 4, inputSignal1, inputSignal2, outputSignal)
  print "InputSignal1:", inputSignal1
  print "InputSignal2:", inputSignal2
  fireProcess(process)
  fireProcess(process)
  print "OutputSignal:", outputSignal

  # UnzipT process test
  print "UnzipT"
  inputSignal = outputSignal
  outputSignal1 = []
  outputSignal2 = []
  
  process = UnzipT(inputSignal, outputSignal1, outputSignal2)
  print "InputSignal:", inputSignal
  fireProcess(process)
  fireProcess(process)
  print "OutputSignal1:", outputSignal1
  print "OutputSignal2:", outputSignal2

# Sample code
if __name__ == "__main__":
  main()
