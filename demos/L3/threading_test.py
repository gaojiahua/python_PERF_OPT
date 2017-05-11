from timer import Timer
import threading
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
	print "=> single thread 10 times : %s s" % t.secs
	
	with Timer() as t:
		thread_list =[]
		for i in xrange(10):
			th = threading.Thread(target = func, args=())
			th.start()
			thread_list.append(th)
		for th in thread_list:
			th.join()
	print "=> multiple threads 1 time : %s s" % t.secs
	
if __name__ == "__main__":
	test(compute)
	test(mysleep)