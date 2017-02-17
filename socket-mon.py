import psutil
from collections import namedtuple
import pandas 
import re
import os

f = open('conn_details.csv', 'w')
sconn = namedtuple('sconn', 'fd family type laddr raddr status pid')
conn = psutil.net_connections(kind='tcp') #fetching TCP socket connection details created by web applications
for n in conn:
  b = [n.pid, n.laddr, n.raddr, n.status]
  if b[2] != (): #filtering out data that does not have socket connections
    print >>f, ("'%s','%s','%s','%s'" % (n.pid, '@'.join(map(str, n.laddr)), '@'.join(map(str,n.raddr)), n.status)) 

f.close()

#Using 'Python Pandas' methods for read file, groupby and sort
cols = ['pid','laddr','raddr','status']
data = pandas.read_csv('conn_details.csv', index_col=False, header=None, names=cols)
g = data.groupby('pid').size().sort_values(ascending=False).reset_index(name='Count') #Creating dataframe g that groups PID in order of number of connections it has based on column 'Count'

f1 = open('out.txt', 'w')
dg = data.groupby('pid') #returns a dictionary with 'pid' as key and connection details as values
for index, row in g.iterrows(): #iterating through g dataframe that has 'pid' and 'Count'
  k = row['pid']
  print >>f1, dg.get_group(k) # returns groups based on key 'pid' and writing it to a file 'out.txt'
f1.close()

input_file = open('out.txt', 'r') #Reading grouped and ordered data from 'out.txt' and processing it using regular expression 
print '\"pid\",\"laddr\",\"raddr\",\"status\"'
for line in input_file:
  matchobj = re.match(r"^\d+\s+\'(.*)\'\s+\'(.*)\'\s+\'(.*)\'\s+\'(.*)\'$",line)
  if matchobj:
    print ("\"%s\",\"%s\",\"%s\",\"%s\"" % (matchobj.group(1),matchobj.group(2),matchobj.group(3),matchobj.group(4)))

#removing all temporary files used for storing unprocessed output
os.remove("conn_details.csv")
os.remove("out.txt")

 



 





