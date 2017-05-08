#map_test2.py
from timer import *

MAX = 2000000

with Timer() as t:
	for i in xrange(MAX):
	
		oldlist =  ['Bob','Tom','alice','Jerry','Wendy','Smith']
		newlist = []
		for word in oldlist:
			newlist.append(word.upper())
			
print "for %s"%t.secs

with Timer() as t:
	for i in xrange(MAX):
	
		oldlist =  ['Bob','Tom','alice','Jerry','Wendy','Smith']
		newlist = map(lambda x: x.upper(),oldlist)
		
print "map %s"%t.secs

with Timer() as t:
	for i in xrange(MAX):
	
		oldlist =  ['Bob','Tom','alice','Jerry','Wendy','Smith']
		newlist = [s.upper() for s in oldlist]
		
print "list compre %s"%t.secs







