#!/usr/bin/env python

import Processes

class MealyT(Processes.MealyProcess):
  def __init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal):
    Processes.MealyProcess.__init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)

class ZipT(Processes.ZipProcess):
  pass

class UnzipT(Process.UnzipProcess):
  pass
