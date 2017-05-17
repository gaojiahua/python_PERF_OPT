#python 性能优化实践

​															stevegao(高家华)

***

##1. 真假多线程
开发多线程的应用程序，是日常软件开发中经常会遇到的需求。

### Python支持多线程threading模块

```Python
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
```
***
![](pics\threading_test.png)

### GIL

（Global Interpreter Lock）全局解释器锁

  Python解释器被GIL保护，该锁定只允许一次执行一个线程，即便存在多个可用的处理器。在计算型密集的程序中，严重限制了线程的作用。实际上，就像上边我们看到的那样，在密集计算型程序中使用多线程，经常比顺序执行慢很多。

### threading模块的意义何在
既然多线程会慢，那么threading模块的存在的意义是什么
对于爬虫或者下载这种I/O密集型的程序，使用threading模块是有意义的

### 计算密集型程序的并发
使用C扩展，或者multiprocessing模块，重复下上边的例子
```Python
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
```
-  测试结果
  ![](pics\multiprocessing_test.png)

multiprocessing可以绕过GIL锁实现真正的并发，但是创建进程这个操作比创建线程重很多

两个关键点：

第一是衡量你的程序是I/O密集还是计算密集

第二是不要频繁去创建新进程

### 小结

| 多进程的优势              | 多进程的劣势                                   |
| ------------------- | ---------------------------------------- |
| 避开GIL的限制，可以使用多核操作系统 | 更多的内存消耗                                  |
| 进程使用独立的内存空间，避免竞态问题  | 进程间的数据共享变得更加困难                           |
| 子进程容易中断（killable）   | IPC（Interprocess communication，进程间通信）处理比线程困难 |





##2. JSON解析

JSON文件解析是日常工作比较常见的一个任务。

[JSON](http://baike.baidu.com/item/JSON)([JavaScript](http://baike.baidu.com/item/JavaScript) Object Notation, JS 对象标记) 是一种轻量级的数据交换格式。它基于 [ECMAScript](http://baike.baidu.com/item/ECMAScript) 规范的一个子集，采用完全独立于编程语言的文本格式来存储和表示数据。简洁和清晰的层次结构使得 JSON 成为理想的数据交换语言。 易于人阅读和编写，同时也易于机器解析和生成，并有效地提升网络传输效率。

### JSON demo
```Json
"Resource": [{
		"ID": "3277400",
		"Type": "Cursor",
		"Size": "134"
	},
	{
		"ID": "3277400",
		"Type": "Cursor",
		"Size": "134"
	},
	{
		"ID": "3277400",
		"Type": "Cursor",
		"Size": "134"
	}
	]
```

### 测试代码

```Python
#json_test.py
import json
from  timer import  *
import  sys
with Timer() as t:
	for i in  xrange(10):
		json.loads(open(sys.path[0]+"//test.json").read())
print  "json loads %s" % t.secs
```

***

### 测试结果

python2.7.13中运行

![](pics\py27_json_test.png)

python2.6.5中运行
![](pics\py26_json_test.png)

###原因分析

Python2.6的json解析并不是没有使用C语言加速，而是C语言加速模块效果不如Python2.7的好。

直观点看，左边是2.6的C加速代码，右边是2.7的。

![](pics\json_src.png)

### 选用合适的第三方库

这里介绍一个simplejson，pip 安装

![](pics\simplejson_install.png)

```Python
#json_test.py
import json
from  timer import  *
import  sys
with Timer() as t:
	for i in  xrange(10):
		json.loads(open(sys.path[0]+"//test.json").read())
print  "json loads %s" % t.secs


import simplejson
with Timer() as t:
	for i in  xrange(10):
		simplejson.loads(open(sys.path[0]+"//test.json").read())
print  "simplejson loads %s" % t.secs

```

***

加载速度测试：

![](pics\simplejson_loads_test.png)



### 小结

* 去了解你import进来的模块，随便装个轮子你的程序可以跑，但不一定跑得远跑得快，通过测试对比选取合适的库

* 不要功能实现了就觉得万事大吉，多做一点，很多时候进步是由这一点带来的

* 有条件的情况下，尽量去升级到较新的Python版本和库的版本

  ​
>PS :必须 采用编译安装的方式（编译安装会开启c语言优化，而源码拷贝功能是正常的，但是由python实现的）效率是高于python2.7自带的json库的。
>


##3. URL中提取域名

前段时间一个网址安全检测的项目里边需要从网址中提取域名，eg : http://sports.qq.com/a/20170511/003170.htm，域名就是qq.com。看起来挺简单的一个算法，Python中也有专门的库，tldextract。

### 安装

```Shell
>>pip install tldextract
***
***
Successfully installed tldextract-2.0.2
```

***
###  测试
```Python
#tldextract_test.py
import  tldextract
from timer  import *
urls = ["https://www.baidu.com/s?wd=asdf", "http://sports.qq.com/a/20170511/003170.htm", "abc.sd.def.ru", "http://blog.csdn.net/arbel/article/details/7957782", 
	              "http://www.vrplumber.com/programming/runsnakerun/"
	              ]

with Timer() as t:			  
	for i in xrange(10):
		for url in urls:
			ext = tldextract.extract(url)
			#print ext.domain
print "tldextract %s"%t.secs
```
***
![](pics\tldextract_test.png)

5个url取域名，重复运行10次，耗时2s以上。

### 原因分析

```Python
python -m cProfile -o tld.prof tldextract_test.py
```

![](pics\tldprof.png)

Python27\Lib\site-packages\tldextract\\.tld_set

Python27\Lib\site-packages\tldextract\\.tld_set_snapshot

### 小结

  从耗时分析入手，找到程序运营不正常的原因

##4. simhash算法

### 原理

![](pics\simhash.png)
![](pics\simhash2.png)
```Python
from hashtype import hashtype

class simhash(hashtype):
    def create_hash(self, tokens):
        """Calculates a Charikar simhash with appropriate bitlength.
        
        Input can be any iterable, but for strings it will automatically
        break it into words first, assuming you don't want to iterate
        over the individual characters. Returns nothing.
        
        Reference used: http://dsrg.mff.cuni.cz/~holub/sw/shash
        """
        if type(tokens) == str:
            tokens = tokens.split()
        v = [0]*self.hashbits    
        for t in [self._string_hash(x) for x in tokens]:
            bitmask = 0
            for i in xrange(self.hashbits):
                bitmask = 1 << i
                if t & bitmask:
                    v[i] += 1
                else:
                    v[i] -= 1

        fingerprint = 0
        for i in xrange(self.hashbits):
            if v[i] >= 0:
                fingerprint += 1 << i        
        self.hash = fingerprint

    def _string_hash(self, v):
        "A variable-length version of Python's builtin hash. Neat!"
        if v == "":
            return 0
        else:
            x = ord(v[0])<<7
            m = 1000003
            mask = 2**self.hashbits-1
            for c in v:
                x = ((x*m)^ord(c)) & mask
            x ^= len(v)
            if x == -1: 
                x = -2
            return x

    def similarity(self, other_hash):
        """Calculate how different this hash is from another simhash.
        Returns a float from 0.0 to 1.0 (inclusive)
        """
        if type(other_hash) != simhash:
            raise Exception('Hashes must be of same type to find similarity')
        b = self.hashbits
        if b!= other_hash.hashbits:
            raise Exception('Hashes must be of equal size to find similarity')
        return float(b - self.hamming_distance(other_hash)) / b
```