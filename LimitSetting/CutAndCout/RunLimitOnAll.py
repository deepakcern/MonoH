import sys 
import os 

os.system('rm bin/limits_monoH2016.txt')
#os.system('rm bin/limits_bbDM2016pseudo.txt')

def createAndrunSetup(signalStr):
    fout = open('datacard_bbDM_2016_'+signalStr+'.txt', 'w')
    
    for iline in open('comb_tmpl.txt'):
        iline = iline.replace("SIGNALPOINT", signalStr)
        fout.write(iline)


signal_ = ['MH4_150_MH3_600','MH4_200_MH3_600','MH4_250_MH3_600','MH4_300_MH3_600','MH4_350_MH3_600','MH4_400_MH3_600','MH4_500_MH3_600']
## add signal mass point histograms here if you want to extent the analysis 

if len(sys.argv) > 1:
    if sys.argv[1]=='create':
        print "Please use CardMaker.py file"
        #for sig in signal_:
            #createAndrunSetup(sig)
    if sys.argv[1]=='run':
        for sig in signal_:
            datacardname = 'datacard_monoH_2016_'+sig+'.txt'
            command_ = 'python scan.py '+datacardname
            os.system(command_)
