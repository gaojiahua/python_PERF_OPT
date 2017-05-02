#!/usr/bin/env python
import sys 
import bisect
import timer
if __name__ == "__main__":

	with timer.Timer() as t:
		a = range(1000*1000)
		for i in xrange(1000*1000):
			k = 100
			bisect.bisect_left(a,k)
	print "=> bisect: %s s" % t.secs

