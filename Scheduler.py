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
