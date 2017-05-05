import cProfile
import re
def test():
	for i in xrange(10**6):
		re.compile("foo|bar")	
cProfile.run('test()')