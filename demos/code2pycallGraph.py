from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
import sys
class MyBigFatObject(object):
	def __init__(self):
		self.data =  [2]

def computate_something(_cache={}):
	_cache[42] = dict(foo=MyBigFatObject(),
	                  bar=MyBigFatObject())
	x = MyBigFatObject()
with PyCallGraph(output=GraphvizOutput()):
	computate_something()