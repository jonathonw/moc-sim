#!/usr/bin/env python

import utilities
from Processes import Process


class Scheduler:
  '''
  Scheduler for processes.  By the time the process graph reaches here, we
  should have a directed acyclic graph of processes (feedback loops should
  already be resolved).  Processes is the list of processes (in any arbitrary
  order; it'll be sorted by us); processDependencies is a list of pairs
  expressing dependencies between processes (the output of the first process
  is connected to the input of the second process).
  '''
  def __init__(self, processes, processDependencies, inputSignals, outputSignals):
    self._processes = utilities.topological_sort(processes, processDependencies)
  
  def runModel(self):
    pass
  
  def runOneStep(self):
    for p in self._processes:
      #need to catch an out of range exception (or something like that) to determine
      #when something doesn't have enough input
      p.runOneStep()
      
