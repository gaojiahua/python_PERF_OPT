#Python性能分析

​															stevegao(高家华)

***
# 前言

- 什么是性能分析

- python性能分析的重不重要



#1. 运行时间
- 运行时间复杂度

  | 名称     | 复杂度       | 算法举例         |
  | ------ | :-------- | :----------- |
  | 常数时间   | O(1)      | 判断一个数是基数还是偶数 |
  | 对数时间   | O(logn)   | 二分查找         |
  | 线性时间   | O(n)      | 查找无序列表的最小元素  |
  | 线性对数时间 | O(n logn) | 快速排序(平均时间)   |
  | 平方时间   | O(n2)     | 插入排序         |

##1.1 Shell 命令time
linux shell  time命令常用于测量一个命令的运行时间，注意不是用来显示和修改系统时间的，不仅仅用于python其他命令也可以测试。

![](pics\time_ls.png)

- test_shell_time0.py
```python
rs = 0
for i in xrange(100*100):
    rs += i
print rs
```
![](pics\time0.png)

- test_shell_time1.py
```python
from time import *
sleep(2)
```
![](pics\time1.png)
- 一点结论
  + real != user + sys
  + real 和 user + sys的值越接近，证明程序越重计算，反之说明程序更重IO

##1.2 Python自带模块time

time. time() 返回当前时间的时间戳（1970纪元后经过的浮点秒数）
- time_demo.py  
>time函数的作用
```python
import time
print time.time()
print time.asctime( time.localtime(time.time()) )
print time.asctime( time.localtime(0) )
```
***
    1493454752.49
    Sat Apr 29 16:32:32 2017
    Thu Jan 01 08:00:00 1970
- time.time()的简单应用
```python
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

为什么x = range(100)的耗时会这么高，默认循环1000000次。

	default_number = 1000000
***
**上边讲的三种方法都比较简单，适合做粗略统计，下面讲两个性能分析器**

***


##1.4 Python默认性能分析器cProfile

cProfile自Python 2.5以来就是标准版Python解释器默认的性能分析器，测量CPU，统计函数调用次数，不关心内存相关信息。尽管如此，它是性能优化过程中一个近似于标准化的起点，绝大多数时候这个分析工具都可以快速为我们提供一组优化方案。

- 在py代码中使用

```python
#cprofiler_inpy.py
import cProfile
import re
cProfile.run('re.compile("foo|bar")')
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
- 使用

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

python  kernprof.py   -l  -v  xxx.py

#-l 选项通知kernprof注入@profile装饰器

#-v 选项通知kernprof在脚本执行完毕的时候显示计时信息
```
- 效果
  ![line_profiler](pics\line_profiler.png)

#2. 内存占用

##2.1 内存占用memory_profiler
现在机器学习和深度学习很火热，很多学习任务比较吃内存，memory_profiler这种场景下可以起到一定作用

- 安装
```python
pip install memory_profiler
```
- 使用

```python
python -m memory_profiler memory_profiler_test.py
```
![](pics\memory_profiler.png)
##2.2 内存泄漏objgraph
- 安装

  ```PYTHON
  pip install objgraph
  ```
- python可能出现的内存泄露：
  (1)所用到的用 C 语言开发的底层模块中出现了内存泄露
  (2)代码中用到了全局的 list、 dict 或其它容器，不停的往这些容器中插入对象，而忘记了在使用完之后进行删除回收
  (3)代码中有“引用循环”

```python
#memLeak.py
#import pdb
class MyBigFatObject(object):
	def __init__(self):
		self.data =  [2] * (2 * 10 ** 7)

def computate_something(_cache={}):
	_cache[42] = dict(foo=MyBigFatObject(),
	                  bar=MyBigFatObject())
	x = MyBigFatObject()
@profile
def test():
	#pdb.set_trace()
	print "b"
	computate_something()
	print "f"	
if __name__ == '__main__':
	test()
```
***
	#显示距离上次执行此命令之间生成的对象
	objgraph.show_growth()
#3. 可视化工具与日志分析
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