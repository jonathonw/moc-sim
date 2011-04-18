#!/usr/bin/env python

import utilities
from Processes import Process


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
    for p in self._processes:
      #need to catch an out of range exception (or something like that) to determine
      #when something doesn't have enough input
      p.runOneStep()
      
