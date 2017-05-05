import time
#func = time.time
func = time.clock
t0 = func()
time.sleep(2)
t1 = func()
print t1 - t0

print func()
print time.asctime( time.localtime(func()) )
print time.asctime( time.localtime(0) )