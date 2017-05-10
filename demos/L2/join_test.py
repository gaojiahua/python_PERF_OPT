import timer
jlist_long = ["a",  "b", "a",  "b","a",  "b","a",  "b","a",  "b" ]
jlist_short =  ["a",  "b"]
MAX_RANGE =  10 * 1000 * 1000
def test_join0():
	for i in xrange(MAX_RANGE):
		rs =  "a" + "b"

def test_join1():
	for i in xrange(MAX_RANGE):
		rs =  "".join(jlist_short)

def test_join2():
	for i in xrange(MAX_RANGE):
			rs = jlist_long[0] +  jlist_long[1] +  jlist_long[2] +  jlist_long[3] +  jlist_long[4] +  jlist_long[5] +  jlist_long[6] +  jlist_long[7] + jlist_long[8] + jlist_long[9]

def test_join3():
	for i in xrange(MAX_RANGE):
			rs =  "".join(jlist_long)
				
if __name__ == "__main__":
	for i in  xrange(4):
		with timer.Timer() as   t:
			eval("test_join%d()"%i)
		print "=> join%d: %s s" % (i, t.secs)
	