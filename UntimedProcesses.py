#!/usr/bin/env python
import Processes

'''
Untimed processes
'''

## An untimed Mealy process.
class MealyU(Processes.MealyProcess):
  pass

## An untimed Zip process.
class ZipU(Processes.ZipProcess):
  pass

## An untimed Unzip process.
class UnzipU(Processes.UnzipProcess):
  pass

## An untimed Map process. Basically, a simplified untimed Mealy process.
class MapU(MealyU):
  ## Instantiates a MapU process with an input partition constant and an output
  #  function. The output of MapU is just a function of the input, as opposed
  #  MealyU, where the output is a function of both the input and the state.
  #
  #  Each function should be specified as a string containing Python code (which
  #  will be evaluated at runtime); parameters are w (the current state), and x 
  #  (the input).  x will be a list containing the input partition for this 
  #  execution of the process.
  #
  #  @param partitionConstant     The partition constant (c) for this process.
  #  @param outputFunction        The output function (f) for this process.  Should
  #                               return the process's output (as a list).
  #  @param inputSignal           The input signal to this process.
  #  @param outputSignal          The output signal from this process.
  def __init__(self, partitionConstant, outputFunction, inputSignal, outputSignal):
    # The input partition is constant, so we must pass "return c" as a partition
    # function to MealyU.
    #
    # The untimed Map process is stateless, so we just pass a dummy function and
    # initial state to the generic mealy process.    
    partitionFunction = "return %s" % str(partitionConstant)
    nextStateFunction = "return 0"
    initialState = 0
    MealyU.__init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)

## An untimed Scan process.
class ScanU(Processes.ScanProcess):
  pass
  
## An untimed ScandU process.  The same as ScanU, except that the process
#  outputs its initial state before receiving or handling any input.
class ScandU(MealyU):
  ## Instantiates a ScandU process with a next state function and initial 
  #  state.
  #
  #  Each function should be specified as a string containing Python code (which
  #  will be evaluated at runtime); parameters are w (the current state), and x 
  #  (the input).  x will be a list containing the input partition for this 
  #  execution of the process.
  #
  #  @param partitionFunction The partition function (gamma) for this process.
  #  @param nextStateFunction The next state function (g) for this process.
  #                           Should return the next state (consistent with the
  #                           type used for the initial state).
  #  @param initialState      The initial state for the system.  Can be any
  #                           type, but should be consistent with the type
  #                           returned by nextStateFunction.
  #  @param inputSignal       The input signal to this process.
  #  @param outputSignal      The output signal from this process.
  def __init__(self, partitionFunction, nextStateFunction, initialState, inputSignal, outputSignal):
    outputFunction = "return [w]"
    MealyU.__init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)

## An untimed Source process.
class SourceU(Processes.SourceProcess):
  pass

## An untimed Init process.
class InitU(Processes.InitProcess):
  pass

def fireProcess(process):
  if process.preFire():
    process.fire()
    process.postFire()
  else:
    print "Precondition not met"

def main():
  # MapU process test
  print "MapU"
  partitionConstant = 3
  outputFunction = "return [(x[0] + x[1] + x[2])]"
  
  inputSignal = range(9)
  outputSignal = []
  
  process = MapU(partitionConstant, outputFunction, inputSignal, outputSignal)

  print "InputSignal:", inputSignal
  fireProcess(process)
  fireProcess(process)
  fireProcess(process)
  print "OutputSignal:", outputSignal

  # ScanU process test
  print "ScanU"
  partitionFunction = "return 3"
  nextStateFunction = "return [(x[0] + x[1] + x[2])]"
  initialState = 0
  
  inputSignal = range(9)
  outputSignal = []
  
  process = ScanU(partitionFunction, nextStateFunction, initialState, inputSignal, outputSignal)

  print "InputSignal:", inputSignal
  fireProcess(process)
  fireProcess(process)
  fireProcess(process)
  print "OutputSignal:", outputSignal
  
  # MealyU process test
  print "MealyU"
  partitionFunction = "return 3"
  outputFunction = "return [(x[0] + x[2] + w)]"
  nextStateFunction = "return x[1]"
  initialState = 0
  
  inputSignal = range(9)
  outputSignal = []
  
  process = MealyU(partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)
  print "InputSignal:", inputSignal
  fireProcess(process)
  fireProcess(process)
  fireProcess(process)

  print "OutputSignal:", outputSignal
  
  # ZipU process test
  print "ZipU"
  
  inputSignal1 = range(9)
  inputSignal2 = range(10,19)
  outputSignal = []
  
  process = ZipU(2, 4, inputSignal1, inputSignal2, outputSignal)
  print "InputSignal1:", inputSignal1
  print "InputSignal2:", inputSignal2
  fireProcess(process)
  fireProcess(process)
  print "OutputSignal:", outputSignal

  # UnzipU process test
  print "UnzipU"
  inputSignal = outputSignal
  outputSignal1 = []
  outputSignal2 = []
  
  process = UnzipU(inputSignal, outputSignal1, outputSignal2)
  print "InputSignal:", inputSignal
  fireProcess(process)
  fireProcess(process)
  print "OutputSignal1:", outputSignal1
  print "OutputSignal2:", outputSignal2
	
	 # Source process test
  print "Source"
  
  initialState = 1
  nextStateFunction = "return w + 1"
  outputSignal = []

  process = SourceU(nextStateFunction, initialState, outputSignal)
  fireProcess(process)
  fireProcess(process)
  fireProcess(process)
  fireProcess(process)
  print "OutputSignal:", outputSignal

  # Init process test
  print "Init"

  initialValue = 17
  inputSignal = range(4)
  outputSignal = []

  process = InitU(initialValue, inputSignal, outputSignal)
  fireProcess(process)
  fireProcess(process)
  fireProcess(process)
  fireProcess(process)
  print "OutputSignal:", outputSignal

# Sample code
if __name__ == "__main__":
  main()

  
  
