#!/usr/bin/env python
import Processes
import UntimedProcesses

'''
Synchronous processes
'''

## Synchronous Mealy process.  Same as generic Mealy but with partition function
#  of 1.
class MealyS(Processes.MealyProcess):
  def __init__(self, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal):
    partitionFunction = "return 1"
    Processes.MealyProcess.__init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)
    
## Synchronous Zip process.  Same as generic Zip but with input partition 
#  functions of 1.
class ZipS(Processes.ZipProcess):
  def __init__(self, inputSignal1, inputSignal2, outputSignal):
    signal1Count = 1
    signal2Count = 1
    Processes.ZipProcess.__init__(self, signal1Count, signal1Count, inputSignal1, inputSignal2, outputSignal)

## Synchronous Unzip process.  Same as generic Unzip.
class UnzipS(Processes.UnzipProcess):
  pass

## Synchronous Map process.  Basically, a simplified Synchronous Mealy process.
class MapS(MealyS):
  ## Instantiates a Map process with a specified output function.  The output of
  #  MapS is just a function of the input, as opposed to MealyS, where the 
  #  output is a function of both the input and the state.
  #
  #  Each function should be specified as a string containing Python code (which
  #  will be evaluated at runtime); parameters are w (the current state), and x 
  #  (the input).  x will be a list containing the input partition for this 
  #  execution of the process.
  #
  #  @param outputFunction    The output function (f) for this process.  Should
  #                           return the process's output (as a list).
  #  @param inputSignal       The input signal to this process.
  #  @param outputSignal      The output signal from this process.
  def __init__(self, outputFunction, inputSignal, outputSignal):
    #The Synchronous Map process is stateless, so we just pass a dummy function and
    #initial state to the generic mealy process.
    nextStateFunction = "return 0"
    initialState = 0
    MealyS.__init__(self, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)

## Synchronous Scan process.
class ScanS(Processes.ScanProcess):
  def __init__(self, nextStateFunction, initialState, inputSignal, outputSignal):
    Processes.ScanProcess.__init__(self, "return 1", nextStateFunction, initialState, inputSignal, outputSignal)
  pass

## Synchronous ScandS process.  The same as ScanS, except that the process
#  outputs its initial state before receiving or handling any input.
class ScandS(MealyS):
  ## Instantiates a ScandS process with a next state function and initial 
  #  state.
  #
  #  Each function should be specified as a string containing Python code (which
  #  will be evaluated at runtime); parameters are w (the current state), and x 
  #  (the input).  x will be a list containing the input partition for this 
  #  execution of the process.
  #
  #  @param nextStateFunction The next state function (g) for this process.
  #                           Should return the next state (consistent with the
  #                           type used for the initial state).
  #  @param initialState      The initial state for the system.  Can be any
  #                           type, but should be consistent with the type
  #                           returned by nextStateFunction.
  #  @param inputSignal       The input signal to this process.
  #  @param outputSignal      The output signal from this process.
  def __init__(self, nextStateFunction, initialState, inputSignal, outputSignal):
    outputFunction = "return [w]"
    MealyS.__init__(self, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)

## A synchronous Source process.  Same as the generic Source process.
class SourceS(Processes.SourceProcess):
  pass

## A synchronous Init process.  Same as the generic Init process.
class InitS(Processes.InitProcess):
  pass

def fireProcess(process):
  if process.preFire():
    process.fire()
    process.postFire()
  else:
    print "Precondition not met"

def main():
  # MapS process test
  print "MapS"
  outputFunction = "return [(x[0]+2)]"
  
  inputSignal = range(9)
  outputSignal = []
  
  process = MapS(outputFunction, inputSignal, outputSignal)

  print "InputSignal:", inputSignal
  fireProcess(process)
  fireProcess(process)
  fireProcess(process)
  print "OutputSignal:", outputSignal

  # ScanS process test
  print "ScanS"
  nextStateFunction = "return [(x[0]*x[0])]"
  initialState = [0]
  
  inputSignal = range(9)
  outputSignal = []
  
  process = ScanS(nextStateFunction, initialState, inputSignal, outputSignal)

  print "InputSignal:", inputSignal
  fireProcess(process)
  fireProcess(process)
  fireProcess(process)
  print "OutputSignal:", outputSignal
  
  # MealyS process test
  print "MealyS"
  outputFunction = "return [(x[0] + 3 + w)]"
  nextStateFunction = "return x[0]"
  initialState = 0
  
  inputSignal = range(9)
  outputSignal = []
  
  process = MealyS(outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)
  print "InputSignal:", inputSignal
  fireProcess(process)
  fireProcess(process)
  fireProcess(process)

  print "OutputSignal:", outputSignal
  
  # ZipS process test
  print "ZipS"
  
  inputSignal1 = range(9)
  inputSignal2 = range(10,19)
  outputSignal = []
  
  process = ZipS(inputSignal1, inputSignal2, outputSignal)
  print "InputSignal1:", inputSignal1
  print "InputSignal2:", inputSignal2
  fireProcess(process)
  fireProcess(process)
  print "OutputSignal:", outputSignal

  # UnzipS process test
  print "UnzipS"
  inputSignal = outputSignal
  outputSignal1 = []
  outputSignal2 = []
  
  process = UnzipS(inputSignal, outputSignal1, outputSignal2)
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

  process = SourceS(nextStateFunction, initialState, outputSignal)
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

  process = InitS(initialValue, inputSignal, outputSignal)
  fireProcess(process)
  fireProcess(process)
  fireProcess(process)
  fireProcess(process)
  print "OutputSignal:", outputSignal

# Sample code
if __name__ == "__main__":
  main()

