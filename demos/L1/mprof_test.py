import time
def my_func():
	a = [1] * (10 ** 6)
	b = [2] * (2 * 10 ** 7)
	del b
	return a

if __name__ == '__main__':
	for i in xrange(15):
		my_func()
		time.sleep(0.1)