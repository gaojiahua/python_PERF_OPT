import  tldextract
from timer  import *
import  logging

logger = logging.getLogger('tldextract')
logger.setLevel(logging.CRITICAL)

urls = ["https://www.baidu.com/s?wd=asdf", "http://sports.qq.com/a/20170511/003170.htm", "abc.sd.def.ru", "http://blog.csdn.net/arbel/article/details/7957782", 
	              "http://www.vrplumber.com/programming/runsnakerun/"
	              ]

with Timer() as t:			  
	for i in xrange(10):
		for url in urls:
			ext = tldextract.extract(url)
			#print ext.domain
print "tldextract %s"%t.secs