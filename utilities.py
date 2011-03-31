
#From http://code.activestate.com/recipes/550804-create-a-restricted-python-function-from-a-string/
#except we don't restrict input
def stringToFunction(sourceCode, args):
  s = "def __TheFunction__(%s):\n" % args
  s += "\t" + "\n\t".join(sourceCode.split('\n')) + "\n"
  
  # Byte-compilation (optional)
  byteCode = compile(s, "<string>", 'exec')  
  
  # Setup the local and global dictionaries of the execution
  # environment for __TheFunction__
  bis   = dict() # builtins
  globs = dict()
  locs  = dict()

  # Setup a standard-compatible python environment
  bis["locals"]  = lambda: locs
  bis["globals"] = lambda: globs
  globs["__builtins__"] = bis
  globs["__name__"] = "SUBENV"
  globs["__doc__"] = sourceCode

  # Determine how the __builtins__ dictionary should be accessed
  if type(__builtins__) is dict:
    bi_dict = __builtins__
  else:
    bi_dict = __builtins__.__dict__
    
  eval(byteCode, globs, locs)
  # As a result, the function is defined as the item __TheFunction__
  # in the locals dictionary
  fct = locs["__TheFunction__"]
  # Attach the function to the globals so that it can be recursive
  del locs["__TheFunction__"]
  globs["__TheFunction__"] = fct
  # Attach the actual source code to the docstring
  fct.__doc__ = sourceCode
  return fct
  
#A little bit of test code:
if __name__ == "__main__":
  functionString = "x = x + 3\n\
return w + x"
  
  func = stringToFunction(functionString, "x, w")
  print func(1,3)
  print func(6,2)
