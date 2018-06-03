import os
import glob

path='/home/dekumar/deepak/MonoH/bbDM/bbMET/BR_Condor_Farmout/output/*.out'

files=sorted(glob.glob(path))

counts=[]

for file in files:
    f=open(file,'r')
    last_line=f.readlines()[-1]
    if not str(last_line.split()[0])=='Completed.':
        print "======Please check this cluster Id(Not finished) in error directory"
        print file.split('/')[-1]
        counts.append(1)

print "Total errors:  ", len(counts)
