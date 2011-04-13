#!/usr/bin/env python

from Processes import Process

class ProcessContainer:
  '''
  XML parser (or model checker) will create a bunch of these, connect them in a
  directed graph corresponding to their dependencies (if a process's output is
  connected to another process's input, its ProcessContainer should be in this
  process's children), and pass that to the scheduler.
  '''
  def __init__(self, process, childrenList):
    self._process = process
    self._childrenList = childrenList
    
  def getProcess(self):
    return self._process
    
  def getChildren(self):
    return self._childrenList
    
class Scheduler:
  '''
  Scheduler for processes.  By the time the process graph reaches here, we
  should have a directed acyclic graph of processes (feedback loops should
  already be resolved).  Head is an empty ProcessContainer (process assigned to
  None), whose children are the processes which only take input from our input
  CSV file.
  '''
  def __init__(self, head):
    pass
  
  def runModel(self):
    pass
