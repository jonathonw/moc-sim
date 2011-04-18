#!/usr/bin/env python
import utilities

class Process:
  pass

class MealyProcess(Process):
  '''A generic Mealy process.'''
  def __init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal):
    '''
    Instantiates a Mealy state machine with a partition function (lambda), 
    output function (f), next state function (g), and initial state (w_0).
    
    Each function should be specified as a string (which will be evaluated at
    runtime); parameters are w (the current state), and x (the input).  x will
    be a list containing the input partition for this execution of the process.
    
    partitionFunction should return an positive integer corresponding to the
    number of elements in the partition, outputFunction should return the output
    (as a list), and nextStateFunction should return the initial state.
    
    nextStateFunction and initialState should use consistent types for states.
    '''
    self._partitionFunction = utilities.stringToFunction(partitionFunction, "w")
    self._outputFunction = utilities.stringToFunction(outputFunction, "w, x")
    self._nextStateFunction = utilities.stringToFunction(nextStateFunction, "w, x")
    self._state = initialState
    self._inputSignal = inputSignal
    self._outputSignal = outputSignal
    self._nextState = initialState
    
  def preFire(self):
    inputPartitionSize = self._partitionFunction(self._state)
    if len(self._inputSignal) >= inputPartitionSize:
      return True
    else:
      return False
    
  def fire(self):
    '''
    Runs this Mealy process for one step.
    
    TODO:  figure out how the process gets its input and output.
    '''
    
    inputPartitionSize = self._partitionFunction(self._state)
    inputEvents = []
    for i in range(inputPartitionSize):
      inputEvents.append(self._inputSignal.pop(0))
    outputEvents = self._outputFunction(self._state, inputEvents)
    self._nextState = self._nextStateFunction(self._state, inputEvents)
    self._outputSignal.extend(outputEvents)
    
  def postFire(self):
    self._state = self._nextState
    
class ZipProcess(Process):
  def __init__(self, signal1Count, signal2Count, inputSignal1, inputSignal2, outputSignal):
    self._signal1Count = signal1Count
    self._signal2Count = signal2Count
    self._inputSignal1 = inputSignal1
    self._inputSignal2 = inputSignal2
    self._outputSignal = outputSignal
    
  def preFire(self):
    if (len(inputSignal1) >= self._signal1Count) and (len(inputSignal2) >= self._signal2Count):
      return True
    else:
      return False
    
  def fire(self):
    signal1Events = []
    for i in range(self._signal1Count):
      signal1Events.append(self._inputSignal1.pop(0))
    signal2Events = []
    for i in range(self._signal2Count):
      signal2Events.append(self._inputSignal2.pop(0))
    outputEvents = (signal1Events, signal2Events)
    self._outputSignal.append(outputEvents)
  
  def postFire(self):
    pass
    
class UnzipProcess(Process):
  def __init__(self, inputSignal, outputSignal1, outputSignal2):
    self._inputSignal = inputSignal
    self._outputSignal1 = outputSignal1
    self._outputSignal2 = outputSignal2
    
  def preFire(self):
    if len(inputSignal) >= 1:
      return True
    else:
      return False
    
  def fire(self):
    (signal1Events, signal2Events) = self._inputSignal.pop(0)
    self._outputSignal1.extend(signal1Events)
    self._outputSignal2.extend(signal2Events)
    
  def postFire(self):
    pass

class SourceProcess(Process):
  '''
  TODO: implement this - MealyProcess needs an input signal to
  function and has no way of modifying the input signal.
  '''
  def __init__(self, nextStateFunction, initialState, outputSignal):
    self._nextStateFunction = utilities.stringToFunction(nextStateFunction, "w")
    self._state = initialState
    self._outputSignal = outputSignal
    self._nextState = initialState
    
  def preFire(self):
    return True

  def fire(self):
    self._outputSignal.append(self._state)
    self._nextState = self._nextStateFunction(self._state)
    
  def postFire(self):
    self._state = self._nextState

class InitProcess(MealyProcess):
  def __init__(self, initialValue, inputSignal, outputSignal):
    partitionFunction = "return 1"
    outputFunction = "if w == True:\n\
  return [%s]\n\
else:\n\
  return [x[0]]" % str(initialValue)
    nextState = "return False"
    initialState = True
    MealyProcess.__init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)
    
# a little bit of sample code, so I don't forget what I meant for this to do:
if __name__ == "__main__":  
  def fireProcess(process):
    if process.preFire():
      process.fire()
      process.postFire()
    else:
      print "Precondition not met"
  
  print "Mealy"
  # Mealy process test
  partitionFunction = "return 3"
  outputFunction = "return [(x[0] + x[2] + w)]"
  nextStateFunction = "return x[1]"
  initialState = 0
  
  inputSignal = range(9)
  outputSignal = []
  
  process = MealyProcess(partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)
  fireProcess(process)
  fireProcess(process)
  fireProcess(process)
  
  print "InputSignal:", inputSignal
  print "OutputSignal:", outputSignal
  
  # Zip process test
  print "Zip"
  
  inputSignal1 = range(9)
  inputSignal2 = range(10,19)
  outputSignal = []
  process = ZipProcess(2, 4, inputSignal1, inputSignal2, outputSignal)
  fireProcess(process)
  fireProcess(process)
  
  print "InputSignal1:", inputSignal1
  print "InputSignal2:", inputSignal2
  print "OutputSignal:", outputSignal
  
  print "Unzip"
  inputSignal = outputSignal
  outputSignal1 = []
  outputSignal2 = []
  
  process = UnzipProcess(inputSignal, outputSignal1, outputSignal2)
  fireProcess(process)
  fireProcess(process)
  print "InputSignal:", inputSignal
  print "OutputSignal1:", outputSignal1
  print "OutputSignal2:", outputSignal2

  # Source process test
  print "Source"
  
  initialState = 1
  nextStateFunction = "return w + 1"
  outputSignal = []

  process = SourceProcess(nextStateFunction, initialState, outputSignal)
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

  process = InitProcess(initialValue, inputSignal, outputSignal)
  fireProcess(process)
  fireProcess(process)
  fireProcess(process)
  fireProcess(process)
  print "OutputSignal:", outputSignal
