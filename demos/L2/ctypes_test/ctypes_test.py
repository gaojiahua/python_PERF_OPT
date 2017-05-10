import math
from timer import *
import ctypes

MAX = 1000000
def check_prime(x):
    values = xrange(2, int(math.sqrt(x)))
    for i in values:
        if x % i == 0:
            return False

    return True
	
c_check_prime = ctypes.CDLL(r'.\ctypes\dll2ctypes\x64\Release\dll2ctypes.dll').c_check_prime


with Timer() as t:
	numbers_py = [x for x in xrange(MAX) if check_prime(x)]
print "python %s"%t.secs



with Timer() as t:
	numbers_py = [x for x in xrange(MAX) if c_check_prime(x)]
print "ctypes %s"%t.secs
