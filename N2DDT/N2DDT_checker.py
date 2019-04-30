#!/usr/bin/env python
from ROOT import TFile, TTree, TH1F, TH1D, TH1, TCanvas, TChain,TGraphAsymmErrors, TMath, TH2D, TLorentzVector, TF1, AddressOf
import ROOT as ROOT
import os
import random
import sys, optparse
from array import array
import math

ROOT.gROOT.SetBatch(True)


c = ROOT.TCanvas()
c.SetLogz()


h_N2 = TH1D("h_N2","h_N2_",500, 0, 0.5)
h_AK8PT = TH1D("h_AK8","h_AK8_",1000, 0, 1000)
h_CA15PT = TH1D("h_CA15PT","h_CA15PT",1000, 0, 1000)

pileup2016file = TFile('pileUPinfo2016.root')
pileup2016histo=pileup2016file.Get('hpileUPhist')


ROOT.gROOT.ProcessLine('.L BTagCalibrationStandalone.cpp+')

usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)

## data will be true if -d is passed and will be false if -m is passed
parser.add_option("-i", "--inputfile",  dest="inputfile")
parser.add_option("-o", "--outputfile", dest="outputfile")
parser.add_option("-D", "--outputdir", dest="outputdir")

parser.add_option("-a", "--analyze", action="store_true",  dest="analyze")

parser.add_option("-e", "--efficiency", action="store_true",  dest="efficiency")
parser.add_option("-F", "--farmout", action="store_true",  dest="farmout")
parser.add_option("-t", "--table", action="store_true",  dest="table")
parser.add_option("-P", "--OtherPlots", action="store_true",  dest="OtherPlots")
'''
parser.add_option("--csv", action="store_true",  dest="CSV")
parser.add_option("--deepcsv", action="store_true",  dest="DeepCSV")
'''

(options, args) = parser.parse_args()

if options.farmout==None:
    isfarmout = False
else:
    isfarmout = options.farmout
'''
if options.CSV==None:
    options.CSV = False

if options.DeepCSV==None:
    options.DeepCSV = False
'''

#if not options.SE and not options.MET and not options.SP:
    #print "Please run using --se or --met or --sp. Exiting."
    #sys.exit()
'''
if options.CSV: print "Using CSVv2 as b-tag discriminator."
if options.DeepCSV: print "Using DeepCSV as b-tag discriminator."

if not options.CSV and not options.DeepCSV:
    print "Please run using --csv or --deepcsv. Exiting."
    sys.exit()
'''

inputfilename = options.inputfile
outputdir = options.outputdir

pathlist = inputfilename.split("/")
sizeoflist = len(pathlist)
#print ('sizeoflist = ',sizeoflist)
rootfile='tmphist'
rootfile = pathlist[sizeoflist-1]
textfile = rootfile+".txt"

#outputdir='bbMETSamples/'
if outputdir!='.': os.system('mkdir -p '+outputdir)

if options.outputfile is None or options.outputfile==rootfile:
    if not isfarmout:
        outputfilename = "/Output_"+rootfile
    else:
        outputfilename = "/Output_"+rootfile.split('.')[0]+".root"
else:
    outputfilename = "/"+options.outputfile

#if isfarmout:
outfilename = outputdir + outputfilename
print "Input:",options.inputfile, "; Output:", outfilename

skimmedTree = TChain("outTree")

def WhichSample(filename):
    samplename = 'all'
    if filename.find('WJets')>-1:
        samplename = 'WJETS'
    elif filename.find('ZJets')>-1 or filename.find('DYJets')>-1:
        samplename = 'ZJETS'
    elif filename.find('TT')>-1:
        samplename  = 'TT'
    else:
        samplename = 'all'
#    print samplename
    return samplename

h_t = TH1F('h_t','h_t',2,0,2)
h_t_weight = TH1F('h_t_weight','h_t_weight',2,0,2)

samplename = 'all'
if isfarmout:
    infile = open(inputfilename)
    failcount=0
    for ifile in infile:
        try:
            f_tmp = TFile.Open(ifile.rstrip(),'READ')
            if f_tmp.IsZombie():            # or fileIsCorr(ifile.rstrip()):
                failcount += 1
                continue
            skimmedTree.Add(ifile.rstrip())
            h_tmp = f_tmp.Get('h_total')
            h_tmp_weight = f_tmp.Get('h_total_mcweight')
            h_t.Add(h_tmp)
            h_t_weight.Add(h_tmp_weight)
        except:
            failcount += 1
    if failcount>0: print "Could not read %d files. Skipping them." %failcount

if not isfarmout:
    skimmedTree.Add(inputfilename)
#    samplename = WhichSample(inputfilename)
    ## for histograms
    f_tmp = TFile.Open(inputfilename,'READ')
    h_tmp = f_tmp.Get('h_total')
    h_tmp_weight = f_tmp.Get('h_total_mcweight')
    h_t.Add(h_tmp)
    h_t_weight.Add(h_tmp_weight)

debug = False

try:
    samplepath = str(f_tmp.Get('samplepath').GetTitle())
    if not isfarmout: print "Original source file: " + samplepath
except:
#    samplepath=inputfilename
    samplepath='TT'
    print "WARNING: Looks like the input was skimmed with an older version of SkimTree. Using " + samplepath + " as sample path. Gen pT Reweighting may NOT work."

samplename = WhichSample(samplepath)
print "Dataset classified as: " + samplename

def AnalyzeDataSet():

    NEntries = skimmedTree.GetEntries()
    print 'NEntries = '+str(NEntries)
    npass = 0


    for ievent in range(NEntries):
        skimmedTree.GetEntry(ievent)
        try:
            if ievent%100==0: print (ievent)

            #CA15jets
#            CA15njets                 = skimmedTree.__getattr__('st_CA15njets')
#            CA15jetP4                 = skimmedTree.__getattr__('st_CA15jetP4')
            CA15SDmass                = skimmedTree.__getattr__('st_CA15SDmass')
#            CA15Puppi_doublebtag      = skimmedTree.__getattr__('st_CA15Puppi_doublebtag')
            CA15PuppiECF_1_2_10        = skimmedTree.__getattr__('st_CA15PuppiECF_1_2_10')
            CA15PuppiECF_2_3_10        = skimmedTree.__getattr__('st_CA15PuppiECF_2_3_10')

            isData                     = skimmedTree.__getattr__('st_isData')
            mcWeight                   = skimmedTree.__getattr__('mcweight')
            pu_nTrueInt                = int(skimmedTree.__getattr__('st_pu_nTrueInt'))

            #AK8JET

#            AK8thikjetP4               = skimmedTree.__getattr__('st_AK8thikjetP4')
#            AK8SDmass                  = skimmedTree.__getattr__('st_AK8SDmass')
#            AK8Puppijet_DoubleSV       = skimmedTree.__getattr__('st_AK8Puppijet_DoubleSV')

        except Exception as e:
            print e
            print "Corrupt file detected! Skipping 1 event."
            continue


        # print ("nCA15Jets:  ",CA15njets, ":",len(CA15PuppiECF_1_2_10))
        #if CA15SDmass > 100 and CA15SDmass < 150:

	puweight = 0.0
	mcWeight = 0.0
        
        if isData: 
	    puweight = 1.0
   	    mcWeight = 1.0
        if not isData:
		if mcWeight<0:  mcweight = -1.0
		if mcWeight>0:  mcweight =  1.0

		if pu_nTrueInt < 100:
		    puweight = pileup2016histo.GetBinContent(pu_nTrueInt)
		else:
		    puweight = 1.
        Weight = puweight*mcWeight
	if Weight==0:
		Weight=1.0

	myN2=[]
        if len(CA15PuppiECF_2_3_10)==0: continue
        for i in range(len(CA15PuppiECF_2_3_10)):
		if CA15SDmass[i] > 100.0 and CA15SDmass[i] < 150.0 :
                    print ("N2 variable:   ", CA15PuppiECF_2_3_10[i]/(CA15PuppiECF_1_2_10[i])**2)
 		    try:
                	N2=CA15PuppiECF_2_3_10[i]/(CA15PuppiECF_1_2_10[i])**2
                        N2DDT=N2-0.24
                        #h_N2.Fill(N2,Weight)
			myN2.append(N2)
		    except Exception as e:
                        N2DDT=99999
                        continue

	if len(myN2)!=1: continue
	h_N2.Fill(myN2[0],Weight)


#        myca15jetsP4=[]
#        for ca15jet in range(CA15njets):
#            if N2DDT < 0 and CA15jetP4[ca15jet].Pt() > 200. and abs(CA15jetP4[ca15jet].Eta()) < 2.4 and CA15SDmass[ca15jet] > 100. and CA15SDmass[ca15jet] < 150. and CA15Puppi_doublebtag[ca15jet] > 0.75:
#                        myca15jetsP4.append(CA15jetP4[ca15jet])
#        mynCA15=len(myca15jetsP4)
#
#        ak8jets=[]
#        for ak8jet in range(len(AK8thikjetP4)):
#            if N2DDT < 0 and AK8thikjetP4[ak8jet].Pt() > 200. and abs(AK8thikjetP4[ak8jet].Eta()) < 2.4 and AK8SDmass[ak8jet] > 100. and AK8SDmass[ak8jet] < 150. and AK8Puppijet_DoubleSV[ak8jet] > 0.6:
#                        ak8jets.append(AK8thikjetP4[ak8jet])
#        mynAK8=len(ak8jets)

    f = TFile(outfilename,'RECREATE')
    f.cd()
    h_N2.Write()

#    h_t_weight.Write()
#    h_t.Write()
#    h_AK8PT.Write()
#    h_CA15PT.Write()

    #h_N2.Draw()
    # c.SaveAs("N2_Distribution.pdf")
    # c.SaveAs("N2_Distribution.png")

if __name__ == "__main__":
    ## analyze the tree and make histograms and all the 2D plots and Efficiency plots.
    if options.analyze:
        print "now calling analyzedataset"
        AnalyzeDataSet()
