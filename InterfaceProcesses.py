#!/usr/bin/env python
import Processes
import UntimedProcesses
import TimedProcesses
import SynchronousProcesses
import utilities


## Synchronous to Untimed Interface Process
class StripS2U(Processes.Process):
  ## Instantiates a StripS2U process.  The output signal is basically just the
  #  first event of the input signal as long as it is not null.
  #
  #  @param inputSignal       The input signal to this process.
  #  @param outputSignal      The output signal from this process.
  def __init__(self, inputSignal, outputSignal):

    self._inputSignal = inputSignal
    self._outputSignal = outputSignal
	
  def preFire(self):
    inputPartitionSize = 1
    if len(self._inputSignal) >= inputPartitionSize:
      return True
    else:
      return False	
	
  def fire(self):    
    inputPartitionSize = 1
    inputEvents = []
    for i in range(inputPartitionSize):
      singleEvent = self._inputSignal.pop(0)
      if(singleEvent!=None):
        inputEvents.append(singleEvent)
    outputEvents = inputEvents
    self._outputSignal.extend(outputEvents)
	
  def postFire(self):
    pass
		

## Timed to Untimed Interface process
class StripT2U(Processes.Process):
  ## Instantiates a StripT2U process.  The output signal is basically just the
  #  first event of the input signal as long as it is not null.
  #
  #  @param inputSignal       The input signal to this process.
  #  @param outputSignal      The output signal from this process.
  def __init__(self, inputSignal, outputSignal):

    self._inputSignal = inputSignal
    self._outputSignal = outputSignal
	
  def preFire(self):
    inputPartitionSize = 1
    if len(self._inputSignal) >= inputPartitionSize:
      return True
    else:
      return False
  
  def fire(self):
    inputPartitionSize = 1
    inputEvents = []
    for i in range(inputPartitionSize):
      singleEvent = self._inputSignal.pop(0)
      if(singleEvent!=None):
        inputEvents.append(singleEvent)
    outputEvents = inputEvents
    self._outputSignal.extend(outputEvents)
	
  def postFire(self):
    pass
	

## Timed to Synchronous Interface Process
class StripT2S(Processes.Process):
  ## Instantiates a StripT2S process.  The output signal is basically the
  #  same as the input signal as long as the events are not null.
  #
  #  @param r                 The input partition.
  #  @param inputSignal       The input signal to this process.
  #  @param outputSignal      The output signal from this process.
  def __init__(self, r, inputSignal, outputSignal):

	self._r  = r
	self._inputSignal = inputSignal
	self._outputSignal = outputSignal
	
  def preFire(self):
    inputPartitionSize = self._r
    if len(self._inputSignal) >= inputPartitionSize:
      return True
    else:
      return False
	
  def fire(self):
    inputPartitionSize = self._r
    inputEvents = []
    for i in range(inputPartitionSize):
      singleEvent = self._inputSignal.pop(0)
      if(singleEvent!=None):
        inputEvents.append(singleEvent)
      elif(singleEvent==None):
        if i==0:
          inputEvents[0]=None
          break
    outputEvents = inputEvents
    self._outputSignal.extend(outputEvents)
 
  def postFire(self):
    pass
  
## Synchronous to Timed Interface Process
class InsertS2T(Processes.Process):
  ## Instantiates an InsertS2T process.  The output signal is
  #  an r number of events of the first event of the input
  #  signal.
  #
  #  @param r                 The input partition.
  #  @param inputSignal       The input signal to this process.
  #  @param outputSignal      The output signal from this process.
  def __init__(self, r, inputSignal, outputSignal):

	self._r = r
	self._inputSignal = inputSignal
	self._outputSignal = outputSignal

  def preFire(self):
    inputPartitionSize = 1
    if len(self._inputSignal) >= inputPartitionSize:
      return True
    else:
      return False
	
  def fire(self):
    inputPartitionSize = 1
    inputEvents = []
    singleEvent = self._inputSignal.pop(0)
    if(singleEvent!=None):
      for i in range(self._r):
        inputEvents.append(singleEvent)
    outputEvents = inputEvents
    self._outputSignal.extend(outputEvents)
 
  def postFire(self):
    pass

## Untimed to Timed Interface Process
class InsertU2T(Processes.Process):
  ## Instantiates an InsertU2T process.  The output signal is
  #  an r number of events of the first event of the input
  #  signal.
  #
  #  @param r                 The input partition.
  #  @param inputSignal       The input signal to this process.
  #  @param outputSignal      The output signal from this process.
  def __init__(self, r, inputSignal, outputSignal):
    self._r = r
    self._inputSignal = inputSignal
    self._outputSignal = outputSignal

  def preFire(self):
    inputPartitionSize = 1
    if len(self._inputSignal) >= inputPartitionSize:
      return True
    else:
      return False
	
  def fire(self):
    inputEvents = []
    singleEvent = self._inputSignal.pop(0)
    if(singleEvent!=None):
      for i in range(self._r):
        inputEvents.append(singleEvent)
    outputEvents = inputEvents
    self._outputSignal.extend(outputEvents)
 
  def postFire(self):
    pass
		
## Untimed to Synchronous Interface Process
class InsertU2S(Processes.Process):
  ## Instantiates an InsertU2S process.  The output signal is
  #  an r number of events of the first event of the input
  #  signal.
  #
  #  @param r                 The input partition.
  #  @param inputSignal       The input signal to this process.
  #  @param outputSignal      The output signal from this process.
  def __init__(self, r, inputSignal, outputSignal):
    self._r = r
    self._inputSignal = inputSignal
    self._outputSignal = outputSignal
	
  def preFire(self):
    inputPartitionSize = 1
    if len(self._inputSignal) >= inputPartitionSize:
      return True
    else:
      return False
	
  def fire(self):
    inputEvents = []
    singleEvent = self._inputSignal.pop(0)
    if(singleEvent!=None):
      for i in range(self._r):
        inputEvents.append(singleEvent)
    outputEvents = inputEvents
    self._outputSignal.extend(outputEvents)

  def postFire(self):
    pass

def fireProcess(process):
  if process.preFire():
    process.fire()
    process.postFire()
  else:
    print "Precondition not met" 
		
def main():
  print "MealyT"
  partitionFunction = "return 3"
  #outputFunction = "return [(x[0] + x[2] + w)]"
  outputFunction = "if x[0] == None:\n\
  return [(x[2] +w)]\n\
elif x[2] == None:\n\
  return [(x[0] + w)]\n\
else:\n\
  return [(x[0] + x[2] + w)]"  
  
  '''if x[0]+x[1]+x[2]+x[3]+x[4] > 500:\n\
  return w-1\n\
elif x[0]+x[1]+x[2]+x[3]+x[4] < 400:\n\
  return w+1\n\
else:\n\
  return w"'''
  nextStateFunction = "return x[1]"
  initialState = 0
  
  in_synchronous = [0,1,None,3,4,5,6,7,8]
  out_synchronous = []
  
  synchronousProcess = TimedProcesses.MealyT(partitionFunction, outputFunction, nextStateFunction, initialState, in_synchronous, out_synchronous)

  outputFunction = "return [(x[0]+w)]"
  nextStateFunction = "return x[0]"
  in_interface = out_synchronous
  out_interface = []
  interface = InsertS2T(1, in_interface,out_interface)#outputFunction, nextStateFunction, initialState, in_interface,out_interface)
  
  outputFunction = "return [(x[0]+w)]"
  nextStateFunction = "return x[0]"
  in_timed = out_interface
  out_timed = []
  timedProcess = SynchronousProcesses.MealyS(outputFunction, nextStateFunction, initialState, in_timed, out_timed)  

  for i in range(0,3):
    print "After step",i,":"
    print "InputSignal:", in_synchronous
      
    #fireProcess(timedProcess)
    fireProcess(synchronousProcess)
    print in_interface
    fireProcess(interface)
    print out_interface
	
    #fireProcess(synchronousProcess)
    fireProcess(timedProcess)
    print "OutputSignal:", out_timed
  
  
  
# a little bit of sample code, so I don't forget what I meant for this to do:
if __name__ == "__main__":  
  main()

