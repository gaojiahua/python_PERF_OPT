from timer import Timer

with Timer() as t:
	for i in xrange(100000):
		rs = 0
		for i in xrange(1000):
			rs += i
print "=> elasped : %s s" % t.secs

