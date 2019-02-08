#!/usr/bin/env python
from ROOT import TFile, TTree, TH1F, TH1D, TH1, TCanvas, TChain,TGraphAsymmErrors, TMath, TH2D, TLorentzVector, TF1, AddressOf
import ROOT as ROOT
import os
import random
import sys, optparse
from array import array
import math
import AllVariables
from AllHists import *


ROOT.gROOT.SetBatch(True)

ROOT.gROOT.LoadMacro("Loader.h+")

usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)


parser.add_option("-i", "--inputfile",  dest="inputfile")
parser.add_option("-o", "--outputfile", dest="outputfile")
parser.add_option("-D", "--outputdir", dest="outputdir")
parser.add_option("-F", "--farmout", action="store_true",  dest="farmout")

(options, args) = parser.parse_args()


if options.farmout==None:
    isfarmout = False
else:
    isfarmout = options.farmout


inputfilename = options.inputfile
outputdir = options.outputdir


pathlist = inputfilename.split("/")
sizeoflist = len(pathlist)
#print ('sizeoflist = ',sizeoflist)
rootfile='tmphist'
rootfile = pathlist[sizeoflist-1]
textfile = rootfile+".txt"

if outputdir!='.': os.system('mkdir -p '+outputdir)

if options.outputfile is None or options.outputfile==rootfile:
    if not isfarmout:
        outputfilename = "/Output_"+rootfile
    else:
        outputfilename = "/Output_"+rootfile.split('.')[0]+".root"
else:
    outputfilename = "/"+options.outputfile



outfilename = outputdir + outputfilename
#else:
#    outfilename = options.outputfile

print "Input:",options.inputfile, "; Output:", outfilename


#outfilename= 'SkimmedTree.root'
skimmedTree = TChain("tree/treeMaker")

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
        except:
            failcount += 1
    if failcount>0: print "Could not read %d files. Skipping them." %failcount

if not isfarmout:
    skimmedTree.Add(inputfilename)


#
# skimmedTree.Add(sys.argv[1])

def arctan(x,y):
    corr=0
    if (x>0 and y>=0) or (x>0 and y<0):
        corr=0
    elif x<0 and y>=0:
        corr=math.pi
    elif x<0 and y<0:
        corr=-math.pi
    if x!=0.:
        return math.atan(y/x)+corr
    else:
        return math.pi/2+corr

def getPT(P4):
    return P4.Pt()


def AnalyzeDataSet():


    allquantities = trigeerTurnOn(outfilename)
    allquantities.defineHisto()

    triglist=['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_v','HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v','HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v']
    triglist_mu=['HLT_IsoMu24_v']

    outfile = TFile(outfilename,'RECREATE')
    #
    # outTree = TTree( 'outTree', 'tree branches' )
    # samplepath = TNamed('samplepath', str(sys.argv[1]))

    NEntries = skimmedTree.GetEntries()
    #NEntries = 1000
    print 'NEntries = '+str(NEntries)
    npass = 0

    for ievent in range(NEntries):


#    print "\n*****\nWARNING: *Test run* Processing 200 events only.\n*****\n"
#    for ievent in range(200):
        if ievent%100==0: print "Processed "+str(ievent)+" of "+str(NEntries)+" events."
        skimmedTree.GetEntry(ievent)
        ## Get all relevant branches
        try:

            run                        = skimmedTree.__getattr__('runId')
            lumi                       = skimmedTree.__getattr__('lumiSection')
            event                      = skimmedTree.__getattr__('eventId')
    #        print "Run:"+str(run)+"; Lumi:"+str(lumi)+"; Event:"+str(event)
            trigName                   = skimmedTree.__getattr__('hlt_trigName')
            trigResult                 = skimmedTree.__getattr__('hlt_trigResult')
            filterName                 = skimmedTree.__getattr__('hlt_filterName')
            filterResult               = skimmedTree.__getattr__('hlt_filterResult')


            pfMet                      = skimmedTree.__getattr__('pfMetCorrPt')
            pfMetPhi                   = skimmedTree.__getattr__('pfMetCorrPhi')
            pfMetJetUnc                = skimmedTree.__getattr__('pfMetCorrUnc')


            nTHINJets                  = skimmedTree.__getattr__('THINnJet')
            thinjetP4                  = skimmedTree.__getattr__('THINjetP4')
            thinJetCSV                 = skimmedTree.__getattr__('THINjetCISVV2')
            thinJetdeepCSV             = skimmedTree.__getattr__('THINjetDeepCSV_b')
            passThinJetTightID         = skimmedTree.__getattr__('THINjetPassIDTight')
            THINjetHadronFlavor        = skimmedTree.__getattr__('THINjetHadronFlavor')
            THINjetNPV                 = skimmedTree.__getattr__('THINjetNPV')         #int()
            thinjetNhadEF              = skimmedTree.__getattr__('THINjetNHadEF')
            thinjetChadEF              = skimmedTree.__getattr__('THINjetCHadEF')
            thinjetCEmEF               = skimmedTree.__getattr__('THINjetCEmEF')
            thinjetPhoEF               = skimmedTree.__getattr__('THINjetPhoEF')
            thinjetEleEF               = skimmedTree.__getattr__('THINjetEleEF')
            thinjetMuoEF               = skimmedTree.__getattr__('THINjetMuoEF')
            thinjetCorrUnc             = skimmedTree.__getattr__('THINjetCorrUncUp')


            nEle                       = skimmedTree.__getattr__('nEle')
            eleP4                      = skimmedTree.__getattr__('eleP4')
            eleIsPassLoose             = skimmedTree.__getattr__('eleIsPassLoose')
            eleIsPassMedium            = skimmedTree.__getattr__('eleIsPassMedium')
            eleIsPassTight             = skimmedTree.__getattr__('eleIsPassTight')
            eleCharge                  = skimmedTree.__getattr__('eleCharge')

            nMu                        = skimmedTree.__getattr__('nMu')
            muP4                       = skimmedTree.__getattr__('muP4')
            isLooseMuon                = skimmedTree.__getattr__('isLooseMuon')
            isMediumMuon               = skimmedTree.__getattr__('isMediumMuon')
            isTightMuon                = skimmedTree.__getattr__('isTightMuon')
            muChHadIso                 = skimmedTree.__getattr__('muChHadIso')
            muNeHadIso                 = skimmedTree.__getattr__('muNeHadIso')
            muGamIso                   = skimmedTree.__getattr__('muGamIso')
            muPUPt                     = skimmedTree.__getattr__('muPUPt')
            muCharge                   = skimmedTree.__getattr__('muCharge')

            nTau                       = skimmedTree.__getattr__('HPSTau_n')
            tauP4                      = skimmedTree.__getattr__('HPSTau_4Momentum')
            isDecayModeFinding         = skimmedTree.__getattr__('disc_decayModeFinding')
            passLooseTauIso            = skimmedTree.__getattr__('disc_byLooseIsolationMVArun2017v2DBoldDMwLT2017')

            disc_againstElectronLoose  = skimmedTree.__getattr__('disc_againstElectronLooseMVA6')
            disc_againstElectronMedium = skimmedTree.__getattr__('disc_againstElectronMediumMVA6')
            disc_againstElectronTight  = skimmedTree.__getattr__('disc_againstElectronTightMVA6')
            disc_againstMuonLoose      = skimmedTree.__getattr__('disc_againstMuonLoose3')
            disc_againstMuonTight      = skimmedTree.__getattr__('disc_againstMuonTight3')

            isData                     = skimmedTree.__getattr__('isData')
            mcWeight                   = skimmedTree.__getattr__('mcWeight')
            pu_nTrueInt                = skimmedTree.__getattr__('pu_nTrueInt')         #int()
            pu_nPUVert                 = skimmedTree.__getattr__('pu_nPUVert')

        except Exception as e:
            print e
            print "Corrupt file detected! Skipping 1 event."
            continue

        trigstatus=False
        trigstatus_mu=False

        for itrig in range(len(triglist_mu)):
            exec(triglist_mu[itrig]+" = CheckFilter(trigName, trigResult, " + "'" + triglist_mu[itrig] + "')")        #Runs the above commented-off code dynamically.
            exec("if "+triglist_mu[itrig]+": trigstatus_mu=True")

        for itrig in range(len(triglist)):
            exec(triglist[itrig]+" = CheckFilter(trigName, trigResult, " + "'" + triglist[itrig] + "')")        #Runs the above commented-off code dynamically.
            exec("if "+triglist[itrig]+": trigstatus=True")

        filterstatus = False
        filter1 = False; filter2 = False;filter3 = False;filter4 = False; filter5 = False; filter6 = False; filter7 =False; filter8 = False
        ifilter_=0
        filter1 = CheckFilter(filterName, filterResult, 'Flag_HBHENoiseFilter')
        filter2 = CheckFilter(filterName, filterResult, 'Flag_globalSuperTightHalo2016Filter')
        filter3 = CheckFilter(filterName, filterResult, 'Flag_eeBadScFilter')
        filter4 = CheckFilter(filterName, filterResult, 'Flag_goodVertices')
        filter5 = CheckFilter(filterName, filterResult, 'Flag_EcalDeadCellTriggerPrimitiveFilter')
        filter6 = CheckFilter(filterName, filterResult, 'Flag_BadPFMuonFilter')
        filter7 = CheckFilter(filterName, filterResult, 'Flag_BadChargedCandidateFilter')

        filter8 = CheckFilter(filterName, filterResult, 'Flag_HBHENoiseIsoFilter')

        if not isData:
	        filterstatus = True
        if isData:
        	filterstatus = filter1 & filter2 & filter3 & filter4 & filter5 & filter6 & filter7 & filter8
        if filterstatus == False: continue

        jetCond=False
        muonCond=False
        eleCond=False
        ## Electron selection
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        myEles=[]
        for iele in range(nEle):
            if (eleP4[iele].Pt() > 30. ) & (abs(eleP4[iele].Eta()) <2.5) & (bool(eleIsPassTight[iele]) == True) :
                myEles.append(iele)
                eleCond=True

        ## Muon selection
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        myMuos = []
        for imu in range(nMu):
            if (muP4[imu].Pt()>30.) & (abs(muP4[imu].Eta()) < 2.5) & (bool(isTightMuon[imu]) == True):
                relPFIso = (muChHadIso[imu]+ max(0., muNeHadIso[imu] + muGamIso[imu] - 0.5*muPUPt[imu]))/muP4[imu].Pt()
                if relPFIso<0.25 :
                    myMuos.append(imu)
                    muonCond=True


#thin jet selection


        thinjetpassindex=[]
        myJets_ = []

        for nb in range(nTHINJets):
            #---Fake jet cleaner, wrt electrons and muons----
            isClean=True
            for imu in myMuos:
                if DeltaR(muP4[imu],thinjetP4[nb]) < 0.5:
                    isClean=False
                    break
            if not isClean: continue
            myJets_.append(nb)

        for ithinjet in myJets_:
            j1 = thinjetP4[ithinjet]
            if (j1.Pt() > 50.0) and (abs(j1.Eta())<2.5) and (bool(passThinJetTightID[ithinjet])==True) and (thinjetNhadEF[ithinjet] < 0.8) and (thinjetChadEF[ithinjet] > 0.1):
                #thinjetpassindex.append(ithinjet)
                jetCond=True

# ------------------
# Z CR
# ------------------

        ## for dielectron
        if len(myEles) == 2:

            iele1=myEles[0]
            iele2=myEles[1]
            p4_ele1 = eleP4[iele1]
            p4_ele2 = eleP4[iele2]
            if eleCharge[iele1]*eleCharge[iele2]<0:
                ee_mass = ( p4_ele1 + p4_ele2 ).M()
                zeeRecoilPx = -( pfMet*math.cos(pfMetPhi) + p4_ele1.Px() + p4_ele2.Px())
                zeeRecoilPy = -( pfMet*math.sin(pfMetPhi) + p4_ele1.Py() + p4_ele2.Py())
                ZeeRecoilPt =  math.sqrt(zeeRecoilPx**2  +  zeeRecoilPy**2)

        ## for dimu
        if len(myMuos) ==2:
            imu1=myMuos[0]
            imu2=myMuos[1]
            p4_mu1 = muP4[imu1]
            p4_mu2 = muP4[imu2]
            if muCharge[imu1]*muCharge[imu2]<0:
                mumu_mass = ( p4_mu1 + p4_mu2 ).M()
                zmumuRecoilPx = -( pfMet*math.cos(pfMetPhi) + p4_mu1.Px() + p4_mu2.Px())
                zmumuRecoilPy = -( pfMet*math.sin(pfMetPhi) + p4_mu1.Py() + p4_mu2.Py())
                ZmumuRecoilPt =  math.sqrt(zmumuRecoilPx**2  +  zmumuRecoilPy**2)


# ------------------
# W CR
# ------------------

        ## for Single electron
        if len(myEles) == 1:
           ele1 = myEles[0]
           p4_ele1 = eleP4[ele1]

           e_mass = MT(p4_ele1.Pt(),pfMet, DeltaPhi(p4_ele1.Phi(),pfMetPhi)) #transverse mass defined as sqrt{2pT*MET*(1-cos(dphi)}

           WenuRecoilPx = -( pfMet*math.cos(pfMetPhi) + p4_ele1.Px())
           WenuRecoilPy = -( pfMet*math.sin(pfMetPhi) + p4_ele1.Py())
           WenuRecoilPt = math.sqrt(WenuRecoilPx**2  +  WenuRecoilPy**2)



        ## for Single muon
        if len(myMuos) == 1:
           mu1 = myMuos[0]
           p4_mu1 = muP4[mu1]

           mu_mass = MT(p4_mu1.Pt(),pfMet, DeltaPhi(p4_mu1.Phi(),pfMetPhi)) #transverse mass defined as sqrt{2pT*MET*(1-cos(dphi)}

           WmunuRecoilPx = -( pfMet*math.cos(pfMetPhi) + p4_mu1.Px())
           WmunuRecoilPy = -( pfMet*math.sin(pfMetPhi) + p4_mu1.Py())
           WmunuRecoilPt = math.sqrt(WmunuRecoilPx**2  +  WmunuRecoilPy**2)



# append variable to fill histograms

        regquants=AllVariables.getAll()

        for quant in regquants:
            exec("allquantities."+quant+" = None")

        if trigstatus and trigstatus_mu and jetCond and muonCond and len(myMuos) ==1 :
            allquantities.frac_recoil = WmunuRecoilPt

        if jetCond and trigstatus_mu and muonCond and len(myMuos) == 1:
            allquantities.full_recoil = WmunuRecoilPt



#Fill all the Histograms
        allquantities.FillHisto()

    allquantities.WriteHisto()

    print "ROOT file written to", outfilename

    print "Completed."

        # outTree.Fill()
#here your main fuction end
    # h_total_mcweight.Write()
    # h_total.Write()
    # samplepath.Write()
    # outfile.Write()




def CheckFilter(filterName, filterResult,filtercompare):
    ifilter_=0
    filter1 = False
    for ifilter in filterName:
        filter1 = (ifilter.find(filtercompare) != -1)  & (bool(filterResult[ifilter_]) == True)
        if filter1: break
        ifilter_ = ifilter_ + 1
    return filter1

def DeltaR(p4_1, p4_2):
    eta1 = p4_1.Eta()
    eta2 = p4_2.Eta()
    eta = eta1 - eta2
    eta_2 = eta * eta

    phi1 = p4_1.Phi()
    phi2 = p4_2.Phi()
    phi = Phi_mpi_pi(phi1-phi2)
    phi_2 = phi * phi

    return math.sqrt(eta_2 + phi_2)

def Phi_mpi_pi(x):
    kPI = 3.14159265358979323846
    kTWOPI = 2 * kPI

    while (x >= kPI): x = x - kTWOPI;
    while (x < -kPI): x = x + kTWOPI;
    return x;

def DeltaPhi(phi1,phi2):
   phi = Phi_mpi_pi(phi1-phi2)

   return abs(phi)

def CheckFilter(filterName, filterResult,filtercompare):
    ifilter_=0
    filter1 = False
    for ifilter in filterName:
        filter1 = (ifilter.find(filtercompare) != -1)  & (bool(filterResult[ifilter_]) == True)
        if filter1: break
        ifilter_ = ifilter_ + 1
    return filter1



def MT(Pt, met, dphi):
    return ROOT.TMath.Sqrt( 2 * Pt * met * (1.0 - ROOT.TMath.Cos(dphi)) )

if __name__ == "__main__":
    AnalyzeDataSet()
