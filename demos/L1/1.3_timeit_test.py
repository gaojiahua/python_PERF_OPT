import  timeit
import  timer

with  timer.Timer() as  t:
	for i in  xrange(1000000):
		x = range(100)
print  t.secs

print timeit.timeit("x = range(100)")