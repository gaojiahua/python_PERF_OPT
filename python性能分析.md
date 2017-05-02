#Python性能分析

​															stevegao(高家华)

***
#1. 运行时间
##1.1 Shell 命令time
- test_shell_time0.py
```python
rs = 0
for i in range(100*100):
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
##1.3 Python自带模块cProfile
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
```shell
ncalls：表示函数调用的次数；
tottime：表示指定函数的总的运行时间，除掉函数中调用子函数的运行时间；
percall：（第一个percall）等于 tottime/ncalls；
cumtime：表示该函数及其所有子函数的调用运行的时间，即函数开始调用到返回的时间；
percall：（第二个percall）即函数运行一次的平均时间，等于 cumtime/ncalls；
filename:lineno(function)：每个函数调用的具体信息；
```
##1.4 Python第三方模块line_profiler
- 安装
  使用pip安装，linux直接pip  install  line_profiler

  可能的失败情况：

  ![](pics\pip_line_profiler.png)

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