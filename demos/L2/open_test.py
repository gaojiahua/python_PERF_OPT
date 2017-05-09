from timer import *

#@profile
def test():
	t_len = 0
	with Timer() as t:
		fobj = open("data.txt")
		lines = fobj.readlines()
		for line in  lines:
			t_len += len(line)
	print  t_len
	print  "readlines %s" % t.secs
	
	t_len =  0
	with Timer() as t:
		with open("data.txt") as  f:
			for line in  f:
				t_len += len(line)
	print  t_len
	print  "iter %s" % t.secs
	
@profile
def test1():
	t_len = 0
	fobj = open("data.txt")
	lines = fobj.readlines()
	for line in  lines:
		t_len += len(line)
	
	t_len = 0
	with open("data.txt") as  f:
	    for line in  f:
		t_len += len(line)
test1()