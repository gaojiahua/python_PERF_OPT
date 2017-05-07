@profile
def line_profiler():
	rs = 0
	for i in range(100*100):
		rs += i
	print rs

if __name__ == "__main__":
	line_profiler()