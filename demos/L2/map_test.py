from timer import *


MAX = 1000000
def doSomethingWithX(x):
	y = x*x


with Timer() as t:
	for x in xrange(0, MAX):
		doSomethingWithX(x)
print "xrange %s"%t.secs

with Timer() as t:
	map(doSomethingWithX, xrange(0,MAX))
print "map %s"%t.secs