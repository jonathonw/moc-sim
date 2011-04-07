#!/usr/bin/env python

import Processes

class MealyT(Processes.MealyProcess):
  def __init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal):
    Processes.MealyProcess.__init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)

class MooreT(MealyT):
  def __init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal):
    MealyT.__init__(self, partitionFunction, outputFunction, nextStateFunction, initialState, inputSignal, outputSignal)
