#!/usr/bin/env python

import utilities
import UntimedProcesses
import Processes
from Processes import Process

## An exception thrown when the model is not executable.  Thrown either because 
#  there's not enough input or because there's an unresolvable feedback loop).
class CausalityException(Exception):
  pass

## The process scheduler; decides when processes should be activated.
class Scheduler:
  '''
  Scheduler for processes.  Processes is the list of processes, inputSignals is a
  list of input signals from the CSV file (so, a list of lists), and outputSignals
  is a list of output signals that aren't connected to another process (so, our
  final output).
  '''
  ## Instantiates a Scheduler object.
  #
  #  @param processes The list of processes.
  #  @param inputSignals  A dictionary of input signals (name: signal)
  #                       read from the XML input file.
  #  @param outputSignals A dictionary of output signals (name: signal) read
  #                       from the XML input file.
  def __init__(self, processes, inputSignals, outputSignals):
    self._processes = processes
    self._inputSignals = inputSignals
    self._outputSignals = outputSignals
  
  ## Runs the model.  Runs until either an input signal runs out of input, or
  #  until there are no runnable processes in the system.
  def runModel(self):
    noInput = False
    try:
      while True:
        for (key, signal) in self._inputSignals.items():
          if len(signal) == 0:
            noInput = True
            break
        if not noInput:
          self.runOneStep()
        else:
          print "Out of input."
          return self._outputSignals
    except CausalityException:
      print "Ran out of runnable processes (infinite loop or input wasn't equally dividable into partitions?)"
      return self._outputSignals
      
  ## Runs one step of the simulation.  Determines which processes have input
  #  available, runs them, and loops until all processes have been run.
  def runOneStep(self):
    print "Running one step of simulation"
    unrunProcesses = self._processes[:]
    previousCount = 0
    
    while len(unrunProcesses) > 0:
      #print "Number of unrun processes:", len(unrunProcesses)
      previousCount = len(unrunProcesses)
      for process in unrunProcesses:
        #print "Trying to run a process", process.__class__.__name__
        if process.preFire():
          #print "Process was able to run", process.__class__.__name__
          process.fire()
          unrunProcesses.remove(process)
      if previousCount == len(unrunProcesses):
        #print "Cant reconcile process loop"
        raise CausalityException("Infinite loop")
        
    for process in self._processes:
      process.postFire()
      
  ## Outputs the results (output signals) of the simulation.
  def outputResults(self):
    print ""
    print "--Output-------"
    for (name, signal) in self._outputSignals.items():
      print str(name) + ":",
      for event in signal:
        print str(event),
      print ""

def main():
  # amplifier example p122
  sIn = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
  s1 = []
  s2 = []
  s3 = []
  s3Split1 = []
  s3SplitOut = []
  sOut = []  
  sOut1 = []
  sOut2 = []
  
  inputs = {"sIn": sIn}
  outputs = {"sOut2": sOut2, "s3SplitOut": s3SplitOut}
  
  signal1Count = 1
  signal2Count = 5
  inputSignal1 = s3Split1
  inputSignal2 = sIn
  outputSignal = s1
  A1 = UntimedProcesses.ZipU(signal1Count, signal2Count, inputSignal1, inputSignal2, outputSignal)
  
  partitionConstant = 1
  outputFunction = "return [x[0][0][0]*x[0][1][0],x[0][0][0]*x[0][1][1],x[0][0][0]*x[0][1][2],x[0][0][0]*x[0][1][3],x[0][0][0]*x[0][1][4]]"
  inputSignal = s1
  outputSignal = sOut
  A2 = UntimedProcesses.MapU(partitionConstant, outputFunction, inputSignal, outputSignal)
  
  partitionFunction = "return 5"
  nextStateFunction = "if x[0]+x[1]+x[2]+x[3]+x[4] > 500:\n\
  return w-1\n\
elif x[0]+x[1]+x[2]+x[3]+x[4] < 400:\n\
  return w+1\n\
else:\n\
  return w"
  initialState = 10
  inputSignal = sOut1
  outputSignal = s2
  A3 = UntimedProcesses.ScanU(partitionFunction, nextStateFunction, initialState, inputSignal, outputSignal)
  
  SplitterProcess = Processes.Splitter(sOut, sOut1, sOut2)
  S3Splitter = Processes.Splitter(s3, s3Split1, s3SplitOut)
  
  initialValue = 10
  inputSignal = s2
  outputSignal = s3
  A4 = UntimedProcesses.InitU(initialValue, inputSignal, outputSignal)
  
  processList = [A1,A2,A3,A4, SplitterProcess, S3Splitter]
  
  scheduler = Scheduler(processList, inputs, outputs)
  
  scheduler.runModel()
  scheduler.outputResults()

# sample code
if __name__ == "__main__":  
  main()
