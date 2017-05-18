import cProfile
import re
def test():
	for j in xrange(10):
		for i in xrange(10**6):
			re.compile("foo|bar")	
cProfile.run('test()')