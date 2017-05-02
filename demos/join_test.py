import timer
#jlist = ["a",  "b"]
jlist = ["a",  "b", "a",  "b","a",  "b","a",  "b","a",  "b" ]
MAX_RANGE =  10 * 1000 * 1000
def test_join0():
	for i in xrange(MAX_RANGE):
		rs =  "a" + "b"

def test_join1():
	for i in xrange(MAX_RANGE):
		rs =  "".join(["a",  "b"])

def test_join2():
	for i in xrange(MAX_RANGE):
		rs = "%s%s" % ("a", "b")

def test_join3():
	for i in xrange(MAX_RANGE):
			rs = jlist[0] +  jlist[1] +  jlist[2] +  jlist[3] +  jlist[4] +  jlist[5] +  jlist[6] +  jlist[7] + jlist[8] + jlist[9]

def test_join4():
	for i in xrange(MAX_RANGE):
			rs = ""
			for i in  jlist:
				rs += i
				
if __name__ == "__main__":
	with timer.Timer() as   t:
		test_join0()
	print "=> bisect: %s s" % t.secs
	with timer.Timer() as   t:
		test_join1()
	print "=> bisect: %s s" % t.secs
	with timer.Timer() as   t:
			test_join2()
	print "=> bisect: %s s" % t.secs	