#panda_test.py
import pandas as pd
import time
import csv
import collections
import  os
SOURCE_FILE = os.sys.path[0] + '\\311.csv'

def readCSV(fname):
    with open(fname, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        lines = [line for line in reader]
        return lines

def process(fname):
    content = readCSV(fname)
    incidents_by_zipcode = collections.defaultdict(int)
    for record in content:
        incidents_by_zipcode[toFloat(record['Incident Zip'])] += 1
    return sorted(incidents_by_zipcode.items(), reverse=True, key=lambda a: int(a[1]))[:10]

def toFloat(number):
    try:
        return int(float(number))
    except:
        return 0

def process_pandas(fname):
    df = pd.read_csv(fname, dtype={
                     'Incident Zip': str, 'Landmark': str, 'Vehicle Type': str, 'Ferry Direction': str})
    df['Incident Zip'] = df['Incident Zip'].apply(toFloat)
    column_names = list(df.columns.values)
    column_names.remove("Incident Zip")
    column_names.remove("Unique Key")
    return df.drop(column_names, axis=1).groupby(['Incident Zip'], sort=False).count().sort('Unique Key', ascending=False).head(10)

init = time.clock()
total = process(SOURCE_FILE)
endtime = time.clock() - init
for item in total:
    print "%s\t%s" % (item[0], item[1])

print "(Pure Python) time: %s" % (endtime)

init = time.clock()
total = process_pandas(SOURCE_FILE)
endtime = time.clock() - init
print total
print "(Pandas) time: %s" % (endtime)