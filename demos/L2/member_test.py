from timer import *

MAX =  10000000
my_list = ['a','b','is','python','jason','hello','hill','with','phone','test', 
'dfdf','apple','pddf','ind','basic','none','baecr','var','bana','dd','wrd']

key = "blue"
def test():

	with Timer() as t:
		for i in xrange(MAX):
			rs = False
			for item in my_list:
				if key == item:
					rs =  True
					break
	print  "for if %s" % t.secs
	

	with Timer() as t:
		for i in xrange(MAX):
			rs = False
			if key in my_list:
				rs =  True
	print  "list in %s" % t.secs
	
	myset = set(my_list)
	with Timer() as t:
			for i in xrange(MAX):
				rs = False
				if key in myset:
					rs =  True
	print  "set in %s" % t.secs
test()