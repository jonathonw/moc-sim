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
  
#From http://www.bitformation.com/art/python_toposort.html
def topological_sort(items, partial_order):
  """Perform topological sort.
     items is a list of items to be sorted.
     partial_order is a list of pairs. If pair (a,b) is in it, it means
     that item a should appear before item b.
     Returns a list of the items in one of the possible orders, or None
     if partial_order contains a loop.
  """

  def add_node(graph, node):
    """Add a node to the graph if not already exists."""
    if not graph.has_key(node):
      graph[node] = [0] # 0 = number of arcs coming into this node.

  def add_arc(graph, fromnode, tonode):
    """Add an arc to a graph. Can create multiple arcs.
       The end nodes must already exist."""
    graph[fromnode].append(tonode)
    # Update the count of incoming arcs in tonode.
    graph[tonode][0] = graph[tonode][0] + 1

  # step 1 - create a directed graph with an arc a->b for each input
  # pair (a,b).
  # The graph is represented by a dictionary. The dictionary contains
  # a pair item:list for each node in the graph. /item/ is the value
  # of the node. /list/'s 1st item is the count of incoming arcs, and
  # the rest are the destinations of the outgoing arcs. For example:
  #       {'a':[0,'b','c'], 'b':[1], 'c':[1]}
  # represents the graph:   c <-- a --> b
  # The graph may contain loops and multiple arcs.
  # Note that our representation does not contain reference loops to
  # cause GC problems even when the represented graph contains loops,
  # because we keep the node names rather than references to the nodes.
  graph = {}
  for v in items:
    add_node(graph, v)
  for a,b in partial_order:
    add_arc(graph, a, b)

  # Step 2 - find all roots (nodes with zero incoming arcs).
  roots = [node for (node,nodeinfo) in graph.items() if nodeinfo[0] == 0]

  # step 3 - repeatedly emit a root and remove it from the graph. Removing
  # a node may convert some of the node's direct children into roots.
  # Whenever that happens, we append the new roots to the list of
  # current roots.
  sorted = []
  while len(roots) != 0:
    # If len(roots) is always 1 when we get here, it means that
    # the input describes a complete ordering and there is only
    # one possible output.
    # When len(roots) > 1, we can choose any root to send to the
    # output; this freedom represents the multiple complete orderings
    # that satisfy the input restrictions. We arbitrarily take one of
    # the roots using pop(). Note that for the algorithm to be efficient,
    # this operation must be done in O(1) time.
    root = roots.pop()
    sorted.append(root)
    for child in graph[root][1:]:
      graph[child][0] = graph[child][0] - 1
      if graph[child][0] == 0:
        roots.append(child)
    del graph[root]
  if len(graph.items()) != 0:
    # There is a loop in the input.
    return None
  return sorted
  
#A little bit of test code:
if __name__ == "__main__":
  functionString = "x = x + 3\n\
return w + x"
  
  func = stringToFunction(functionString, "x, w")
  print func(1,3)
  print func(6,2)
