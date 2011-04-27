#!/usr/bin/env python

# Main entry point for the simulator...  this is what you run if you want to run
# the whole simulator (rather than our built-in test code).

import sys
import XMLParser
import Scheduler

def main():
  print "Models of computation simulator"
  if len(sys.argv) != 2:
    print "Usage:", sys.argv[0], "input-file"
    exit -1
  
  inputFile = sys.argv[1]
  print "Parsing input..."
  (input, output, processes) = XMLParser.parseXml(inputFile)
  scheduler = Scheduler.Scheduler(processes, input, output)
  scheduler.runModel()
  scheduler.outputResults()
  
    
if __name__ == "__main__":
  main()
