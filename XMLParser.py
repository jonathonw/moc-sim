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
  sig_stack = []
  sig_list = []
  
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
              print signal
              #print inputs
              #sig_stack.append(signal)
              #sig_list.append(obj.tag + '/' + item.tag)
      elif obj.tag=='outputs':
          for item in obj:
              signal = []
              outputs[obj.tag + '/' + item.tag] = signal
              #print outputs
              #sig_stack.append(signal)
              #sig_list.append(obj.tag + '/' + item.tag)
      else:
          for item in obj:
              if item[0].text=='Timed':
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
                      '''
                      _indin1 = search_signals(sig_list,item[4].text)
                      _indin2 = search_signals(sig_list,item[5].text)
                      _indout = search_signals(sig_list,item[6].text)
                      if _indin1==-1:
                          _sig_in1 = []
                          sig_stack.append(_sig_in1)
                          sig_list.append(item[4].text)
                          _indin1 = search_signals(sig_list,item[4].text)
                      if _indin2==-1:
                          _sig_in2 = []
                          sig_stack.append(_sig_in2)
                          sig_list.append(item[5].text)
                          _indin2 = search_signals(sig_list,item[5].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[6].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[6].tag)
                      '''
                      
                      process = TimedProcesses.ZipT(eval(item[2].text),eval(item[3].text),in1,in2,out)
                      proc_list.append(process)
                  if item[1].text=='UnZip':
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
                      '''
                      _indin = search_signals(sig_list,item[2].text)
                      _indout1 = search_signals(sig_list,item[3].text)
                      _indout2 = search_signals(sig_list,item[4].text)
                      if _indin==-1:
                          _sig_in = []
                          sig_stack.append(_sig_in)
                          sig_list.append(item[2].text)
                          _indin = search_signals(sig_list,item[2].text)
                      if _indout1==-1:
                          _sig_out1 = []
                          sig_stack.append(_sig_out1)
                          sig_list.append(item[3].text)
                          _indout1 = search_signals(sig_list,item[3].text)
                      if _indout2==-1:
                          _sig_out2 = []
                          sig_stack.append(_sig_out2)
                          sig_list.append(item.tag+'/'+item[4].tag)
                          _indout2 = search_signals(sig_list,item.tag+'/'+item[4].tag)
                      '''
                      process = TimedProcesses.UnzipT(in1,out1,out2)
                      proc_list.append(process)
                  if item[1].text=='Mealy':
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
                      '''
                      _indin = search_signals(sig_list,item[6].text)
                      _indout = search_signals(sig_list,item[7].text)
                      if _indin==-1:
                          _sig_in = []
                          sig_stack.append(_sig_in)
                          sig_list.append(item[6].text)
                          _indin = search_signals(sig_list,item[6].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[7].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[7].tag)
                      '''
                      process = TimedProcesses.MealyT(item[2].text,item[3].text,item[4].text,eval(item[5].text),in1,out1)
                      proc_list.append(process)
                  if item[1].text=='Source':
                      print item[1].text
                      if item[4].text in outputs:
                          out1 = outputs[item[4].text]
                      elif item[4].text in signals:
                          out1 = signals[item[4].text]
                      else:
                          out1 = []
                          signals[item[4].text] = out1
                      '''
                      _indout = search_signals(sig_list,item[4].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[4].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[4].tag)
                      '''
                      process = TimedProcesses.SourceT(item[2].text,eval(item[3].text),out1)
                      proc_list.append(process)
                  if item[1].text=='Init':
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
                      '''
                      _indin = search_signals(sig_list,item[3].text)
                      _indout = search_signals(sig_list,item[4].text)
                      if _indin==-1:
                          _sig_in = []
                          sig_stack.append(_sig_in)
                          sig_list.append(item[3].text)
                          _indin = search_signals(sig_list,item[3].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[4].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[4].tag)
                      '''
                      process = TimedProcesses.InitT(eval(item[2].text),in1,out1)
                      proc_list.append(process)
              if item[0].text=='Untimed':
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
                      '''
                      _indin1 = search_signals(sig_list,item[4].text)
                      _indin2 = search_signals(sig_list,item[5].text)
                      _indout = search_signals(sig_list,item[6].text)
                      if _indin1==-1:
                          _sig_in1 = []
                          sig_stack.append(_sig_in1)
                          sig_list.append(item[4].text)
                          _indin1 = search_signals(sig_list,item[4].text)
                      if _indin2==-1:
                          _sig_in2 = []
                          sig_stack.append(_sig_in2)
                          sig_list.append(item[5].text)
                          _indin2 = search_signals(sig_list,item[5].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[6].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[6].tag)
                      '''
                      process = UntimedProcesses.ZipU(eval(item[2].text),eval(item[3].text),in1,in2,out1)
                      proc_list.append(process)
                  if item[1].text=='UnZip':
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
                      '''
                      _indin = search_signals(sig_list,item[2].text)
                      _indout1 = search_signals(sig_list,item[3].text)
                      _indout2 = search_signals(sig_list,item[4].text)
                      if _indin==-1:
                          _sig_in = []
                          sig_stack.append(_sig_in)
                          sig_list.append(item[2].text)
                          _indin = search_signals(sig_list,item[2].text)
                      if _indout1==-1:
                          _sig_out1 = []
                          sig_stack.append(_sig_out1)
                          sig_list.append(item[3].text)
                          _indout1 = search_signals(sig_list,item[3].text)
                      if _indout2==-1:
                          _sig_out2 = []
                          sig_stack.append(_sig_out2)
                          sig_list.append(item.tag+'/'+item[4].tag)
                          _indout2 = search_signals(sig_list,item.tag+'/'+item[4].tag)
                      '''
                      process = UntimedProcesses.UnzipU(in1,out1,out2)
                      proc_list.append(process)
                  if item[1].text=='Mealy':
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
                      '''
                      _indin = search_signals(sig_list,item[6].text)
                      _indout = search_signals(sig_list,item[7].text)
                      if _indin==-1:
                          _sig_in = []
                          sig_stack.append(_sig_in)
                          sig_list.append(item[6].text)
                          _indin = search_signals(sig_list,item[6].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[7].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[7].tag)
                      '''
                      process = UntimedProcesses.MealyU(item[2].text,item[3].text,item[4].text,eval(item[5].text),in1,out1)
                      proc_list.append(process)
                  if item[1].text=='Map':
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
                      '''
                      _indin = search_signals(sig_list,item[4].text)
                      _indout = search_signals(sig_list,item[5].text)
                      if _indin==-1:
                          _sig_in = []
                          sig_stack.append(_sig_in)
                          sig_list.append(item[4].text)
                          _indin = search_signals(sig_list,item[4].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[5].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[5].tag)
                      '''
                      process = UntimedProcesses.MapU(eval(item[2].text),item[3].text,in1,out1)
                      proc_list.append(process)
                  if item[1].text=='Scan':
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
                      '''
                      _indin = search_signals(sig_list,item[5].text)
                      _indout = search_signals(sig_list,item[6].text)
                      if _indin==-1:
                          _sig_in = []
                          sig_stack.append(_sig_in)
                          sig_list.append(item[5].text)
                          _indin = search_signals(sig_list,item[5].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[6].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[6].tag)
                      '''
                      process = UntimedProcesses.ScanU(item[2].text,item[3].text,eval(item[4].text),in1,out1)
                      proc_list.append(process)
                  if item[1].text=='Scand':
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
                      '''
                      _indin = search_signals(sig_list,item[5].text)
                      _indout = search_signals(sig_list,item[6].text)
                      if _indin==-1:
                          _sig_in = []
                          sig_stack.append(_sig_in)
                          sig_list.append(item[5].text)
                          _indin = search_signals(sig_list,item[5].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[6].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[6].tag)
                      '''
                      process = UntimedProcesses.ScandU(item[2].text,item[3].text,eval(item[4].text),in1,out1)
                      proc_list.append(process)
                  if item[1].text=='Source':
                      print item[1].text
                      if item[4].text in outputs:
                          out1 = outputs[item[4].text]
                      elif item[4].text in signals:
                          out1 = signals[item[4].text]
                      else:
                          out1 = []
                          signals[item[4].text] = out1
                      '''
                      _indout = search_signals(sig_list,item[4].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[4].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[4].tag)
                      '''
                      process = UntimedProcesses.SourceU(item[2].text,eval(item[3].text),out1)
                      proc_list.append(process)
                  if item[1].text=='Init':
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
                      '''
                      _indin = search_signals(sig_list,item[3].text)
                      _indout = search_signals(sig_list,item[4].text)
                      if _indin==-1:
                          _sig_in = []
                          sig_stack.append(_sig_in)
                          sig_list.append(item[3].text)
                          _indin = search_signals(sig_list,item[3].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[4].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[4].tag)
                      '''
                      process = UntimedProcesses.InitU(eval(item[2].text),in1,out1)
                      proc_list.append(process)
              if item[0].text=='Synchronous':
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
                      '''
                      _indin1 = search_signals(sig_list,item[2].text)
                      _indin2 = search_signals(sig_list,item[3].text)
                      _indout = search_signals(sig_list,item[4].text)
                      if _indin1==-1:
                          _sig_in1 = []
                          sig_stack.append(_sig_in1)
                          sig_list.append(item[2].text)
                          _indin1 = search_signals(sig_list,item[2].text)
                      if _indin2==-1:
                          _sig_in2 = []
                          sig_stack.append(_sig_in2)
                          sig_list.append(item[3].text)
                          _indin2 = search_signals(sig_list,item[3].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[4].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[4].tag)
                      '''
                      process = SynchronousProcesses.ZipS(in1,in2,out1)
                      proc_list.append(process)
                  if item[1].text=='UnZip':
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
                      '''
                      _indin = search_signals(sig_list,item[2].text)
                      _indout1 = search_signals(sig_list,item[3].text)
                      _indout2 = search_signals(sig_list,item[4].text)
                      if _indin==-1:
                          _sig_in = []
                          sig_stack.append(_sig_in)
                          sig_list.append(item[2].text)
                          _indin = search_signals(sig_list,item[2].text)
                      if _indout1==-1:
                          _sig_out1 = []
                          sig_stack.append(_sig_out1)
                          sig_list.append(item[3].text)
                          _indout1 = search_signals(sig_list,item[3].text)
                      if _indout2==-1:
                          _sig_out2 = []
                          sig_stack.append(_sig_out2)
                          sig_list.append(item.tag+'/'+item[4].tag)
                          _indout2 = search_signals(sig_list,item.tag+'/'+item[4].tag)
                      '''
                      process = SynchronousProcesses.UnzipS(in1,out1,out2)
                      proc_list.append(process)
                  if item[1].text=='Mealy':
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
                      '''
                      _indin = search_signals(sig_list,item[5].text)
                      _indout = search_signals(sig_list,item[6].text)
                      if _indin==-1:
                          _sig_in = []
                          sig_stack.append(_sig_in)
                          sig_list.append(item[5].text)
                          _indin = search_signals(sig_list,item[5].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[6].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[6].tag)
                      '''
                      process = SynchronousProcesses.MealyS(item[2].text,item[3].text,eval(item[4].text),in1,out1)
                      proc_list.append(process)
                  if item[1].text=='Map':
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
                      '''
                      _indin = search_signals(sig_list,item[3].text)
                      _indout = search_signals(sig_list,item[4].text)
                      if _indin==-1:
                          _sig_in = []
                          sig_stack.append(_sig_in)
                          sig_list.append(item[3].text)
                          _indin = search_signals(sig_list,item[3].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[4].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[4].tag)
                      '''
                      process = SynchronousProcesses.MapS(item[2].text,in1,out1)
                      proc_list.append(process)
                  if item[1].text=='Scan':
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
                      '''
                      _indin = search_signals(sig_list,item[4].text)
                      _indout = search_signals(sig_list,item[5].text)
                      if _indin==-1:
                          _sig_in = []
                          sig_stack.append(_sig_in)
                          sig_list.append(item[4].text)
                          _indin = search_signals(sig_list,item[4].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[5].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[5].tag)
                      '''
                      process = SynchronousProcesses.ScanS(item[2].text,eval(item[3].text),in1,out1)
                      proc_list.append(process)
                  if item[1].text=='Scand':
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
                      '''
                      _indin = search_signals(sig_list,item[5].text)
                      _indout = search_signals(sig_list,item[6].text)
                      if _indin==-1:
                          _sig_in = []
                          sig_stack.append(_sig_in)
                          sig_list.append(item[5].text)
                          _indin = search_signals(sig_list,item[5].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[6].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[6].tag)
                      '''
                      process = SynchronousProcesses.ScandS(item[2].text,item[3].text,eval(item[4].text),in1,out1)
                      proc_list.append(process)
                  if item[1].text=='Source':
                      print item[1].text
                      if item[4].text in outputs:
                          out1 = outputs[item[4].text]
                      elif item[4].text in signals:
                          out1 = signals[item[4].text]
                      else:
                          out1 = []
                          signals[item[4].text] = out1
                      '''
                      _indout = search_signals(sig_list,item[4].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[4].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[4].tag)
                      '''
                      process = SynchronousProcesses.SourceS(item[2].text,eval(item[3].text),out1)
                      proc_list.append(process)
                  if item[1].text=='Init':
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
                      '''
                      _indin = search_signals(sig_list,item[3].text)
                      _indout = search_signals(sig_list,item[4].text)
                      if _indin==-1:
                          _sig_in = []
                          sig_stack.append(_sig_in)
                          sig_list.append(item[3].text)
                          _indin = search_signals(sig_list,item[3].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[4].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[4].tag)
                      '''
                      process = SynchronousProcesses.InitS(eval(item[2].text),in1,out1)
                      proc_list.append(process)
                  '''
              for field in item:
                  if field.tag=='In1' or field.tag=='In2' or field.tag=='Out1' or field.tag=='Out2':
                      signal = []
                      sig_stack.append(signal)
                      sig_list.append(field.tag)'''
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
  '''
  print inputs
  print outputs
  print signals
  print proc_list

  return (inputs,outputs,proc_list)
  
def main():
  print "Parsing XML"
  parseXml("sample.xml")  
  
if __name__ == "__main__":
  main()
