#!/usr/bin/env python
from ROOT import TFile, TTree, TH1F, TH1D, TH1, TCanvas, TChain,TGraphAsymmErrors, TMath, TH2D, TLorentzVector, AddressOf, gROOT, TNamed
import ROOT as ROOT
import os
import sys, optparse
from array import array
import math
import numpy as numpy_

ROOT.gROOT.LoadMacro("Loader.h+")

#to find which sample is being used
#def WhichSample(filename):
#    samplename = 'all'
#    if filename.find('WJets')>-1:
#        samplename = 'WJETS'
#    elif filename.find('ZJets')>-1:
#        samplename = 'ZJETS'
#    elif filename.find('TT')>-1:
#        samplename  = 'TT'
#    else:
#        samplename = 'all'
#    return samplename

## When not running on farmout
#inputfilename= 'FileList.txt' uncomment it for providing list of file
outfilename= 'SkimmedTree.root'
PUPPI = True
CA15  = True

## When running on farmout
#inputfilename = os.environ['INPUT']
#outfilename   = os.environ['OUTPUT']


skimmedTree = TChain("tree/treeMaker")
##======use this for providing list of file======##
#infile = open(inputfilename)
#for ifile in infile:
#    skimmedTree.Add(ifile.rstrip())
#    samplename = WhichSample(inputfilename)
##======use this for providing list of file======##
skimmedTree.Add(sys.argv[1])
#samplename = WhichSample(sys.argv[1])

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
    CSVMWP=0.8484
    DCSVMWP=0.6324
    NEntries = skimmedTree.GetEntries()
#    NEntries = 1000
    h_total = TH1F('h_total','h_total',2,0,2)
    h_total_mcweight = TH1F('h_total_mcweight','h_total_mcweight',2,0,2)

    triglist=['HLT_PFMET170_','HLT_PFMET170_NoiseCleaned','HLT_PFMET170_JetIdCleaned_v','HLT_PFMET170_HBHECleaned_v',
        'HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v','HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v','HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v',
        'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v','HLT_PFMET110_PFMHT110_','HLT_IsoMu24_v','HLT_IsoTkMu24_v','HLT_IsoMu27_v','HLT_IsoTkMu27_v','HLT_Ele27_WPTight_Gsf',
        'HLT_IsoMu20','HLT_Ele27_WPLoose_Gsf','HLT_Ele105_CaloIdVT_GsfTrkIdT_v','HLT_Ele115_CaloIdVT_GsfTrkIdT_v','HLT_Ele32_WPTight_Gsf_v','HLT_Ele32_eta2p1_WPTight_Gsf_v','HLT_Ele27_eta2p1_WPTight_Gsf_v','HLT_Photon165_HE10','HLT_Photon175']

#['HLT_PFMET170_','HLT_PFMET170_NoiseCleaned','HLT_PFMET170_JetIdCleaned_v','HLT_PFMET170_HBHECleaned_v','HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v','HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v','HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v','HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v','HLT_PFMET110_PFMHT110_','HLT_IsoMu24_v','HLT_IsoTkMu24_v','HLT_IsoMu27_v','HLT_IsoTkMu27_v','HLT_Ele27_WPTight_Gsf','HLT_Ele105_CaloIdVT_GsfTrkIdT_v','HLT_Ele115_CaloIdVT_GsfTrkIdT_v','HLT_Ele32_WPTight_Gsf_v','HLT_IsoMu20','HLT_Ele27_eta2p1_WPTight_Gsf_v','HLT_Ele27_WPLoose_Gsf_v','HLT_Ele32_eta2p1_WPTight_Gsf_v','HLT_Photon165_HE10','HLT_Photon175']

#    METtrigs = ['HLT_PFMET120_Mu5_v', 'HLT_MET600_v', 'HLT_PFMET100_PFMHT100_IDTight_v', 'HLT_MET250_v', 'HLT_PFMET400_v', 'HLT_PFMETTypeOne190_HBHE_BeamHaloCleaned_v', 'HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v', 'HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v', 'HLT_PFMET90_PFMHT90_IDTight_v', 'HLT_Mu6_PFHT200_PFMET100_v', 'HLT_PFMET600_v', 'HLT_Mu14er_PFMET100_v', 'HLT_PFMET170_NoiseCleaned_v', 'HLT_CaloMHTNoPU90_PFMET90_PFMHT90_IDTight_v', 'HLT_PFMET170_NotCleaned_v', 'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v', 'HLT_PFMET100_PFMHT100_IDTight_BeamHaloCleaned_v', 'HLT_Mu3er_PFHT140_PFMET125_v', 'HLT_MET200_v', 'HLT_PFMET170_HBHE_BeamHaloCleaned_v', 'HLT_MET75_IsoTrk50_v', 'HLT_MET90_IsoTrk50_v', 'HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v', 'HLT_DoubleMu3_PFMET50_v', 'HLT_MonoCentralPFJet80_PFMETNoMu110_PFMHTNoMu110_IDTight_v', 'HLT_PFMET110_PFMHT110_IDTight_v', 'HLT_DiCentralPFJet55_PFMET110_v', 'HLT_MET700_v', 'HLT_MonoCentralPFJet80_PFMETNoMu90_PFMHTNoMu90_IDTight_v', 'HLT_MET60_IsoTrk35_Loose_v', 'HLT_PFMET170_JetIdCleaned_v', 'HLT_PFMET170_BeamHaloCleaned_v', 'HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight_v', 'HLT_MET300_v', 'HLT_PFMET120_PFMHT120_IDTight_v', 'HLT_Mu6_PFHT200_PFMET80_BTagCSV_p067_v', 'HLT_MonoCentralPFJet80_PFMETNoMu100_PFMHTNoMu100_IDTight_v', 'HLT_CaloMHTNoPU90_PFMET90_PFMHT90_IDTight_BTagCSV_p067_v', 'HLT_PFMET170_HBHECleaned_v', 'HLT_PFMET120_BTagCSV_p067_v', 'HLT_PFMET500_v','HLT_PFMET300_v']

#    SingleElectrontrigs=['HLT_Ele15_IsoVVVL_PFHT350_PFMET50_v', 'HLT_Ele45_WPLoose_Gsf_v', 'HLT_Ele32_eta2p1_WPLoose_Gsf_v', 'HLT_Ele27_WPTight_Gsf_L1JetTauSeeded_v', 'HLT_Ele32_WPTight_Gsf_v', 'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v', 'HLT_Ele105_CaloIdVT_GsfTrkIdT_v', 'HLT_Ele25_eta2p1_WPTight_Gsf_v', 'HLT_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v', 'HLT_Ele32_eta2p1_WPTight_Gsf_v', 'HLT_Ele27_WPLoose_Gsf_v', 'HLT_Ele27_eta2p1_WPLoose_Gsf_DoubleMediumIsoPFTau32_Trk1_eta2p1_Reg_v', 'HLT_Ele27_WPLoose_Gsf_WHbbBoost_v', 'HLT_Ele27_eta2p1_WPLoose_Gsf_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v', 'HLT_Ele300_CaloIdVT_GsfTrkIdT_v', 'HLT_Ele35_WPLoose_Gsf_v', 'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet140_v', 'HLT_Ele50_IsoVVVL_PFHT400_v', 'HLT_Ele25_eta2p1_WPLoose_Gsf_v', 'HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v' , 'HLT_Ele250_CaloIdVT_GsfTrkIdT_v', 'HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v', 'HLT_Ele15_IsoVVVL_PFHT400_PFMET50_v', 'HLT_Ele24_eta2p1_WPLoose_Gsf_v', 'HLT_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau29_v', 'HLT_Ele32_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v', 'HLT_Ele27_WPTight_Gsf_v', 'HLT_Ele15_IsoVVVL_PFHT350_v', 'HLT_Ele35_CaloIdVT_GsfTrkIdT_PFJet150_PFJet50_v', 'HLT_Ele30_eta2p1_WPLoose_Gsf_v', 'HLT_Ele200_CaloIdVT_GsfTrkIdT_v', 'HLT_Ele30_eta2p1_WPTight_Gsf_v', 'HLT_Ele45_WPLoose_Gsf_L1JetTauSeeded_v', 'HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30_v', 'HLT_Ele22_eta2p1_WPLoose_Gsf_v', 'HLT_Ele15_IsoVVVL_BTagCSV_p067_PFHT400_v', 'HLT_Ele36_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v', 'HLT_Ele115_CaloIdVT_GsfTrkIdT_v', 'HLT_Ele23_WPLoose_Gsf_v', 'HLT_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v', 'HLT_Ele145_CaloIdVT_GsfTrkIdT_v', 'HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v', 'HLT_Ele23_WPLoose_Gsf_WHbbBoost_v', 'HLT_Ele20_eta2p1_WPLoose_Gsf_LooseIsoPFTau28_v', 'HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v', 'HLT_Ele27_eta2p1_WPLoose_Gsf_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg_v', 'HLT_Ele27_eta2p1_WPTight_Gsf_v', 'HLT_Ele15_IsoVVVL_PFHT400_v', 'HLT_Ele30_WPTight_Gsf_v', 'HLT_Ele15_IsoVVVL_PFHT600_v', 'HLT_Ele27_eta2p1_WPLoose_Gsf_v', 'HLT_Ele25_WPTight_Gsf_v']

#    SinglePhotontrigs = ['HLT_Photon120_R9Id90_HE10_Iso40_EBOnly_PFMET40_v',
#    'HLT_Photon120_R9Id90_HE10_Iso40_EBOnly_VBF_v',
#    'HLT_Photon120_R9Id90_HE10_IsoM_v',
#    'HLT_Photon120_v',
#    'HLT_Photon135_PFMET100_v',
#    'HLT_Photon165_HE10_v',
#    'HLT_Photon165_R9Id90_HE10_IsoM_v',
#    'HLT_Photon175_v',
#    'HLT_Photon22_R9Id90_HE10_Iso40_EBOnly_PFMET40_v',
#    'HLT_Photon22_R9Id90_HE10_Iso40_EBOnly_VBF_v',
#    'HLT_Photon22_R9Id90_HE10_IsoM_v',
#    'HLT_Photon22_v',
#    'HLT_Photon250_NoHE_v',
#    'HLT_Photon300_NoHE_v',
#    'HLT_Photon30_R9Id90_HE10_IsoM_v',
#    'HLT_Photon30_v',
#    'HLT_Photon36_R9Id90_HE10_Iso40_EBOnly_PFMET40_v',
#    'HLT_Photon36_R9Id90_HE10_Iso40_EBOnly_VBF_v',
#    'HLT_Photon36_R9Id90_HE10_IsoM_v',
#    'HLT_Photon36_v',
#    'HLT_Photon500_v',
#    'HLT_Photon50_R9Id90_HE10_Iso40_EBOnly_PFMET40_v',
#    'HLT_Photon50_R9Id90_HE10_Iso40_EBOnly_VBF_v',
#    'HLT_Photon50_R9Id90_HE10_IsoM_v',
#    'HLT_Photon50_v',
#    'HLT_Photon600_v',
#    'HLT_Photon75_R9Id90_HE10_Iso40_EBOnly_PFMET40_v',
#    'HLT_Photon75_R9Id90_HE10_Iso40_EBOnly_VBF_v',
#    'HLT_Photon75_R9Id90_HE10_IsoM_v',
#    'HLT_Photon75_v',
#    'HLT_Photon90_CaloIdL_PFHT500_v',
#    'HLT_Photon90_CaloIdL_PFHT600_v',
#    'HLT_Photon90_R9Id90_HE10_Iso40_EBOnly_PFMET40_v',
#    'HLT_Photon90_R9Id90_HE10_Iso40_EBOnly_VBF_v',
#    'HLT_Photon90_R9Id90_HE10_IsoM_v',
#    'HLT_Photon90_v']



    outfile = TFile(outfilename,'RECREATE')

    outTree = TTree( 'outTree', 'tree branches' )
    samplepath = TNamed('samplepath', str(sys.argv[1]))

    st_runId            = numpy_.zeros(1, dtype=int)
    st_lumiSection      = array( 'L', [ 0 ] )
    st_eventId          = array( 'L', [ 0 ] )
    st_pfMetCorrPt      = array( 'f', [ 0. ] )
    st_pfMetCorrPhi     = array( 'f', [ 0. ] )
    st_pfMetUncJetResUp       = ROOT.std.vector('float')()
    st_pfMetUncJetResDown     = ROOT.std.vector('float')()
    st_pfMetUncJetEnUp        = ROOT.std.vector('float')()
    st_pfMetUncJetEnDown      = ROOT.std.vector('float')()
    st_isData           = array( 'b', [ 0 ] )

    for trigs in triglist:
        exec("st_"+trigs+"  = array( 'b', [ 0 ] )")
#    st_HLT_IsoMu20      = array( 'b', [ 0 ] )
#    st_HLT_Ele27_WPLoose_Gsf = array( 'b', [ 0 ] )
#    st_MET_trig = array( 'b', [ 0 ] )
#    st_SE_trig  = array( 'b', [ 0 ] )
#    st_SP_trig  = array( 'b', [ 0 ] )

    maxn = 10

    st_THINnJet                     = array( 'L', [ 0 ] ) #ROOT.std.vector('int')()
    st_THINjetP4                    = ROOT.std.vector('TLorentzVector')()
    st_THINjetCISVV2                = ROOT.std.vector('float')()
    st_THINjetHadronFlavor          = ROOT.std.vector('int')()
    st_THINjetNHadEF                = ROOT.std.vector('float')()
    st_THINjetCHadEF                = ROOT.std.vector('float')()

    st_THINjetCEmEF                 = ROOT.std.vector('float')()
    st_THINjetPhoEF                 = ROOT.std.vector('float')()
    st_THINjetEleEF                 = ROOT.std.vector('float')()
    st_THINjetMuoEF                 = ROOT.std.vector('float')()
    st_THINjetCorrUnc               = ROOT.std.vector('float')()

    st_AK4deepCSVnJet               = array( 'L', [ 0 ] ) #ROOT.std.vector('int')()
    st_AK4deepCSVjetP4              = ROOT.std.vector('TLorentzVector')()
    st_AK4deepCSVNNCorrjetP4        = ROOT.std.vector('TLorentzVector')()
    st_AK4deepCSVjetDeepCSV_b       = ROOT.std.vector('float')()
    st_AK4deepCSVjetHadronFlavor    = ROOT.std.vector('int')()
    st_AK4deepCSVjetNHadEF          = ROOT.std.vector('float')()
    st_AK4deepCSVjetCHadEF          = ROOT.std.vector('float')()
    st_AK4deepCSVjetCorrUnc         = ROOT.std.vector('float')()



#AK8Jets
    st_AK8nthikJets               = array( 'L', [ 0 ] ) #ROOT.std.vector('int')()
    st_AK8thikjetP4               = ROOT.std.vector('TLorentzVector')()
    st_AK8thikjetNhadEF           = ROOT.std.vector('float')()
    st_AK8thikjetChadEF           = ROOT.std.vector('float')()
    st_AK8SDmass                  = ROOT.std.vector('float')()
    st_AK8Puppijet_DoubleSV       = ROOT.std.vector('float')()
    st_AK8thikJetLooseID          = ROOT.std.vector('float')()
    st_AK8thikjetTightID          = ROOT.std.vector('float')()
    st_AK8PuppisubjetCSV          = ROOT.std.vector(ROOT.std.vector('float'))()


#CA15Jets
    st_CA15njets                =array( 'L', [ 0 ] ) #ROOT.std.vector('int')()
    st_CA15jetP4                = ROOT.std.vector('TLorentzVector')()
    st_CA15jetNhadEF            = ROOT.std.vector('float')()
    st_CA15jetChadEF            = ROOT.std.vector('float')()
    st_CA15SDmass               = ROOT.std.vector('float')()
    st_CA15Puppi_doublebtag     = ROOT.std.vector('float')()
    st_CA15PuppiECF_2_3_10      = ROOT.std.vector('float')()
    st_CA15PuppiECF_1_2_10      = ROOT.std.vector('float')()
    st_CA15PassIDTight          = ROOT.std.vector('bool')()
    st_CA15PassIDLoose          = ROOT.std.vector('bool')()
    st_CA15PuppisubjetCSV       = ROOT.std.vector(ROOT.std.vector('float'))()



    st_nEle                = array( 'L', [ 0 ] ) #ROOT.std.vector('int')()
    st_eleP4               = ROOT.std.vector('TLorentzVector')()
    st_eleIsPassLoose      = ROOT.std.vector('bool')()
    st_eleIsPassMedium     = ROOT.std.vector('bool')()
    st_eleIsPassTight      = ROOT.std.vector('bool')()
   # st_eleIsPassVeto       = ROOT.std.vector('bool')()

    st_nPho                = array( 'L', [ 0 ] ) #ROOT.std.vector('int')()
    st_phoP4               = ROOT.std.vector('TLorentzVector')()
    st_phoIsPassLoose      = ROOT.std.vector('bool')()
    st_phoIsPassMedium     = ROOT.std.vector('bool')()
    st_phoIsPassTight      = ROOT.std.vector('bool')()

    st_nMu= array( 'L', [ 0 ] ) #ROOT.std.vector('int')()
    st_muP4                = ROOT.std.vector('TLorentzVector')()
    st_isLooseMuon         = ROOT.std.vector('bool')()
    st_isMediumMuon        = ROOT.std.vector('bool')()
    st_isTightMuon         = ROOT.std.vector('bool')()
    st_muChHadIso          = ROOT.std.vector('float')()
    st_muNeHadIso          = ROOT.std.vector('float')()
    st_muGamIso            = ROOT.std.vector('float')()
    st_muPUPt              = ROOT.std.vector('float')()
    st_muCharge            = ROOT.std.vector('int')()

#    st_trigResult          = ROOT.std.vector('bool')()
#    st_trigName            = ROOT.std.vector('string')()

    st_HPSTau_n= array( 'L', [ 0 ] ) #ROOT.std.vector('int')()
    st_HPSTau_4Momentum= ROOT.std.vector('TLorentzVector')()

    st_disc_againstElectronLoose    =    ROOT.std.vector('bool')()
    st_disc_againstElectronMedium   =    ROOT.std.vector('bool')()
    st_disc_againstElectronTight    =    ROOT.std.vector('bool')()
    st_disc_againstMuonLoose        =    ROOT.std.vector('bool')()
#    st_disc_againstMuonMedium       =    ROOT.std.vector('bool')()
    st_disc_againstMuonTight        =    ROOT.std.vector('bool')()
    #st_disc_LooseIsolationMVA    =    ROOT.std.vector('bool')()


    mcweight = array( 'f', [ 0 ] )
    st_pu_nTrueInt= array( 'f', [ 0 ] ) #ROOT.std.vector('std::vector<float>')()
    st_pu_nPUVert= array( 'f', [ 0 ] )
    st_THINjetNPV= array( 'f', [ 0 ] ) #ROOT.std.vector('std::vector<float>')()
    st_AK4deepCSVjetNPV= array( 'f', [ 0 ] )

    st_nGenPar = array( 'L', [ 0 ] )
    st_genParId = ROOT.std.vector('int')()
    st_genMomParId = ROOT.std.vector('int')()
    st_genParSt = ROOT.std.vector('int')()
    st_genParP4 = ROOT.std.vector('TLorentzVector')()

    WenuRecoil = array( 'f', [ 0. ] )
    Wenumass = array( 'f', [ 0. ] )
    WenuPhi = array( 'f', [ 0. ] )

    WmunuRecoil = array( 'f', [ 0. ] )
    Wmunumass = array( 'f', [ 0. ] )
    WmunuPhi = array( 'f', [ 0. ] )

    ZeeRecoil = array( 'f', [ 0. ] )
    ZeeMass = array( 'f', [ 0. ] )
    ZeePhi = array( 'f', [ 0. ] )

    ZmumuRecoil = array( 'f', [ 0. ] )
    ZmumuMass = array( 'f', [ 0. ] )
    ZmumuPhi = array( 'f', [ 0. ] )

    TOPRecoil = array( 'f', [ 0. ] )
    TOPPhi = array( 'f', [ 0. ] )

    GammaRecoil = array('f',[0.])
    GammaPhi = array( 'f', [ 0. ] )

    outTree.Branch( 'st_runId', st_runId , 'st_runId/L')
    outTree.Branch( 'st_lumiSection', st_lumiSection , 'st_lumiSection/L')
    outTree.Branch( 'st_eventId',  st_eventId, 'st_eventId/L')
    outTree.Branch( 'st_pfMetCorrPt', st_pfMetCorrPt , 'st_pfMetCorrPt/F')
    outTree.Branch( 'st_pfMetCorrPhi', st_pfMetCorrPhi , 'st_pfMetCorrPhi/F')
    outTree.Branch( 'st_pfMetUncJetResUp', st_pfMetUncJetResUp)
    outTree.Branch( 'st_pfMetUncJetResDown', st_pfMetUncJetResDown)
    outTree.Branch( 'st_pfMetUncJetEnUp', st_pfMetUncJetEnUp )
    outTree.Branch( 'st_pfMetUncJetEnDown', st_pfMetUncJetEnDown)
    outTree.Branch( 'st_isData', st_isData , 'st_isData/O')

    for trigs in triglist:
        exec("outTree.Branch( 'st_"+trigs+"', st_"+trigs+" , 'st_"+trigs+"/O')")

#    outTree.Branch( 'st_MET_trig', st_MET_trig , 'st_MET_trig/O')
#    outTree.Branch( 'st_SE_trig', st_SE_trig , 'st_SE_trig/O')
#    outTree.Branch( 'st_SP_trig', st_SP_trig , 'st_SP_trig/O')
#    outTree.Branch( 'st_HLT_IsoMu20', st_HLT_IsoMu20 , 'st_HLT_IsoMu20/O')
#    outTree.Branch( 'st_HLT_Ele27_WPLoose_Gsf', st_HLT_Ele27_WPLoose_Gsf , 'st_HLT_Ele27_WPLoose_Gsf/O')

    outTree.Branch( 'st_THINnJet',st_THINnJet, 'st_THINnJet/L' )
    outTree.Branch( 'st_THINjetP4',st_THINjetP4 )
    outTree.Branch( 'st_THINjetCISVV2',st_THINjetCISVV2 )
    outTree.Branch( 'st_THINjetHadronFlavor',st_THINjetHadronFlavor )
    outTree.Branch( 'st_THINjetNHadEF',st_THINjetNHadEF )
    outTree.Branch( 'st_THINjetCHadEF',st_THINjetCHadEF )

    outTree.Branch( 'st_THINjetCEmEF',st_THINjetCEmEF )
    outTree.Branch( 'st_THINjetPhoEF',st_THINjetPhoEF )
    outTree.Branch( 'st_THINjetEleEF',st_THINjetEleEF )
    outTree.Branch( 'st_THINjetMuoEF',st_THINjetMuoEF )
    outTree.Branch('st_THINjetCorrUnc', st_THINjetCorrUnc)

    outTree.Branch( 'st_AK4deepCSVnJet',st_AK4deepCSVnJet, 'st_AK4deepCSVnJet/L' )
    outTree.Branch( 'st_AK4deepCSVjetP4',st_AK4deepCSVjetP4 )
    outTree.Branch('st_AK4deepCSVNNCorrjetP4',st_AK4deepCSVNNCorrjetP4)
    outTree.Branch( 'st_AK4deepCSVjetDeepCSV_b',st_AK4deepCSVjetDeepCSV_b )
    outTree.Branch( 'st_AK4deepCSVjetHadronFlavor',st_AK4deepCSVjetHadronFlavor )
    outTree.Branch( 'st_AK4deepCSVjetNHadEF',st_AK4deepCSVjetNHadEF )
    outTree.Branch( 'st_AK4deepCSVjetCHadEF',st_AK4deepCSVjetCHadEF )


#AK8 JETS BRANCHES
    outTree.Branch( 'st_AK8nthikJets',st_AK8nthikJets,'st_AK8nthikJets/L' )
    outTree.Branch( 'st_AK8thikjetP4',st_AK8thikjetP4)
    #outTree.Branch( 'st_AK8thikjetNhadEF',st_AK8thikjetNhadEF)
    #outTree.Branch( 'st_AK8thikjetChadEF',st_AK8thikjetChadEF)
    outTree.Branch( 'st_AK8SDmass',st_AK8SDmass)
    #outTree.Branch( 'st_AK8PuppisubjetCSV',st_AK8PuppisubjetCSV)
    outTree.Branch( 'st_AK8Puppijet_DoubleSV',st_AK8Puppijet_DoubleSV)

    #outTree.Branch( 'st_AK8thikJetLooseID',st_AK8thikJetLooseID)
    outTree.Branch( 'st_AK8thikjetTightID',st_AK8thikjetTightID)


#CA15jets
    outTree.Branch( 'st_CA15njets',st_CA15njets,'st_CA15njets/L')
    outTree.Branch( 'st_CA15jetP4',st_CA15jetP4)
    #outTree.Branch( 'st_CA15jetNhadEF',st_CA15jetNhadEF)
    #outTree.Branch( 'st_CA15jetChadEF',st_CA15jetChadEF)
    outTree.Branch( 'st_CA15SDmass',st_CA15SDmass)
    #outTree.Branch( 'st_CA15PuppisubjetCSV',st_CA15PuppisubjetCSV)
    outTree.Branch( 'st_CA15Puppi_doublebtag',st_CA15Puppi_doublebtag)
    outTree.Branch( 'st_CA15PuppiECF_2_3_10',st_CA15PuppiECF_2_3_10)
    outTree.Branch( 'st_CA15PuppiECF_1_2_10',st_CA15PuppiECF_1_2_10)
    #outTree.Branch( 'st_CA15PassIDLoose',st_CA15PassIDLoose)
    outTree.Branch( 'st_CA15PassIDTight',st_CA15PassIDTight)






    outTree.Branch( 'st_nEle',st_nEle , 'st_nEle/L')
    outTree.Branch( 'st_eleP4',st_eleP4 )
#    outTree.Branch('st_eleIsPassVeto',st_eleIsPassVeto)
    #outTree.Branch( 'st_eleIsPassLoose', st_eleIsPassLoose)#, 'st_eleIsPassLoose/O' )
    outTree.Branch( 'st_eleIsPassMedium', st_eleIsPassMedium)#, 'st_eleIsPassMedium/O' )
    outTree.Branch( 'st_eleIsPassTight', st_eleIsPassTight)#, 'st_eleIsPassTight/O' )

    outTree.Branch( 'st_nPho',st_nPho , 'st_nPho/L')
    outTree.Branch( 'st_phoP4',st_phoP4 )
    #outTree.Branch( 'st_phoIsPassLoose', st_phoIsPassLoose)#, 'st_phoIsPassLoose/O' )
    outTree.Branch( 'st_phoIsPassMedium', st_phoIsPassMedium)#, 'st_phoIsPassMedium/O' )
    outTree.Branch( 'st_phoIsPassTight', st_phoIsPassTight)#, 'st_phoIsPassTight/O' )


    outTree.Branch( 'st_nMu',st_nMu , 'st_nMu/L')
    outTree.Branch( 'st_muP4',st_muP4 )
    #outTree.Branch( 'st_isLooseMuon', st_isLooseMuon)#, 'st_isLooseMuon/O' )
    outTree.Branch( 'st_isMediumMuon', st_isMediumMuon)#, 'st_isMediumMuon/O' )
    outTree.Branch( 'st_isTightMuon', st_isTightMuon)#, 'st_isTightMuon/O' )
    outTree.Branch( 'st_muChHadIso', st_muChHadIso)#, 'st_muChHadIso/F')
    outTree.Branch( 'st_muNeHadIso', st_muNeHadIso)#, 'st_muNeHadIso/F')
    outTree.Branch( 'st_muGamIso', st_muGamIso)#, 'st_muGamIso/F')
    outTree.Branch( 'st_muPUPt', st_muPUPt)#, 'st_muPUPt/F')

#    outTree.Branch( 'st_trigName', st_trigName)
#    outTree.Branch( 'st_trigResult', st_trigResult)

    outTree.Branch( 'st_HPSTau_n', st_HPSTau_n, 'st_HPSTau_n/L')
    outTree.Branch( 'st_HPSTau_4Momentum', st_HPSTau_4Momentum)

    outTree.Branch( 'st_disc_againstElectronLoose', st_disc_againstElectronLoose)
    outTree.Branch( 'st_disc_againstElectronMedium', st_disc_againstElectronMedium)
    outTree.Branch( 'st_disc_againstElectronTight', st_disc_againstElectronTight)
    outTree.Branch( 'st_disc_againstMuonLoose', st_disc_againstMuonLoose)
#    outTree.Branch( 'st_disc_againstMuonMedium', st_disc_againstMuonMedium)
    outTree.Branch( 'st_disc_againstMuonTight', st_disc_againstMuonTight)
    #outTree.Branch('st_disc_LooseIsolationMVA',st_disc_LooseIsolationMVA)

    outTree.Branch( 'st_pu_nTrueInt', st_pu_nTrueInt, 'st_pu_nTrueInt/F')
    outTree.Branch( 'st_pu_nPUVert', st_pu_nPUVert, 'st_pu_nPUVert/F')
    outTree.Branch( 'st_AK4deepCSVjetNPV', st_AK4deepCSVjetNPV, 'st_AK4deepCSVjetNPV/F')
    outTree.Branch( 'st_THINjetNPV', st_THINjetNPV, 'st_THINjetNPV/F')
    outTree.Branch( 'mcweight', mcweight, 'mcweight/F')
    outTree.Branch( 'st_nGenPar',st_nGenPar,'st_nGenPar/L' )  #nGenPar/I
    outTree.Branch( 'st_genParId',st_genParId )  #vector<int>
    outTree.Branch( 'st_genMomParId',st_genMomParId )
    outTree.Branch( 'st_genParSt',st_genParSt )
    outTree.Branch( 'st_genParP4', st_genParP4)

    outTree.Branch( 'WenuRecoil', WenuRecoil, 'WenuRecoil/F')
    outTree.Branch( 'Wenumass', Wenumass, 'Wenumass/F')
    outTree.Branch( 'WenuPhi', WenuPhi, 'WenuPhi/F')

    outTree.Branch( 'WmunuRecoil', WmunuRecoil, 'WmunuRecoil/F')
    outTree.Branch( 'Wmunumass', Wmunumass, 'Wmunumass/F')
    outTree.Branch( 'WmunuPhi', WmunuPhi, 'WmunuPhi/F')

    outTree.Branch( 'ZeeRecoil', ZeeRecoil, 'ZeeRecoil/F')
    outTree.Branch( 'ZeeMass', ZeeMass, 'ZeeMass/F')
    outTree.Branch( 'ZeePhi', ZeePhi, 'ZeePhi/F')

    outTree.Branch( 'ZmumuRecoil', ZmumuRecoil, 'ZmumuRecoil/F')
    outTree.Branch( 'ZmumuMass', ZmumuMass, 'ZmumuMass/F')
    outTree.Branch( 'ZmumuPhi', ZmumuPhi, 'ZmumuPhi/F')

    outTree.Branch( 'TOPRecoil', TOPRecoil, 'TOPRecoil/F')
    outTree.Branch( 'TOPPhi', TOPPhi, 'TOPPhi/F')

    outTree.Branch( 'GammaRecoil', GammaRecoil, 'GammaRecoil/F')
    outTree.Branch( 'GammaPhi', GammaPhi, 'GammaPhi/F')

    if len(sys.argv)>2:
        NEntries=int(sys.argv[2])
        print "WARNING: Running in TEST MODE"

    for ievent in range(NEntries):

#    print "\n*****\nWARNING: *Test run* Processing 200 events only.\n*****\n"
#    for ievent in range(200):
        if ievent%100==0: print "Processed "+str(ievent)+" of "+str(NEntries)+" events."
        skimmedTree.GetEntry(ievent)
        ## Get all relevant branches
        run                        = skimmedTree.__getattr__('runId')
        lumi                       = skimmedTree.__getattr__('lumiSection')
        event                      = skimmedTree.__getattr__('eventId')
#        print "Run:"+str(run)+"; Lumi:"+str(lumi)+"; Event:"+str(event)
        trigName                   = skimmedTree.__getattr__('hlt_trigName')
        trigResult                 = skimmedTree.__getattr__('hlt_trigResult')
        filterName                 = skimmedTree.__getattr__('hlt_filterName')
        filterResult               = skimmedTree.__getattr__('hlt_filterResult')
        BadPFMuonFilter            = skimmedTree.__getattr__('hlt_filterbadPFMuon')

        pfMet                      = skimmedTree.__getattr__('pfMetCorrPt')
        pfMetPhi                   = skimmedTree.__getattr__('pfMetCorrPhi')
        pfMetJetUnc                = skimmedTree.__getattr__('pfMetCorrUnc')


        nTHINJets                  = skimmedTree.__getattr__('THINnJet')
        thinjetP4                  = skimmedTree.__getattr__('THINjetP4')
        thinJetCSV                 = skimmedTree.__getattr__('THINjetCISVV2')
        passThinJetLooseID         = skimmedTree.__getattr__('THINjetPassIDLoose')
        THINjetHadronFlavor        = skimmedTree.__getattr__('THINjetHadronFlavor')
        THINjetNPV                 = skimmedTree.__getattr__('THINjetNPV')         #int()
        thinjetNhadEF              = skimmedTree.__getattr__('THINjetNHadEF')
        thinjetChadEF              = skimmedTree.__getattr__('THINjetCHadEF')
        thinjetCEmEF               = skimmedTree.__getattr__('THINjetCEmEF')
        thinjetPhoEF               = skimmedTree.__getattr__('THINjetPhoEF')
        thinjetEleEF               = skimmedTree.__getattr__('THINjetEleEF')
        thinjetMuoEF               = skimmedTree.__getattr__('THINjetMuoEF')
        thinjetCorrUnc             = skimmedTree.__getattr__('THINjetCorrUncUp')

        nTHINdeepCSVJets           = skimmedTree.__getattr__('AK4deepCSVnJet')
        thindeepCSVjetP4           = skimmedTree.__getattr__('AK4deepCSVjetP4')
        thinJetdeepCSV             = skimmedTree.__getattr__('AK4deepCSVjetDeepCSV_b')
        THINdeepCSVjetHadronFlavor = skimmedTree.__getattr__('AK4deepCSVjetHadronFlavor')
        thindeepCSVjetNhadEF       = skimmedTree.__getattr__('AK4deepCSVjetNHadEF')
        thindeepCSVjetChadEF       = skimmedTree.__getattr__('AK4deepCSVjetCHadEF')
        THINdeepCSVjetNPV          = skimmedTree.__getattr__('AK4deepCSVjetNPV')

        thindeepbRegNNCorr           = skimmedTree.__getattr__('AK4deepCSVbRegNNCorr')
        thindeepbRegNNResolution     = skimmedTree.__getattr__('AK4deepCSVbRegNNResolution')

        #AK8jets branches
        AK8nthikJets               = skimmedTree.__getattr__('AK8PuppinJet')
        AK8thikjetP4               = skimmedTree.__getattr__('AK8PuppijetP4')


        AK8thikjetNhadEF           = skimmedTree.__getattr__('AK8PuppijetNHadEF')
        AK8thikjetChadEF           = skimmedTree.__getattr__('AK8PuppijetCHadEF')
        AK8THIKjetNPV              = skimmedTree.__getattr__('AK8PuppijetNPV')
        AK8thikJetLooseID          = skimmedTree.__getattr__('AK8PuppijetPassIDLoose')
        AK8thikjetTightID          = skimmedTree.__getattr__('AK8PuppijetPassIDTight')
        AK8SDmass                  = skimmedTree.__getattr__('AK8PuppijetSDmass')
        AK8PuppisubjetCSV          = skimmedTree.__getattr__('AK8PuppisubjetSDCSV')
        AK8Puppijet_DoubleSV       = skimmedTree.__getattr__('AK8Puppijet_DoubleSV')

        #AK8subjet
        #nAK8subjets               = skimmedTree.__getattr__('AK8PuppinSubSDJet')
        #AK8subjetPx               = skimmedTree.__getattr__('AK8PuppisubjetSDPx')
        #AK8subjetPy               = skimmedTree.__getattr__('AK8PuppisubjetSDPy')
        #AK8subjetPz               = skimmedTree.__getattr__('AK8PuppisubjetSDPz')
        #AK8subjetCSV              = skimmedTree.__getattr__('AK8PuppisubjetSDCSV')


        #CA15jets
        CA15njets                 = skimmedTree.__getattr__('CA15PuppinJet')
        CA15jetP4                 = skimmedTree.__getattr__('CA15PuppijetP4')
        CA15SDmass                = skimmedTree.__getattr__('CA15PuppijetSDmass')
        CA15jetNhadEF             = skimmedTree.__getattr__('CA15PuppijetNHadEF')
        CA15jetChadEF             = skimmedTree.__getattr__('CA15PuppijetCHadEF')
        CA15PassIDLoose           = skimmedTree.__getattr__('CA15PuppijetPassIDLoose')
        CA15PassIDTight           = skimmedTree.__getattr__('CA15PuppijetPassIDTight')
        CA15Puppi_doublebtag      = skimmedTree.__getattr__('CA15Puppi_doublebtag')
        CA15PuppiECF_1_2_10       = skimmedTree.__getattr__('CA15PuppiECF_1_2_10')
        CA15PuppiECF_2_3_10       = skimmedTree.__getattr__('CA15PuppiECF_2_3_10')
        CA15PuppisubjetCSV        = skimmedTree.__getattr__('CA15PuppisubjetSDCSV')

        try:
            thindeepCSVjetCorrUnc      = skimmedTree.__getattr__('AK4deepCSVjetCorrUncUp')
        except:
            if ievent==0: print "\n**********WARNING: Looks like the ntuple is from an older version, as DeepCSV jet correction Unc is missing. DeepCSV jet correction Unc will NOT be stored.**********\n"
            thindeepCSVjetCorrUnc = 1.


        try:
            thindeepCSVJetLooseID      = skimmedTree.__getattr__('AK4deepCSVjetPassIDLoose')
        except:
            if ievent==0: print "\n**********WARNING: Looks like the ntuple is from an older version, as DeepCSV Loose ID is missing. DeepCSV jet ID will NOT be stored.**********\n"
            thindeepCSVJetLooseID = None

        nEle                       = skimmedTree.__getattr__('nEle')
        eleP4                      = skimmedTree.__getattr__('eleP4')
        eleIsPassVeto              = skimmedTree.__getattr__('eleIsPassVeto')
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
        passLooseTauIso            = skimmedTree.__getattr__('disc_byLooseIsolationMVA3oldDMwLT')

        disc_againstElectronLoose  = skimmedTree.__getattr__('disc_againstElectronLooseMVA5')
        disc_againstElectronMedium = skimmedTree.__getattr__('disc_againstElectronMediumMVA5')
        disc_againstElectronTight  = skimmedTree.__getattr__('disc_againstElectronTightMVA5')
        disc_againstMuonLoose      = skimmedTree.__getattr__('disc_againstMuonLoose3')
        disc_againstMuonTight      = skimmedTree.__getattr__('disc_againstMuonTight3')
        LooseIsolationMVA          = skimmedTree.__getattr__('disc_byVLooseIsolationMVArun2v1DBnewDMwLT')

        isData                     = skimmedTree.__getattr__('isData')
        mcWeight                   = skimmedTree.__getattr__('mcWeight')
        pu_nTrueInt                = skimmedTree.__getattr__('pu_nTrueInt')         #int()
        pu_nPUVert                 = skimmedTree.__getattr__('pu_nPUVert')

        nPho                       = skimmedTree.__getattr__('nPho')
        phoP4                      = skimmedTree.__getattr__('phoP4')
        phoIsPassLoose             = skimmedTree.__getattr__('phoIsPassLoose')
        phoIsPassMedium            = skimmedTree.__getattr__('phoIsPassMedium')
        phoIsPassTight             = skimmedTree.__getattr__('phoIsPassTight')

#        print skimmedTree.__getattr__('pu_nTrueInt')
#        print pu_nTrueInt
#        print

        nGenPar                    = skimmedTree.__getattr__('nGenPar')
        genParId                   = skimmedTree.__getattr__('genParId')
        genMomParId                = skimmedTree.__getattr__('genMomParId')
        genParSt                   = skimmedTree.__getattr__('genParSt')
        genParP4                   = skimmedTree.__getattr__('genParP4')

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
#        print len(tauP4), len(disc_againstElectronLoose),len(disc_againstElectronMedium),len(disc_againstElectronTight), len(disc_againstMuonLoose),len(disc_againstMuonTight)
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # MC Weights ----------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        mcweight[0] = 0.0
        if isData==1:   mcweight[0] =  1.0
        if not isData :
            if mcWeight<0:  mcweight[0] = -1.0
            if mcWeight>0:  mcweight[0] =  1.0


        h_total.Fill(1.);
        h_total_mcweight.Fill(1.,mcweight[0]);

        trigstatus=False
        for itrig in range(len(triglist)):
            exec(triglist[itrig]+" = CheckFilter(trigName, trigResult, " + "'" + triglist[itrig] + "')")        #Runs the above commented-off code dynamically.
            exec("if "+triglist[itrig]+": trigstatus=True")                                                     #If any of the trigs is true, the event is kept.
#            exec("trig"+str(itrig+1)+"="+triglist[itrig])                                                       #Saves them as trig1, trig2, etc. #Deprecated
            exec("st_"+triglist[itrig]+"[0]="+triglist[itrig])                                                  #Adds to SkimmedTree output.

        if not isData: trigstatus=True

        if not trigstatus: continue

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Filter selection
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        filterstatus = False
        filter1 = False; filter2 = False;filter3 = False;filter4 = False; filter5 = False; filter6 = False; filter7=False
        ifilter_=0
        filter1 = CheckFilter(filterName, filterResult, 'Flag_HBHENoiseFilter')
        filter2 = CheckFilter(filterName, filterResult, 'Flag_HBHENoiseIsoFilter')
        filter3 = CheckFilter(filterName, filterResult, 'Flag_EcalDeadCellTriggerPrimitiveFilter')
        filter4 = CheckFilter(filterName, filterResult, 'Flag_globalSuperTightHalo2016Filter')
        filter5 = CheckFilter(filterName, filterResult, 'Flag_eeBadScFilter')
        filter6 = CheckFilter(filterName, filterResult, 'Flag_goodVertices')

        filter7 = BadPFMuonFilter#CheckFilter(filterName, filterResult, 'Flag_BadPFMuonFilter')

        if not isData:
            filterstatus = True
        if isData:
            filterstatus =  filter1 & filter2 & filter3 & filter4 & filter5 & filter6 #& filter7
        if filterstatus == False: continue


        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## PFMET Selection
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------

#        if samplename=="all":
        pfmetstatus = ( pfMet > 150.0 )
#           if pfmetstatus == False : continue

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------



        #-------------------------------------------------
        #AK8Jets collections
        AK8jetspassindex=[]
        for iak8jet in range(AK8nthikJets):
            j1 = AK8thikjetP4[iak8jet]

            if AK8thikJetLooseID==None:
                ak8looseid=True
            else:
                ak8looseid=bool(AK8thikJetLooseID[iak8jet])
            if (j1.Pt() > 150.0)&(abs(j1.Eta())<2.5) and ak8looseid: #  &(bool(passThinJetLooseID[jthinjet])==True):
                AK8jetspassindex.append(iak8jet)




#  CA15jets collections
        CA15jetspassindex=[]
        for ica15jet in range(CA15njets):
            j1 = CA15jetP4[ica15jet]

            if CA15PassIDLoose==None:
                ca15looseid=True
            else:
                ca15looseid=bool(CA15PassIDLoose[ica15jet])
            if (j1.Pt() > 150.0)&(abs(j1.Eta())<2.5) and ca15looseid: #  &(bool(passThinJetLooseID[jthinjet])==True):
                CA15jetspassindex.append(ica15jet)




#----------------------------------------------------------------------------------


        thinjetpassindex=[]
        nBjets=0
        for ithinjet in range(nTHINJets):
            j1 = thinjetP4[ithinjet]
            #if (j1.Pt() > 30.0)&(abs(j1.Eta())<2.4)&(bool(passThinJetLooseID[ithinjet])==True)&(bool(passThinJetPUID[ithinjet]) == True):
            if (j1.Pt() > 30.0)&(abs(j1.Eta())<4.5)&(bool(passThinJetLooseID[ithinjet])==True):
                thinjetpassindex.append(ithinjet)
                if thinJetCSV[ithinjet] > CSVMWP and abs(j1.Eta())<2.4 : nBjets += 1

        thindCSVjetpassindex=[]
        ndBjets=0


        for jthinjet in range(nTHINdeepCSVJets):
            j1 = thindeepCSVjetP4[jthinjet]

            if thindeepCSVJetLooseID==None:
                deepCSVJetLooseID=True
            else:
                deepCSVJetLooseID=bool(thindeepCSVJetLooseID[jthinjet])

            if (j1.Pt() > 30.0)&(abs(j1.Eta())<4.5) and deepCSVJetLooseID: #  &(bool(passThinJetLooseID[jthinjet])==True):
                thindCSVjetpassindex.append(jthinjet)
            if thinJetdeepCSV[jthinjet] > DCSVMWP and abs(j1.Eta())<2.4 : ndBjets += 1


        # if len(thinjetpassindex) < 1 and len(thindCSVjetpassindex) < 1 : continue

#        except:
#            if len(thinjetpassindex) < 1: continue

#        print ('njet: ',len(thinjetpassindex))
#        if len(thindCSVjetpassindex) < 1 : continue
#        print nBjets
#        if nBjets < 1: continue

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Photon Veto
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        myPhos=[]
        for ipho in range(nPho):
            if (phoP4[ipho].Pt() > 15.) & (abs(phoP4[ipho].Eta()) <2.5) & (bool(phoIsPassLoose[ipho]) == True):
                myPhos.append(ipho)

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Electron Veto
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        myEles=[]
        for iele in range(nEle):
            if (eleP4[iele].Pt() > 10. ) & (abs(eleP4[iele].Eta()) <2.5) & (bool(eleIsPassVeto[iele]) == True) :

#                # Clean eles against jets: if ele in jet coll, remove ele. Currently only for CSV coll
#                isClean=True
#                for ithinjet in thinjetpassindex:
#                    if DeltaR(thinjetP4[ithinjet],eleP4[iele]) < 0.4:
#                        isClean=False
#                        break
#                        #print DeltaR(thinjetP4[ithinjet],eleP4[iele])
#                if isClean:

                myEles.append(iele)

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Muon Veto
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        myMuos = []
        for imu in range(nMu):
            if (muP4[imu].Pt()>10.) & (abs(muP4[imu].Eta()) < 2.4) & (bool(isLooseMuon[imu]) == True):
                relPFIso = (muChHadIso[imu]+ max(0., muNeHadIso[imu] + muGamIso[imu] - 0.5*muPUPt[imu]))/muP4[imu].Pt()
                if relPFIso<0.25 :
                    myMuos.append(imu)

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        #
#        if len(myEles)+len(myMuos)>2: continue #----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Tau Veto
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        myTaus=[]
        for itau in range(nTau):
            if (tauP4[itau].Pt()>18.) & (abs(tauP4[itau].Eta())<2.3) & (bool(isDecayModeFinding[itau]) == True) & (bool(LooseIsolationMVA[itau]) == True):
                myTaus.append(itau)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------



        st_runId[0]             = long(run)
        st_lumiSection[0]       = lumi
        st_eventId[0]           = event
#        print '-----------'+str(st_runId)+", "+str(st_lumiSection)+", "+str(st_eventId)

        st_pfMetCorrPt[0]       = pfMet
        st_pfMetCorrPhi[0]      = pfMetPhi
        st_isData[0]            = isData

        st_pfMetUncJetResUp.clear()
        st_pfMetUncJetResDown.clear()

        st_pfMetUncJetEnUp.clear()
        st_pfMetUncJetEnDown.clear()

        st_THINjetP4.clear()
        st_THINjetCISVV2.clear()
        st_THINjetHadronFlavor.clear()
        st_THINjetNHadEF.clear()
        st_THINjetCHadEF.clear()

        st_THINjetCEmEF.clear()
        st_THINjetPhoEF.clear()
        st_THINjetEleEF.clear()
        st_THINjetMuoEF.clear()
        st_THINjetCorrUnc.clear()

        st_AK4deepCSVjetP4.clear()
	st_AK4deepCSVNNCorrjetP4.clear()
        st_AK4deepCSVjetDeepCSV_b.clear()
        st_AK4deepCSVjetHadronFlavor.clear()
        st_AK4deepCSVjetNHadEF.clear()
        st_AK4deepCSVjetCHadEF.clear()
        st_AK4deepCSVjetCorrUnc.clear()


        st_CA15jetP4.clear()
        st_CA15SDmass.clear()
        #st_CA15jetNhadEF.clear()
        #st_CA15jetChadEF.clear()
        st_CA15Puppi_doublebtag.clear()
        st_CA15PuppiECF_1_2_10.clear()
        st_CA15PuppiECF_2_3_10.clear()
        #st_CA15PuppisubjetCSV.clear()
        st_CA15PassIDTight.clear()
        #st_CA15PassIDLoose.clear()


        st_AK8thikjetP4.clear()
        #st_AK8thikjetNhadEF.clear()
        #st_AK8thikjetChadEF.clear()
        st_AK8SDmass.clear()
        #st_AK8PuppisubjetCSV.clear()
        st_AK8Puppijet_DoubleSV.clear()
        #st_AK8thikJetLooseID.clear()
        st_AK8thikjetTightID.clear()



        st_eleP4.clear()
        st_eleIsPassMedium.clear()
        st_eleIsPassTight.clear()
       # st_eleIsPassVeto.clear()


        st_muP4.clear()
        st_isTightMuon.clear()
        st_isMediumMuon.clear()


        st_phoP4.clear()
        st_phoIsPassMedium.clear()
        st_phoIsPassTight.clear()


        st_muChHadIso.clear()
        st_muGamIso.clear()
        st_muNeHadIso.clear()
        st_HPSTau_4Momentum.clear()

        st_disc_againstElectronLoose.clear()
        st_disc_againstElectronMedium.clear()
        st_disc_againstElectronTight.clear()
        st_disc_againstMuonLoose.clear()
#        st_disc_againstMuonMedium.clear()
        st_disc_againstMuonTight.clear()
        #st_disc_LooseIsolationMVA.clear()

        st_genParId.clear()
        st_genMomParId.clear()
        st_genParSt.clear()
        st_genParP4.clear()


        st_THINnJet[0] = len(thinjetpassindex)
        for ithinjet in thinjetpassindex:
            st_THINjetP4.push_back(thinjetP4[ithinjet])
            st_THINjetCISVV2.push_back(thinJetCSV[ithinjet])
            st_THINjetHadronFlavor.push_back(THINjetHadronFlavor[ithinjet])
            st_THINjetNHadEF.push_back(thinjetNhadEF[ithinjet])
            st_THINjetCHadEF.push_back(thinjetChadEF[ithinjet])

            st_THINjetCEmEF.push_back(thinjetCEmEF[ithinjet])
            st_THINjetPhoEF.push_back(thinjetPhoEF[ithinjet])
            st_THINjetEleEF.push_back(thinjetEleEF[ithinjet])
            st_THINjetMuoEF.push_back(thinjetMuoEF[ithinjet])
            st_THINjetCorrUnc.push_back(thinjetCorrUnc[ithinjet])

#        try:
        st_AK4deepCSVnJet[0] = len(thindCSVjetpassindex)
        for ithinjet in thindCSVjetpassindex:
            st_AK4deepCSVjetP4.push_back(thindeepCSVjetP4[ithinjet])
            st_AK4deepCSVjetDeepCSV_b.push_back(thinJetdeepCSV[ithinjet])
            st_AK4deepCSVjetHadronFlavor.push_back(THINdeepCSVjetHadronFlavor[ithinjet])
            st_AK4deepCSVjetNHadEF.push_back(thindeepCSVjetNhadEF[ithinjet])
            st_AK4deepCSVjetCHadEF.push_back(thindeepCSVjetChadEF[ithinjet])
            st_AK4deepCSVjetCorrUnc.push_back(thindeepCSVjetCorrUnc[ithinjet])
#        except:
#            pass



            NNCorr=thindeepbRegNNCorr[ithinjet]
            if NNCorr==0.0:
                NNCorr=1.0

            pt  = thindeepCSVjetP4[ithinjet].Pt()
            eta = thindeepCSVjetP4[ithinjet].Eta()
            phi = thindeepCSVjetP4[ithinjet].Phi()
            ene = thindeepCSVjetP4[ithinjet].E()
            CSVjetP4Corr_temp            =  ROOT.TLorentzVector()
            CSVjetP4Corr_temp.SetPtEtaPhiE(pt*NNCorr,eta,phi,ene*NNCorr)
            st_AK4deepCSVNNCorrjetP4.push_back(CSVjetP4Corr_temp)


        st_CA15njets[0]=len(CA15jetspassindex)
        for ica15 in CA15jetspassindex:
            st_CA15jetP4.push_back(CA15jetP4[ica15])
            st_CA15SDmass.push_back(CA15SDmass[ica15])
            #st_CA15jetNhadEF.push_back(CA15jetNhadEF[ica15])
            #st_CA15jetChadEF.push_back(CA15jetChadEF[ica15])
            st_CA15Puppi_doublebtag.push_back(CA15Puppi_doublebtag[ica15])
            st_CA15PuppiECF_2_3_10.push_back(CA15PuppiECF_2_3_10[ica15])
            st_CA15PuppiECF_1_2_10.push_back(CA15PuppiECF_1_2_10[ica15])
            st_CA15PassIDTight.push_back(bool(CA15PassIDTight[ica15]))
            #st_CA15PassIDLoose.push_back(bool(CA15PassIDLoose[ica15]))
            #st_CA15PuppisubjetCSV.push_back(CA15PuppisubjetCSV[ica15])

        st_AK8nthikJets[0]=len(AK8jetspassindex)
        for iak8jet in AK8jetspassindex:
            st_AK8thikjetP4.push_back(AK8thikjetP4[iak8jet])
            #st_AK8thikjetNhadEF.push_back(AK8thikjetNhadEF[iak8jet])
            #st_AK8thikjetChadEF.push_back(AK8thikjetChadEF[iak8jet])
            st_AK8SDmass.push_back(AK8SDmass[iak8jet])
            #st_AK8PuppisubjetCSV.push_back(AK8PuppisubjetCSV[iak8jet])
            st_AK8Puppijet_DoubleSV.push_back(AK8Puppijet_DoubleSV[iak8jet])
            #st_AK8thikJetLooseID.push_back(bool(AK8thikJetLooseID[iak8jet]))
            st_AK8thikjetTightID.push_back(bool(AK8thikjetTightID[iak8jet]))


        st_nEle[0] = len(myEles)
        for iele in myEles:
            st_eleP4.push_back(eleP4[iele])
            #st_eleIsPassLoose.push_back(bool(eleIsPassLoose[iele]))
            st_eleIsPassMedium.push_back(bool(eleIsPassMedium[iele]))
            st_eleIsPassTight.push_back(bool(eleIsPassTight[iele]))
           # st_eleIsPassVeto.push_back(bool(eleIsPassVeto[iele]))

        st_nMu[0] = len(myMuos)
        for imu in myMuos:
            st_muP4.push_back(muP4[imu])
            #st_isLooseMuon.push_back(bool(isLooseMuon[imu]))
            st_isTightMuon.push_back(bool(isTightMuon[imu]))
            st_isMediumMuon.push_back(bool(isMediumMuon[imu]))
            st_muChHadIso.push_back(muChHadIso[imu])
            st_muNeHadIso.push_back(muNeHadIso[imu])
            st_muGamIso.push_back(muGamIso[imu])
            st_muPUPt.push_back(muPUPt[imu])

        st_HPSTau_n[0] = len(myTaus)
        for itau in myTaus:
            st_HPSTau_4Momentum.push_back(tauP4[itau])
            st_disc_againstElectronLoose.push_back(bool(disc_againstElectronLoose[itau]))
            st_disc_againstElectronMedium.push_back(bool(disc_againstElectronMedium[itau]))
            st_disc_againstElectronTight.push_back(bool(disc_againstElectronTight[itau]))
            st_disc_againstMuonLoose.push_back(bool(disc_againstMuonLoose[itau]))
            st_disc_againstMuonTight.push_back(bool(disc_againstMuonTight[itau]))
            #st_disc_LooseIsolationMVA.push_back(bool(disc_LooseIsolationMVA[itau]))

        st_nPho[0]=nPho
        for ipho in range(nPho):
            st_phoP4.push_back(phoP4[ipho])
            #st_phoIsPassLoose.push_back(bool(phoIsPassLoose[ipho]))
            st_phoIsPassMedium.push_back(bool(phoIsPassMedium[ipho]))
            st_phoIsPassTight.push_back(bool(phoIsPassTight[ipho]))


        st_pu_nTrueInt[0] = pu_nTrueInt
        st_pu_nPUVert[0] = pu_nPUVert
        st_THINjetNPV[0] = THINjetNPV
#        try:
        st_AK4deepCSVjetNPV[0] = THINdeepCSVjetNPV
#        except:
#            pass
#        print pu_nTrueInt
#        print st_pu_nTrueInt[0]
        st_nGenPar[0] =  nGenPar
        for igp in range(nGenPar):
            st_genParId.push_back(genParId[igp])
            st_genMomParId.push_back(genMomParId[igp])
            st_genParSt.push_back(genParSt[igp])
            st_genParP4.push_back(genParP4[igp])

        st_pfMetUncJetResUp.push_back(pfMetJetUnc[0])
        st_pfMetUncJetResDown.push_back(pfMetJetUnc[1])

        st_pfMetUncJetEnUp.push_back(pfMetJetUnc[2])
        st_pfMetUncJetEnDown.push_back(pfMetJetUnc[3])

        ## Fill variables for the CRs.
        WenuRecoil[0] = -1.0
        Wenumass[0] = -1.0
        WenuPhi[0] = -10.

        WmunuRecoil[0] = -1.0
        Wmunumass[0] = -1.0
        WmunuPhi[0] = -10.

        ZeeMass[0] = -1.0
        ZeeRecoil[0] = -1.0
        ZeePhi[0] = -10.

        ZmumuMass[0] = -1.0
        ZmumuRecoil[0] = -1.0
        ZmumuPhi[0] = -10.

        TOPRecoil[0] = -1.0
        TOPPhi[0] = -10.

        GammaRecoil[0] = -1.0
        GammaPhi[0]  = -10.

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
                if ee_mass > 60.0 and ee_mass < 120.0 and ZeeRecoilPt > 150.:
                    ZeeRecoil[0] = ZeeRecoilPt
                    ZeeMass[0] = ee_mass
                    ZeePhi[0] = arctan(zeeRecoilPx,zeeRecoilPy)

        ## for dimu
        if len(myMuos) == 2:
            imu1=myMuos[0]
            imu2=myMuos[1]
            p4_mu1 = muP4[imu1]
            p4_mu2 = muP4[imu2]
            if muCharge[imu1]*muCharge[imu2]<0:
                mumu_mass = ( p4_mu1 + p4_mu2 ).M()
                zmumuRecoilPx = -( pfMet*math.cos(pfMetPhi) + p4_mu1.Px() + p4_mu2.Px())
                zmumuRecoilPy = -( pfMet*math.sin(pfMetPhi) + p4_mu1.Py() + p4_mu2.Py())
                ZmumuRecoilPt =  math.sqrt(zmumuRecoilPx**2  +  zmumuRecoilPy**2)
                if mumu_mass > 60.0 and mumu_mass < 120.0 and ZmumuRecoilPt > 150.:
                    ZmumuRecoil[0] = ZmumuRecoilPt
                    ZmumuMass[0] = mumu_mass
                    ZmumuPhi[0] = arctan(zmumuRecoilPx,zmumuRecoilPy)

        if len(myEles) == 2:
            ZRecoilstatus =(ZeeRecoil[0] > 150)
        elif len(myMuos) == 2:
            ZRecoilstatus =(ZmumuRecoil[0] > 150)
        else:
            ZRecoilstatus=False


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
           if WenuRecoilPt > 150.:
               WenuRecoil[0] = WenuRecoilPt
               Wenumass[0] = e_mass
               WenuPhi[0] = arctan(WenuRecoilPx,WenuRecoilPy)

        ## for Single muon
        if len(myMuos) == 1:
           mu1 = myMuos[0]
           p4_mu1 = muP4[mu1]

           mu_mass = MT(p4_mu1.Pt(),pfMet, DeltaPhi(p4_mu1.Phi(),pfMetPhi)) #transverse mass defined as sqrt{2pT*MET*(1-cos(dphi)}

           WmunuRecoilPx = -( pfMet*math.cos(pfMetPhi) + p4_mu1.Px())
           WmunuRecoilPy = -( pfMet*math.sin(pfMetPhi) + p4_mu1.Py())
           WmunuRecoilPt = math.sqrt(WmunuRecoilPx**2  +  WmunuRecoilPy**2)
           if WmunuRecoilPt > 150.:
               WmunuRecoil[0] = WmunuRecoilPt
               Wmunumass[0] = mu_mass
               WmunuPhi[0] = arctan(WmunuRecoilPx,WmunuRecoilPy)


        if len(myEles) == 1:
            WRecoilstatus =(WenuRecoil[0] > 150)
        elif len(myMuos) == 1:
            WRecoilstatus =(WmunuRecoil[0] > 150)
        else:
            WRecoilstatus=False

# ------------------
# Top CR
# ------------------

        ## for Single electron && Single Muon
        if len(myEles) == 1 and len(myMuos) == 1:
            ele1 = myEles[0]
            p4_ele1 = eleP4[ele1]
            mu1 = myMuos[0]
            p4_mu1 = muP4[mu1]

            if muCharge[mu1]*eleCharge[ele1]<0:
                TOPenumunuRecoilPx = -( pfMet*math.cos(pfMetPhi) + p4_mu1.Px() + p4_ele1.Px())
                TOPenumunuRecoilPy = -( pfMet*math.sin(pfMetPhi) + p4_mu1.Py() + p4_ele1.Py())
                TOPenumunuRecoilPt =  math.sqrt(TOPenumunuRecoilPx**2 + TOPenumunuRecoilPy**2)
                if TOPenumunuRecoilPt > 150:
                    TOPRecoil[0] = TOPenumunuRecoilPt
                    TOPPhi[0] = arctan(TOPenumunuRecoilPx,TOPenumunuRecoilPy)


        TOPRecoilstatus = (TOPRecoil[0] > 150.)


        #if ZRecoilstatus:
            #print ('Z: ',nEle, nMu, ZeeMass[0], ZmumuMass[0])
#        if WRecoilstatus:
#            print ('W: ', Wenumass[0], Wmunumass[0])
        #if TOPRecoilstatus:
            #print ('T: ',nEle, nMu, TOPenumunuRecoilPt)
# ------------------
# Gamma CR
# ------------------
        ## for Single photon
        if len(myPhos) >= 1:
           myPhosP4=[phoP4[myPhos[i]] for i in range(len(myPhos))]
           p4_pho1 = sorted(myPhosP4,key=getPT,reverse=True)[0]
#           if len(myPhos) > 1:
#              print [i.Pt() for i in myPhosP4]
#              print p4_pho1.Pt()
#              print

           GammaRecoilPx = -( pfMet*math.cos(pfMetPhi) + p4_pho1.Px())
           GammaRecoilPy = -( pfMet*math.sin(pfMetPhi) + p4_pho1.Py())
           GammaRecoilPt = math.sqrt(GammaRecoilPx**2  +  GammaRecoilPy**2)
           if GammaRecoilPt > 150.:
               GammaRecoil[0] = GammaRecoilPt
               GammaPhi[0] = arctan(GammaRecoilPx,GammaRecoilPy)

        GammaRecoilStatus = (GammaRecoil[0] > 150)


        if pfmetstatus==False and ZRecoilstatus==False and WRecoilstatus==False and TOPRecoilstatus==False and GammaRecoilStatus==False:
            continue


        outTree.Fill()

    h_total_mcweight.Write()
    h_total.Write()
    samplepath.Write()
    outfile.Write()


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
            #print "inside WJ loop pdgid", PID
            #print ("if status =",      (abs(PID) != 11),( abs(PID) != 12),(  abs(PID) != 13 ),(  abs(PID) != 14),(  abs(PID) != 15),(  abs(PID) != 16))
            #print "and of if status ", ( (abs(PID) != 11) & (abs(PID) != 12) &  (abs(PID) != 13) & (abs(PID) != 14) &  (abs(PID) != 15) &  (abs(PID) != 16) )

            if ( (abs(PID) != 11) & (abs(PID) != 12) &  (abs(PID) != 13) & (abs(PID) != 14) &  (abs(PID) != 15) &  (abs(PID) != 16) ): continue
            #print "lepton found"
            if ( ( (status != 1) & (abs(PID) != 15)) | ( (status != 2) & (abs(PID) == 15)) ): continue
            #print "tau found"
            if ( (abs(momPID) != 24) & (momPID != PID) ): continue
            #print "W found"
            #print "aftrer WJ if statement"
            goodLepID.append(ig)
        #print "length = ",len(goodLepID)
        if len(goodLepID) == 2 :
            l4_thisLep = genParP4[goodLepID[0]]
            l4_thatLep = genParP4[goodLepID[1]]
            l4_z = l4_thisLep + l4_thatLep

            pt = l4_z.Pt()
            pt__ = pt
            print " pt inside "
            k2 = -0.830041 + 7.93714 *TMath.Power( pt - (-877.978) ,(-0.213831) ) ;

    #################
    #ZJets
    #################
    if sample == "ZJETS":
        print " inside zjets "
        goodLepID = []
        for ig in range(nGenPar):
         #   print " inside loop "
            PID    = genParId[ig]
            momPID = genMomParId[ig]
            status = genParSt[ig]
          #  print " after vars "

            if ( (abs(PID) != 12) &  (abs(PID) != 14) &  (abs(PID) != 16) ) : continue
            if ( status != 1 ) : continue
            if ( (momPID != 23) & (momPID != PID) ) : continue
            goodLepID.append(ig)

        if len(goodLepID) == 2 :
            l4_thisLep = genParP4[goodLepID[0]]
            l4_thatLep = genParP4[goodLepID[1]]
            l4_z = l4_thisLep + l4_thatLep
            pt = l4_z.Pt()
            print " pt inside "
            k2 = -0.180805 + 6.04146 *TMath.Power( pt - (-759.098) ,(-0.242556) ) ;

    #################
    #TTBar
    #################
    if (sample=="TT"):
        print " inside ttbar "
        goodLepID = []
        for ig in range(nGenPar):
            print "inside TT loop "
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
    AnalyzeDataSet()
