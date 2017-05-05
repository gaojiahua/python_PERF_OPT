#Python性能分析

​															stevegao(高家华)

***
 > #*课程介绍*
 1. Python性能分析
 2. Python性能优化的技巧
 3. Python性能优化实践
 > #*背景知识*



> ##适合
- 写过一点python
- 思考python的性能问题
- 有python性能优化需求
- 想写出性能更好的python代码
> ##不适合
- 不是一门python编程入门，从来没写过python的人不适合
- python初级偏中级一点的课程，python老鸟不适合
- 对比课程的章节目，如果对涉及到的技术点都了解，也不适合这个课程
***
 > # *概述*

- 什么是性能分析
- 性能分析的一般过程
  + 程序运行的速度如何
  + 时间瓶颈在哪里/内存瓶颈在哪里
  + 性能瓶颈的改进方案

***

> # *正文：*
***
#1. 运行时间分析
- 运行时间复杂度

  | 名称     | 复杂度       | 算法举例         |
  | ------ | :-------- | :----------- |
  | 常数时间   | O(1)      | 判断一个数是基数还是偶数 |
  | 对数时间   | O(logn)   | 二分查找         |
  | 线性时间   | O(n)      | 查找无序列表的最小元素  |
  | 线性对数时间 | O(n logn) | 快速排序(平均时间)   |
  | 平方时间   | O(n**2)   | 冒泡排序         |

##1.1 Shell 命令time
linux shell  time命令常用于测量一个命令的运行时间，注意不是用来显示和修改系统时间的，不仅仅用于python。

windows下使用：


1. 虚拟机
2. **Cygwin这样的模拟环境**
3. git bash


![](pics\time_ls.png)



```python
#test_shell_time0.py
rs = 0
for i in xrange(100*100):
    rs += i
print rs
```
![](pics\time0.png)



```python
#test_shell_time1.py
from time import *
sleep(2)
```
![](pics\time1.png)
- 一点结论
  + real != user + sys
  + real 和 user + sys的值越接近，证明程序越重计算，反之说明程序更重IO

##1.2 Python自带模块time

- time函数的功能

```python
#time_demo.py  
import time
print time.time()
print time.asctime( time.localtime(time.time()) )
print time.asctime( time.localtime(0) )
```
time. time() 返回当前时间的时间戳（1970纪元后经过的浮点秒数）
***
    1493454752.49
    Sat Apr 29 16:32:32 2017
    Thu Jan 01 08:00:00 1970
- time.time()的简单应用
```python
import time
t0 = time.time()
doSomething()
t1 = time.time()
print t1 - t0
```
- time.time()的封装使用
```python
#timer.py
import time
class Timer(object):
        def __init__(self, verbose=False):
                self.verbose = verbose
        
        def __enter__(self):
                self.start = time.time()
                return self
        
        def __exit__(self, *args):
                self.end = time.time()
                self.secs = self.end - self.start
                self.msecs = self.secs * 1000 # millisecs
                if self.verbose:
                        print 'elapsed time: %f ms' % self.msecs
```
***
```python
#python_time_test0.py
from timer import Timer
from redis import Redis
rdb = Redis()

with Timer() as t:
    rdb.lpush("foo", "bar")
print "=> elasped lpush: %s s" % t.secs

with Timer() as t:
   print rdb.lpop("foo")
print "=> elasped lpop: %s s" % t.secs
```
顺便说一个time模块下的clock()函数，windows下推荐用time.clock代替time.time

## 1.3 python模块timeit

测量一段代码的运行时间，在python内可以直接使用timeit。

```python
import timeit
timeit.timeit("x = range(100)")
```
***
```pypthon
0.6274833867336724
```

为什么x = range(100)的耗时会这么高？

	default_number = 1000000
***
**上边讲的三种方法都比较简单，适合做粗略统计，下面讲两个性能分析器**

***


##1.4 Python默认性能分析器cProfile

cProfile自Python 2.5以来就是标准版Python解释器默认的性能分析器，测量CPU运行时间，统计函数调用次数，不关心内存相关信息。尽管如此，它是性能优化过程中一个近似于标准化的起点，绝大多数时候这个都能为我们的分析工作提供有力支持。

- 在py代码中使用

```python
#cprofiler_inpy.py
import cProfile
import re
def test():
	for i in xrange(10**6):
		re.compile("foo|bar")	
cProfile.run('test()')
```
***
>结果太长，实际演示
```shell
ncalls：表示函数调用的次数；
tottime：表示指定函数的总的运行时间，除掉函数中调用子函数的运行时间；
percall：（第一个percall）等于 tottime/ncalls；
cumtime：表示该函数及其所有子函数的调用运行的时间，即函数开始调用到返回的时间；
percall：（第二个percall）即函数运行一次的平均时间，等于 cumtime/ncalls；
filename:lineno(function)：每个函数调用的具体信息；
```
**tips：原生（primitive）调用，表明这些调用不涉及递归**
- 在命令行使用

  使用的Python脚本就是刚才在讲time模块的时候Redis的例子
```python
# 直接把分析结果打印到控制台
python -m cProfile python_time_test0.py
# 把分析结果保存到文件中
python -m cProfile -o result.prf python_time_test0.py
# 增加排序方式
python -m cProfile -s tottime python_time_test0.py
```
***
![](pics\cProfile.png)
***

##1.5 第三方性能分析器line_profiler
核心就在于line这个单词，这个性能分析器和cProfile不同。它可以帮助你一行一行地分析函数性能。cProfile主要关注函数的性能，如果你的程序性能瓶颈出现在某一行python代码中，line_profiler显得非常恰当。
- 安装
  使用pip安装，linux直接pip  install  line_profiler

  windows下pip安装，可能的失败情况：

```shell
error: Microsoft Visual C++ 9.0 is required
```

  Windows下，依赖VS编译，可以调整环境变量
```shell
  VS90COMNTOOLS
  #系统中的VS安装路径
  C:\Program Files (x86)\Microsoft Visual Studio 14.0\Common7\Tools 
```
  或者访问 http://aka.ms/vcpython27 去下载编译支持包
- 使用：line_profiler的作者建议使用其中的kernprof工具，下边的介绍也是基于kernprof的

(1) 修改源代码, 待测试函数上增加@profile   

```python
#line_profiler_test.py
@profile
def line_profiler():
    rs = 0
    for i in range(100*100):
        rs += i
    print rs
if __name__ == "__main__":
    line_profiler()
```
(2) 命令行调用   

```python

python  kernprof.py   -l  -v  line_profiler_test.py

#-l 选项通知kernprof注入@profile装饰器

#-v 选项通知kernprof在脚本执行完毕的时候显示计时信息
```
- 效果
  ![line_profiler](pics\line_profiler.png)

#2. 内存分析

##2.1 内存占用变化memory_profiler
现在机器学习和深度学习很火热，很多学习任务比较吃内存，memory_profiler这种场景下可以起到一定作用

- 安装
```python
pip install memory_profiler
```
- 使用

```python
python -m memory_profiler memory_profiler_test.py
```
- 效果
  ![](pics\memory_profiler.png)
##2.2 ”内存泄漏“objgraph


- 安装

  ```PYTHON
  pip install objgraph
  ```
  ​

  > 首先明确一个点，python中的内存问题相比于C和C++少很多。
  >
  > C或者C++内存管理由开发者负责，Python中内存管理是由Python解释器负责，所以开发人员从内存事务中解脱出来，使得错误更少，程序更健壮，开发周期更短。

+ Python 垃圾回收算法：

  - 引用计数
  - 标记清除
  - 分代回收

- python可能出现的内存泄漏：
  (1)所用到的用 C 语言开发的底层模块中出现了内存泄漏

  (2)代码中用到了全局的 list、 dict 或其它容器，不停的往这些容器中插入对象，而忘记了在使用完之后进行删除回收

- 借助pdb调试，常用的pdb命令

  p(print) 查看一个变量值 
  n(next) 下一步
  s(step) 单步,可进入函数
  c(continue)继续前进
  l(list)看源代码



```python
#memLeak.py
import pdb
class MyBigFatObject(object):
	def __init__(self):
		self.data =  [2] * (2 * 10 ** 7)

def computate_something(_cache={}):
	_cache["default"] = dict(foo=MyBigFatObject(),
	                  bar=MyBigFatObject())
	x = MyBigFatObject()

def test():
	pdb.set_trace()
	print "b"
	computate_something()
	print "f"	
if __name__ == '__main__':
	test()
```
***
	#显示距离上次执行此命令之间生成的对象
	objgraph.show_growth()
#3. 可视化工具
##3.1 log分析Runsnakerun

-安装
依赖wxpython
可以直接在网页上下载安装包,这里介绍下choco下的安装：
+ 安装choco

    安装powshell，然后在cmd命令下输入下边的命令
```shell
  @powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
```
```shell
choco install wxpython
```
- 使用
  python  runsnake.py  result.prf
##3.2 可视化工具pycallgraph

安装过程略(依赖graphviz)
```python
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

with PyCallGraph(output=GraphvizOutput()):
    code_to_profile()
```
***
![](pics\pycallgraph.png)