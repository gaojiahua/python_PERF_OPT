#memLeak.py
import pdb
class MyBigFatObject(object):
	def __init__(self):
		self.data =  [1, 2, 3, 4]
		pass
def computate_something(_cache={}):
	_cache["default"] = dict(foo=MyBigFatObject(),
	                  bar=MyBigFatObject())
	x = MyBigFatObject()
#@profile
def test():
	pdb.set_trace()
	print "b"
	computate_something()
	print "f"
if __name__ == '__main__':
	test()