#!/usr/bin/env python
from ROOT import TFile, TTree, TH1F, TH1D, TH1, TCanvas, TChain,TGraphAsymmErrors, TMath, TH2D, TLorentzVector, TF1, AddressOf
import ROOT as ROOT
import os
import random
import sys, optparse
from array import array
import math
import AllQuantList

ROOT.gROOT.SetBatch(True)
from bbMETQuantities import *
#from PileUpWeights import PUWeight
pileup2016file = TFile('pileUPinfo2016.root')
pileup2016histo=pileup2016file.Get('hpileUPhist')

#Electron Trigger reweights
eleTrigReweightFile = TFile('scalefactors/electron_Trigger_eleTrig.root')
eleTrig_hEffEtaPt = eleTrigReweightFile.Get('hEffEtaPt')

#Electron Reconstruction efficiency. Scale factors for 80X
eleRecoSFsFile = TFile('scalefactors/electron_Reco_SFs_egammaEffi_txt_EGM2D.root')
eleRecoSF_EGamma_SF2D = eleRecoSFsFile.Get('EGamma_SF2D')

#Loose electron ID SFs
eleLooseIDSFsFile = TFile('scalefactors/electron_Loose_ID_SFs_egammaEffi_txt_EGM2D.root')
eleLooseIDSF_EGamma_SF2D = eleLooseIDSFsFile.Get('EGamma_SF2D')

#Tight electron ID SFs
eleTightIDSFsFile = TFile('scalefactors/electron_Tight_ID_SFs_egammaEffi_txt_EGM2D.root')
eleTightIDSF_EGamma_SF2D = eleTightIDSFsFile.Get('EGamma_SF2D')

# Veto cut-based electron ID SFs
eleVetoCutBasedIDSFsFile = TFile('scalefactors/electron_Veto_cut-based_ID_SFs_egammaEffi_txt_EGM2D.root')
eleVetoCutBasedIDSF_egammaEffi_txt_EGM2D = eleVetoCutBasedIDSFsFile.Get('EGamma_SF2D')

#Muon Trigger SFs
#BCDEF
muonTrigSFsRunBCDEFFile = TFile('scalefactors/muon_single_lepton_trigger_EfficienciesAndSF_RunBtoF.root')
muonTrigSFs_EfficienciesAndSF_RunBtoF = muonTrigSFsRunBCDEFFile.Get('IsoMu24_OR_IsoTkMu24_PtEtaBins/abseta_pt_ratio')
#GH
muonTrigSFsRunGHFile = TFile('scalefactors/muon_single_lepton_trigger_EfficienciesAndSF_Period4.root')
muonTrigSFs_EfficienciesAndSF_Period4 = muonTrigSFsRunBCDEFFile.Get('IsoMu24_OR_IsoTkMu24_PtEtaBins/abseta_pt_ratio')

#Muon ID SFs
#BCDEF
muonIDSFsBCDEFFile = TFile('scalefactors/muon_ID_SFs_EfficienciesAndSF_BCDEF.root')
muonLooseIDSFs_EfficienciesAndSF_BCDEF = muonIDSFsBCDEFFile.Get('MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio')
muonTightIDSFs_EfficienciesAndSF_BCDEF = muonIDSFsBCDEFFile.Get('MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio')
#GH
muonIDSFsGHFile = TFile('scalefactors/muon_ID_SFs_EfficienciesAndSF_GH.root')
muonLooseIDSFs_EfficienciesAndSF_GH = muonIDSFsGHFile.Get('MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio')
muonTightIDSFs_EfficienciesAndSF_GH = muonIDSFsGHFile.Get('MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio')

#Muon Iso SFs
#BCDEF
muonIsoSFsBCDEFFile = TFile('scalefactors/muon_Iso_SFs_EfficienciesAndSF_BCDEF.root')
muonLooseIsoSFs_EfficienciesAndSF_BCDEF = muonIsoSFsBCDEFFile.Get('LooseISO_LooseID_pt_eta/abseta_pt_ratio')
muonTightIsoSFs_EfficienciesAndSF_BCDEF = muonIsoSFsBCDEFFile.Get('TightISO_TightID_pt_eta/abseta_pt_ratio')
#GH
muonIsoSFsGHFile = TFile('scalefactors/muon_Iso_SFs_EfficienciesAndSF_GH.root')
muonLooseIsoSFs_EfficienciesAndSF_GH = muonIsoSFsGHFile.Get('LooseISO_LooseID_pt_eta/abseta_pt_ratio')
muonTightIsoSFs_EfficienciesAndSF_GH = muonIsoSFsGHFile.Get('TightISO_TightID_pt_eta/abseta_pt_ratio')

#Muon Tracking SFs
muonTrackingSFsFile = TFile('scalefactors/muon_Tracking_SFs_Tracking_EfficienciesAndSF_BCDEFGH.root')
muonTrackingSFs_EfficienciesAndSF_BCDEFGH = muonTrackingSFsFile.Get('ratio_eff_aeta_dr030e030_corr')


#MET Trigger reweights
metTrigEff_zmmfile = TFile('scalefactors/metTriggerEfficiency_zmm_recoil_monojet_TH1F.root')
metTrig_firstmethod = metTrigEff_zmmfile.Get('hden_monojet_recoil_clone_passed')

metTrigEff_secondfile = TFile('scalefactors/metTriggerEfficiency_recoil_monojet_TH1F.root')
metTrig_secondmethod = metTrigEff_secondfile.Get('hden_monojet_recoil_clone_passed')


ROOT.gROOT.ProcessLine('.L BTagCalibrationStandalone.cpp+')

#ROOT.gROOT.ProcessLine('.L TheaCorrection.cpp+')

######################################
## set up running mode of the code.
######################################

#ROOT.gROOT.ProcessLine('.L PileUpWeights.h')

#print "puweight = ",PUWEIGHT(10)
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

parser.add_option("--csv", action="store_true",  dest="CSV")
parser.add_option("--deepcsv", action="store_true",  dest="DeepCSV")

parser.add_option("--se", action="store_true",  dest="SE")
parser.add_option("--met", action="store_true",  dest="MET")
parser.add_option("--sp", action="store_true",  dest="SP")

########################################################################################################################
########################## cut values########################################################################
########################################################################################################################

parser.add_option("--dbt", action="store_true",  dest="dbt")
parser.add_option( "--dbtcut", type=float,  dest="dbtcut")

parser.add_option("--theac", action="store_true",  dest="theac")

(options, args) = parser.parse_args()

if options.farmout==None:
    isfarmout = False
else:
    isfarmout = options.farmout

if options.CSV==None:
    options.CSV = False

if options.DeepCSV==None:
    options.DeepCSV = False

if options.SE==None:
    options.SE==False

if options.MET==None:
    options.MET==False

if options.SP==None:
    options.SP==False


if options.SE: print "Using SingleElectron dataset."
if options.SP: print "Using SinglePhoton dataset."
if options.MET: print "Using MET dataset."

#if not options.SE and not options.MET and not options.SP:
    #print "Please run using --se or --met or --sp. Exiting."
    #sys.exit()

if options.CSV: print "Using CSVv2 as b-tag discriminator."
if options.DeepCSV: print "Using DeepCSV as b-tag discriminator."

if not options.CSV and not options.DeepCSV:
    print "Please run using --csv or --deepcsv. Exiting."
    sys.exit()

applydPhicut=True

#print 'options = ',[options.inputfile]
inputfilename = options.inputfile
outputdir = options.outputdir

#print inputfilename
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
#else:
#    outfilename = options.outputfile

print "Input:",options.inputfile, "; Output:", outfilename

skimmedTree = TChain("outTree")


#bbMET_tree = TTree( 'bbMET_tree', 'outputTree' )
#print isfarmout



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

def IsoMu20isUnPrescaled(filename):
    if filename.find('2016D')>-1 or filename.find('2016E')>-1 or filename.find('2016F')>-1 or filename.find('2016G')>-1 or filename.find('2016H')>-1:
        return False
    else:
        return True

def TheaCorrection(puppipt=200.0,  puppieta=0.0):
    puppisd_corrGEN      = TF1("puppisd_corrGEN","[0]+[1]*pow(x*[2],-[3])");
    puppisd_corrGEN.SetParameters(
        1.00626,
        -1.06161,
        0.07999,
        1.20454
        )
    puppisd_corrRECO_cen =  TF1("puppisd_corrRECO_cen","[0]+[1]*x+[2]*pow(x,2)+[3]*pow(x,3)+[4]*pow(x,4)+[5]*pow(x,5)");
    puppisd_corrRECO_cen.SetParameters(
        1.05807,
        -5.91971e-05,
        2.296e-07,
        -1.98795e-10,
        6.67382e-14,
        -7.80604e-18
        )

    puppisd_corrRECO_for = TF1("puppisd_corrRECO_for","[0]+[1]*x+[2]*pow(x,2)+[3]*pow(x,3)+[4]*pow(x,4)+[5]*pow(x,5)");
    puppisd_corrRECO_for.SetParameters(
        1.26638,
        -0.000658496,
        9.73779e-07,
        -5.93843e-10,
        1.61619e-13,
        -1.6272e-17)

    genCorr  = 1.
    recoCorr = 1.
    totalWeight = 1.

    genCorr =  puppisd_corrGEN.Eval( puppipt )
    if ( abs(puppieta)  <= 1.3 ) :
        recoCorr = puppisd_corrRECO_cen.Eval( puppipt )
    elif( abs(puppieta) > 1.3 ) :
        recoCorr = puppisd_corrRECO_for.Eval( puppipt )

    totalWeight = genCorr * recoCorr
    return totalWeight

triglist=['HLT_PFMET170_','HLT_PFMET170_NoiseCleaned','HLT_PFMET170_JetIdCleaned_v','HLT_PFMET170_HBHECleaned_v','HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v','HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v','HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v','HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v','HLT_PFMET110_PFMHT110_','HLT_IsoMu24_v','HLT_IsoTkMu24_v','HLT_Ele27_WPTight_Gsf','HLT_IsoMu20','HLT_Ele27_WPLoose_Gsf','HLT_Photon165_HE10','HLT_Photon175']

#st_quantlist = triglist + ['st_lumiSection', 'st_eventId', 'st_pfMetCorrPt', 'st_pfMetCorrPhi', 'st_THINnJet', 'st_THINjetP4', 'st_THINjetCISVV2', 'st_THINjetHadronFlavor', 'st_THINjetNHadEF', 'st_THINjetCHadEF', 'st_THINjetNPV', 'st_AK4deepCSVnJet', 'st_AK4deepCSVjetP4', 'st_AK4deepCSVjetDeepCSV_b', 'st_AK4deepCSVjetHadronFlavor', 'st_AK4deepCSVjetNHadEF', 'st_AK4deepCSVjetCHadEF', 'st_AK4deepCSVjetNPV', 'st_nPho', 'st_phoP4', 'st_phoIsPassLoose', 'st_phoIsPassMedium', 'st_phoIsPassTight', 'st_nEle', 'st_eleP4', 'st_eleIsPassLoose', 'st_eleIsPassMedium', 'st_eleIsPassTight', 'st_nMu', 'st_muP4', 'st_isLooseMuon', 'st_isMediumMuon', 'st_isTightMuon', 'st_muChHadIso', 'st_muNeHadIso', 'st_muGamIso', 'st_muPUPt', 'st_HPSTau_n', 'st_HPSTau_4Momentum', 'st_isData', 'mcweight', 'st_pu_nTrueInt', 'st_pu_nPUVert', 'st_nGenPar', 'st_genParId', 'st_genMomParId', 'st_genParSt', 'st_genParP4', 'WenuRecoil', 'Wenumass', 'WenuPhi', 'WmunuRecoil', 'Wmunumass', 'WmunuPhi', 'ZeeRecoil', 'ZeeMass', 'ZeePhi', 'ZmumuRecoil', 'ZmumuMass', 'ZmumuPhi', 'TOPRecoil', 'TOPPhi', 'GammaRecoil', 'GammaPhi']


h_t = TH1F('h_t','h_t',2,0,2)
h_t_weight = TH1F('h_t_weight','h_t_weight',2,0,2)

samplename = 'all'
if isfarmout:
    infile = open(inputfilename)
    failcount=0
    for ifile in infile:
	skimmedTree_temp = TChain("outTree")
	skimmedTree_temp.Add(ifile)
	try:
	    skimmedTree.GetEntry(1)
	except:
	    print "THis is corrupted file: ",ifile
	    continue
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
UnPrescaledIsoMu20 = IsoMu20isUnPrescaled(samplepath)
#print UnPrescaledIsoMu20
#print samplename
#print

def AnalyzeDataSet():

    NEntries = skimmedTree.GetEntries()
    print 'NEntries = '+str(NEntries)
    npass = 0

    cutStatus={'preselection':NEntries}

    cutStatusSR={'preselection':NEntries}


    cutflownamesSR=['trig','MET','nFATJet','nJets','JetCond','nlepCond','N2DDT']
    for SRname in cutflownamesSR:
        cutStatusSR[SRname] = 0


    CRcutnames=['datatrig','trig','recoil','realMET','mass','nFATJet','nJets','JetCond','nlep','nlepCond','N2DDT']
    regionnames=['2e2b','2mu2b','1e2bW','1mu2bW','1e2bT','1mu2bT']#,'1gamma2b','QCD2b']
    for CRreg in regionnames:
        exec("CR"+CRreg+"CutFlow={'preselection':NEntries}")
        for cutname in CRcutnames:
            exec("CR"+CRreg+"CutFlow['"+cutname+"']=0")


    CRs=['ZCRSR','WCRSR','TopCRSR']

    CRStatus={'total':NEntries}
    for CRname in CRs:
        CRStatus[CRname]=0

    # ---CR Summary---
    # regNames=['1#mu1b','1e1b','1#mu2b','1e2b','2#mu1b','2e1b','2#mu2b','2e2b','1#mu1e1b','1#mu1e2b']
    regNamesMu=['1#mu2bT','1#mu2bW','2#mu2b','1#mu1e2b']#,'2#mu2b','1#mu1e1b','1#mu1e2b']
    regNamesEle=['1e2bT','1e2bW','2e2b']

    # CRSummary={}
    # for ireg in regNames:
    #     CRSummary[ireg]=0.

    CRSummaryMu={}
    for ireg in regNamesMu:
        CRSummaryMu[ireg]=0.

    CRSummaryEle={}
    for ireg in regNamesEle:
        CRSummaryEle[ireg]=0.

    #print outfilename
    allquantities = MonoHbbQuantities(outfilename)
    allquantities.defineHisto()


    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
    # BTag Scale Factor Initialisation
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------

    othersys = ROOT.std.vector('string')()
    othersys.push_back('down')
    othersys.push_back('up')
    ## ThinJets
    if options.CSV:
        calib1 = ROOT.BTagCalibrationStandalone('csvv2', 'CSVv2_Moriond17_B_H.csv')
    if options.DeepCSV:
        calib1 = ROOT.BTagCalibrationStandalone('deepcsv', 'DeepCSV_Moriond17_B_H.csv')

    reader1 = ROOT.BTagCalibrationStandaloneReader( 0, "central", othersys)
    reader1.load(calib1, 0,  "comb" )
    reader1.load(calib1, 1,  "comb" )
    reader1.load(calib1, 2,  "incl" )

    for ievent in range(NEntries):

        sf_resolved1 = []
        sf_resolved2 = []
        sf_resolved3 = []

	skimmedTree.GetEntry(ievent)

        try:
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Extract branches
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
            run                        = skimmedTree.__getattr__('st_runId')
            lumi                       = skimmedTree.__getattr__('st_lumiSection')
            event                      = skimmedTree.__getattr__('st_eventId')

            #if event != 4126: continue
            #if lumi  != 42: continue
            if ievent%100==0: print (ievent)
            #trigName                   = skimmedTree.__getattr__('st_hlt_trigName')
            #trigResult                 = skimmedTree.__getattr__('st_hlt_trigResult')
            #filterName                 = skimmedTree.__getattr__('st_hlt_filterName')
            #filterResult               = skimmedTree.__getattr__('st_hlt_filterResult')

            pfMet                      = skimmedTree.__getattr__('st_pfMetCorrPt')
            pfMetPhi                   = skimmedTree.__getattr__('st_pfMetCorrPhi')

            nTHINJets                  = skimmedTree.__getattr__('st_THINnJet')
            thinjetP4                  = skimmedTree.__getattr__('st_THINjetP4')
            thinJetCSV                 = skimmedTree.__getattr__('st_THINjetCISVV2')
            #passThinJetLooseID         = skimmedTree.__getattr__('st_THINjetPassIDLoose')
            #passThinJetPUID            = skimmedTree.__getattr__('st_THINisPUJetID')
            THINjetHadronFlavor        = skimmedTree.__getattr__('st_THINjetHadronFlavor')
            thinjetNhadEF              = skimmedTree.__getattr__('st_THINjetNHadEF')
            thinjetChadEF              = skimmedTree.__getattr__('st_THINjetCHadEF')
            thinjetNPV                 = skimmedTree.__getattr__('st_THINjetNPV')

            #AK8Jets BRANCHES
            AK8nthikJets               = skimmedTree.__getattr__('st_AK8nthikJets')
            AK8thikjetP4               = skimmedTree.__getattr__('st_AK8thikjetP4')
            AK8SDmass                  = skimmedTree.__getattr__('st_AK8SDmass')
            AK8PuppisubjetCSV          = skimmedTree.__getattr__('st_AK8PuppisubjetCSV')

            #CA15jets
            CA15njets                 = skimmedTree.__getattr__('st_CA15njets')
            CA15jetP4                 = skimmedTree.__getattr__('st_CA15jetP4')
            CA15SDmass                = skimmedTree.__getattr__('st_CA15SDmass')
#            CA15PuppisubjetCSV        = skimmedTree.__getattr__('st_CA15PuppisubjetCSV')
            CA15Puppi_doublebtag      = skimmedTree.__getattr__('st_CA15Puppi_doublebtag')
            CA15PuppiECF_1_2_10       = skimmedTree.__getattr__('st_CA15PuppiECF_1_2_10')
            CA15PuppiECF_2_3_10       = skimmedTree.__getattr__('st_CA15PuppiECF_2_3_10')
            # CA15PassIDTight           = skimmedTree.__getattr__('st_CA15PassIDTight')
            # CA15PassIDLoose           = skimmedTree.__getattr__('st_CA15PassIDLoose')

            #
            # try:
            #     thinjetCEmEF               = skimmedTree.__getattr__('st_THINjetCEmEF')
            #     thinjetPhoEF               = skimmedTree.__getattr__('st_THINjetPhoEF')
            #     thinjetEleEF               = skimmedTree.__getattr__('st_THINjetEleEF')
            #     thinjetMuoEF               = skimmedTree.__getattr__('st_THINjetMuoEF')
            # except:
            #     nulljet=[-1. for i in range(nTHINJets)]
            #     thinjetCEmEF=nulljet
            #     thinjetPhoEF=nulljet
            #     thinjetEleEF=nulljet
            #     thinjetMuoEF=nulljet

            nTHINdeepCSVJets           = skimmedTree.__getattr__('st_AK4deepCSVnJet')
            thindeepCSVjetP4           = skimmedTree.__getattr__('st_AK4deepCSVjetP4')
            thinJetdeepCSV             = skimmedTree.__getattr__('st_AK4deepCSVjetDeepCSV_b')
            THINdeepCSVjetHadronFlavor = skimmedTree.__getattr__('st_AK4deepCSVjetHadronFlavor')
            thindeepCSVjetNhadEF       = skimmedTree.__getattr__('st_AK4deepCSVjetNHadEF')
            thindeepCSVjetChadEF       = skimmedTree.__getattr__('st_AK4deepCSVjetCHadEF')
            thindeepCSVjetNPV          = skimmedTree.__getattr__('st_AK4deepCSVjetNPV')

            nPho                       = skimmedTree.__getattr__('st_nPho')
            phoP4                      = skimmedTree.__getattr__('st_phoP4')
            phoIsPassLoose             = skimmedTree.__getattr__('st_phoIsPassLoose')
            phoIsPassMedium            = skimmedTree.__getattr__('st_phoIsPassMedium')
            phoIsPassTight             = skimmedTree.__getattr__('st_phoIsPassTight')

            nEle                       = skimmedTree.__getattr__('st_nEle')
            eleP4                      = skimmedTree.__getattr__('st_eleP4')
            eleIsPassLoose             = skimmedTree.__getattr__('st_eleIsPassLoose')
            eleIsPassMedium            = skimmedTree.__getattr__('st_eleIsPassMedium')
            eleIsPassTight             = skimmedTree.__getattr__('st_eleIsPassTight')

            nMu                        = skimmedTree.__getattr__('st_nMu')
            muP4                       = skimmedTree.__getattr__('st_muP4')
            isLooseMuon                = skimmedTree.__getattr__('st_isLooseMuon')
            isMediumMuon               = skimmedTree.__getattr__('st_isMediumMuon')
            isTightMuon                = skimmedTree.__getattr__('st_isTightMuon')
            muChHadIso                 = skimmedTree.__getattr__('st_muChHadIso')
            muNeHadIso                 = skimmedTree.__getattr__('st_muNeHadIso')
            muGamIso                   = skimmedTree.__getattr__('st_muGamIso')
            muPUPt                     = skimmedTree.__getattr__('st_muPUPt')

            nTau                       = skimmedTree.__getattr__('st_HPSTau_n')
            tauP4                      = skimmedTree.__getattr__('st_HPSTau_4Momentum')
            #isDecayModeFinding         = skimmedTree.__getattr__('st_disc_decayModeFinding')
            #passLooseTauIso            = skimmedTree.__getattr__('st_disc_byLooseIsolationMVA3oldDMwLT')
            try:
                disc_againstElectronLoose  = skimmedTree.__getattr__('st_disc_againstElectronLoose')
                disc_againstElectronMedium = skimmedTree.__getattr__('st_disc_againstElectronMedium')
                disc_againstElectronTight  = skimmedTree.__getattr__('st_disc_againstElectronTight')
                disc_againstMuonLoose      = skimmedTree.__getattr__('st_disc_againstMuonLoose')
                disc_againstMuonTight      = skimmedTree.__getattr__('st_disc_againstMuonTight')
            except:
                if ievent==0: print "Tau discriminators not found. Skipping tau veto."
                disc_againstElectronLoose=None

            isData                     = skimmedTree.__getattr__('st_isData')
            mcWeight                   = skimmedTree.__getattr__('mcweight')
            pu_nTrueInt                = int(skimmedTree.__getattr__('st_pu_nTrueInt'))
            pu_nPUVert                 = int(skimmedTree.__getattr__('st_pu_nPUVert'))

            nGenPar                    = skimmedTree.__getattr__('st_nGenPar')
            genParId                   = skimmedTree.__getattr__('st_genParId')
            genMomParId                = skimmedTree.__getattr__('st_genMomParId')
            genParSt                   = skimmedTree.__getattr__('st_genParSt')
            genParP4                   = skimmedTree.__getattr__('st_genParP4')

            WenuRecoil                 = skimmedTree.__getattr__('WenuRecoil')
            Wenumass                   = skimmedTree.__getattr__('Wenumass')
            WenuPhi                    = skimmedTree.__getattr__('WenuPhi')
            WmunuRecoil                = skimmedTree.__getattr__('WmunuRecoil')
            Wmunumass                  = skimmedTree.__getattr__('Wmunumass')
            WmunuPhi                   = skimmedTree.__getattr__('WmunuPhi')
            ZeeRecoil                  = skimmedTree.__getattr__('ZeeRecoil')
            ZeeMass                    = skimmedTree.__getattr__('ZeeMass')
            ZeePhi                     = skimmedTree.__getattr__('ZeePhi')
            ZmumuRecoil                = skimmedTree.__getattr__('ZmumuRecoil')
            ZmumuMass                  = skimmedTree.__getattr__('ZmumuMass')
            ZmumuPhi                   = skimmedTree.__getattr__('ZmumuPhi')
            TOPRecoil                  = skimmedTree.__getattr__('TOPRecoil')
            TOPPhi                     = skimmedTree.__getattr__('TOPPhi')
            GammaRecoil                = skimmedTree.__getattr__('GammaRecoil')
            GammaPhi                   = skimmedTree.__getattr__('GammaPhi')

            for trig in triglist:
                exec(trig+" = skimmedTree.__getattr__('st_"+trig+"')")

        except Exception as e:
#        else:
            print e
            print "Corrupt file detected! Skipping 1 event."
            continue

        ##Define region wise triggers

        if isData:
            SRtrigstatus = HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v or HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v or HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v or HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v or HLT_PFMET170_
            MuCRtrigstatus = ((UnPrescaledIsoMu20 and HLT_IsoMu20) or HLT_IsoMu24_v or HLT_IsoTkMu24_v)
            EleCRtrigstatus = (HLT_Ele27_WPLoose_Gsf or HLT_Ele27_WPTight_Gsf)
            PhotonCRtrigstatus = (HLT_Photon165_HE10 or HLT_Photon175)

        else:
            SRtrigstatus = True
            MuCRtrigstatus = True
            EleCRtrigstatus = True
            PhotonCRtrigstatus = True



#        #============================ CAUTION =====================================
#        #**************************************************************************


        jetSRInfo           = []
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # MC Weights ----------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        mcweight = 0.0
        if isData==1:   mcweight =  1.0
        if not isData :
            if mcWeight<0:  mcweight = -1.0
            if mcWeight>0:  mcweight =  1.0


               # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## PFMET Selection
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        pfmetstatus = ( pfMet > 200.0 )
        #----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ##Calculate Muon Relative PF isolation:
        MuIso = [((muChHadIso[imu]+ max(0., muNeHadIso[imu] + muGamIso[imu] - 0.5*muPUPt[imu]))/muP4[imu].Pt()) for imu in range(nMu)]

         # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
#        print (HLT_IsoMu24,HLT_Ele27_WPLoose_Gsf)

        myEles=[]
        myEleLooseID=[]
        myEleTightID=[]
        for iele in range(nEle):
            if eleP4[iele].Pt() < 10 : continue
            if abs(eleP4[iele].Eta()) >2.5: continue

            myEles.append(eleP4[iele])
            myEleLooseID.append(eleIsPassLoose[iele])
            myEleTightID.append(eleIsPassTight[iele])

        myMuos = []
        myMuLooseID=[]
        myMuTightID=[]
        myMuIso=[]
        for imu in range(nMu):
            if muP4[imu].Pt()<10 : continue
            if abs(muP4[imu].Eta()) > 2.4  : continue

            myMuos.append(muP4[imu])
            myMuLooseID.append(isLooseMuon[imu])
            myMuTightID.append(isTightMuon[imu])
            myMuIso.append(MuIso[imu])


        myPhos=[]
        myPhoLooseID=[]
        myPhoTightID=[]
        for ipho in range(nPho):
            if phoP4[ipho].Pt() < 15 : continue
            if phoP4[ipho].Eta() > 2.5 : continue
            #---Fake Pho cleaner----
            # isClean=True
            # for ijet in myJetP4:
            #     pho_jet_dR=DeltaR(ijet,phoP4[ipho])    # math.sqrt(  (  ijet.Eta()-phoP4[ipho].Eta() )**2  + (  DeltaPhi(ijet.Phi(),phoP4[ipho].Phi()) )**2 )
            #     if pho_jet_dR < 0.4:
            #         isClean=False
            #         break
            # if not isClean: continue
            myPhos.append(phoP4[ipho])
            myPhoLooseID.append(phoIsPassLoose[ipho])
            myPhoTightID.append(phoIsPassTight[ipho])

#        myTaus=[]
        nTausDRbased=0
        myTausTightElectron=[]
        myTausTightMuon=[]
        myTausTightEleMu=[]
        myTausLooseEleMu=[]
        for itau in range(nTau):
            if tauP4[itau].Pt()<18. : continue
            if abs(tauP4[itau].Eta())>2.3 : continue
            if disc_againstElectronLoose!=None: # and len(disc_againstElectronLoose)==nTau:
                if disc_againstElectronTight[itau] and disc_againstMuonLoose[itau]:
                    myTausTightElectron.append(tauP4[itau])
                if disc_againstMuonTight[itau] and disc_againstElectronLoose[itau]:
                    myTausTightMuon.append(tauP4[itau])
                if disc_againstMuonTight[itau] and disc_againstElectronTight[itau]:
                    myTausTightEleMu.append(tauP4[itau])
                if disc_againstMuonLoose[itau] and disc_againstElectronLoose[itau]:
                    myTausLooseEleMu.append(tauP4[itau])

            #---Fake tau cleaner----
            isClean=True
            for iele in myEles[:]:
                lep_tau_dR=DeltaR(iele,tauP4[itau])
                if lep_tau_dR < 0.4:
                    isClean=False
                    break
            for imu in myMuos[:]:
                lep_tau_dR=DeltaR(imu,tauP4[itau])
                if lep_tau_dR < 0.4:
                    isClean=False
                    break
            if isClean: nTausDRbased+=1
        #--------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Jet Selection
        ## Also segregate CSV or DeepCSV collection of jets in this step itself
        CSVLWP=0.54
        CSVMWP=0.8484
        deepCSVMWP=0.6324

        mybJetsP4=[]
        mybjets=[]
        bjetIndex=[]

        myJetCSV=[]
        myJetP4=[]
        myJetHadronFlavor=[]
        myJetNhadEF=[]
        myJetChadEF=[]
        myJetCEmEF=[]
        myJetPhoEF=[]
        myJetEleEF=[]
        myJetMuoEF=[]

        myCA15P4=[]
        myCA15Doubleb=[]
        caSDMass=[]
        myfailedbjets=[]
        myfailedbJetsP4=[]


        if options.CSV:

            for nb in range(nTHINJets):

            #---Fake jet cleaner, wrt electrons and muons----
                isClean=True
                for iele in myEles[:]:
                    if DeltaR(iele,thinjetP4[nb]) < 0.4:
                        isClean=False
                        break
                for imu in myMuos[:]:
                    if DeltaR(imu,thinjetP4[nb]) < 0.4:
                        isClean=False
                        break

                for iph in range(nPho):
                    if DeltaR(phoP4[iph],thinjetP4[nb]) < 0.4:
                        isClean=False
                        break
                if not isClean: continue
            #---

                myJetP4.append(thinjetP4[nb])
                myJetCSV.append(thinJetCSV[nb])
                myJetHadronFlavor.append(THINjetHadronFlavor[nb])
                myJetNhadEF.append(thinjetNhadEF[nb])
                myJetChadEF.append(thinjetChadEF[nb])

                if thinJetCSV[nb] > CSVLWP and abs(thinjetP4[nb].Eta())<2.4:
                    mybjets.append(nb)
                    mybJetsP4.append(thinjetP4[nb])
                    #bjetIndex.append(nb)

                if thinJetCSV[nb] < CSVLWP and abs(thinjetP4[nb].Eta())<2.4:
                    myfailedbjets.append(nb)
                    myfailedbJetsP4.append(thinjetP4[nb])

            myJetNPV=thinjetNPV
            nUncleanJets=nTHINJets

        if options.DeepCSV:
            for nb in range(nTHINdeepCSVJets):

            #---Fake jet cleaner, wrt electrons and muons----
                isClean=True
                for iele in myEles:
                    if DeltaR(iele,thindeepCSVjetP4[nb]) < 0.4:
                        isClean=False
                        break
                for imu in myMuos:
                    if DeltaR(imu,thindeepCSVjetP4[nb]) < 0.4:
                        isClean=False
                        break

                if not isClean: continue
            #---
                myJetP4.append(thindeepCSVjetP4[nb])
                myJetCSV.append(thinJetdeepCSV[nb])
                myJetHadronFlavor.append(THINdeepCSVjetHadronFlavor[nb])
                myJetNhadEF.append(thindeepCSVjetNhadEF[nb])
                myJetChadEF.append(thindeepCSVjetChadEF[nb])

                if thinJetdeepCSV[nb] > deepCSVMWP and abs(thindeepCSVjetP4[nb].Eta())<2.4:
                    mybjets.append(nb)
                    mybJetsP4.append(thindeepCSVjetP4[nb])

            myJetNPV=thindeepCSVjetNPV
            nUncleanJets=nTHINdeepCSVJets



#   do FATJet cleaning here

        myCA15P4=[]
        myCA15Mass=[]
        myCA15Tagger=[]
        myCA15_N2DDT=[]
        myCA15_N2=[]

        #if CA15doubleB:
        for ca15jet in range(CA15njets):
            isClean=True
            for iele in myEles:
                if DeltaR(iele,CA15jetP4[ca15jet]) < 0.4:
                    isClean=False
                    break
            for imu in myMuos:
                if DeltaR(imu,CA15jetP4[ca15jet]) < 0.4:
                    isClean=False
                    break
            if not isClean: continue
            myCA15P4.append(CA15jetP4[ca15jet])
            myCA15Mass.append(CA15SDmass[ca15jet])
            myCA15Tagger.append(CA15Puppi_doublebtag[ca15jet])
            if (CA15PuppiECF_1_2_10[ca15jet])**2 == 0 :
                myCA15_N2DDT.append(99999)
                myCA15_N2.append(-99999)
            else:
                N2=(CA15PuppiECF_2_3_10[ca15jet])/((CA15PuppiECF_1_2_10[ca15jet])**2)
                myCA15_N2.append(N2)
                myCA15_N2DDT.append(N2-0.113)








        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------

        nUncleanEle=nEle
        nUncleanMu=nMu
        nUncleanTau=nTau

        nPho=len(myPhos)
        nEle=len(myEles)
        nMu=len(myMuos)
#        nTau=len(myTaus)

        nTauTightElectron=len(myTausTightElectron)
        nTauTightMuon=len(myTausTightMuon)
        nTauTightEleMu=len(myTausTightEleMu)
        nTauLooseEleMu=len(myTausLooseEleMu)
        nTau=nTauLooseEleMu

        nBjets=len(mybjets)
        nfailBjets=len(myfailedbjets)
        nJets=len(myJetCSV)
##################################
        #Fatjet collections
        hasAK8jet=False
        myAK8JetsP4=[]
        myAK8CSV=[]
        AK8csv=[]
        hastwobjets=False
        hasAKMass=False

        Selca15jetsP4=[]
        SelN2DDT=[]
        SelN2=[]
        FatjetIndex=[]
        myCleanFatjet=[]

        hasca15twobjets=False

        CA15doubleB=True



        #if CA15doubleB:
        for i in range(len(myCA15P4)):
            if myCA15P4[i].Pt() > 200. and abs(myCA15P4[i].Eta()) < 2.4 and myCA15Mass[i] > 100. and myCA15Mass[i] < 150. and myCA15Tagger[i] > 0.75:
                        Selca15jetsP4.append(myCA15P4[i])
                        SelN2DDT.append(myCA15_N2DDT[i])
                        SelN2.append(myCA15_N2[i])
                        #FatjetIndex.append(ca15jet)



        # else:
        #     for i in range(AK8nFatJets):
        #         if AK8FatjetP4[i].Pt() > 200 and abs(AK8FatjetP4[i].Eta()) < 2.4 and AK8SDmass[i] > 100 and AK8SDmass[i] < 150 and AK8DoubleBtagger[i] > .6:
        #             myak8jetP4.append(AK8FatjetP4[i])
        #             FatjetIndex.append(i)



        nFatJet=len(Selca15jetsP4)
        N2DDT=9999
        N2DDTCond=False
        if nFatJet==1:
            N2DDT = SelN2DDT[0]
            N2    = SelN2[0]
            N2DDTCond = N2DDT < 0
            # if N2DDTCond:
            #     print "yes"
            #selFatjet=myCleanFatjet[0]
            #selFatjet=CleanFatjetIndex[0]


 #----------------------------------------------------------------------------------------------------------------------------------------------------------------
 #----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Sort jets

        if nFatJet==0: continue
        if nFatJet==1:
            Fatjet1_pT=Selca15jetsP4[0].Pt()
            min_dPhi_Fatjet_MET=DeltaPhi(Selca15jetsP4[0].Phi(),pfMetPhi)


        ifirstjet=0

        if nJets > 0:
            j1 = myJetP4[ifirstjet]
            min_dPhi_jet_MET = DeltaPhi(j1.Phi(),pfMetPhi)

# --------------------------------------------------------------------------------------------------------------------------------------------------------

        allquantlist=AllQuantList.getAll()

        for quant in allquantlist:
            exec("allquantities."+quant+" = None")
# --------------------------------------------------------------------------------------------------------------------------------------------------------


        # SR start

        ###
        #********
        #Part of data is blinded
        #********
        if isData:
            if ievent%20==0:
                keepevent=True
            else:
                keepevent=False
        else:
            keepevent=True
        #********************              REMEMBER TO UNBLIND AT SOME POINT!

        writeSR=False
        isZeeCR=False
        isZmumuCR=False
        isWenuCR=False
        isWmunuCR=False
        isTopCR=False
        isGammaCR=False

        writeSR=False
        isZeeCR=False
        isZmumuCR=False
        isWenuCR2T=False
        isWenuCR2W=False
        isWmunuCR2T=False
        isWmunuCR2W=False
        isTopCR2=False
        isGammaCR2=False

        SRnjetcond=False
        SRjetcond=False


        if nEle+nMu+nTauLooseEleMu==0:
            SRlepcond=True
        else:
            SRlepcond=False

        if nFatJet == 1:
            SRFatjetcond=True
        else:
            SRFatjetcond=False



     ## for SR

        if (nJets == 0 or nJets == 1):
            SRnjetcond    =    True

        SR_Cut7_dPhi_jet_MET        =   True #min_dPhi_jet_MET > 0.4
        SR_Cut_nFATJet              =   nFatJet == 1
        SR_Cut1_nJets               =   nJets == 0 or nJets == 1
        SR_Cut2_nBjets              =   True
        SR_Cut3_trigstatus          =   SRtrigstatus
        SR_Cut4_jet1                =   True

        if nJets ==1:
            #min_dPhi_jet_MET = DeltaPhi(j1.Phi(),pfMetPhi)
            if j1.Pt() < 30.0 and min_dPhi_jet_MET < 0.4:
                SR_Cut4_jet1           = False
                SR_Cut7_dPhi_jet_MET   = False

        SR_Cut8_nLep           =   nEle+nMu+nTauLooseEleMu == 0
        SR_Cut9_pfMET          =   pfmetstatus



        if SR_Cut3_trigstatus and SR_Cut9_pfMET and SR_Cut1_nJets and SR_Cut4_jet1 and SR_Cut7_dPhi_jet_MET and SR_Cut8_nLep:
                allquantities.N2DDT_sr2 = N2DDT
                allquantities.N2_sr2 = N2
                allquantities.nca15jet_sr2 = nFatJet

        if SR_Cut3_trigstatus and SR_Cut9_pfMET and SR_Cut_nFATJet and SR_Cut1_nJets and SR_Cut4_jet1 and SR_Cut7_dPhi_jet_MET and SR_Cut8_nLep and (N2DDT < 0):

            if nJets==1:
                allquantities.jet1_pT_sr2     = j1.Pt()
                allquantities.jet1_eta_sr2    = j1.Eta()
                allquantities.jet1_phi_sr2    = j1.Phi()
                if options.CSV:
                    allquantities.jet1_csv_sr2       = myJetCSV[ifirstjet]
                if options.DeepCSV:
                    allquantities.jet1_deepcsv_sr2   = myJetCSV[ifirstjet]
            allquantities.ca15jet_pT_sr2             = Fatjet1_pT
            #allquantities.min_dPhi_sr2               = min_dPhi_jet_MET
            #allquantities.min_dPhi_CAjet_sr2         = min_dPhi_Fatjet_MET
            allquantities.met_sr2                    = pfMet
            writeSR=True



# --------------------------------------------------------------------------------------------------------------------------------------------------------

        #Control Regions

# --------------------------------------------------------------------------------------------------------------------------------------------------------

        preselquantlist=AllQuantList.getPresel()

        for quant in preselquantlist:
            exec("allquantities."+quant+" = None")


        regquants=AllQuantList.getRegionQuants()

        for quant in regquants:
            exec("allquantities."+quant+" = None")

        Histos2D=AllQuantList.getHistos2D()
        for quant in Histos2D:
            exec("allquantities."+quant+" = None")



        ####new conds
        jetcond=True
        if nJets==1:
            if j1.Pt() < 30.0: jetcond=False

# -------------------------------------------
# Z CR
# -------------------------------------------

        #Z CR specific bools

        ZeePhicond=True
        ZmumuPhicond=True

        if applydPhicut and nJets == 1:
            #if ZeePhi>-10.:
            if DeltaPhi(ZeePhi,myJetP4[ifirstjet].Phi()) < 0.4: ZeePhicond=False
            #if ZmumuPhi>-10.:
            if DeltaPhi(ZmumuPhi,myJetP4[ifirstjet].Phi()) < 0.4: ZmumuPhicond=False

         #2e, 1 b-tagged

        if nEle==2 and nMu==0 and nTauTightElectron==0 and EleCRtrigstatus and ZeeMass>60. and ZeeMass<120. and ZeeRecoil>200. and jetcond and pfMet > 0.:
#            CRCutFlow['nlepcond']+=1
            alllepPT=[lep.Pt() for lep in myEles]
            lepindex=[i for i in range(len(myEles))]

            sortedleps=[lep for pt,lep in sorted(zip(alllepPT,myEles), reverse=True)]      # This gives a list of leps with their pTs in descending order
            sortedindex=[lepind for pt,lepind in sorted(zip(alllepPT,lepindex), reverse=True)]     # Indices of leps in myJetP4 in decscending order of jetPT

            iLeadLep=sortedindex[0]
            iSecondLep=sortedindex[1]

            if myEles[iLeadLep].Pt() > 40. and myEleTightID[iLeadLep] and myEles[iSecondLep].Pt() > 10. and myEleLooseID[iSecondLep]:

                ZpT = math.sqrt( (myEles[iLeadLep].Px()+myEles[iSecondLep].Px())*(myEles[iLeadLep].Px()+myEles[iSecondLep].Px()) + (myEles[iLeadLep].Py()+myEles[iSecondLep].Py())*(myEles[iLeadLep].Py()+myEles[iSecondLep].Py()) )


                if SRnjetcond and ZeePhicond and SRFatjetcond:
                    allquantities.reg_2e2b_N2DDT = N2DDT
                    allquantities.reg_2e2b_N2    = N2

                if SRnjetcond and ZeePhicond and SRFatjetcond and (N2DDT <0):

                    allquantities.reg_2e2b_Zmass = ZeeMass
                    allquantities.reg_2e2b_ZpT=ZpT

                    allquantities.reg_2e2b_hadrecoil = ZeeRecoil
                    allquantities.reg_2e2b_MET = pfMet
                    allquantities.reg_2e2b_ca15jet_pT = Fatjet1_pT

                    allquantities.reg_2e2b_lep1_pT=myEles[iLeadLep].Pt()
                    allquantities.reg_2e2b_lep2_pT=myEles[iSecondLep].Pt()
                    allquantities.reg_2e2b_njet = nJets
                    # allquantities.reg_2e2b_CA15Doublebtag  = CA15cvs[0]
                    # if nJets==1:
                    #     allquantities.reg_2e2b_min_dPhi_jet_Recoil = min( [DeltaPhi(ZeePhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    #     allquantities.reg_2e2b_min_dPhi_jet_MET = min( [DeltaPhi(pfMetPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    #allquantities.reg_2e2b_min_dPhi_CAjet_MET=min_dPhi_CAjet_MET
                    allquantities.reg_2e2b_ntau = nTauTightElectron
                    allquantities.reg_2e2b_nele = nEle
                    allquantities.reg_2e2b_nmu = nMu
                    isZeeCR = True


        #2mu, 1 b-tagged
        if nMu==2 and nEle==0 and nTauTightMuon==0 and MuCRtrigstatus and ZmumuMass>60. and ZmumuMass<120. and ZmumuRecoil>200. and jetcond and pfMet > 0.:

#            CRCutFlow['nlepcond']+=1
            alllepPT=[lep.Pt() for lep in myMuos]
            lepindex=[i for i in range(len(myMuos))]

            sortedleps=[lep for pt,lep in sorted(zip(alllepPT,myMuos), reverse=True)]      # This gives a list of leps with their pTs in descending order
            sortedindex=[lepind for pt,lepind in sorted(zip(alllepPT,lepindex), reverse=True)]     # Indices of leps in myJetP4 in decscending order of jetPT

            iLeadLep=sortedindex[0]
            iSecondLep=sortedindex[1]

            if myMuos[iLeadLep].Pt() > 20. and myMuTightID[iLeadLep] and myMuIso[iLeadLep]<0.15 and myMuos[iSecondLep].Pt() > 10. and myMuLooseID[iSecondLep] and myMuIso[iSecondLep]<0.25:

                ZpT = math.sqrt( (myMuos[iLeadLep].Px()+myMuos[iSecondLep].Px())*(myMuos[iLeadLep].Px()+myMuos[iSecondLep].Px()) + (myMuos[iLeadLep].Py()+myMuos[iSecondLep].Py())*(myMuos[iLeadLep].Py()+myMuos[iSecondLep].Py()) )

                if SRnjetcond and ZmumuPhicond and SRFatjetcond:
                    allquantities.reg_2mu2b_N2DDT = N2DDT
                    allquantities.reg_2mu2b_N2    = N2

                if  SRnjetcond and ZmumuPhicond and SRFatjetcond and (N2DDT < 0):

                    allquantities.reg_2mu2b_Zmass = ZmumuMass
                    allquantities.reg_2mu2b_ZpT=ZpT

                    allquantities.reg_2mu2b_hadrecoil = ZmumuRecoil
                    allquantities.reg_2mu2b_MET = pfMet
                    allquantities.reg_2mu2b_ca15jet_pT = Fatjet1_pT

                    allquantities.reg_2mu2b_lep1_pT=myMuos[iLeadLep].Pt()
                    allquantities.reg_2mu2b_lep2_pT=myMuos[iSecondLep].Pt()

                    allquantities.reg_2mu2b_lep1_iso=myMuIso[iLeadLep]
                    allquantities.reg_2mu2b_lep2_iso=myMuIso[iSecondLep]
                    allquantities.reg_2mu2b_njet = nJets
                    # allquantities.reg_2mu2b_CA15Doublebtag  = CA15cvs[0]
                    # if nJets==1:
                    #     allquantities.reg_2mu2b_min_dPhi_jet_Recoil = min( [DeltaPhi(ZmumuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    #     allquantities.reg_2mu2b_min_dPhi_jet_MET = min( [DeltaPhi(pfMetPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    #allquantities.reg_2mu2b_min_dPhi_CAjet_MET=min_dPhi_CAjet_MET
                    #allquantities.reg_2mu2b_ntau = nTauTightMuon
                    #allquantities.reg_2mu2b_nele = nEle
                    allquantities.reg_2mu2b_nmu = nMu
                    isZmumuCR = True


# -------------------------------------------
# W CR
# -------------------------------------------

        #W CR specific bools

        WePhicond=True
        WmuPhicond=True

        WCond=False
        if ((nfailBjets==1 and nJets==1 ) or nJets==0):
            WCond=True

        if applydPhicut and nJets==1:
            #if WenuPhi>-10.:
            if DeltaPhi(WenuPhi,myJetP4[ifirstjet].Phi()) < 0.4: WePhicond=False
            #if WmunuPhi>-10.:
            if DeltaPhi(WmunuPhi,myJetP4[ifirstjet].Phi()) < 0.4: WmuPhicond=False


        #1e, 1 b-tagged
        if nEle==1 and nMu==0 and nTauTightElectron==0 and EleCRtrigstatus and WenuRecoil>200. and jetcond and Wenumass > 0. and pfMet > 50.:

            iLeadLep=0

            if myEles[iLeadLep].Pt() > 40. and myEleTightID[iLeadLep]:

                WpT = math.sqrt( ( pfMet*math.cos(pfMetPhi) + myEles[iLeadLep].Px())**2 + ( pfMet*math.sin(pfMetPhi) + myEles[iLeadLep].Py())**2)
                #

                if  WePhicond and SRFatjetcond and WCond:
                    allquantities.reg_1e2bW_N2DDT = N2DDT
                    allquantities.reg_1e2bW_N2    = N2

                if  WePhicond and SRFatjetcond and WCond and (N2DDT<0):

                    allquantities.reg_1e2bW_Wmass = Wenumass
                    allquantities.reg_1e2bW_WpT=WpT

                    allquantities.reg_1e2bW_hadrecoil = WenuRecoil
                    allquantities.reg_1e2bW_MET = pfMet
                    allquantities.reg_1e2bW_ca15jet_pT = Fatjet1_pT

                    allquantities.reg_1e2bW_lep1_pT=myEles[iLeadLep].Pt()
                    allquantities.reg_1e2bW_njet = nJets
                    # allquantities.reg_1e2bW_CA15Doublebtag  = CA15cvs[0]
                    if nJets==1:
                        allquantities.reg_1e2bW_min_dPhi_jet_Recoil = min( [DeltaPhi(WenuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                        allquantities.reg_1e2bW_min_dPhi_jet_MET = min( [DeltaPhi(pfMetPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    #allquantities.reg_1e2bW_min_dPhi_CAjet_MET=min_dPhi_CAjet_MET
                    #allquantities.reg_1e2bW_ntau = nTauTightElectron
                    #allquantities.reg_1e2bW_nele = nEle
                    allquantities.reg_1e2bW_nmu = nMu
                    isWenuCR2W = True


        #1mu, 1 b-tagged
        if nMu==1 and nEle==0 and nTauTightMuon==0 and MuCRtrigstatus and WmunuRecoil>200. and jetcond and Wmunumass > 0. and pfMet > 50.:
            iLeadLep=0

            if myMuos[iLeadLep].Pt() > 20. and myMuTightID[iLeadLep] and myMuIso[iLeadLep]<0.15:

                WpT = math.sqrt( ( pfMet*math.cos(pfMetPhi) + myMuos[iLeadLep].Px())**2 + ( pfMet*math.sin(pfMetPhi) + myMuos[iLeadLep].Py())**2)

                if  WmuPhicond and SRFatjetcond and WCond:
                    allquantities.reg_1mu2bW_N2DDT = N2DDT
                    allquantities.reg_1mu2bW_N2    = N2

                if  WmuPhicond and SRFatjetcond and WCond and (N2DDT <0):

                    allquantities.reg_1mu2bW_Wmass = Wmunumass
                    allquantities.reg_1mu2bW_WpT=WpT

                    allquantities.reg_1mu2bW_hadrecoil = WmunuRecoil
                    allquantities.reg_1mu2bW_MET = pfMet
                    allquantities.reg_1mu2bW_ca15jet_pT = Fatjet1_pT

                    allquantities.reg_1mu2bW_lep1_pT=myMuos[iLeadLep].Pt()
                    allquantities.reg_1mu2bW_lep1_iso=myMuIso[iLeadLep]
                    allquantities.reg_1mu2bW_njet = nJets
                    # allquantities.reg_1mu2bW_CA15Doublebtag  = CA15cvs[0]
                    if nJets==1:
                        allquantities.reg_1mu2bW_min_dPhi_jet_Recoil = min( [DeltaPhi(WmunuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                        allquantities.reg_1mu2bW_min_dPhi_jet_MET = min( [DeltaPhi(pfMetPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    #allquantities.reg_1mu2bW_min_dPhi_CAjet_MET=min_dPhi_CAjet_MET
                    #allquantities.reg_1mu2bW_ntau = nTauTightMuon
                    #allquantities.reg_1mu2bW_nele = nEle
                    allquantities.reg_1mu2bW_nmu = nMu
                    isWmunuCR2W = True


########--------------------------------------

#Top CR

        TopdPhicond2=True
	TopdPhicond1=True

        TopCond=False
        if nJets==1 and nBjets==1:
            TopCond=True

        if applydPhicut and nBjets==1:
        #     if WenuPhi>-10.:
            if DeltaPhi(WenuPhi,mybJetsP4[0].Phi()) < 0.4: TopdPhicond1=False
        #     if WmunuPhi>-10.:
            if DeltaPhi(WmunuPhi,mybJetsP4[0].Phi()) < 0.4: TopdPhicond2=False


        #1e, 1 b-tagged
        if nEle==1 and nMu==0 and nTauTightElectron==0 and EleCRtrigstatus and WenuRecoil>200. and jetcond and  Wenumass > 0. and pfMet > 50.:

            iLeadLep=0

            if myEles[iLeadLep].Pt() > 40. and myEleTightID[iLeadLep]:

                WpT = math.sqrt( ( pfMet*math.cos(pfMetPhi) + myEles[iLeadLep].Px())**2 + ( pfMet*math.sin(pfMetPhi) + myEles[iLeadLep].Py())**2)

                if TopdPhicond1 and SRFatjetcond and TopCond:
                    allquantities.reg_1e2bT_N2DDT = N2DDT
                    allquantities.reg_1e2bT_N2    = N2

                if TopdPhicond1 and SRFatjetcond and TopCond and (N2DDT<0):

                    allquantities.reg_1e2bT_Wmass = Wenumass
                    allquantities.reg_1e2bT_WpT=WpT

                    allquantities.reg_1e2bT_hadrecoil = WenuRecoil
                    allquantities.reg_1e2bT_MET = pfMet
                    allquantities.reg_1e2bT_ca15jet_pT = Fatjet1_pT

                    allquantities.reg_1e2bT_lep1_pT=myEles[iLeadLep].Pt()
                    allquantities.reg_1e2bT_njet = nJets
                    # allquantities.reg_1e2bT_CA15Doublebtag  = CA15cvs[0]
                    if nJets==1:
                        allquantities.reg_1e2bT_min_dPhi_jet_Recoil = min( [DeltaPhi(WenuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                        allquantities.reg_1e2bT_min_dPhi_jet_MET = min( [DeltaPhi(pfMetPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    #allquantities.reg_1e2bT_min_dPhi_CAjet_MET=min_dPhi_CAjet_MET
                    allquantities.reg_1e2bT_ntau = nTauTightElectron
                    allquantities.reg_1e2bT_nele = nEle
                    allquantities.reg_1e2bT_nmu = nMu
                    isWenuCR2T = True


        #1mu, 1 b-tagged
        if nMu==1 and nEle==0 and nTauTightMuon==0 and MuCRtrigstatus and WmunuRecoil>200. and jetcond and Wmunumass > 0. and pfMet > 50.:
            iLeadLep=0

            if myMuos[iLeadLep].Pt() > 20. and myMuTightID[iLeadLep] and myMuIso[iLeadLep]<0.15:

                #WpT = math.sqrt( ( pfMet*math.cos(pfMetPhi) + myMuos[iLeadLep].Px())**2 + ( pfMet*math.sin(pfMetPhi) + myMuos[iLeadLep].Py())**2)
                if  TopdPhicond2 and SRFatjetcond and TopCond:
                    allquantities.reg_1mu2bT_N2DDT = N2DDT
                    allquantities.reg_1mu2bT_N2    = N2

                if  TopdPhicond2 and SRFatjetcond and TopCond and (N2DDT<0):

                    allquantities.reg_1mu2bT_Wmass = Wmunumass
                    allquantities.reg_1mu2bT_WpT=WpT

                    allquantities.reg_1mu2bT_hadrecoil = WmunuRecoil
                    allquantities.reg_1mu2bT_MET = pfMet
                    allquantities.reg_1mu2bT_ca15jet_pT = Fatjet1_pT

                    allquantities.reg_1mu2bT_lep1_pT=myMuos[iLeadLep].Pt()
                    allquantities.reg_1mu2bT_lep1_iso=myMuIso[iLeadLep]
                    allquantities.reg_1mu2bT_njet = nJets
                    # allquantities.reg_1mu2bT_CA15Doublebtag  = CA15cvs[0]
                    if nJets==1:
                        allquantities.reg_1mu2bT_min_dPhi_jet_Recoil = min( [DeltaPhi(WmunuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                        allquantities.reg_1mu2bT_min_dPhi_jet_MET = min( [DeltaPhi(pfMetPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    #allquantities.reg_1mu2bT_min_dPhi_CAjet_MET=min_dPhi_CAjet_MET
                    allquantities.reg_1mu2bT_ntau = nTauTightMuon
                    allquantities.reg_1mu2bT_nele = nEle
                    allquantities.reg_1mu2bT_nmu = nMu
                    isWmunuCR2T = True

        # QCD CR

        # QCD2b_Cut_CA15          =   SR2_Cut_CA15
        # QCD2b_Cut1_nJets        =   SR2_Cut1_nJets
        # QCD2b_Cut2_nBjets       =   SR2_Cut2_nBjets
        # QCD2b_Cut3_trigstatus   =   SR2_Cut3_trigstatus
        # QCD2b_Cut4_jet1         =   SR2_Cut4_jet1
        # # QCD2b_Cut5_jet2         =   SR2_Cut5_jet2
        # #
        # # QCD2b_Cut6_jet3         =   SR2_Cut6_jet3
        # QCD2b_Cut7_dPhi_jet_MET =   not SR2_Cut7_dPhi_jet_MET
        # QCD2b_Cut8_nLep         =   SR2_Cut8_nLep
        # QCD2b_Cut9_pfMET        =   SR2_Cut9_pfMET
        #
        # if QCD2b_Cut1_nJets and QCD2b_Cut2_nBjets and QCD2b_Cut3_trigstatus and QCD2b_Cut4_jet1 and QCD2b_Cut7_dPhi_jet_MET and QCD2b_Cut8_nLep and QCD2b_Cut9_pfMET and QCD2b_Cut_CA15:
        #         allquantities.reg_QCD2b_MET         =   pfMet
        #         allquantities.reg_QCD2b_ca15jet_pT = Fatjet1_pT
        #         allquantities.reg_QCD2b_njet    =   nJets
        #         allquantities.reg_QCD2b_ntau    =   nTauLooseEleMu
        #         allquantities.reg_QCD2b_nele    =   nEle
        #         allquantities.reg_QCD2b_nmu     =   nMu
                # allquantities.reg_QCD2b_nUncleanEle =   nUncleanEle
                # allquantities.reg_QCD2b_nUncleanMu  =   nUncleanMu
                # allquantities.reg_QCD2b_nUncleanTau =   nUncleanTau
                # allquantities.reg_QCD2b_min_dPhi_jet_MET    =   min_dPhi_jet_MET
                # allquantities.reg_QCD2b_min_dPhi_CAjet_MET    =   min_dPhi_CAjet_MET
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------------------------------


        if pfmetstatus and SRlepcond and SRnjetcond:
            #print "pass"
            npass =+1

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
#       ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        genpTReweighting = 1.0
        if isData==1:   genpTReweighting  =  1.0
        if not isData :  genpTReweighting = GenWeightProducer(samplename, nGenPar, genParId, genMomParId, genParSt,genParP4)
#        print genpTReweighting
        #----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## MET reweights
        #----------------------------------------------------------------------------------------------------------------------------------------------------------------
        metTrig_firstmethodReweight=1.0
        metTrig_secondmethodReweight=1.0
        metTrig_firstmethodReweight_up=1.0
        metTrig_firstmethodReweight_down=1.0
        if writeSR:
            xbin1 = metTrig_firstmethod.GetXaxis().FindBin(pfMet)
            xbin2 = metTrig_secondmethod.GetXaxis().FindBin(pfMet)
            metTrig_firstmethodReweight = metTrig_firstmethod.GetBinContent(xbin1)
            metTrig_secondmethodReweight = metTrig_secondmethod.GetBinContent(xbin2)
            metTrig_firstmethodReweight_up = metTrig_firstmethodReweight + (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
            metTrig_firstmethodReweight_down = metTrig_firstmethodReweight - (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
        if ZmumuRecoil > 200:
            xbin1 = metTrig_firstmethod.GetXaxis().FindBin(ZmumuRecoil)
            xbin2 = metTrig_secondmethod.GetXaxis().FindBin(ZmumuRecoil)
            metTrig_firstmethodReweight = metTrig_firstmethod.GetBinContent(xbin1)
            metTrig_secondmethodReweight = metTrig_secondmethod.GetBinContent(xbin2)
            metTrig_firstmethodReweight_up = metTrig_firstmethodReweight + (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
            metTrig_firstmethodReweight_down = metTrig_firstmethodReweight - (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
        elif ZeeRecoil > 200:
            xbin1 = metTrig_firstmethod.GetXaxis().FindBin(ZeeRecoil)
            xbin2 = metTrig_secondmethod.GetXaxis().FindBin(ZeeRecoil)
            metTrig_firstmethodReweight = metTrig_firstmethod.GetBinContent(xbin1)
            metTrig_secondmethodReweight = metTrig_secondmethod.GetBinContent(xbin2)
            metTrig_firstmethodReweight_up = metTrig_firstmethodReweight + (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
            metTrig_firstmethodReweight_down = metTrig_firstmethodReweight - (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
        elif WmunuRecoil > 200:
            xbin1 = metTrig_firstmethod.GetXaxis().FindBin(WmunuRecoil)
            xbin2 = metTrig_secondmethod.GetXaxis().FindBin(WmunuRecoil)
            metTrig_firstmethodReweight = metTrig_firstmethod.GetBinContent(xbin1)
            metTrig_secondmethodReweight = metTrig_secondmethod.GetBinContent(xbin2)
            metTrig_firstmethodReweight_up = metTrig_firstmethodReweight + (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
            metTrig_firstmethodReweight_down = metTrig_firstmethodReweight - (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
        elif WenuRecoil > 200:
            xbin1 = metTrig_firstmethod.GetXaxis().FindBin(WenuRecoil)
            xbin2 = metTrig_secondmethod.GetXaxis().FindBin(WenuRecoil)
            metTrig_firstmethodReweight = metTrig_firstmethod.GetBinContent(xbin1)
            metTrig_secondmethodReweight = metTrig_secondmethod.GetBinContent(xbin2)
            metTrig_firstmethodReweight_up = metTrig_firstmethodReweight + (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
            metTrig_firstmethodReweight_down = metTrig_firstmethodReweight - (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
        elif TOPRecoil > 200:
            xbin1 = metTrig_firstmethod.GetXaxis().FindBin(TOPRecoil)
            xbin2 = metTrig_secondmethod.GetXaxis().FindBin(TOPRecoil)
            metTrig_firstmethodReweight = metTrig_firstmethod.GetBinContent(xbin1)
            metTrig_secondmethodReweight = metTrig_secondmethod.GetBinContent(xbin2)
            metTrig_firstmethodReweight_up = metTrig_firstmethodReweight + (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
            metTrig_firstmethodReweight_down = metTrig_firstmethodReweight - (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
        elif GammaRecoil > 200:
            xbin1 = metTrig_firstmethod.GetXaxis().FindBin(GammaRecoil)
            xbin2 = metTrig_secondmethod.GetXaxis().FindBin(GammaRecoil)
            metTrig_firstmethodReweight = metTrig_firstmethod.GetBinContent(xbin1)
            metTrig_secondmethodReweight = metTrig_secondmethod.GetBinContent(xbin2)
            metTrig_firstmethodReweight_up = metTrig_firstmethodReweight + (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
            metTrig_firstmethodReweight_down = metTrig_firstmethodReweight - (metTrig_firstmethodReweight-metTrig_secondmethodReweight)

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Muon reweight
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        #
        uni = random.uniform(0., 1.)
        muonTrig_SF = 1.0
        muonTrig_SF_systUP=1.0
        muonTrig_SF_systDOWN=1.0
        if nMu == 1:
            mupt = muP4[0].Pt()
            abeta = abs(muP4[0].Eta())
        if nMu == 2:
            if muP4[0].Pt() > muP4[1].Pt():
                leadmu=0
            else:
                leadmu=1
            mupt = muP4[leadmu].Pt()
            abeta = abs(muP4[leadmu].Eta())
        if nMu==1 or nMu==2:
            if uni < 0.54:
                xbin = muonTrigSFs_EfficienciesAndSF_RunBtoF.GetXaxis().FindBin(abeta)
                ybin = muonTrigSFs_EfficienciesAndSF_RunBtoF.GetYaxis().FindBin(mupt)
                muonTrig_SF *= muonTrigSFs_EfficienciesAndSF_RunBtoF.GetBinContent(xbin,ybin)
                muonTrig_SF_systUP *= muonTrigSFs_EfficienciesAndSF_RunBtoF.GetBinContent(xbin,ybin) + muonTrigSFs_EfficienciesAndSF_RunBtoF.GetBinErrorUp(xbin,ybin)
                muonTrig_SF_systDOWN *= muonTrigSFs_EfficienciesAndSF_RunBtoF.GetBinContent(xbin,ybin) - muonTrigSFs_EfficienciesAndSF_RunBtoF.GetBinErrorLow(xbin,ybin)
            elif uni > 0.54:
                xbin = muonTrigSFs_EfficienciesAndSF_Period4.GetXaxis().FindBin(abeta)
                ybin = muonTrigSFs_EfficienciesAndSF_Period4.GetYaxis().FindBin(mupt)
                muonTrig_SF *= muonTrigSFs_EfficienciesAndSF_Period4.GetBinContent(xbin,ybin)
                muonTrig_SF_systUP *= muonTrigSFs_EfficienciesAndSF_Period4.GetBinContent(xbin,ybin) + muonTrigSFs_EfficienciesAndSF_Period4.GetBinErrorUp(xbin,ybin)
                muonTrig_SF_systDOWN *= muonTrigSFs_EfficienciesAndSF_Period4.GetBinContent(xbin,ybin) - muonTrigSFs_EfficienciesAndSF_Period4.GetBinErrorLow(xbin,ybin)
        muIDSF_loose = 1.0
        muIDSF_loose_systUP=1.0
        muIDSF_loose_systDOWN=1.0
        muIDSF_tight = 1.0
        muIDSF_tight_systUP=1.0
        muIDSF_tight_systDOWN=1.0
        for imu in range(nMu):
            mupt = muP4[imu].Pt()
            abeta = abs(muP4[imu].Eta())
            if uni < 0.54:
                if mupt > 20:
                    xbin = muonTightIDSFs_EfficienciesAndSF_BCDEF.GetXaxis().FindBin(abeta)
                    ybin = muonTightIDSFs_EfficienciesAndSF_BCDEF.GetYaxis().FindBin(mupt)
                    muIDSF_tight *= muonTightIDSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin)
                    muIDSF_tight_systUP *= (muonTightIDSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin) + muonTightIDSFs_EfficienciesAndSF_BCDEF.GetBinErrorUp(xbin,ybin))
                    muIDSF_tight_systDOWN *= (muonTightIDSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin) - muonTightIDSFs_EfficienciesAndSF_BCDEF.GetBinErrorLow(xbin,ybin))
                else:
                    xbin = muonLooseIDSFs_EfficienciesAndSF_BCDEF.GetXaxis().FindBin(abeta)
                    ybin = muonLooseIDSFs_EfficienciesAndSF_BCDEF.GetYaxis().FindBin(mupt)
                    muIDSF_loose *= muonLooseIDSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin)
                    muIDSF_loose_systUP *= (muonLooseIDSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin) + muonLooseIDSFs_EfficienciesAndSF_BCDEF.GetBinErrorUp(xbin,ybin))
                    muIDSF_loose_systDOWN *= (muonLooseIDSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin) - muonLooseIDSFs_EfficienciesAndSF_BCDEF.GetBinErrorLow(xbin,ybin))
            if uni > 0.54:
                if mupt > 20:
                    xbin = muonTightIDSFs_EfficienciesAndSF_GH.GetXaxis().FindBin(abeta)
                    ybin = muonTightIDSFs_EfficienciesAndSF_GH.GetYaxis().FindBin(mupt)
                    muIDSF_tight *= muonTightIDSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin)
                    muIDSF_tight_systUP *= (muonTightIDSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin) - muonTightIDSFs_EfficienciesAndSF_GH.GetBinErrorUp(xbin,ybin))
                    muIDSF_tight_systDOWN *= (muonTightIDSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin) + muonTightIDSFs_EfficienciesAndSF_GH.GetBinErrorLow(xbin,ybin))
                else:
                    xbin = muonLooseIDSFs_EfficienciesAndSF_GH.GetXaxis().FindBin(abeta)
                    ybin = muonLooseIDSFs_EfficienciesAndSF_GH.GetYaxis().FindBin(mupt)
                    muIDSF_loose *= muonLooseIDSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin)
                    muIDSF_loose_systUP *= (muonLooseIDSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin) + muonLooseIDSFs_EfficienciesAndSF_GH.GetBinErrorUp(xbin,ybin))
                    muIDSF_loose_systDOWN *= (muonLooseIDSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin) - muonLooseIDSFs_EfficienciesAndSF_GH.GetBinErrorLow(xbin,ybin))

        muIsoSF_loose = 1.0
        muIsoSF_loose_systUP=1.0
        muIsoSF_loose_systDOWN=1.0
        muIsoSF_tight = 1.0
        muIsoSF_tight_systUP=1.0
        muIsoSF_tight_systDOWN=1.0
        for imu in range(nMu):
            mupt = muP4[imu].Pt()
            abeta = abs(muP4[imu].Eta())
            muiso = MuIso[imu]
            if uni < 0.54:
                if muiso < 0.15:
                    xbin = muonTightIsoSFs_EfficienciesAndSF_BCDEF.GetXaxis().FindBin(abeta)
                    ybin = muonTightIsoSFs_EfficienciesAndSF_BCDEF.GetYaxis().FindBin(mupt)
                    muIsoSF_tight *= muonTightIsoSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin)
                    muIsoSF_tight_systUP *= (muonTightIsoSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin) + muonTightIsoSFs_EfficienciesAndSF_BCDEF.GetBinErrorUp(xbin,ybin))
                    muIsoSF_tight_systDOWN *= (muonTightIsoSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin) - muonTightIsoSFs_EfficienciesAndSF_BCDEF.GetBinErrorLow(xbin,ybin))
                elif muiso < 0.25:
                    xbin = muonLooseIsoSFs_EfficienciesAndSF_BCDEF.GetXaxis().FindBin(abeta)
                    ybin = muonLooseIsoSFs_EfficienciesAndSF_BCDEF.GetYaxis().FindBin(mupt)
                    muIsoSF_loose *= muonLooseIsoSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin)
                    muIsoSF_loose_systUP *= (muonLooseIsoSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin) + muonLooseIsoSFs_EfficienciesAndSF_BCDEF.GetBinErrorUp(xbin,ybin))
                    muIsoSF_loose_systDOWN *= (muonLooseIsoSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin) - muonLooseIsoSFs_EfficienciesAndSF_BCDEF.GetBinErrorLow(xbin,ybin))
            if uni > 0.54:
                if muiso < 0.15:
                    xbin = muonTightIsoSFs_EfficienciesAndSF_GH.GetXaxis().FindBin(abeta)
                    ybin = muonTightIsoSFs_EfficienciesAndSF_GH.GetYaxis().FindBin(mupt)
                    muIsoSF_tight *= muonTightIsoSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin)
                    muIsoSF_tight_systUP *= (muonTightIsoSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin) + muonTightIsoSFs_EfficienciesAndSF_GH.GetBinErrorUp(xbin,ybin))
                    muIsoSF_tight_systDOWN *= (muonTightIsoSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin) - muonTightIsoSFs_EfficienciesAndSF_GH.GetBinErrorLow(xbin,ybin))
                elif muiso < 0.25:
                    xbin = muonLooseIsoSFs_EfficienciesAndSF_GH.GetXaxis().FindBin(abeta)
                    ybin = muonLooseIsoSFs_EfficienciesAndSF_GH.GetYaxis().FindBin(mupt)
                    muIsoSF_loose *= muonLooseIsoSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin)
                    muIsoSF_loose_systUP *= (muonLooseIsoSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin) + muonLooseIsoSFs_EfficienciesAndSF_GH.GetBinErrorUp(xbin,ybin))
                    muIsoSF_loose_systDOWN *= (muonLooseIsoSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin) - muonLooseIsoSFs_EfficienciesAndSF_GH.GetBinErrorLow(xbin,ybin))

        muTracking_SF = 1.0
        muTracking_SF_systUP=1.0
        muTracking_SF_systDOWN=1.0
        for imu in range(nMu):
            abeta = abs(muP4[imu].Eta())
            muTracking_SF *= muonTrackingSFs_EfficienciesAndSF_BCDEFGH.Eval(abeta)
            ybin = muonTrackingSFs_EfficienciesAndSF_BCDEFGH.GetYaxis().FindBin(abeta)
            muTracking_SF_systUP *= (muonTrackingSFs_EfficienciesAndSF_BCDEFGH.Eval(abeta) + muonTrackingSFs_EfficienciesAndSF_BCDEFGH.GetErrorYhigh(ybin))
            muTracking_SF_systDOWN *= (muonTrackingSFs_EfficienciesAndSF_BCDEFGH.Eval(abeta) - muonTrackingSFs_EfficienciesAndSF_BCDEFGH.GetErrorYlow(ybin))


        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Electron reweight
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        eleTrig_reweight = 1.0
        eleTrig_reweight_systUP = 1.0
        eleTrig_reweight_systDOWN = 1.0
        if nEle == 1:
            elept = eleP4[0].Pt()
            eleeta = eleP4[0].Eta()
        if nEle == 2:
            if eleP4[0].Pt() > eleP4[1].Pt():
                leadele=0
            else:
                leadele=1
            elept = eleP4[leadele].Pt()
            eleeta = eleP4[leadele].Eta()
        if nEle==1 or nEle==2:
            xbin = eleTrig_hEffEtaPt.GetXaxis().FindBin(eleeta)
            ybin = eleTrig_hEffEtaPt.GetYaxis().FindBin(elept)
            eleTrig_reweight *= eleTrig_hEffEtaPt.GetBinContent(xbin,ybin)
            eleTrig_reweight_systUP *= (eleTrig_hEffEtaPt.GetBinContent(xbin,ybin) + eleTrig_hEffEtaPt.GetBinErrorUp(xbin,ybin))
            eleTrig_reweight_systDOWN *= (eleTrig_hEffEtaPt.GetBinContent(xbin,ybin) - eleTrig_hEffEtaPt.GetBinErrorLow(xbin,ybin))
#            print 'eleTrig_reweight_systUP, eleTrig_reweight, eleTrig_reweight_systDOWN', eleTrig_reweight_systUP, eleTrig_reweight, eleTrig_reweight_systDOWN


        eleRecoSF = 1.0
        eleRecoSF_systUP = 1.0
        eleRecoSF_systDOWN = 1.0
        for iele in range(nEle):
            elept = eleP4[iele].Pt()
            eleeta = eleP4[iele].Eta()
            xbin = eleRecoSF_EGamma_SF2D.GetXaxis().FindBin(eleeta)
            ybin = eleRecoSF_EGamma_SF2D.GetYaxis().FindBin(elept)
            eleRecoSF *= eleRecoSF_EGamma_SF2D.GetBinContent(xbin,ybin)
            eleRecoSF_systUP *= (eleRecoSF_EGamma_SF2D.GetBinContent(xbin,ybin) + eleRecoSF_EGamma_SF2D.GetBinErrorUp(xbin,ybin))
            eleRecoSF_systDOWN *= (eleRecoSF_EGamma_SF2D.GetBinContent(xbin,ybin) - eleRecoSF_EGamma_SF2D.GetBinErrorLow(xbin,ybin))
#            print 'eleRecoSF_systUP, eleRecoSF, eleRecoSF_systDOWN', eleRecoSF_systUP, eleRecoSF, eleRecoSF_systDOWN


        eleIDSF_loose = 1.0
        eleIDSF_loose_systUP = 1.0
        eleIDSF_loose_systDOWN = 1.0
        eleIDSF_tight = 1.0
        eleIDSF_tight_systUP = 1.0
        eleIDSF_tight_systDOWN = 1.0
        for iele in range(nEle):
            elept = eleP4[iele].Pt()
            eleeta = eleP4[iele].Eta()
            if elept > 40:
                xbin = eleTightIDSF_EGamma_SF2D.GetXaxis().FindBin(eleeta)
                ybin = eleTightIDSF_EGamma_SF2D.GetYaxis().FindBin(elept)
                eleIDSF_tight *= eleTightIDSF_EGamma_SF2D.GetBinContent(xbin,ybin)
                eleIDSF_tight_systUP *= (eleTightIDSF_EGamma_SF2D.GetBinContent(xbin,ybin) + eleTightIDSF_EGamma_SF2D.GetBinErrorUp(xbin,ybin))
                eleIDSF_tight_systDOWN *= (eleTightIDSF_EGamma_SF2D.GetBinContent(xbin,ybin) - eleTightIDSF_EGamma_SF2D.GetBinErrorLow(xbin,ybin))
            else:
                xbin = eleLooseIDSF_EGamma_SF2D.GetXaxis().FindBin(eleeta)
                ybin = eleLooseIDSF_EGamma_SF2D.GetYaxis().FindBin(elept)
                eleIDSF_loose *= eleLooseIDSF_EGamma_SF2D.GetBinContent(xbin,ybin)
                eleIDSF_loose_systUP *= (eleLooseIDSF_EGamma_SF2D.GetBinContent(xbin,ybin) + eleLooseIDSF_EGamma_SF2D.GetBinErrorUp(xbin,ybin))
                eleIDSF_loose_systDOWN *= (eleLooseIDSF_EGamma_SF2D.GetBinContent(xbin,ybin) - eleLooseIDSF_EGamma_SF2D.GetBinErrorLow(xbin,ybin))

        #eleVetoCutBasedIDSF = 1.0
        #for iele in range(nEle):
        #    elept = eleP4[iele].Pt()
        #    eleeta = eleP4[iele].Eta()
        #    xbin = eleVetoCutBasedIDSF_egammaEffi_txt_EGM2D.GetXaxis().FindBin(eleeta)
        #    ybin = eleVetoCutBasedIDSF_egammaEffi_txt_EGM2D.GetYaxis().FindBin(elept)
        #    eleVetoCutBasedIDSF *= eleVetoCutBasedIDSF_egammaEffi_txt_EGM2D.GetBinContent(xbin,ybin)

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Pileup weight
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
#        allpuweights = PUWeight()
#        len_puweight = len(allpuweights)
        puweight = 0.0
        if isData: puweight = 1.0
        if not isData:
#            if pu_nTrueInt  <= len_puweight: puweight = allpuweights[pu_nTrueInt-1]
#            if pu_nTrueInt  > len_puweight : puweight = 0.0
            if pu_nTrueInt < 100:
                puweight = pileup2016histo.GetBinContent(pu_nTrueInt)
            else:
                puweight = 1.

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Total weight
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        if puweight == 0.0:
            puweight = 1.0

        if genpTReweighting == 0.0:
            genpTReweighting = 1.0

        if metTrig_firstmethodReweight == 0.0:
            metTrig_firstmethodReweight = 1.0

        if metTrig_firstmethodReweight_up == 0.0:
            metTrig_firstmethodReweight_up = 1.0

        if metTrig_firstmethodReweight_down == 0.0:
            metTrig_firstmethodReweight_down = 1.0

        muweights = muonTrig_SF * muIDSF_loose * muIDSF_tight * muIsoSF_loose * muIsoSF_tight * muTracking_SF
        if muweights == 0.0:
            muweights = 1.0

        #eleweights = eleTrig_reweight * eleRecoSF * eleIDSF_loose * eleIDSF_tight * eleVetoCutBasedIDSF
        eleweights = eleTrig_reweight * eleRecoSF * eleIDSF_loose * eleIDSF_tight
        if eleweights == 0.0:
            eleweights = 1.0

        allweights = puweight * mcweight * genpTReweighting * eleweights * metTrig_firstmethodReweight * muweights

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        temp_weight_withOutBtag = allweights
        ## BTag Scale Factor

#        if SRnjetcond:
        if nJets==0:
            sf_resolved1.append(1.0)
        else:
            ij=0
            jj=1
            reader1.eval_auto_bounds('central', 0, 1.2, 50.)
            flav1 = jetflav(myJetHadronFlavor[ij])
            sf_resolved1 = weightbtag(reader1, flav1, myJetP4[ij].Pt(), myJetP4[ij].Eta())
            if nJets > 1:
                flav2 = jetflav(myJetHadronFlavor[jj])
                sf_resolved2 = weightbtag(reader1, flav2, myJetP4[jj].Pt(), myJetP4[jj].Eta())

        # if SRnjetcond or WCond:
        #     if sf_resolved1[0]==0.0:
        #         sf_resolved1[0]=1.0
        #     if sf_resolved2[0]==0.0:
        #         sf_resolved2[0]=1.0
        #     allweights = allweights * sf_resolved1[0]


        if TopCond:
            if sf_resolved1[0]==0.0:
                sf_resolved1[0]=1.0
        #    if sf_resolved2[0]==0.0:
        #        sf_resolved2[0]=1.0
            allweights = allweights * sf_resolved1[0]



        temp_original_weight  = allweights
        allweights_ewkW_down = temp_original_weight
        allweights_ewkW_up = temp_original_weight
        allweights_ewkZ_down = temp_original_weight
        allweights_ewkZ_up = temp_original_weight
        allweights_ewkTop_down = temp_original_weight
        allweights_ewkTop_up = temp_original_weight
        allweights_metTrig_up = temp_original_weight
        allweights_metTrig_down = temp_original_weight

        allweights_metTrig_up = (allweights/metTrig_firstmethodReweight)*metTrig_firstmethodReweight_up
        allweights_metTrig_down = (allweights/metTrig_firstmethodReweight)*metTrig_firstmethodReweight_down
        temp_weight_withBtag = allweights/(eleweights*muweights)

        if isData: allweights = 1.0
        allweights_noPU = allweights/puweight


#----------------------------------------------------------------------------------------------------------------------------------------------------------------

        if samplename=="WJETS":
            allweights_ewkW_down = temp_original_weight/genpTReweighting
            allweights_ewkW_up = temp_original_weight*genpTReweighting
            allquantities.weight_ewkW_up  = allweights_ewkW_up
            allquantities.weight_ewkW_down  =  allweights_ewkW_down

        if samplename == "ZJETS":
            allweights_ewkZ_down = temp_original_weight/genpTReweighting
            allweights_ewkZ_up = temp_original_weight*genpTReweighting
            allquantities.weight_ewkZ_up  = allweights_ewkZ_up
            allquantities.weight_ewkZ_down  =  allweights_ewkZ_down
        if samplename == "TT":
            allweights_ewkTop_down = temp_original_weight/genpTReweighting
            allweights_ewkTop_up = temp_original_weight*genpTReweighting
            allquantities.weight_ewkTop_up  = allweights_ewkTop_up
            allquantities.weight_ewkTop_down  =  allweights_ewkTop_down
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #SR2 Cutflow

            if SR_Cut3_trigstatus:
                cutStatusSR['trig']+=allweights

                if SR_Cut9_pfMET:
                    cutStatusSR['MET']+=allweights

                    if SR_Cut_nFATJet:
                        cutStatusSR['nFATJet']+=allweights

                        # if UncleanedFatjet[selFatjet].Pt() >200.0:
                        #     cutStatusSR['FatjetPT']+=allweights
                        #
                        #     if SDMass[selFatjet] > 100.0 and SDMass[selFatjet] < 150 :
                        #         cutStatusSR['SDMass']+=allweights

                        if SR_Cut1_nJets:
                            cutStatusSR['nJets']+=allweights

                            if SR_Cut4_jet1:
                                cutStatusSR['JetCond']+=allweights

                                if SR_Cut8_nLep:
                                    cutStatusSR['nlepCond']+=allweights
                                    if N2DDT <0:
                                        cutStatusSR['N2DDT']+=allweights


        # 2e cutflow

        for CRreg in regionnames:
            exec("CR"+CRreg+"CutFlow['datatrig']+=allweights")


        if EleCRtrigstatus:
            CR2e2bCutFlow['trig']+=allweights

            if ZeeRecoil>200.:
                CR2e2bCutFlow['recoil']+=allweights

                if pfMet > 0.:
                    CR2e2bCutFlow['realMET']+=allweights

                    if ZeeMass>60. and ZeeMass<120.:
                        CR2e2bCutFlow['mass']+=allweights

                        if SRFatjetcond:
                            CR2e2bCutFlow['nFATJet']+=allweights

                            # if UncleanedFatjet[selFatjet].Pt() >200.0:
                            #     CR2e2bCutFlow['FatjetPT']+=allweights
                            #
                            #     if SDMass[selFatjet] > 100.0 and SDMass[selFatjet] < 150 :
                            #         CR2e2bCutFlow['SDMass']+=allweights

                            if (nJets==0 or nJets ==1):
                                CR2e2bCutFlow['nJets']+=allweights

                                if jetcond:
                                    CR2e2bCutFlow['JetCond']+=allweights
                    #CR2e2bCutFlow['nlepCond']+=allweights
                                    if nEle==2 and nMu==0 and nTauTightElectron==0:
                                        CR2e2bCutFlow['nlep']+=allweights
                                        if myEles[0].Pt()>myEles[1].Pt():
                                            iLeadLep=0
                                            iSecondLep=1
                                        else:
                                            iLeadLep=1
                                            iSecondLep=0

                                        if myEles[iLeadLep].Pt() > 40. and myEleTightID[iLeadLep] and myEles[iSecondLep].Pt() > 10. and myEleLooseID[iSecondLep]:
                                            CR2e2bCutFlow['nlepCond']+=allweights
                                            if N2DDT <0:
                                                CR2e2bCutFlow['N2DDT']+=allweights




        if MuCRtrigstatus:
            CR2mu2bCutFlow['trig']+=allweights

            if ZmumuRecoil>200.:
                CR2mu2bCutFlow['recoil']+=allweights

                if pfMet > 0.:
                    CR2mu2bCutFlow['realMET']+=allweights

                    if ZmumuMass>60. and ZmumuMass<120.:
                        CR2mu2bCutFlow['mass']+=allweights

                        if SRFatjetcond:
                            CR2mu2bCutFlow['nFATJet']+=allweights

                            # if UncleanedFatjet[selFatjet].Pt() >200.0:
                            #     CR2mu2bCutFlow['FatjetPT']+=allweights
                            #
                            #     if SDMass[selFatjet] > 100.0 and SDMass[selFatjet] < 150 :
                            #         CR2mu2bCutFlow['SDMass']+=allweights

                            if WCond:
                                CR2mu2bCutFlow['nJets']+=allweights

                                if jetcond:
                                    CR2mu2bCutFlow['JetCond']+=allweights

                                    if nMu==2 and nEle==0 and nTauTightMuon==0:
                                        CR2mu2bCutFlow['nlep']+=allweights
                                        if myMuos[0].Pt()>myMuos[1].Pt():
                                            iLeadLep=0
                                            iSecondLep=1
                                        else:
                                            iLeadLep=1
                                            iSecondLep=0

                                        if myMuos[iLeadLep].Pt() > 20. and myMuTightID[iLeadLep] and myMuIso[iLeadLep]<0.15 and myMuos[iSecondLep].Pt() > 10. and myMuLooseID[iSecondLep] and myMuIso[iSecondLep]<0.25:
                                            CR2mu2bCutFlow['nlepCond']+=allweights
                                            if N2DDT <0:
                                                CR2mu2bCutFlow['N2DDT']+=allweights


        if EleCRtrigstatus:
            CR1e2bWCutFlow['trig']+=allweights

            if WenuRecoil>200.:
                CR1e2bWCutFlow['recoil']+=allweights

                if pfMet > 50.:
                    CR1e2bWCutFlow['realMET']+=allweights

                    if Wenumass>0:
                        CR1e2bWCutFlow['mass']+=allweights

                        if SRFatjetcond:
                            CR1e2bWCutFlow['nFATJet']+=allweights

                            # if UncleanedFatjet[selFatjet].Pt() >200.0:
                            #     CR1e2bWCutFlow['FatjetPT']+=allweights
                            #
                            #     if SDMass[selFatjet] > 100.0 and SDMass[selFatjet] < 150 :
                            #         CR1e2bWCutFlow['SDMass']+=allweights

                            if WCond:
                                CR1e2bWCutFlow['nJets']+=allweights

                                if jetcond:
                                    CR1e2bWCutFlow['JetCond']+=allweights

                                    if nEle==1 and nMu==0 and nTauTightElectron==0:
                                        CR1e2bWCutFlow['nlep']+=allweights

                                        if myEles[0].Pt() > 40. and myEleTightID[0]:
                                            CR1e2bWCutFlow['nlepCond']+=allweights
                                            if N2DDT <0:
                                                CR1e2bWCutFlow['N2DDT']+=allweights


  #Cutflow
        if MuCRtrigstatus:
            CR1mu2bWCutFlow['trig']+=allweights

            if WmunuRecoil>200.:
                CR1mu2bWCutFlow['recoil']+=allweights

                if pfMet > 50.:
                    CR1mu2bWCutFlow['realMET']+=allweights

                    if Wmunumass>0.:
                        CR1mu2bWCutFlow['mass']+=allweights

                        if SRFatjetcond:
                            CR1mu2bWCutFlow['nFATJet']+=allweights

                            # if UncleanedFatjet[selFatjet].Pt() >200.0:
                            #     CR1mu2bWCutFlow['FatjetPT']+=allweights
                            #
                            #     if SDMass[selFatjet] > 100.0 and SDMass[selFatjet] < 150 :
                            #         CR1mu2bWCutFlow['SDMass']+=allweights

                            if (nJets==0 or nJets ==1):
                                CR1mu2bWCutFlow['nJets']+=allweights

                                if jetcond:
                                    CR1mu2bWCutFlow['JetCond']+=allweights


                                    if nEle==0 and nMu==1 and nTauTightMuon==0:
                                        CR1mu2bWCutFlow['nlep']+=allweights

                                        if myMuos[0].Pt() > 30. and myMuTightID[0] and myMuIso[0]<0.15:
                                            CR1mu2bWCutFlow['nlepCond']+=allweights
                                            if N2DDT <0:
                                                CR1mu2bWCutFlow['N2DDT']+=allweights



        if EleCRtrigstatus:
            CR1e2bTCutFlow['trig']+=allweights

            if WenuRecoil>200.:
                CR1e2bTCutFlow['recoil']+=allweights

                if pfMet > 50.:
                    CR1e2bTCutFlow['realMET']+=allweights

                    if Wenumass>0.:
                        CR1e2bTCutFlow['mass']+=allweights

                        if SRFatjetcond:
                            CR1e2bTCutFlow['nFATJet']+=allweights

                            # if UncleanedFatjet[selFatjet].Pt() >200.0:
                            #     CR1e2bTCutFlow['FatjetPT']+=allweights
                            #
                            #     if SDMass[selFatjet] > 100.0 and SDMass[selFatjet] < 150 :
                            #         CR1e2bTCutFlow['SDMass']+=allweights

                            if TopCond:
                                CR1e2bTCutFlow['nJets']+=allweights

                                if jetcond:
                                    CR1e2bTCutFlow['JetCond']+=allweights

                                    if nEle==1 and nMu==0 and nTauTightElectron==0:
                                        CR1e2bTCutFlow['nlep']+=allweights

                                        if myEles[0].Pt() > 40. and myEleTightID[0]:
                                            CR1e2bTCutFlow['nlepCond']+=allweights
                                            if N2DDT <0:
                                                CR1e2bTCutFlow['N2DDT']+=allweights



  #Cutflow
        if MuCRtrigstatus:
            CR1mu2bTCutFlow['trig']+=allweights

            if WmunuRecoil>200.:
                CR1mu2bTCutFlow['recoil']+=allweights

                if pfMet > 50.:
                    CR1mu2bTCutFlow['realMET']+=allweights

                    if Wmunumass>0.:
                        CR1mu2bTCutFlow['mass']+=allweights

                        if SRFatjetcond:
                            CR1mu2bTCutFlow['nFATJet']+=allweights

                            # if UncleanedFatjet[selFatjet].Pt() >200.0:
                            #     CR1mu2bTCutFlow['FatjetPT']+=allweights
                            #
                            #     if SDMass[selFatjet] > 100.0 and SDMass[selFatjet] < 150 :
                            #         CR1mu2bTCutFlow['SDMass']+=allweights

                            if TopCond:
                                CR1mu2bTCutFlow['nJets']+=allweights

                                if jetcond:
                                    CR1mu2bTCutFlow['JetCond']+=allweights

                                    if nEle==0 and nMu==1 and nTauTightMuon==0:
                                        CR1mu2bTCutFlow['nlep']+=allweights

                                        if myMuos[0].Pt() > 20. and myMuTightID[0] and myMuIso[0]<0.15:
                                            CR1mu2bTCutFlow['nlepCond']+=allweights
                                            if N2DDT <0:
                                                CR1mu2bTCutFlow['N2DDT']+=allweights

 # # ---
        #CR Summary
        if isZeeCR:
            CRSummaryEle['2e2b']+=allweights

        if isZmumuCR:
            CRSummaryMu['2#mu2b']+=allweights

        if isWenuCR2W:
            CRSummaryEle['1e2bW']+=allweights

        if isWenuCR2T:
            CRSummaryEle['1e2bT']+=allweights

        if isWmunuCR2W:
            CRSummaryMu['1#mu2bW']+=allweights

        if isWmunuCR2T:
            CRSummaryMu['1#mu2bT']+=allweights


 #--------------------------------------------------------------------------------------------------------------------------------------------------------------------
        allquantities.met             = pfMet
        allquantities.N_e             = nEle
        allquantities.N_mu            = nMu
        allquantities.N_tau           = nTauLooseEleMu
        allquantities.N_Pho           = nPho
        allquantities.N_b             = nBjets
        allquantities.N_j             = nJets
        allquantities.weight          = allweights
        # allquantities.weight_NoPU     = allweights_noPU
        # allquantities.weight_met_up   = allweights_metTrig_up
        # allquantities.weight_met_down = allweights_metTrig_down
        allquantities.totalevents     = 1

        btag_sysnum=0
#         for btag_sysnum in[1,2]:
#             allweights = temp_weight_withOutBtag
#             # if SR1njetcond:
#             #     if sf_resolved1[btag_sysnum]==0.0: sf_resolved1[btag_sysnum]=1.0
#             #     allweights = allweights*sf_resolved1[btag_sysnum]
#             #     if nJets>1:
#             #         if sf_resolved2[btag_sysnum]==0.0: sf_resolved2[btag_sysnum]=1.0
#             #         allweights = allweights *sf_resolved2[btag_sysnum]
#             if TopCond:
#                 if sf_resolved1[btag_sysnum]==0.0: sf_resolved1[btag_sysnum]=1.0
#                 # if sf_resolved2[btag_sysnum]==0.0: sf_resolved2[btag_sysnum]=1.0
#                 allweights = allweights * sf_resolved1[btag_sysnum] * sf_resolved2[btag_sysnum]
#                 if nJets>2:
#                     if sf_resolved3[btag_sysnum]==0.0: sf_resolved3[btag_sysnum]=1.0
#                     allweights = allweights * sf_resolved3[btag_sysnum]
# #                print 'btag central weight', temp_original_weight
#                 if btag_sysnum==2:
#                     allquantities.weight_btag_up = allweights
# #                    print 'btag up weight', allweights
#                 if btag_sysnum==1:
#                     allquantities.weight_btag_down = allweights
#                    print 'btag down weight', allweights
        allweights = temp_weight_withBtag
        muweights_systUP = muonTrig_SF_systUP * muIDSF_loose_systUP * muIDSF_tight_systUP * muIsoSF_loose_systUP * muIsoSF_tight_systUP * muTracking_SF_systUP
        muweights_systDOWN = muonTrig_SF_systDOWN * muIDSF_loose_systDOWN * muIDSF_tight_systDOWN * muIsoSF_loose_systDOWN * muIsoSF_tight_systDOWN * muTracking_SF_systDOWN
        eleweights_systUP = eleTrig_reweight_systUP * eleRecoSF_systUP * eleIDSF_loose_systUP * eleIDSF_tight_systUP
        eleweights_systDOWN = eleTrig_reweight_systDOWN * eleRecoSF_systDOWN * eleIDSF_loose_systDOWN * eleIDSF_tight_systDOWN
        if muweights_systUP == 0.0:
            muweights_systUP = 1.0
        if muweights_systDOWN == 0.0:
            muweights_systDOWN = 1.0
        if eleweights_systUP == 0.0:
            eleweights_systUP = 1.0
        if eleweights_systDOWN == 0.0:
            eleweights_systDOWN = 1.0
#                print 'muweights_systUP, eleweights_systUP',muweights_systUP ,eleweights_systUP
#                print 'muweights_systDOWN, eleweights_systDOWN',muweights_systDOWN,eleweights_systDOWN
        allweights = allweights * muweights_systUP * eleweights_systUP
        allquantities.weight_lep_up = allweights
        allweights = temp_weight_withBtag
        allweights = allweights * muweights_systDOWN * eleweights_systDOWN
        allquantities.weight_lep_down = allweights

        nPV = myJetNPV

        allquantities.PuReweightPV = nPV
        allquantities.noPuReweightPV = nPV

        if nMu==2 and nEle==0 and MuCRtrigstatus:
            allquantities.mu_PuReweightPV = nPV*puweight
            allquantities.mu_noPuReweightPV = nPV

        if nEle==2 and nMu==0 and EleCRtrigstatus:
            allquantities.ele_PuReweightPV = nPV*puweight
            allquantities.ele_noPuReweightPV = nPV
        #
        # if nPho==1 and nEle==0 and nMu==0 and PhotonCRtrigstatus:
        #     allquantities.pho_PuReweightPV = nPV
        #     allquantities.pho_noPuReweightPV = nPV

        #print (allquantities.regime, allquantities.met,allquantities.mass )
        allquantities.FillRegionHisto()
        allquantities.FillHisto()

    #print cutStatus
    NEntries_Weight = h_t_weight.Integral()
    NEntries_total  = h_t.Integral()
    # cutStatus['total'] = int(NEntries_total)
    # cutStatusSR1['total'] = int(NEntries_total)
    cutStatusSR['total'] = int(NEntries_total)

    for CRreg in regionnames:
        exec("CR"+CRreg+"CutFlow['total']=int(NEntries_total)")


    #cutStatusSR1['pfmet'] = cutStatus['pfmet']
    #cutStatusSR2['pfmet'] = cutStatus['pfmet']
    print "Total events =", int(NEntries_total)
    print "Preselected events=", cutStatus['preselection']
    print "Selected events =", npass

    # Cutflow
    cutflowTable=""
    cutflowHeader=""
    cutflowvalues=[]
    #cutflownames=['total','preselection','pfmet','njet+nBjet','jet1','jet2/3','lep']
    # for cutflowname in cutflownames:
    #     cutflowvalues.append(cutStatus[cutflowname])
    #     cutflowTable += str(cutStatus[cutflowname])+" "
    #     cutflowHeader += cutflowname+" "

    cutflowvaluesSR=[]
    #cutflownamesSR1=['total','preselection','pfmet','njet+nBjet','jet1','jet2','lep']
    # for cutflowname in cutflownamesSR1:
    #     cutflowvaluesSR1.append(cutStatusSR1[cutflowname])

    cutflowvaluesSR=[]
    #cutflownamesSR2=['total','preselection','pfmet','njet+nBjet','jet1','jet2','jet3','lep']
    for cutflowname in cutflownamesSR:
        cutflowvaluesSR.append(cutStatusSR[cutflowname])

    # CR counts
    CRTable=""
    CRHeader=""
    CRvalues=[]
    # for CRname in CRs:
    #     CRvalues.append(CRStatus[CRname])
    #     CRTable += str(CRStatus[CRname])+" "
    #     CRHeader += CRname+" "

    #Cutflows for SR1 and SR2
    print "\nCutflow:"
    # print cutStatus
    # print
    # print "SR1:"
    # print cutStatusSR1
    print
    print "SR:"
    print cutStatusSR
    #print
    #print "CRs:"
    #print CRStatus
#    print
#    print "CR Cutflow:"
#    print CRCutFlow
    # print

    CRcutflowvaluesSet=[]
    CRcutnames=['total','preselection']+CRcutnames
    for CRreg in regionnames:
        CFvalues=[]
        for cutname in CRcutnames:
            exec("CFvalues.append(CR"+CRreg+"CutFlow['"+cutname+"'])")
        CRcutflowvaluesSet.append(CFvalues)

    # print CRSummary

    allquantities.WriteHisto((NEntries_total,NEntries_Weight,npass,cutflowvaluesSR,cutflownamesSR,CRvalues,CRs,regionnames,CRcutnames,CRcutflowvaluesSet,CRSummaryMu,regNamesMu, CRSummaryEle,regNamesEle))

    if NEntries > 0:
        eff=round(float(npass/float(NEntries_total)),5)
    else:
        eff = "NA"
    print "efficiency =", eff

#    os.system("mkdir -p "+outputdir+'/efficiencyfiles/')

#    f = open(outputdir+'/efficiencyfiles/'+textfile, 'w')
#    f.write(str(eff)+"\n\n#Cutflow Table:\n"+cutflowHeader[:-1]+"\n"+cutflowTable[:-1]+"\n\n#CR Table:\n"+CRHeader[:-1]+"\n"+CRTable[:-1])
    print "ROOT file written to", outfilename
#    print "Log written to "+outputdir+'/efficiencyfiles/'+textfile
#    f.close()
    print "Completed."




def CheckFilter(filterName, filterResult,filtercompare):
    ifilter_=0
    filter1 = False
    for ifilter in filterName:
        filter1 = (ifilter.find(filtercompare) != -1)  & (bool(filterResult[ifilter_]) == True)
        if filter1: break
        ifilter_ = ifilter_ + 1
    return filter1





######################################
######################################
######################################
def MakeTable():
    print "called MakeTable"
    files= [inputfilename]
    legend=legendTemplate
    prefix="V_met_"
    effnamelist = [prefix + ihisto  for ihisto in namelist]
    inputfile={}
    histList=[]
    for ifile_ in range(len(files)):
        print ("opening file  "+files[ifile_])
        inputfile[ifile_] = TFile( files[ifile_] )
        print "fetching histograms"
        for ihisto_ in range(len(effnamelist)):
            histo = inputfile[ifile_].Get(effnamelist[ihisto_])
            histList.append(histo)

    for ih in range(len(histList)):
        eff = ("%0.4f" % float(histList[ih].Integral()/histList[0].Integral()))
        toprint =  legendTemplate[ih] + " & " + str(eff) + " \\\\"
        print toprint


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

def DeltaPhi(phi1,phi2):
   phi = Phi_mpi_pi(phi1-phi2)

   return abs(phi)

def DeltaR(P4_1,P4_2):
    return math.sqrt(  (  P4_1.Eta()-P4_2.Eta() )**2  + (  DeltaPhi(P4_1.Phi(),P4_2.Phi()) )**2 )


def Phi_mpi_pi(x):
    kPI = 3.14159265358979323846
    kTWOPI = 2 * kPI

    while (x >= kPI): x = x - kTWOPI;
    while (x < -kPI): x = x + kTWOPI;
    return x;

def weightbtag(reader, flav, pt, eta):
    sf_c = reader.eval_auto_bounds('central', flav, eta, pt)
    sf_low = reader.eval_auto_bounds('down', flav, eta, pt)
    sf_up  = reader.eval_auto_bounds('up', flav, eta, pt)
    btagsf = [sf_c, sf_low, sf_up]
    return btagsf

def jetflav(flav):
    if flav == 5:
        flavor = 0
    elif flav == 4:
        flavor = 1
    else:
        flavor = 2
    return flavor




def GenWeightProducer(sample,nGenPar, genParId, genMomParId, genParSt,genParP4):
    pt__=0;
    #print " inside gen weight "
    k2=1.0
    #################
    # WJets
    #################
    if sample=="WJETS":
        goodLepID = []
        for ig in range(nGenPar):
            PID    = genParId[ig]
            momPID = genMomParId[ig]
            status = genParSt[ig]
            if ( (abs(PID) != 11) & (abs(PID) != 12) &  (abs(PID) != 13) & (abs(PID) != 14) &  (abs(PID) != 15) &  (abs(PID) != 16) ): continue
            if ( ( (status != 1) & (abs(PID) != 15)) | ( (status != 2) & (abs(PID) == 15)) ): continue
            if ( (abs(momPID) != 24) & (momPID != PID) ): continue
            goodLepID.append(ig)

        if len(goodLepID) == 2 :
            l4_thisLep = genParP4[goodLepID[0]]
            l4_thatLep = genParP4[goodLepID[1]]
            l4_z = l4_thisLep + l4_thatLep

            pt = l4_z.Pt()
            pt__ = pt

            k2 = -0.830041 + 7.93714 *TMath.Power( pt - (-877.978) ,(-0.213831) ) ;

    #################
    #ZJets
    #################
    if sample == "ZJETS":
        goodLepID = []
        for ig in range(nGenPar):
            PID    = genParId[ig]
            momPID = genMomParId[ig]
            status = genParSt[ig]


            if ( (abs(PID) != 12) &  (abs(PID) != 14) &  (abs(PID) != 16) ) : continue
            if ( status != 1 ) : continue
            if ( (momPID != 23) & (momPID != PID) ) : continue
            goodLepID.append(ig)

        if len(goodLepID) == 2 :
            l4_thisLep = genParP4[goodLepID[0]]
            l4_thatLep = genParP4[goodLepID[1]]
            l4_z = l4_thisLep + l4_thatLep
            pt = l4_z.Pt()
            k2 = -0.180805 + 6.04146 *TMath.Power( pt - (-759.098) ,(-0.242556) ) ;

    #################
    #TTBar
    #################
    if (sample=="TT"):
        goodLepID = []
        for ig in range(nGenPar):
            PID    = genParId[ig]
            momPID = genMomParId[ig]
            status = genParSt[ig]
            if ( abs(PID) == 6) :
                goodLepID.append(ig)
        if(len(goodLepID)==2):
            l4_thisLep = genParP4[goodLepID[0]]
            l4_thatLep = genParP4[goodLepID[1]]
            pt1 = TMath.Min(400.0, l4_thisLep.Pt())
            pt2 = TMath.Min(400.0, l4_thatLep.Pt())

            w1 = TMath.Exp(0.156 - 0.00137*pt1);
            w2 = TMath.Exp(0.156 - 0.00137*pt2);
            k2 =  1.001*TMath.Sqrt(w1*w2);

    if(sample=="all"):
        k2 = 1.0

    return k2


def MT(Pt, met, dphi):
    return ROOT.TMath.Sqrt( 2 * Pt * met * (1.0 - ROOT.TMath.Cos(dphi)) )

if __name__ == "__main__":
    ## analyze the tree and make histograms and all the 2D plots and Efficiency plots.
    if options.analyze:
        print "now calling analyzedataset"
        AnalyzeDataSet()
