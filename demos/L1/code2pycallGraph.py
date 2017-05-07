from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
import sys
from memLeak import *

with PyCallGraph(output=GraphvizOutput()):
	computate_something()