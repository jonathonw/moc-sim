#!/usr/bin/env python

import Processses
import UntimedProcesses
import TimedProcesses
	
class Interface(Processes.MealyProcess):
	  ''' Interface process - same as generic Mealy '''
  def __init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal):
    Processes.MealyProcess.__init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)

  def runOneStep(self):
    Processes.MealyProcess.runOneStep(self)

	
class intSup(Interface):  
	''' 
	Uprate process for interfaces between two domains of the same MoC
	intSup(r,f) = mapU(1,f) 
	'''
  def __init__(self, partitionConstant, outputFunction, inputSignal, outputSignal):

    MealyU.__init__(self, "return %d", outputFunction, "return 0", 0, inputSignal, outputSignal)

  def runOneStep(self):
    ''' same as generic Mealy's runOneStep '''
    Interface.runOneStep(self)


class intSdown(Interface):  
	''' 
	Downrate process for interfaces between two domains of the same MoC
	intSup(r,f) = mapU(r,f) 
	'''
  def __init__(self, partitionConstant, outputFunction, inputSignal, outputSignal):

    MealyU.__init__(self, "return %d" % partitionConstant, outputFunction, "return 0", 0, inputSignal, outputSignal)

  def runOneStep(self):
    ''' same as generic Mealy's runOneStep '''
    Interface.runOneStep(self)
	
class StripU2T(MealyU):
	#def __init__():
	def runOneStep(self):
		MealyT.runOneStep(self)

class StripT2S(MealyT):
	#def __init__():
	def runOneStep(self):
		MealyS.runOneStep(self)
		
class StripT2U(MealyT):
	#def __init__():
	def runOneStep(self):
		MealyU.runOneStep(self)
		
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
		MealyS.runOneStep(self)
