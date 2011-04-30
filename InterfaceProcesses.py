#!/usr/bin/env python
import Processes
import UntimedProcesses
import TimedProcesses
import SynchronousProcesses
import utilities
	
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
  #timedProcess = Processes.TimedProcesses
  #untimedProcess = Process.UntimedProcesses
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
  
  inputSignal = [0,1,2,3,4,5,6,7,8]
  outputSignal = []
  
  timedProcess = TimedProcesses.MealyT(partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)
  print "InputSignal:", inputSignal
  fireProcess(timedProcess)
  fireProcess(timedProcess)
  fireProcess(timedProcess)

  print "OutputSignal:", outputSignal
  
  #untimedProcess = UntimedProcesses.MealyU(partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)
  synchronousProcess = SynchronousProcesses.MealyS(outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)
  
  inputSignal = outputSignal
  outputSignal = []
  interface = StripT2S(partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)
  
  
  print "InputSignal:", inputSignal
  fireProcess(interface)
  print "OutputSignal:", outputSignal
  
  
  
  
  #print "InputSignal:", inputSignal
  #fireProcess(untimedProcess)
  #fireProcess(untimedProcess)
  #fireProcess(untimedProcess)
  #print "OutputSignal:", outputSignal
  
  
  
  
  
  
# a little bit of sample code, so I don't forget what I meant for this to do:
if __name__ == "__main__":  
  main()

