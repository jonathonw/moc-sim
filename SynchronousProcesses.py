#!/usr/bin/env python
import Processes
import UntimedProcesses

'''
Synchronous processes
'''

class MealyS(Processes.MealyProcess):
  ''' Synchronous Mealy process - same as generic Mealy but with partition function of 1'''
  def __init__(self, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal):
    Processes.MealyProcess.__init__(self, "return 1", outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)

  def runOneStep(self):
    Processes.MealyProcess.runOneStep(self)
  
class ZipS(Processes.ZipProcess):
  ''' Synchronous Zip process - same as generic Zip
      but with input partition functions of 1
  '''
  def __init__(self, inputSignal1, inputSignal2, outputSignal):
    Processes.ZipProcess.__init__(self, 1, 1, inputSignal1, inputSignal2, outputSignal)

  def runOneStep(self):
      Processes.ZipProcess.runOneStep(self)

class UnzipS(Processes.UnzipProcess):
  ''' Synchronous Unzip process - same as generic Unzip '''
  def __init__(self, inputSignal, outputSignal1, outputSignal2):
    Processes.UnzipProcess.__init__(self, inputSignal, outputSignal1, outputSignal2)

  def runOneStep(self):
      Processes.UnzipProcess.runOneStep(self)

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
    MealyS.__init__(self, outputFunction, "return 0", 0, inputSignal, outputSignal)

  def runOneStep(self):
    ''' same as generic Mealy's runOneStep '''
    MealyS.runOneStep(self)

class ScanS(MealyS):
  def __init__(self, nextStateFunction, initialState, inputSignal, outputSignal):
    '''
    Instantiates a ScanU process with a next state function (g) and an initial state (w_0).

    The output of ScanU is just the current state, so its output function
    is "return w".

    The next state function and initial sate are simply passed directly to
    the MealyU constructor.
    '''
    MealyS.__init__(self, "return w", nextStateFunction, initialState, inputSignal, outputSignal)

  def runOneStep(self):
    ''' same as generic Mealy's runOneStep '''
    MealyS.runOneStep(self)


class ScandS(MealyS):
  '''
  Instantiates a ScanU process with an input partition function (gamma),
  a next state function (g), and an initial state (w_0).

  This is exactly the same as ScanU, except that the process outputs
  its initial state before receiving/handling any input.
  TODO: figure out how to do this!
  '''
  pass

class SourceS(MealyS):
  '''
  Need new base class - right now, base Mealy needs an input signal to
  function and has no way of modifying the input signal.
  '''
  pass

class SinkS(MealyS):
  pass

class InitS(MealyS):
  pass


# Sample code
if __name__ == "__main__":
  
  # MapS process test
  print "MapS"
  outputFunction = "return [(x[0]+2)]"
  
  inputSignal = range(9)
  outputSignal = []
  
  process = MapS(outputFunction, inputSignal, outputSignal)

  print "InputSignal:", inputSignal
  process.runOneStep()
  process.runOneStep()
  process.runOneStep()
  print "OutputSignal:", outputSignal

  # ScanS process test
  print "ScanS"
  nextStateFunction = "return [(x[0]*x[0])]"
  initialState = [0]
  
  inputSignal = range(9)
  outputSignal = []
  
  process = ScanS(nextStateFunction, initialState, inputSignal, outputSignal)

  print "InputSignal:", inputSignal
  process.runOneStep()
  process.runOneStep()
  process.runOneStep()
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
  process.runOneStep()
  process.runOneStep()
  process.runOneStep()

  print "OutputSignal:", outputSignal
  
  # ZipS process test
  print "ZipS"
  
  inputSignal1 = range(9)
  inputSignal2 = range(10,19)
  outputSignal = []
  
  process = ZipS(inputSignal1, inputSignal2, outputSignal)
  print "InputSignal1:", inputSignal1
  print "InputSignal2:", inputSignal2
  process.runOneStep()
  process.runOneStep()
  print "OutputSignal:", outputSignal

  # UnzipS process test
  print "UnzipS"
  inputSignal = outputSignal
  outputSignal1 = []
  outputSignal2 = []
  
  process = UnzipS(inputSignal, outputSignal1, outputSignal2)
  print "InputSignal:", inputSignal
  process.runOneStep()
  process.runOneStep()
  print "OutputSignal1:", outputSignal1
  print "OutputSignal2:", outputSignal2
