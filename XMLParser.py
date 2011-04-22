import Processes
import UntimedProcesses
import TimedProcesses
import SynchronousProcesses
import utilities
import os
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

def parseXml(filename):
  tree = ET.parse(filename)
  system = tree.getroot()
  for obj in system:
      for item in obj:
          for field in item:
              if field.tag!='StateFunc' or field.tag!='OutFunc' or field.tag!='PartFunc':
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
  
  sig_list = []       #list of signals for initialization
  proc_list = []      #list of processes (which will be sent to the scheduler
  sig_stack = []      #stack to hold created signals, search to see if signal has been initialized
  
  for obj in system:
      if obj.tag=='inputs' or obj.tag=='outputs':
          for item in obj:
              signal = []
              sig_stack.append(signal)
              sig_list.append(obj.tag + '/' + item.tag)              
      else:
          for item in obj:
              if item[0].text=='Timed':
                  if item[1].text=='Zip':
                      print item[1].text
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
                      process = TimedProcesses.ZipT(eval(item[2].text),eval(item[3].text),sig_list[_indin1],sig_list[_indin2],sig_list[_indout])
                      proc_list.append(process)
                  if item[1].text=='UnZip':
                      print item[1].text
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
                      process = TimedProcesses.UnzipT(sig_list[_indin],sig_list[_indout1],sig_list[_indout2])
                      proc_list.append(process)
                  if item[1].text=='Mealy':
                      print item[1].text
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
                      process = TimedProcesses.MealyT(item[2].text,item[3].text,item[4].text,eval(item[5].text),sig_list[_indin],sig_list[_indout])
                      proc_list.append(process)
                  if item[1].text=='Source':
                      print item[1].text
                      _indout = search_signals(sig_list,item[4].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[4].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[4].tag)
                      process = TimedProcesses.SourceT(item[2].text,eval(item[3].text),sig_list[_indout])
                      proc_list.append(process)
                  if item[1].text=='Init':
                      print item[1].text
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
                      process = TimedProcesses.InitT(eval(item[2].text),sig_list[_indin],sig_list[_indout])
                      proc_list.append(process)
              if item[0].text=='Untimed':
                  if item[1].text=='Zip':
                      print item[1].text
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
                      process = UntimedProcesses.ZipU(eval(item[2].text),eval(item[3].text),sig_list[_indin1],sig_list[_indin2],sig_list[_indout])
                      proc_list.append(process)
                  if item[1].text=='UnZip':
                      print item[1].text
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
                      process = UntimedProcesses.UnzipU(sig_list[_indin],sig_list[_indout1],sig_list[_indout2])
                      proc_list.append(process)
                  if item[1].text=='Mealy':
                      print item[1].text
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
                      process = UntimedProcesses.MealyU(item[2].text,item[3].text,item[4].text,eval(item[5].text),sig_list[_indin],sig_list[_indout])
                      proc_list.append(process)
                  if item[1].text=='Map':
                      print item[1].text
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
                      process = UntimedProcesses.MapU(eval(item[2].text),item[3].text,sig_list[_indin],sig_list[_indout])
                      proc_list.append(process)
                  if item[1].text=='Scan':
                      print item[1].text
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
                      process = UntimedProcesses.ScanU(item[2].text,item[3].text,eval(item[4].text),sig_list[_indin],sig_list[_indout])
                      proc_list.append(process)
                  if item[1].text=='Scand':
                      print item[1].text
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
                      process = UntimedProcesses.ScandU(item[2].text,item[3].text,eval(item[4].text),sig_list[_indin],sig_list[_indout])
                      proc_list.append(process)
                  if item[1].text=='Source':
                      print item[1].text
                      _indout = search_signals(sig_list,item[4].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[4].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[4].tag)
                      process = UntimedProcesses.SourceU(item[2].text,eval(item[3].text),sig_list[_indout])
                      proc_list.append(process)
                  if item[1].text=='Init':
                      print item[1].text
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
                      process = UntimedProcesses.InitU(eval(item[2].text),sig_list[_indin],sig_list[_indout])
                      proc_list.append(process)
              if item[0].text=='Synchronous':
                  if item[1].text=='Zip':
                      print item[1].text
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
                      process = SynchronousProcesses.ZipS(sig_list[_indin1],sig_list[_indin2],sig_list[_indout])
                      proc_list.append(process)
                  if item[1].text=='UnZip':
                      print item[1].text
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
                      process = SynchronousProcesses.UnzipS(sig_list[_indin],sig_list[_indout1],sig_list[_indout2])
                      proc_list.append(process)
                  if item[1].text=='Mealy':
                      print item[1].text
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
                      process = SynchronousProcesses.MealyS(item[2].text,item[3].text,eval(item[4].text),sig_list[_indin],sig_list[_indout])
                      proc_list.append(process)
                  if item[1].text=='Map':
                      print item[1].text
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
                      process = SynchronousProcesses.MapS(item[2].text,sig_list[_indin],sig_list[_indout])
                      proc_list.append(process)
                  if item[1].text=='Scan':
                      print item[1].text
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
                      process = SynchronousProcesses.ScanS(item[2].text,eval(item[3].text),sig_list[_indin],sig_list[_indout])
                      proc_list.append(process)
                  if item[1].text=='Scand':
                      print item[1].text
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
                      process = SynchronousProcesses.ScandS(item[2].text,item[3].text,eval(item[4].text),sig_list[_indin],sig_list[_indout])
                      proc_list.append(process)
                  if item[1].text=='Source':
                      print item[1].text
                      _indout = search_signals(sig_list,item[4].text)
                      if _indout==-1:
                          _sig_out = []
                          sig_stack.append(_sig_out)
                          sig_list.append(item.tag+'/'+item[4].tag)
                          _indout = search_signals(sig_list,item.tag+'/'+item[4].tag)
                      process = SynchronousProcesses.SourceS(item[2].text,eval(item[3].text),sig_list[_indout])
                      proc_list.append(process)
                  if item[1].text=='Init':
                      print item[1].text
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
                      process = SynchronousProcesses.InitS(eval(item[2].text),sig_list[_indin],sig_list[_indout])
                      proc_list.append(process)
                  '''
              for field in item:
                  if field.tag=='In1' or field.tag=='In2' or field.tag=='Out1' or field.tag=='Out2':
                      signal = []
                      sig_stack.append(signal)
                      sig_list.append(field.tag)'''
  #everything above this point is code for use in the actual parser
  print sig_list
  print sig_stack
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

  return proc_list
  
def main():
  print "Parsing XML"
  parseXml("sample.xml")  
  
if __name__ == "__main__":
  main()
