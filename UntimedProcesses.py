#!/usr/bin/env python
import Processes

'''
Untimed processes - some of these processes are identical to their
generic counterparts; others are simplified versions.
'''

class MealyU(Processes.MealyProcess):
  ''' Untimed Mealy process - same as generic Mealy '''
  def __init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal):
    Processes.MealyProcess.__init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)

  def runOneStep(self):
    Processes.MealyProcess.runOneStep(self)
  
class ZipU(Processes.ZipProcess):
  ''' Untimed Zip process - same as generic Zip '''
  def __init__(self, signal1Count, signal2Count, inputSignal1, inputSignal2, outputSignal):
    Processes.ZipProcess.__init__(self, signal1Count, signal2Count, inputSignal1, inputSignal2, outputSignal)

  def runOneStep(self):
      Processes.ZipProcess.runOneStep(self)

class UnzipU(Processes.UnzipProcess):
  ''' Untimed Unzip process - same as generic Unzip '''
  def __init__(self, inputSignal, outputSignal1, outputSignal2):
    Processes.UnzipProcess.__init__(self, inputSignal, outputSignal1, outputSignal2)

  def runOneStep(self):
      Processes.UnzipProcess.runOneStep(self)

class MapU(MealyU):
  ''' Untimed Map process - basically a simplified Untimed Mealy process '''
  def __init__(self, partitionConstant, outputFunction, inputSignal, outputSignal):
    '''
    Instantiates an MapU process with an input partition constant (c)
    and an output function (f).

    The input partition is constant, so we must pass "return c" as a partition
    function to MealyU.

    The output of MapU is just a function of the input, as opposed MealyU, where
    the output is a function of both the input and the state. This is fine - MealyU
    still works just fine without any state (w) arguments in its output function.

    The untimed Map process is stateless, so we just pass a dummy function and
    initial state to the generic mealy process.
    '''
    MealyU.__init__(self, "return %d" % partitionConstant, outputFunction, "return 0", 0, inputSignal, outputSignal)

  def runOneStep(self):
    ''' same as generic Mealy's runOneStep '''
    MealyU.runOneStep(self)

class ScanU(MealyU):
  def __init__(self, partitionFunction, nextStateFunction, initialState, inputSignal, outputSignal):
    '''
    Instantiates a ScanU process with an input partition function (gamma),
    a next state function (g), and an initial state (w_0).

    The input partition function is simply passed directly to the MealyU
    constructor.

    The output of ScanU is just the current state, so its output function
    is "return w".
    NOTE: SOMETIMES WE ASSUME STATE IS A NUMBER, SOMETIMES AN EVENT - WHICH IS IT??

    The next state function and initial sate are simply passed directly to
    the MealyU constructor.
    '''
    MealyU.__init__(self, partitionFunction, "return w", nextStateFunction, initialState, inputSignal, outputSignal)

  def runOneStep(self):
    ''' same as generic Mealy's runOneStep '''
    MealyU.runOneStep(self)


class ScandU(MealyU):
  '''
  Instantiates a ScanU process with an input partition function (gamma),
  a next state function (g), and an initial state (w_0).

  This is exactly the same as ScanU, except that the process outputs
  its initial state before receiving/handling any input.
  TODO: figure out how to do this!
  '''
  pass

class SourceU(MealyU):
  '''
  Need new base class - right now, base Mealy needs an input signal to
  function and has no way of modifying the input signal.
  '''
  pass

class SinkU(MealyU):
  pass

class InitU(MealyU):
  pass


# Sample code
if __name__ == "__main__":
  
  # MapU process test
  print "MapU"
  partitionConstant = 3
  outputFunction = "return [(x[0] + x[1] + x[2])]"
  
  inputSignal = range(9)
  outputSignal = []
  
  process = MapU(partitionConstant, outputFunction, inputSignal, outputSignal)

  print "InputSignal:", inputSignal
  process.runOneStep()
  process.runOneStep()
  process.runOneStep()
  print "OutputSignal:", outputSignal

  # ScanU process test
  print "ScanU"
  partitionFunction = "return 3"
  nextStateFunction = "return [(x[0] + x[1] + x[2])]"
  initialState = [0]
  
  inputSignal = range(9)
  outputSignal = []
  
  process = ScanU(partitionFunction, nextStateFunction, initialState, inputSignal, outputSignal)

  print "InputSignal:", inputSignal
  process.runOneStep()
  process.runOneStep()
  process.runOneStep()
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
  process.runOneStep()
  process.runOneStep()
  process.runOneStep()

  print "OutputSignal:", outputSignal
  
  # ZipU process test
  print "ZipU"
  
  inputSignal1 = range(9)
  inputSignal2 = range(10,19)
  outputSignal = []
  
  process = ZipU(2, 4, inputSignal1, inputSignal2, outputSignal)
  print "InputSignal1:", inputSignal1
  print "InputSignal2:", inputSignal2
  process.runOneStep()
  process.runOneStep()
  print "OutputSignal:", outputSignal

  # UnzipU process test
  print "UnzipU"
  inputSignal = outputSignal
  outputSignal1 = []
  outputSignal2 = []
  
  process = UnzipU(inputSignal, outputSignal1, outputSignal2)
  print "InputSignal:", inputSignal
  process.runOneStep()
  process.runOneStep()
  print "OutputSignal1:", outputSignal1
  print "OutputSignal2:", outputSignal2