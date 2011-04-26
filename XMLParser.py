import Processes
import UntimedProcesses
import TimedProcesses
import SynchronousProcesses
import utilities
import os
import csv
from xml.etree import ElementTree as ET

def search_signals(_sigs,_tst):
    '''
    Returns the index into _sigs if _tst is found
        -1 otherwise
    '''
    for _ind in range(0,len(_sigs)):
        if _sigs[_ind]==_tst:
            return _ind
    return -1

def convertType(s):
    for func in (int, float, eval):
        try:
            n = func(s)
            return n
        except:
            pass
    return s

def parseXml(filename):
  tree = ET.parse(filename)
  system = tree.getroot()
  for obj in system:
      for item in obj:
          for field in item:
              if field.tag!='StateFunc' and field.tag!='OutFunc' and field.tag!='PartFunc':
                  field.text = field.text.replace('\n','')    # remove all the extra newlines
                  field.text = field.text.replace('\t','')    # remove all the extra tabs
  '''
  The code below prints out the tree,
  use it for debugging
  '''
  #for obj in system:
  #    print obj.tag
  #    for item in obj:
  #      print '\t'+item.tag
  #      for field in item:
  #          print '\t\t'+field.tag
  #          print '\t\t\t'+field.text

  inputs = {}
  outputs = {}
  signals = {}
  proc_list = []      #list of processes (which will be sent to the scheduler
  
  for obj in system:
      if obj.tag=='inputs':
          for item in obj:
              signal = []
              inputs[obj.tag + '/' + item.tag] = signal
              temp = item.text
              temp = temp.replace('\n','')
              temp = temp.replace('\t','')
              data = temp.split(',')
              for val in data:
                  signal.append(float(val))
              #print signal
      elif obj.tag=='outputs':
          for item in obj:
              signal = []
              outputs[obj.tag + '/' + item.tag] = signal
      else:
          for item in obj:
              if item[0].text=='Splitter':
                  print item[0].text
                  if item[1].text in inputs:
                      in1 = inputs[item[1].text]
                  elif item[1].text in signals:
                      in1 = signals[item[1].text]
                  else:
                      in1 = []
                      signals[item[1].text] = in1
                  if item[2].text in outputs:
                      out1 = outputs[item[2].text]
                  elif item[2].text in signals:
                      out1 = signals[item[2].text]
                  else:
                      out1 = []
                      signals[item[2].text] = out1
                  if item[3].text in outputs:
                      out2 = outputs[item[3].text]
                  elif item[3].text in signals:
                      out2 = signals[item[3].text]
                  else:
                      out2 = []
                      signals[item[3].text] = out2
                  process = Processes.Splitter(in1,out1,out2)
                  proc_list.append(process)
              elif item[0].text=='Timed':
                  if item[1].text=='Zip':
                      print item[1].text
                      if item[4].text in inputs:
                          in1 = inputs[item[4].text]
                      elif item[4].text in signals:
                          in1 = signals[item[4].text]
                      else:
                          in1 = []
                          signals[item[4].text] = in1
                      if item[5].text in inputs:
                          in2 = inputs[item[5].text]
                      elif item[5].text in signals:
                          in2 = signals[item[5].text]
                      else:
                          in2 = []
                          signals[item[5].text] = in2
                      if item[6].text in outputs:
                          out = outputs[item[6].text]
                      elif item[6].text in signals:
                          out = signals[item[6].text]
                      else:
                          out = []
                          signals[item[6].text] = out
                      process = TimedProcesses.ZipT(eval(item[2].text),eval(item[3].text),in1,in2,out)
                      proc_list.append(process)
                  elif item[1].text=='UnZip':
                      print item[1].text
                      if item[2].text in inputs:
                          in1 = inputs[item[2].text]
                      elif item[2].text in signals:
                          in1 = signals[item[2].text]
                      else:
                          in1 = []
                          signals[item[2].text] = in1
                      if item[3].text in outputs:
                          out1 = outputs[item[3].text]
                      elif item[3].text in signals:
                          out1 = signals[item[3].text]
                      else:
                          out1 = []
                          signals[item[3].text] = out1
                      if item[4].text in outputs:
                          out2 = outputs[item[4].text]
                      elif item[4].text in signals:
                          out2 = signals[item[4].text]
                      else:
                          out2 = []
                          signals[item[4].text] = out2
                      process = TimedProcesses.UnzipT(in1,out1,out2)
                      proc_list.append(process)
                  elif item[1].text=='Mealy':
                      print item[1].text
                      if item[6].text in inputs:
                          in1 = inputs[item[6].text]
                      elif item[6].text in signals:
                          in1 = signals[item[6].text]
                      else:
                          in1 = []
                          signals[item[6].text] = in1
                      if item[7].text in outputs:
                          out1 = outputs[item[7].text]
                      elif item[7].text in signals:
                          out1 = signals[item[7].text]
                      else:
                          out1 = []
                          signals[item[7].text] = out1
                      process = TimedProcesses.MealyT(item[2].text,item[3].text,item[4].text,eval(item[5].text),in1,out1)
                      proc_list.append(process)
                  elif item[1].text=='Source':
                      print item[1].text
                      if item[4].text in outputs:
                          out1 = outputs[item[4].text]
                      elif item[4].text in signals:
                          out1 = signals[item[4].text]
                      else:
                          out1 = []
                          signals[item[4].text] = out1
                      process = TimedProcesses.SourceT(item[2].text,eval(item[3].text),out1)
                      proc_list.append(process)
                  elif item[1].text=='Init':
                      print item[1].text
                      if item[3].text in inputs:
                          in1 = inputs[item[3].text]
                      elif item[3].text in signals:
                          in1 = signals[item[3].text]
                      else:
                          in1 = []
                          signals[item[3].text] = in1
                      if item[4].text in outputs:
                          out1 = outputs[item[4].text]
                      elif item[4].text in signals:
                          out1 = signals[item[4].text]
                      else:
                          out1 = []
                          signals[item[4].text] = out1
                      process = TimedProcesses.InitT(eval(item[2].text),in1,out1)
                      proc_list.append(process)
              elif item[0].text=='Untimed':
                  if item[1].text=='Zip':
                      print item[1].text
                      if item[4].text in inputs:
                          in1 = inputs[item[4].text]
                      elif item[4].text in signals:
                          in1 = signals[item[4].text]
                      else:
                          in1 = []
                          signals[item[4].text] = in1
                      if item[5].text in inputs:
                          in2 = inputs[item[5].text]
                      elif item[5].text in signals:
                          in2 = signals[item[5].text]
                      else:
                          in2 = []
                          signals[item[5].text] = in2
                      if item[6].text in outputs:
                          out1 = outputs[item[6].text]
                      elif item[6].text in signals:
                          out1 = signals[item[6].text]
                      else:
                          out1 = []
                          signals[item[6].text] = out1
                      process = UntimedProcesses.ZipU(eval(item[2].text),eval(item[3].text),in1,in2,out1)
                      proc_list.append(process)
                  elif item[1].text=='UnZip':
                      print item[1].text
                      if item[2].text in inputs:
                          in1 = inputs[item[2].text]
                      elif item[2].text in signals:
                          in1 = signals[item[2].text]
                      else:
                          in1 = []
                          signals[item[2].text] = in1
                      if item[3].text in outputs:
                          out1 = outputs[item[3].text]
                      elif item[3].text in signals:
                          out1 = signals[item[3].text]
                      else:
                          out1 = []
                          signals[item[3].text] = out1
                      if item[4].text in outputs:
                          out2 = outputs[item[4].text]
                      elif item[4].text in signals:
                          out2 = signals[item[4].text]
                      else:
                          out2 = []
                          signals[item[4].text] = out2
                      process = UntimedProcesses.UnzipU(in1,out1,out2)
                      proc_list.append(process)
                  elif item[1].text=='Mealy':
                      print item[1].text
                      if item[6].text in inputs:
                          in1 = inputs[item[6].text]
                      elif item[6].text in signals:
                          in1 = signals[item[6].text]
                      else:
                          in1 = []
                          signals[item[6].text] = in1
                      if item[7].text in outputs:
                          out1 = outputs[item[7].text]
                      elif item[7].text in signals:
                          out1 = signals[item[7].text]
                      else:
                          out1 = []
                          signals[item[7].text] = out1
                      process = UntimedProcesses.MealyU(item[2].text,item[3].text,item[4].text,eval(item[5].text),in1,out1)
                      proc_list.append(process)
                  elif item[1].text=='Map':
                      print item[1].text
                      if item[4].text in inputs:
                          in1 = inputs[item[4].text]
                      elif item[4].text in signals:
                          in1 = signals[item[4].text]
                      else:
                          in1 = []
                          signals[item[4].text] = in1
                      if item[5].text in outputs:
                          out1 = outputs[item[5].text]
                      elif item[5].text in signals:
                          out1 = signals[item[5].text]
                      else:
                          out1 = []
                          signals[item[5].text] = out1
                      process = UntimedProcesses.MapU(eval(item[2].text),item[3].text,in1,out1)
                      proc_list.append(process)
                  elif item[1].text=='Scan':
                      print item[1].text
                      if item[5].text in inputs:
                          in1 = inputs[item[5].text]
                      elif item[5].text in signals:
                          in1 = signals[item[5].text]
                      else:
                          in1 = []
                          signals[item[5].text] = in1
                      if item[6].text in outputs:
                          out1 = outputs[item[6].text]
                      elif item[6].text in signals:
                          out1 = signals[item[6].text]
                      else:
                          out1 = []
                          signals[item[6].text] = out1
                      process = UntimedProcesses.ScanU(item[2].text,item[3].text,eval(item[4].text),in1,out1)
                      proc_list.append(process)
                  elif item[1].text=='Scand':
                      print item[1].text
                      if item[5].text in inputs:
                          in1 = inputs[item[5].text]
                      elif item[5].text in signals:
                          in1 = signals[item[5].text]
                      else:
                          in1 = []
                          signals[item[5].text] = in1
                      if item[6].text in outputs:
                          out1 = outputs[item[6].text]
                      elif item[6].text in signals:
                          out1 = signals[item[6].text]
                      else:
                          out1 = []
                          signals[item[6].text] = out1
                      process = UntimedProcesses.ScandU(item[2].text,item[3].text,eval(item[4].text),in1,out1)
                      proc_list.append(process)
                  elif item[1].text=='Source':
                      print item[1].text
                      if item[4].text in outputs:
                          out1 = outputs[item[4].text]
                      elif item[4].text in signals:
                          out1 = signals[item[4].text]
                      else:
                          out1 = []
                          signals[item[4].text] = out1
                      process = UntimedProcesses.SourceU(item[2].text,eval(item[3].text),out1)
                      proc_list.append(process)
                  elif item[1].text=='Init':
                      print item[1].text
                      if item[3].text in inputs:
                          in1 = inputs[item[3].text]
                      elif item[3].text in signals:
                          in1 = signals[item[3].text]
                      else:
                          in1 = []
                          signals[item[3].text] = in1
                      if item[4].text in outputs:
                          out1 = outputs[item[4].text]
                      elif item[4].text in signals:
                          out1 = signals[item[4].text]
                      else:
                          out1 = []
                          signals[item[4].text] = out1
                      process = UntimedProcesses.InitU(eval(item[2].text),in1,out1)
                      proc_list.append(process)
              elif item[0].text=='Synchronous':
                  if item[1].text=='Zip':
                      print item[1].text
                      if item[2].text in inputs:
                          in1 = inputs[item[2].text]
                      elif item[2].text in signals:
                          in1 = signals[item[2].text]
                      else:
                          in1 = []
                          signals[item[2].text] = in1
                      if item[3].text in inputs:
                          in2 = inputs[item[3].text]
                      elif item[3].text in signals:
                          in2 = signals[item[3].text]
                      else:
                          in2 = []
                          signals[item[3].text] = in2
                      if item[4].text in outputs:
                          out1 = outputs[item[4].text]
                      elif item[4].text in signals:
                          out1 = signals[item[4].text]
                      else:
                          out1 = []
                          signals[item[4].text] = out1
                      process = SynchronousProcesses.ZipS(in1,in2,out1)
                      proc_list.append(process)
                  elif item[1].text=='UnZip':
                      print item[1].text
                      if item[2].text in inputs:
                          in1 = inputs[item[2].text]
                      elif item[2].text in signals:
                          in1 = signals[item[2].text]
                      else:
                          in1 = []
                          signals[item[2].text] = in1
                      if item[3].text in outputs:
                          out1 = outputs[item[3].text]
                      elif item[3].text in signals:
                          out1 = signals[item[3].text]
                      else:
                          out1 = []
                          signals[item[3].text] = out1
                      if item[4].text in outputs:
                          out2 = outputs[item[4].text]
                      elif item[4].text in signals:
                          out2 = signals[item[4].text]
                      else:
                          out2 = []
                          signals[item[4].text] = out2
                      process = SynchronousProcesses.UnzipS(in1,out1,out2)
                      proc_list.append(process)
                  elif item[1].text=='Mealy':
                      print item[1].text
                      if item[5].text in inputs:
                          in1 = inputs[item[5].text]
                      elif item[5].text in signals:
                          in1 = signals[item[5].text]
                      else:
                          in1 = []
                          signals[item[5].text] = in1
                      if item[6].text in outputs:
                          out1 = outputs[item[6].text]
                      elif item[6].text in signals:
                          out1 = signals[item[6].text]
                      else:
                          out1 = []
                          signals[item[6].text] = out1
                      process = SynchronousProcesses.MealyS(item[2].text,item[3].text,eval(item[4].text),in1,out1)
                      proc_list.append(process)
                  elif item[1].text=='Map':
                      print item[1].text
                      if item[3].text in inputs:
                          in1 = inputs[item[3].text]
                      elif item[3].text in signals:
                          in1 = signals[item[3].text]
                      else:
                          in1 = []
                          signals[item[3].text] = in1
                      if item[4].text in outputs:
                          out1 = outputs[item[4].text]
                      elif item[4].text in signals:
                          out1 = signals[item[4].text]
                      else:
                          out1 = []
                          signals[item[4].text] = out1
                      process = SynchronousProcesses.MapS(item[2].text,in1,out1)
                      proc_list.append(process)
                  elif item[1].text=='Scan':
                      print item[1].text
                      if item[4].text in inputs:
                          in1 = inputs[item[4].text]
                      elif item[4].text in signals:
                          in1 = signals[item[4].text]
                      else:
                          in1 = []
                          signals[item[4].text] = in1
                      if item[5].text in outputs:
                          out1 = outputs[item[5].text]
                      elif item[5].text in signals:
                          out1 = signals[item[5].text]
                      else:
                          out1 = []
                          signals[item[5].text] = out1
                      process = SynchronousProcesses.ScanS(item[2].text,eval(item[3].text),in1,out1)
                      proc_list.append(process)
                  elif item[1].text=='Scand':
                      print item[1].text
                      if item[5].text in inputs:
                          in1 = inputs[item[5].text]
                      elif item[5].text in signals:
                          in1 = signals[item[5].text]
                      else:
                          in1 = []
                          signals[item[5].text] = in1
                      if item[6].text in outputs:
                          out1 = outputs[item[6].text]
                      elif item[6].text in signals:
                          out1 = signals[item[6].text]
                      else:
                          out1 = []
                          signals[item[6].text] = out1
                      process = SynchronousProcesses.ScandS(item[2].text,item[3].text,eval(item[4].text),in1,out1)
                      proc_list.append(process)
                  elif item[1].text=='Source':
                      print item[1].text
                      if item[4].text in outputs:
                          out1 = outputs[item[4].text]
                      elif item[4].text in signals:
                          out1 = signals[item[4].text]
                      else:
                          out1 = []
                          signals[item[4].text] = out1
                      process = SynchronousProcesses.SourceS(item[2].text,eval(item[3].text),out1)
                      proc_list.append(process)
                  elif item[1].text=='Init':
                      print item[1].text
                      if item[3].text in inputs:
                          in1 = inputs[item[3].text]
                      elif item[3].text in signals:
                          in1 = signals[item[3].text]
                      else:
                          in1 = []
                          signals[item[3].text] = in1
                      if item[4].text in outputs:
                          out1 = outputs[item[4].text]
                      elif item[4].text in signals:
                          out1 = signals[item[4].text]
                      else:
                          out1 = []
                          signals[item[4].text] = out1
                      process = SynchronousProcesses.InitS(eval(item[2].text),in1,out1)
                      proc_list.append(process)
  #everything above this point is code for use in the actual parser
  '''
  function = utilities.stringToFunction(system[2][2][2].text, "w, x")
  x = [1, 2, 3]
  y=function(eval(system[2][2][4].text),x)
  print y
  print x[0]
  print function(1,x)
  state = system[2][2][5].text
  print state
  signal = system[2][2][6].text
  siglist = []
  siglist = signal.split('/')
  print siglist
  print inputs
  print outputs
  print signals
  print proc_list
  '''
  #print signals
  return (inputs,outputs,proc_list)
  
def main():
  print "Parsing XML"
  print parseXml("sample.xml")  
  
if __name__ == "__main__":
  main()
