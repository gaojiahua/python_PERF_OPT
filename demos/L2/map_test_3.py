#map_test3.py
from timer import *

MAX = 1000000

oldlist =  range(1, 10)
def doSomethingWithX(x):
	return x*x

with Timer() as t:
	for x in xrange(0, MAX):
		newlist = []
		for x in  oldlist:
			newlist.append(doSomethingWithX(x))
print "for %s"%t.secs

with Timer() as t:
	for x in xrange(0, MAX):
		newlist =  map(doSomethingWithX,  oldlist)
print "map %s"%t.secs

with Timer() as t:
	for x in xrange(0, MAX):
		newlist = [doSomethingWithX(i) for i in  oldlist]
print "list compre %s"%t.secs


newlist = []
for x in  oldlist:
	newlist.append(doSomethingWithX(x))
print newlist

newlist =  map(doSomethingWithX,  oldlist)
print newlist

newlist = [doSomethingWithX(i) for i in  oldlist]
print newlist