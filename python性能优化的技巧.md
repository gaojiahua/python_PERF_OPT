#Python性能优化技巧及原理
​															stevegao(高家华)
***
#1 少造轮子
##1.1 二分查找
二分查找是大家比较容易接触到的一个算法，应用也很广泛。
- 一个轮子：

```python
def bsearch(a, x, lo=0, hi=None):
	if lo < 0:
		raise ValueError('lo must be non-negative')
	if hi is None:
		hi = len(a)
	while lo < hi:
		mid = (lo+hi)//2
		if a[mid] < x: lo = mid+1
		else: hi = mid
	return lo
```
***
- 使用库函数：
```python
import bisect
bisect.bisect_left(a,k)
```
***
- 性能测试：
```python
with timer.Timer() as t:
    a = range(1000*1000)
    for i in xrange(1000*1000):
        k = 100
        bisect.bisect_left(a,k)# or bsearch(a, k)
print "=> bisect: %s s" % t.secs
```
- 测试结果
  ![](pics\bisect.png)
***
- **原因分析**

  + 源码分析  Python-src\Modules\_bisectmodule.c
  + python调试演示
  + windows c语言python源码调试演示

##1.2 排序
- 一个轮子
```python
def quick_sort(lists, left, right):
    # 快速排序
    if left >= right:
        return lists
    key = lists[left]
    low = left
    high = right
    while left < right:
        while left < right and lists[right] >= key:
            right -= 1
        lists[left] = lists[right]
        while left < right and lists[left] <= key:
            left += 1
        lists[right] = lists[left]
    lists[right] = key
    quick_sort(lists, low, left - 1)
    quick_sort(lists, left + 1, high)
    return lists
```
- 对应的库函数
```python
l = [6,4,2,1,7,8,9,3,0,5]
rs = sorted(l)
```
- 执行1000次性能测试
  ![](pics/qsort.png)
- 原因分析：
  + python源码定位
```python
Python-src\Python\bltinmodule.c      builtin_sorted
Python-src\Objects\listobject.c		 PyList_Sort
```
   ***
#2. 使用效率更高的语法
##2.1 字符串连接
- 效率不好的语法
```python
s = ""
for x in somelist:
    s += x
```
- 效率改进
```python
s = "".join(slist)
```
##2.2 range和xrange（python3不适用）
- 效率不好的语法
```python
for i in range(1000):
	dosomething()
```
- 效率改进
```python
for i in xrange(1000):
	dosomething()
```
##2.3 推导式
- 将列表中的所有单词变成大写的一般写法
```python
newlist = []
for word in oldlist:
    newlist.append(word.upper())
```
- 使用列表推导
```python
newlist = [s.upper() for s in oldlist]
```
- 带if语句的列表推导
```python
names = ['Bob','Tom','alice','Jerry','Wendy','Smith']
newlist = []
for name in names:
    if len(name) > 3:
        newlist.append(name.upper())
```
***
```python
names = ['Bob','Tom','alice','Jerry','Wendy','Smith'] 
newlist = [name.upper() for name in names if len(name)>3]  
```
- 字典推导
```python
strings = ['import','is','with','if','file','exception']  
D = {key: val for val,key in enumerate(strings)}  
>>> D  
{'exception': 5, 'is': 1, 'file': 4, 'import': 0, 'with': 2, 'if': 3}  
```
- 集合推导
```python
strings = ['a','is','with','if','file','exception']  
S = {len(s) for s in strings}
>>>S
set([1, 2, 4, 9])#set 没有重复项
```
##2.4 循环优化
- 一般写法
```python
for x in xrange(0, 100):
    doSomethingWithX(x)
```
***
- 进行优化
  map()接收一个函数 f 和一个 list，并通过把函数 f 依次作用在 list 的每个元素上，得到一个新的 list 并返回
```python
map(doSomethingWithX, xrange(0,100))
```
##2.5 生成器
//TODO
#3 python脚本运行方式

##3.1 pypy
##3.2 Cython