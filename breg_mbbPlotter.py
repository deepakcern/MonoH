#!/usr/bin/env python
from ROOT import TFile, TTree, TH1F, TH1D, TH1, TCanvas, TChain,TGraphAsymmErrors, TMath, TH2D, TLorentzVector, AddressOf, gROOT, TNamed, gStyle
import ROOT as ROOT
import os
import sys, optparse
from array import array
import math
import numpy as numpy_

#ROOT.gROOT.LoadMacro("Loader.h+")

skimmedTree = TChain("tree/treeMaker")
skimmedTree.Add(sys.argv[1])


#NEntries = ntuple.GetEntries()

#if len(sys.argv)>2:
    #if sys.argv[2]=="test":
#    NEntries=int(sys.argv[2])
#    print "WARNING: Running in TEST MODE"

#print 'NEntries = '+str(NEntries)

def SetCanvas():

    # CMS inputs
    # -------------
    H_ref = 1000;
    W_ref = 1000;
    W = W_ref
    H  = H_ref

    T = 0.08*H_ref
    B = 0.21*H_ref
    L = 0.12*W_ref
    R = 0.08*W_ref
    # --------------

    c1 = TCanvas("c2","c2",0,0,2000,1500)
    c1.SetFillColor(0)
    c1.SetBorderMode(0)
    c1.SetFrameFillStyle(0)
    c1.SetFrameBorderMode(0)
    c1.SetLeftMargin( L/W )
    c1.SetRightMargin( R/W )
    c1.SetTopMargin( T/H )
    c1.SetBottomMargin( B/H )
    c1.SetTickx(0)
    c1.SetTicky(0)
    c1.SetTickx(1)
    c1.SetTicky(1)
    c1.SetGridy()
    c1.SetGridx()
    c1.SetLogy(1)
    return c1

def CreateLegend(x1, y1, x2, y2, header):

    leg = ROOT.TLegend(x1, x2, y1, y2)
    leg.SetFillColor(0)
    leg.SetFillStyle(3002)
    leg.SetBorderSize(0)
    leg.SetHeader(header)
    return leg

def AddText(txt):
    texcms = ROOT.TLatex(-20.0, 50.0, txt)
    texcms.SetNDC()
    texcms.SetTextAlign(12)
    texcms.SetX(0.1)
    texcms.SetY(0.94)
    texcms.SetTextSize(0.02)
    texcms.SetTextSizePixels(22)
    return texcms


def AddTextCat(cat):
    texCat = ROOT.TLatex(-20.0, 50.0, cat)
    texCat.SetNDC()
    texCat.SetTextAlign(12)
    texCat.SetX(0.85)
    texCat.SetY(0.94)
    texCat.SetTextFont(40)
    texCat.SetTextSize(0.025)
    texCat.SetTextSizePixels(22)
    return texCat


gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
gStyle.SetErrorX(0.)
ROOT.gROOT.SetBatch(True)

def Analyze():
    DCSVMWP=0.6324
    NEntries = skimmedTree.GetEntries()

    h_Mbb                     =TH1F('h_Mbb_',  'h_Mbb_',  50,0.,250.)
    h_regMbb                  =TH1F('h_regMbb_',  'h_regMbb_',  50,0.,250.)

    h_jet1_pT                 =TH1F('h_jet1_pT_',  'h_jet1_pT_',  50,0.0,500.)
    h_jet2_pT                 =TH1F('h_jet2_pT',  'h_jet2_pT',  50,0.0,500.)

    h_regjet1_pT              =TH1F('h_regjet1_pT_',  'h_regjet1_pT_',  50,0.0,500.)
    h_regjet2_pT              =TH1F('h_regjet2_pT',  'h_regjet2_pT',  50,0.0,500.)


    if len(sys.argv)>2:
        NEntries=int(sys.argv[2])
        print "WARNING: Running in TEST MODE"

    for ievent in range(NEntries):
        if ievent%100==0: print "Processed "+str(ievent)+" of "+str(NEntries)+" events."
        skimmedTree.GetEntry(ievent)


        nTHINdeepCSVJets             = skimmedTree.__getattr__('AK4deepCSVnJet')
        thindeepCSVjetP4             = skimmedTree.__getattr__('AK4deepCSVjetP4')
        thindeepbRegNNCorr           = skimmedTree.__getattr__('AK4deepCSVbRegNNCorr')
        thindeepbRegNNResolution     = skimmedTree.__getattr__('AK4deepCSVbRegNNResolution')
        passThinJetLooseID         = skimmedTree.__getattr__('THINjetPassIDLoose')
        thinJetdeepCSV             = skimmedTree.__getattr__('AK4deepCSVjetDeepCSV_b')


        try:
            thindeepCSVJetLooseID      = skimmedTree.__getattr__('AK4deepCSVjetPassIDLoose')
        except:
            if ievent==0: print "\n**********WARNING: Looks like the ntuple is from an older version, as DeepCSV Loose ID is missing. DeepCSV jet ID will NOT be stored.**********\n"
            thindeepCSVJetLooseID = None


        CSVjetP4Corr                 =  []#ROOT.std.vector('TLorentzVector')()

        # for njet in range(nTHINdeepCSVJets):
        #     NNCorr=thindeepbRegNNCorr[njet]
        #     if NNCorr==0.0:
        #         NNCorr=1.0
        #
        #     pt  = thindeepCSVjetP4[njet].Pt()
        #     eta = thindeepCSVjetP4[njet].Eta()
        #     phi = thindeepCSVjetP4[njet].Phi()
        #     ene = thindeepCSVjetP4[njet].E()
        #
        #     CSVjetP4Corr_temp            =  ROOT.TLorentzVector()
        #     CSVjetP4Corr_temp.SetPtEtaPhiE(pt*NNCorr,eta,phi,ene*NNCorr)
        #
        #     print "pT before correction:  ", pt
        #     print "pT after correction:   ", CSVjetP4Corr_temp.Pt()
        #
        #     CSVjetP4Corr.push_back(CSVjetP4Corr_temp)



        myBjetsP4=[]
        for jthinjet in range(nTHINdeepCSVJets):
            j1 = thindeepCSVjetP4[jthinjet]

            if thindeepCSVJetLooseID==None:
                deepCSVJetLooseID=True
            else:
                deepCSVJetLooseID=bool(passThinJetLooseID[jthinjet])

            if (j1.Pt() > 30.0)&(abs(j1.Eta())<2.4) and deepCSVJetLooseID and thinJetdeepCSV[jthinjet] > DCSVMWP :
                myBjetsP4.append(thindeepCSVjetP4[jthinjet])

                NNCorr=thindeepbRegNNCorr[jthinjet]
                if NNCorr==0.0:
                    NNCorr=1.0

                pt  = thindeepCSVjetP4[jthinjet].Pt()
                eta = thindeepCSVjetP4[jthinjet].Eta()
                phi = thindeepCSVjetP4[jthinjet].Phi()
                ene = thindeepCSVjetP4[jthinjet].E()

                CSVjetP4Corr_temp            =  ROOT.TLorentzVector()
                CSVjetP4Corr_temp.SetPtEtaPhiE(pt*NNCorr,eta,phi,ene*NNCorr)

                print "pT before correction:  ", pt
                print "pT after correction:   ", CSVjetP4Corr_temp.Pt()

                CSVjetP4Corr.append(CSVjetP4Corr_temp)
        nBjets=len(myBjetsP4)

        if nBjets==2:
            j1p4   = myBjetsP4[0]
            j2p4   = myBjetsP4[1]

            addJet=(j1p4+j2p4)

            regJ1P4= CSVjetP4Corr[0]
            reJ2P4 = CSVjetP4Corr[1]

            addJetReg=(regJ1P4+reJ2P4)

            h_Mbb.Fill(addJet.M())
            h_regMbb.Fill(addJetReg.M())

    c      = SetCanvas()
    legend = CreateLegend(0.60, 0.94, 0.75, 0.92, "")

    h_Mbb.SetLineColor(2)
    h_Mbb.SetLineWidth(3)
    legend.AddEntry(h_Mbb,"without regression")
    h_regMbb.SetLineColor(3)
    h_regMbb.SetLineWidth(3)
    legend.AddEntry(h_regMbb,"with b jet regression")


    h_Mbb.Draw('HIST')
    h_regMbb.Draw('HIST same')
    legend.Draw()

    txt = 'monoHbb'
    texcms = AddText(txt)
    texCat= AddTextCat("2HDM+a")
    texcms.Draw("same")
    texCat.Draw("same")
    t = ROOT.TPaveLabel(0.1, 0.96, 0.95, 0.99, "Mbb distribution", "brNDC")
    t.Draw('same')
    c.Update()

    c.SaveAs('Mbb.pdf')
    c.SaveAs('Mbb.png')

if __name__ == "__main__":
    Analyze()
