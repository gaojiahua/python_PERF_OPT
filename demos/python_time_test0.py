from timer import Timer
from redis import Redis
rdb = Redis()

with Timer() as t:
	rdb.lpush("foo", "bar")
print "=> elasped lpush: %s s" % t.secs

with Timer() as t:
	print rdb.lpop("foo")
print "=> elasped lpop: %s s" % t.secs
