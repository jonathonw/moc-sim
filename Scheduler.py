#!/usr/bin/env python

import utilities
from Processes import Process

class CausalityException(Exception):
  pass

class Scheduler:
  '''
  Scheduler for processes.  Processes is the list of processes, inputSignals is a
  list of input signals from the CSV file (so, a list of lists), and outputSignals
  is a list of output signals that aren't connected to another process (so, our
  final output).
  '''
  def __init__(self, processes, inputSignals, outputSignals):
    self._processes = processes
    self._inputSignals = inputSignals
    self._outputSignals = outputSignals
  
  def runModel(self):
    pass
  
  def runOneStep(self):
    unrunProcesses = self._processes[:]
    previousCount = 0
    while len(unrunProcesses) > 0:
      previousCount = len(unrunProcesses)
      for process in unrunProcesses:
        if process.preFire():
          process.fire
          unrunProcesses.remove(process)
      if previousCount == len(unrunProcesses):
        print "Can't reconcile process loop"
        raise CausalityException("Infinite loop")
        
    for process in self._processes:
      process.postFire()
      
