#!/usr/bin/env python
import utilities

class MealyProcess:
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
    
  def runOneStep(self):
    '''
    Runs this Mealy process for one step.
    
    TODO:  figure out how the process gets its input and output.
    '''
    
    inputPartitionSize = self._partitionFunction(self._state)
    inputEvents = []
    for i in range(inputPartitionSize):
      inputEvents.append(self._inputSignal.pop(0))
    outputEvents = self._outputFunction(self._state, inputEvents)
    self._state = self._nextStateFunction(self._state, inputEvents)
    self._outputSignal.append(outputEvents)
    
class ZipProcess:
  def __init__(self, signal1Count, signal2Count, inputSignal1, inputSignal2, outputSignal):
    self._signal1Count = signal1Count
    self._signal2Count = signal2Count
    self._inputSignal1 = inputSignal1
    self._inputSignal2 = inputSignal2
    self._outputSignal = outputSignal
    
  def runOneStep(self):
    signal1Events = []
    for i in range(self._signal1Count):
      signal1Events.append(self._inputSignal1.pop(0))
    signal2Events = []
    for i in range(self._signal2Count):
      signal2Events.append(self._inputSignal2.pop(0))
    outputEvents = (signal1Events, signal2Events)
    self._outputSignal.append(outputEvents)
    
# a little bit of sample code, so I don't forget what I meant for this to do:
if __name__ == "__main__":
  
  print "Mealy"
  # Mealy process test
  partitionFunction = "return 3"
  outputFunction = "return [(x[0] + x[2] + w)]"
  nextStateFunction = "return x[1]"
  initialState = 0
  
  inputSignal = range(9)
  outputSignal = []
  
  process = MealyProcess(partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)
  process.runOneStep()
  process.runOneStep()
  process.runOneStep()
  
  print "InputSignal:", inputSignal
  print "OutputSignal:", outputSignal
  
  # Zip process test
  print "Zip"
  
  inputSignal1 = range(9)
  inputSignal2 = range(10,19)
  outputSignal = []
  process = ZipProcess(2, 4, inputSignal1, inputSignal2, outputSignal)
  process.runOneStep()
  process.runOneStep()
  
  print "InputSignal1:", inputSignal1
  print "InputSignal2:", inputSignal2
  print "OutputSignal:", outputSignal
