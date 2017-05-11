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

##2. json解析

json文件解析是日常工作比较常见的一个任务。

### 测试代码

```Python
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


##3. url中提取域名

##4. simhash算法