#encoding=utf-8
import sys,os
import timer
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
if __name__ == "__main__":
	with timer.Timer() as t:
		for i in xrange(100000):
			l = [6,4,2,1,7,8,9,3,0,5]
			rs = quick_sort(l, 0 , len(l)-1)
			#rs = sorted(l)
		print rs
	print "=> quick_sort: %s s" % t.secs
	
	with timer.Timer() as t:
			for i in xrange(100000):
				l = [6,4,2,1,7,8,9,3,0,5]
				#rs = quick_sort(l, 0 , len(l)-1)
				rs = sorted(l)
			print rs
	print "=> sorted: %s s" % t.secs	