oldlist =  ['Bob','Tom','alice','Jerry','Wendy','Smith']
newlist = []
for word in oldlist:
	newlist.append(word.upper())
print "for append\n%s"%newlist

oldlist =  ['Bob','Tom','alice','Jerry','Wendy','Smith']
newlist = map(lambda x: x.upper(),oldlist)
print "map\n%s"%newlist


oldlist =  ['Bob','Tom','alice','Jerry','Wendy','Smith']
newlist = [s.upper() for s in oldlist]		
print "list compre\n%s"%newlist