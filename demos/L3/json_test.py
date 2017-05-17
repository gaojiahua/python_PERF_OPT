import json
from  timer import  *
import  sys
with Timer() as t:
	for i in  xrange(10):
		json.loads(open(sys.path[0]+"//test.json").read())
print  "json loads %s" % t.secs


import simplejson
with Timer() as t:
	for i in  xrange(10):
		simplejson.loads(open(sys.path[0]+"//test.json").read())
print  "simplejson loads %s" % t.secs
