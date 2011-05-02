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
    #inputPartitionSize = 1
    inputEvents = []
    singleEvent = self._inputSignal.pop(0)
    if(singleEvent!=None):
      for i in range(self._r):
        inputEvents.append(singleEvent)
		#print i
		
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

  outputFunction = "if x[0] == None:\n\
  return [(x[2] +w)]\n\
elif x[2] == None:\n\
  return [(x[0] + w)]\n\
else:\n\
  return [(x[0] + x[2] + w)]"  
  
  nextStateFunction = "if x[1] == None:\n\
  return 0\n\
else:\n\
  return x[1]"
  initialState = 0
  '''  Timed to Synchronous   '''
  in_timed = [0,1,None,3,4,5,6,7,8]
  out_timed = []
  
  timedProcess = TimedProcesses.MealyT(partitionFunction, outputFunction, nextStateFunction, initialState, in_timed, out_timed)

  in_interface = out_timed
  out_interface = []
  interface = StripT2S(1, in_interface,out_interface)
  
  outputFunction = "return [(x[0]+w)]"
  nextStateFunction = "return x[0]"
  in_synchronous = out_interface
  out_synchronous = []
  synchronousProcess = SynchronousProcesses.MealyS(outputFunction, nextStateFunction, initialState, in_synchronous, out_synchronous)  

  print "Timed to Synchronous"
  for i in range(0,3):
    print "After step",i,":"
    print "InputSignal:", in_timed
      
    fireProcess(timedProcess)
    print in_interface
    fireProcess(interface)
    print out_interface
	
    fireProcess(synchronousProcess)
    print "OutputSignal:", out_synchronous
  
  ''' Timed to Untimed '''
  in_timed = [0,1,None,3,4,5,6,7,8]
  out_timed = []
  partitionFunction = "return 3"
  outputFunction = "if x[0] == None:\n\
  return [(x[2] +w)]\n\
elif x[2] == None:\n\
  return [(x[0] + w)]\n\
else:\n\
  return [(x[0] + x[2] + w)]"  
  initialState = 0
  nextStateFunction = "if x[1] == None:\n\
  return 0\n\
else:\n\
  return x[1]"
  
  timedProcess = TimedProcesses.MealyT(partitionFunction, outputFunction, nextStateFunction, initialState, in_timed, out_timed)

  in_interface = out_timed
  out_interface = []
  interface = StripT2U(in_interface,out_interface)
  
  outputFunction = "return [(x[0]+w)]"
  nextStateFunction = "return x[0]"
  partitionFunction = "return 1"
  in_untimed = out_interface
  out_untimed = []
  untimedProcess = UntimedProcesses.MealyU(partitionFunction, outputFunction, nextStateFunction, initialState, in_untimed, out_untimed)  

  print "Timed to Untimed"
  for i in range(0,3):
    print "After step",i,":"
    print "InputSignal:", in_timed
      
    fireProcess(timedProcess)
    print in_interface
    fireProcess(interface)
    print out_interface
    fireProcess(untimedProcess)
    print "OutputSignal:", out_untimed

  ''' Untimed to Timed '''
  in_untimed = [0,1,None,3,4,5,6,7,8]
  out_untimed = []
  partitionFunction = "return 3"
  outputFunction = "if x[0] == None:\n\
  return [(x[2] +w)]\n\
elif x[2] == None:\n\
  return [(x[0] + w)]\n\
else:\n\
  return [(x[0] + x[2] + w)]"  
  nextStateFunction = "if x[1] == None:\n\
  return 0\n\
else:\n\
  return x[1]"
  initialState = 0
  
  untimedProcess = UntimedProcesses.MealyU(partitionFunction, outputFunction, nextStateFunction, initialState, in_untimed, out_untimed)

  in_interface = out_untimed
  out_interface = []
  interface = InsertU2T(1,in_interface,out_interface)
  
  outputFunction = "return [(x[0]+w)]"
  nextStateFunction = "return x[0]"
  partitionFunction = "return 1"
  in_timed = out_interface
  out_timed = []
  timedProcess = TimedProcesses.MealyT(partitionFunction, outputFunction, nextStateFunction, initialState, in_timed, out_timed)  

  print "Untimed to Timed"
  for i in range(0,3):
    print "After step",i,":"
    print "InputSignal:", in_untimed
      
    fireProcess(untimedProcess)
    print in_interface
    fireProcess(interface)
    print out_interface
    fireProcess(timedProcess)
    print "OutputSignal:", out_timed
  
  ''' Untimed to Synchronous '''
  in_untimed = [0,1,None,3,4,5,6,7,8]
  out_untimed = []
  partitionFunction = "return 3"
  outputFunction = "if x[0] == None:\n\
  return [(x[2] +w)]\n\
elif x[2] == None:\n\
  return [(x[0] + w)]\n\
else:\n\
  return [(x[0] + x[2] + w)]"  
  nextStateFunction = "if x[1] == None:\n\
  return 0\n\
else:\n\
  return x[1]"
  initialState = 0
  
  untimedProcess = UntimedProcesses.MealyU(partitionFunction, outputFunction, nextStateFunction, initialState, in_untimed, out_untimed)

  in_interface = out_untimed
  out_interface = []
  interface = InsertU2S(1,in_interface,out_interface)
  
  outputFunction = "return [(x[0]+w)]"
  nextStateFunction = "return x[0]"
  initialState = 0
  in_synchronous = out_interface
  out_synchronous = []
  synchronousProcess = SynchronousProcesses.MealyS(outputFunction, nextStateFunction, initialState, in_synchronous, out_synchronous)  
  
  print "Untimed to Synchronous"
  for i in range(0,3):
    print "After step",i,":"
    print "InputSignal:", in_untimed
      
    fireProcess(untimedProcess)
    print in_interface
    fireProcess(interface)
    print out_interface
    fireProcess(synchronousProcess)
    print "OutputSignal:", out_synchronous
	
  ''' Synchronous to Untimed '''
  in_synchronous = [0,None,2,3,4,5,6,7,8]
  out_synchronous= []
  outputFunction = "if x[0] == None:\n\
  return [(w)]\n\
else:\n\
  return [(x[0] + w)]"  
  nextStateFunction = "if x[0] == None:\n\
  return 0\n\
else:\n\
  return x[0]"
  initialState = 0
  
  synchronousProcess = SynchronousProcesses.MealyS(outputFunction, nextStateFunction, initialState, in_synchronous, out_synchronous)

  in_interface = out_synchronous
  out_interface = []
  interface = StripS2U(in_interface,out_interface)
  
  outputFunction = "return [(x[0]+w)]"
  nextStateFunction = "return x[0]"
  partitionFunction = "return 1"
  initialState = 0
  in_untimed = out_interface
  out_untimed = []
  untimedProcess = UntimedProcesses.MealyU(partitionFunction, outputFunction, nextStateFunction, initialState, in_untimed, out_untimed)  
  
  print "Synchronous to Untimed"
  for i in range(0,3):
    print "After step",i,":"
    print "InputSignal:", in_synchronous
      
    fireProcess(synchronousProcess)
    print in_interface
    fireProcess(interface)
    print out_interface
    fireProcess(untimedProcess)
    print "OutputSignal:", out_untimed
	
	
  ''' Synchronous to Timed '''
  in_synchronous = [0,None,2,3,4,5,6,7,8]
  out_synchronous= []
  outputFunction = "if x[0] == None:\n\
  return [(w)]\n\
else:\n\
  return [(x[0] + w)]"  
  nextStateFunction = "if x[0] == None:\n\
  return 0\n\
else:\n\
  return x[0]"
  initialState = 0
  
  synchronousProcess = SynchronousProcesses.MealyS(outputFunction, nextStateFunction, initialState, in_synchronous, out_synchronous)

  in_interface = out_synchronous
  out_interface = []
  interface = InsertS2T(1,in_interface, out_interface)
  
  outputFunction = "return [(x[0]+w)]"
  nextStateFunction = "return x[0]"
  partitionFunction = "return 1"
  in_timed = out_interface
  out_timed = []
  timedProcess = TimedProcesses.MealyT(partitionFunction, outputFunction, nextStateFunction, initialState, in_timed, out_timed)    
  
  print "Synchronous to Timed"
  for i in range(0,3):
    print "After step",i,":"
    print "InputSignal:", in_synchronous
      
    fireProcess(synchronousProcess)
    print in_interface
    fireProcess(interface)
    print out_interface
    fireProcess(timedProcess)
    print "OutputSignal:", out_timed
	
  
# a little bit of sample code, so I don't forget what I meant for this to do:
if __name__ == "__main__":  
  main()

