#!/usr/bin/env python
import utilities

class Process:
  ## Evaluates the partition function and decides if the input signal(s) have
  #  enough input for this process to run.
  #
  #  @return True if there is enough input; False if there is not.
  def preFire(self):
    return False
    
  ## Takes input, runs the output function, and puts the output in the output
  #  signals.  Should compute but does not \em update the next state.
  def fire(self):
    pass
  
  ## Updates the state of the process.  Typically, the state would be computed
  #  in the fire() method, then the state member variable would be updated in
  #  this method.
  def postFire(self):
    pass

## A generic Mealy process.
class MealyProcess(Process):
  ## Instantiates a Mealy state machine with a partition function, output
  #  function, next state function, and initial state.
  #
  #  Each function should be specified as a string containing Python code (which
  #  will be evaluated at runtime); parameters are w (the current state), and x 
  #  (the input).  x will be a list containing the input partition for this 
  #  execution of the process.
  #
  #  @param partitionFunction The partition function (lambda) for this process.
  #                           Should return a positive integer corresponding to
  #                           the number of elements in the partition.
  #  @param outputFunction    The output function (f) for this process.  Should
  #                           return the process's output (as a list).
  #  @param nextStateFunction The next state function (g) for this process.
  #                           Should return the next state (consistent with the
  #                           type used for the initial state).
  #  @param initialState      The initial state for the system.  Can be any
  #                           type, but should be consistent with the type
  #                           returned by nextStateFunction.
  #  @param inputSignal       The input signal to this process.
  #  @param outputSignal      The output signal from this process.
  def __init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal):
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
    inputPartitionSize = self._partitionFunction(self._state)
    inputEvents = []
    for i in range(inputPartitionSize):
      inputEvents.append(self._inputSignal.pop(0))
    outputEvents = self._outputFunction(self._state, inputEvents)
    self._nextState = self._nextStateFunction(self._state, inputEvents)
    self._outputSignal.extend(outputEvents)
    
  def postFire(self):
    self._state = self._nextState
    
## A generic Scan process.
class ScanProcess(Process):
  ## Instantiates a Scan process with a partition function, next state function,
  #  and initial state.
  #
  #  As with a Mealy process, each function should be specified as a string
  #  containing Python code to be evaluated at runtime.  Parameters to these
  #  functions are w (the current state), and x (the current input).  x will be
  #  a list containing the input partition for this execution of the process.
  #
  #  @param partitionFunction The partition function (lambda) for this process.
  #                           Should return a positive integer corresponding to
  #                           the number of elements in the parittion.
  #  @param nextStateFunction The next state function (g) for this process.
  #                           Should return the next state (consistent with the
  #                           type used for the initial state).
  #  @param initialState      The initial state for the system.  Can be any
  #                           type, but should be consistent with the type
  #                           returned by nextStateFunction.
  #  @param inputSignal       The input signal to this process.
  #  @param outputSignal      The output signal from this process.
  def __init__(self, partitionFunction, nextStateFunction, initialState, inputSignal, outputSignal):
    self._partitionFunction = utilities.stringToFunction(partitionFunction, "w")
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
    inputPartitionSize = self._partitionFunction(self._state)
    inputEvents = []
    for i in range(inputPartitionSize):
      inputEvents.append(self._inputSignal.pop(0))
    self._nextState = self._nextStateFunction(self._state, inputEvents)
    self._outputSignal.append(self._nextState)
    
  def postFire(self):
    self._state = self._nextState
    
## A generic Zip process (actually, equivalent to ZipUS from the text).
class ZipProcess(Process):
  ## Instantiates a zip process which takes in the specified number of events
  #  from each signal.  The output signal will be composed of pairs of lists
  #  of events, so if the inputs of this process were [1, 2, 3] and [4, 5, 6],
  #  and you took two from each, the result of the first execution would be 
  #  ([1,2], [4, 5]).
  #  
  #  @param signal1Count the number of events to take in from Signal 1 on each
  #                      execution of this process.
  #  @param signal2Count the number of events to take in from Signal 2 on each
  #                      execution of this process.
  #  @param inputSignal1 The first input signal to this process.
  #  @param inputSignal2 The second input signal to this process.
  #  @param outputSignal The output signal from this process                 
  def __init__(self, signal1Count, signal2Count, inputSignal1, inputSignal2, outputSignal):
    self._signal1Count = signal1Count
    self._signal2Count = signal2Count
    self._inputSignal1 = inputSignal1
    self._inputSignal2 = inputSignal2
    self._outputSignal = outputSignal
    
  def preFire(self):
    if (len(self._inputSignal1) >= self._signal1Count) and (len(self._inputSignal2) >= self._signal2Count):
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
    
## A generic Unzip process.
class UnzipProcess(Process):
  ## Instantiates an Unzip process.  The input signal should be composed of
  #  pairs of lists of events (like the output from ZipProcess).
  #
  #  @param inputSignal   The input signal to this process.
  #  @param outputSignal1 The first output signal from this process.
  #  @param outputSignal2 The second output signal from this process.
  def __init__(self, inputSignal, outputSignal1, outputSignal2):
    self._inputSignal = inputSignal
    self._outputSignal1 = outputSignal1
    self._outputSignal2 = outputSignal2
    
  def preFire(self):
    if len(self._inputSignal) >= 1:
      return True
    else:
      return False
    
  def fire(self):
    (signal1Events, signal2Events) = self._inputSignal.pop(0)
    self._outputSignal1.extend(signal1Events)
    self._outputSignal2.extend(signal2Events)
    
  def postFire(self):
    pass

## A generic Source process.
class SourceProcess(Process):
  ## Instantiates a Source process with the given next state function.  A Source
  #  process always outputs its current state.
  #
  #  @param nextStateFunction The next state function (g) for this process.
  #                           Should return the next state (consistent with the
  #                           type used for the initial state).
  #  @param intialState       The initial state for the system.  Can be any
  #                           type, but should be consistent with the type
  #                           returned by nextStateFunction.
  #  @param inputSignal       The input signal to this process.
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

## A generic Init process.
class InitProcess(MealyProcess):
  ## Instantiates an Init process with the given initial value.  Outputs
  #  initialValue on its first execution, outputs its input on all subsequent
  #  iterations.
  #
  #  @param initialValue The value to output on the first execution of this
  #                      process.
  #  @param inputSignal  The input signal to this process.
  #  @param outputSignal The output signal from this process.
  def __init__(self, initialValue, inputSignal, outputSignal):
    partitionFunction = "if w == False:\n\
  return 1\n\
else:\n\
  return 0"
    outputFunction = "if w == True:\n\
  return [%s]\n\
else:\n\
  return [x[0]]" % str(initialValue)
    nextState = "return False"
    initialState = True
    MealyProcess.__init__(self, partitionFunction, outputFunction, nextState, initialState, inputSignal, outputSignal)
    
## A signal splitting process.  Takes everything that comes in on one signal and
#  outputs it on two signals--  this lets you use the same signal as an output
#  signal and as input to another process.
class Splitter:
  ## Instantiates a splitter process.
  #  
  #  @param inputSignal   The input signal to this process.
  #  @param outputSignal1 The first output signal from this process.
  #  @param outputSignal2 The second output signal from this process.
  def __init__(self, inputSignal, outputSignal1, outputSignal2):
    self._inputSignal = inputSignal
    self._outputSignal1 = outputSignal1
    self._outputSignal2 = outputSignal2
    
  def preFire(self):
    if len(self._inputSignal) != 0:
      return True
    else:
      return False
      
  def fire(self):
    while len(self._inputSignal) > 0:
      stuff = self._inputSignal.pop(0)
      self._outputSignal1.append(stuff)
      self._outputSignal2.append(stuff)
      
  def postFire(self):
    pass
 
def fireProcess(process):
  if process.preFire():
    process.fire()
    process.postFire()
  else:
    print "Precondition not met" 
 
def main():
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
    
# a little bit of sample code, so I don't forget what I meant for this to do:
if __name__ == "__main__":  
  main()
  

