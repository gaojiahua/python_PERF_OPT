from timer import Timer
import multiprocessing
import time
def compute():
	for i in xrange(10000):
		rs = 0
		for i in xrange(1000):
			rs += i

def mysleep():
	time.sleep(1)

def test(func):
	print func.__name__
	with Timer() as t:
		for i in xrange(10):
			func()
	print "=> single Process 10 times : %s s" % t.secs
	
	with Timer() as t:
		process_list =[]
		for i in xrange(10):
			th = multiprocessing.Process(target = func, args=())
			th.start()
			process_list.append(th)
		for th in process_list:
			th.join()
	print "=> multiple Processes 1 time : %s s" % t.secs
	
if __name__ == "__main__":
	test(compute)
	test(mysleep)