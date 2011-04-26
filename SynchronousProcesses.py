#!/usr/bin/env python
import Processes
import UntimedProcesses

'''
Synchronous processes
'''

class MealyS(Processes.MealyProcess):
  ''' Synchronous Mealy process - same as generic Mealy but with partition function of 1'''
  def __init__(self, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal):
    partitionFunction = "return 1"
    Processes.MealyProcess.__init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)
    
class ZipS(Processes.ZipProcess):
  '''
  Synchronous Zip process - same as generic Zip
  but with input partition functions of 1
  '''
  def __init__(self, inputSignal1, inputSignal2, outputSignal):
    signal1Count = 1
    signal2Count = 1
    Processes.ZipProcess.__init__(self, signal1Count, signal1Count, inputSignal1, inputSignal2, outputSignal)

class UnzipS(Processes.UnzipProcess):
  ''' Synchronous Unzip process - same as generic Unzip '''
  pass

class MapS(MealyS):
  ''' Synchronous Map process - basically a simplified Synchronous Mealy process '''
  def __init__(self, outputFunction, inputSignal, outputSignal):
    '''
    Instantiates an MapS process with an output function (f).

    The output of MapS is just a function of the input, as opposed MealyS, where
    the output is a function of both the input and the state. This is fine - MealyS
    still works just fine without any state (w) arguments in its output function.

    The Synchronous Map process is stateless, so we just pass a dummy function and
    initial state to the generic mealy process.
    '''
    nextStateFunction = "return 0"
    initialState = 0
    MealyS.__init__(self, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)

class ScanS(Processes.ScanProcess):
  '''
    Instantiates a ScanS process with an input partition function (gamma),
    a next state function (g), and an initial state (w_0).
  '''
  pass

class ScandS(MealyS):
  '''
  Instantiates a ScanS process with an input partition function (gamma),
  a next state function (g), and an initial state (w_0).

  This is exactly the same as ScanS, except that the process outputs
  its initial state before receiving/handling any input.
  '''
  def __init__(self, nextStateFunction, initialState, inputSignal, outputSignal):
    outputFunction = "return [w]"
    MealyS.__init__(self, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)

class SourceS(Processes.SourceProcess):
  '''
  Synchronous Source process - same as generic Source process.
  '''
  pass

class InitS(Processes.InitProcess):
  '''
  Synchronous Init process - same as generic Source process.
  '''
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

