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
    for i in range(inputPartitionSize)
      inputEvents.append(self._inputSignal.pop(0))
    outputEvents = self._outputFunction(self._state, inputEvents)
    self._state = self._nextStateFunction(self._state, inputEvents)
    self._outputSignal.append(self._outputEvents)
    
#a little bit of sample code, so I don't forget what I meant for this to do:
if __name__ == "__main__":
  partitionFunction = "return 3"
  outputFunction = "return [(x[0] + x[2] + w)]"
  nextStateFunction = "return x[1]"
  initialState = 0
  
  process = MealyProcess(partitionFunction, outputFunction, nextStateFunction, initialState)
  process.runOneStep()
  process.runOneStep()
  process.runOneStep()
