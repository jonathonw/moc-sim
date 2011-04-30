#!/usr/bin/env python
import Processes
import UntimedProcesses
import TimedProcesses
import SynchronousProcesses
import utilities
	
class Interface(Processes.MealyProcess):

  '''def __init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal):
    Processes.MealyProcess.__init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)'''
  pass
	
class intSup(Processes.Process):#UntimedProcesses.MapU):  

  def __init__(self, partitionConstant, outputFunction, inputSignal, outputSignal):
    UntimedProcesses.MapU("return 1", outputFunction, inputSignal, outputSignal)
	
  #def preFire(self):
  
  #def fire(self):
  
  #def postFire(self):
  

class intSdown(Processes.Process):#UntimedProcesses.MapU):  

  def __init__(self, partitionConstant, outputFunction, inputSignal, outputSignal):
    UntimedProcesses.MapU(partitionConstant, outputFunction, inputSignal, outputSignal)

class intTup(Processes.Process):#UntimedProcesses.MapU):

  def __init__(self, partitionConstant, outputFunction, inputSignal, outputSignal):
    UntimedProcesses.MapU("return 1", outputFunction, inputSignal, outputSignal)
	
  #def preFire(self):
    
  #def fire(self):
  
  #def postFire(self):
	
class intTdown(UntimedProcesses.MapU):

  def __init__(self, partitionConstant, outputFunction, inputSignal, outputSignal):
    UntimedProcesses.MapU(partitionConstant, outputFunction, inputSignal, outputSignal)

 # connects two MoC domains in the case that they are not a simple multiple of each other
#class intSups(UntimedProcesses.MealyU):
  #def __init__(self, partitionConstant, outputFunction, inputSignal, outputSignal):
  
  
  
  
  
  
  
  

class StripS2U(Processes.Process):
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
    '''
    Removes the time events
    '''
    
    inputPartitionSize = self._partitionFunction(self._state)
    inputEvents = []
    for i in range(inputPartitionSize):
      singleEvent = self._inputSignal.pop(0)
      if(singleEvent!=None):
        inputEvents.append(singleEvent)
    outputEvents = self._outputFunction(self._state, inputEvents)
    self._nextState = self._nextStateFunction(self._state, inputEvents)
    self._outputSignal.extend(outputEvents)
	
  def postFire(self):
    self._state = self._nextState
		
# removes the time information from a timed process
class StripT2U(Processes.Process):

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
    '''
    Removes the time events
    '''
    
    inputPartitionSize = self._partitionFunction(self._state)
    inputEvents = []
    for i in range(inputPartitionSize):
      singleEvent = self._inputSignal.pop(0)
      if(singleEvent!=None):
        inputEvents.append(singleEvent)
    outputEvents = self._outputFunction(self._state, inputEvents)
    self._nextState = self._nextStateFunction(self._state, inputEvents)
    self._outputSignal.extend(outputEvents)
	
  def postFire(self):
    self._state = self._nextState
	
class StripT2S(Processes.Process):#MealyT):
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
    '''
    Removes the time events
    '''
    
    inputPartitionSize = self._partitionFunction(self._state)
    inputEvents = []
    for i in range(inputPartitionSize):
      singleEvent = self._inputSignal.pop(0)
      if(singleEvent!=None):
        inputEvents.append(singleEvent)
      elif(singleEvent==None):
        if i==0:
          inputEvents[0]=None
          break
    outputEvents = self._outputFunction(self._state, inputEvents)
    self._nextState = self._nextStateFunction(self._state, inputEvents)
    self._outputSignal.extend(outputEvents)
 
  def postFire(self):
    self._state = self._nextState
  

class InsertS2T(Processes.Process):
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
    '''
    Adds the time events
    '''
    r = 2 #r is the positive constant that represents the number of output events to inject per event in the input
    inputPartitionSize = self._partitionFunction(self._state)
    inputEvents = []
    for i in range(inputPartitionSize-1):
      singleEvent = self._inputSignal.pop(0)
      if(singleEvent!=None):
        for i in range(r):
          inputEvents.append(singleEvent)
    outputEvents = self._outputFunction(self._state, inputEvents)
    self._nextState = self._nextStateFunction(self._state, inputEvents)
    self._outputSignal.extend(outputEvents)
 
  def postFire(self):
    self._state = self._nextState
		
class InsertU2T(Processes.Process):
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
    '''
    Adds the time events
    '''
    r = 2 #r is the positive constant that represents the number of output events to inject per event in the input
    inputPartitionSize = self._partitionFunction(self._state)
    inputEvents = []
    for i in range(inputPartitionSize-1):
      singleEvent = self._inputSignal.pop(0)
      if(singleEvent!=None):
        for i in range(r):
          inputEvents.append(singleEvent)
    outputEvents = self._outputFunction(self._state, inputEvents)
    self._nextState = self._nextStateFunction(self._state, inputEvents)
    self._outputSignal.extend(outputEvents)
 
  def postFire(self):
    self._state = self._nextState
		
class InsertU2S(Processes.Process):
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
    '''
    Adds the time events
    '''
    r = 2 #r is the positive constant that represents the number of output events to inject per event in the input
    inputPartitionSize = self._partitionFunction(self._state)
    inputEvents = []
    for i in range(inputPartitionSize-1):
      singleEvent = self._inputSignal.pop(0)
      if(singleEvent!=None):
        for i in range(r):
          inputEvents.append(singleEvent)
    outputEvents = self._outputFunction(self._state, inputEvents)
    self._nextState = self._nextStateFunction(self._state, inputEvents)
    self._outputSignal.extend(outputEvents)
 
  def postFire(self):
    self._state = self._nextState
 
def fireProcess(process):
  if process.preFire():
    process.fire()
    process.postFire()
  else:
    print "Precondition not met" 
		
def main():
  print "MealyT"
  partitionFunction = "return 3"
  outputFunction = "return [(x[0] + x[2] + w)]"
  '''outputFunction = "if x[0]+x[1]+x[2]+x[3]+x[4] > 500:\n\
  return w-1\n\
elif x[0]+x[1]+x[2]+x[3]+x[4] < 400:\n\
  return w+1\n\
else:\n\
  return w"'''
  nextStateFunction = "return x[1]"
  initialState = 0
  
  in_timed = [0,1,2,3,4,5,6,7,8]
  out_timed = []
  
  timedProcess = TimedProcesses.MealyT(partitionFunction, outputFunction, nextStateFunction, initialState, in_timed, out_timed)

  in_interface = out_timed
  out_interface = []
  interface = StripT2S("return 3", outputFunction, nextStateFunction, initialState, in_interface,out_interface)
  
  outputFunction = "return [(x[0]+w)]"
  nextStateFunction = "return x[0]"
  in_synchronous = out_interface
  out_synchronous = []
  synchronousProcess = SynchronousProcesses.MealyS(outputFunction, nextStateFunction, initialState, in_synchronous, out_synchronous)  

  print "InputSignal:", in_timed
    
  fireProcess(timedProcess)
  fireProcess(timedProcess)
  fireProcess(timedProcess)
  fireProcess(interface)
  fireProcess(synchronousProcess)

  print "OutputSignal:", out_synchronous
  
  
  
# a little bit of sample code, so I don't forget what I meant for this to do:
if __name__ == "__main__":  
  main()

