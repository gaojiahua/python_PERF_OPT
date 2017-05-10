from timer import Timer
from Cython_compute import *
if __name__ == '__main__':
	with Timer() as t:
		test()
	print "Cython %s"%t.secs