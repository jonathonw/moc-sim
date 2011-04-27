#!/usr/bin/env python

import Processses
import UntimedProcesses
import TimedProcesses
	
class Interface(Processes.MealyProcess):

  '''def __init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal):
    Processes.MealyProcess.__init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)'''
	pass
	
class intSup(UntimedProcesses.MapU):  
	''' 
	Uprate process for interfaces between two domains of the same MoC
	intSup(r,f) = mapU(1,f) 
	'''
  def __init__(self, partitionConstant, outputFunction, inputSignal, outputSignal):
    UntimedProcesses.MapU.__init__(self, "return 1", outputFunction, inputSignal, outputSignal)

class intSdown(UntimedProcesses.MapU):  
	''' 
	Downrate process for interfaces between two domains of the same MoC
	intSup(r,f) = mapU(r,f) 
	'''
  pass

class intTup(UntimedProcesses.MapU):
	''' 
	Uprate process for interfaces between two domains of the same MoC
	intSup(r,f) = mapU(1,f) 
	'''
  def __init__(self, partitionConstant, outputFunction, inputSignal, outputSignal):
    UntimedProcesses.MapU.__init__(self, "return 1", outputFunction, inputSignal, outputSignal)
	
class intTdown(UntimedProcesses.MapU):
	''' 
	Downrate process for interfaces between two domains of the same MoC
	intSup(r,f) = mapU(r,f) 
	'''
  pass

 # connects two MoC domains in the case that they are not a simple multiple of each other
#class intSups(UntimedProcesses.MealyU):
  #def __init__(self, partitionConstant, outputFunction, inputSignal, outputSignal):
  
  
  
  
  
  
  
  

class StripS2U(Processes.MealyProcess):
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
      if(singleEvent>0):
		inputEvents.append(singleEvent))
    outputEvents = self._outputFunction(self._state, inputEvents)
    self._nextState = self._nextStateFunction(self._state, inputEvents)
    self._outputSignal.extend(outputEvents)
	
  def postFire(self):
    self._state = self._nextState

class StripT2S(MealyT):
  # still need to figure out
    
		
# removes the time information from a timed process
class StripT2U(MealyT):

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
      if(singleEvent>0):
		inputEvents.append(singleEvent))
    outputEvents = self._outputFunction(self._state, inputEvents)
    self._nextState = self._nextStateFunction(self._state, inputEvents)
    self._outputSignal.extend(outputEvents)
	
  def postFire(self):
    self._state = self._nextState
'''  
class InsertS2T
	#def __init__():
	def runOneStep(self):
		MealyT.runOneStep(self)
		
class InsertU2T
	#def __init__():
	def runOneStep(self):
		MealyT.runOneStep(self)
		
class InsertU2S
	#def __init__():
	def runOneStep(self):
		MealyS.runOneStep(self)'''
