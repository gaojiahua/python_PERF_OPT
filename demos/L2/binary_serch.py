#!/usr/bin/env python
import sys 
import timer
def bsearch(a, x, lo=0, hi=None):
	if lo < 0:
		raise ValueError('lo must be non-negative')
	if hi is None:
		hi = len(a)
	while lo < hi:
		mid = (lo+hi)//2
		if a[mid] < x: lo = mid+1
		else: hi = mid
	return lo

if __name__ == "__main__":
	with timer.Timer() as t:
		a = range(1000*1000)
		for i in xrange(1000*1000):
			k = 100
			bsearch(a,k)
	print "=> bisect: %s s" % t.secs
