import os
from ROOT import TFile, kGreen,TLatex, TGraph, TTree, TH1F, TH2F, TCanvas, TChain, TMath, TLorentzVector, AddressOf, gROOT, TNamed, gStyle, TLegend
import glob


def getEvents(file,hist):
    f=TFile.Open(file,'read')
    temp_hist=f.Get(hist)
    TotalEv=temp_hist.Integral()
    return TotalEv

lumi=35.9*1000

def getExpectedEvents(eff,cross,lumi):
    expEvents=eff*cross*lumi
    return expEvents

CrossSec={'MH4_150':0.3217,'MH4_200':0.2453,'MH4_250':0.1758,'MH4_300':.1224,'MH4_350':0.08198,'MH4_400':0.0423,'MH4_500':0.005887}
def getCross(file):
    MH4=file.split('/')[-1].strip('.root').split('_')[-4]
    XSec=CrossSec['MH4_'+str(MH4)]
    return XSec,MH4

bkg=False


path='/Users/dekumar/cernbox/Limit_work/Files/*.root'
files=sorted(glob.glob(path))

for file in files:
    if 'met_sr2' in file:
        print (file)

        DIBOSON=getEvents(file,'DIBOSON')
        print ('%.2f' % DIBOSON)
        Top=getEvents(file,'TT')
        print ('%.2f' % Top)
        STop=getEvents(file,'STop')
        print ('%.2f' % STop)
        WJets=getEvents(file,'WJets')
        print ('%.2f' % WJets)
        DYJets=getEvents(file,'DYJets')
        print ('%.2f' % DYJets)
        ZJets=getEvents(file,'ZJets')
        print ('%.2f' % ZJets)
        GJets=getEvents(file,'GJets')
        print ('%.2f' % GJets)
        QCD=getEvents(file,'QCD')
        print ('%.2f' % QCD)
        bkg=True

for file in files:
    tempfile=open('monoH_MH4_xx_MH3_600.txt')
    if 'MH4_100' in file.split('/')[-1]: continue

    if '2HDMa_gg_tb_1p0' in file.split('/')[-1] and bkg:
        # print (file)
        selEvents=getEvents(file,'h_met_sr2_')
        TotalEvents=getEvents(file,'h_total_weight')

        eff=(float (selEvents))/(float (TotalEvents))
        print ("sel",eff)
        XSec,MH4 = getCross(file)
        ggHDM=getExpectedEvents(eff,XSec,lumi)
        print ('%.4f' % ggHDM)

        fout=open('monoH_MH4_'+str(MH4)+'_MH3_600.txt','w')
        for line in tempfile:
            if 'rate' in line:
                fout.write('rate'+'                           '+str('%.4f' % ggHDM)+'        '+str('%.4f' % DIBOSON)+'       '+str('%.4f' % Top)+'      '+str('%.4f' % STop)+'       '+str('%.4f' % WJets)+'       '+str('%.4f' % DYJets)+'       '+str('%.4f' % ZJets)+'       '+str('%.4f' % GJets)+'       '+str('%.4f' % QCD)+'\n')
            else:
                fout.write(line)

        fout.close()
        tempfile.close()
