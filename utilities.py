#!/usr/bin/env python

#From http://code.activestate.com/recipes/550804-create-a-restricted-python-function-from-a-string/
#except we don't restrict input
# The list of symbols that are included by default in the generated
# function's environment
SAFE_SYMBOLS = ["list", "dict", "tuple", "set", "long", "float", "object",
                "bool", "callable", "True", "False", "dir",
                "frozenset", "getattr", "hasattr", "abs", "cmp", "complex",
                "divmod", "id", "pow", "round", "slice", "vars",
                "hash", "hex", "int", "isinstance", "issubclass", "len",
                "map", "filter", "max", "min", "oct", "chr", "ord", "range",
                "reduce", "repr", "str", "type", "zip", "xrange", "None",
                "Exception", "KeyboardInterrupt"]
# Also add the standard exceptions
__bi = __builtins__
if type(__bi) is not dict:
    __bi = __bi.__dict__
for k in __bi:
    if k.endswith("Error") or k.endswith("Warning"):
        SAFE_SYMBOLS.append(k)
del __bi

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
    
    # Include the safe symbols
  for k in SAFE_SYMBOLS:
    # try from current locals
    try:
      locs[k] = locals()[k]
      continue
    except KeyError:
      pass
    # Try from globals
    try:
      globs[k] = globals()[k]
      continue
    except KeyError:
      pass
    # Try from builtins
    try:
      bis[k] = bi_dict[k]
    except KeyError:
      # Symbol not available anywhere: silently ignored
      pass

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
