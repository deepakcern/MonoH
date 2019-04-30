from ROOT import TCanvas, TGraph,TAxis,TColor, TGaxis, TH1F, TPad, TFile, TGraphAsymmErrors,TLatex,TLine,gStyle,TLegend
from ROOT import kBlack, kBlue, kRed
from array import array
import glob
from os import listdir
from os.path import isfile, join

gStyle.SetFrameLineWidth(3)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
gStyle.SetLegendBorderSize(0)
#gStyle.SetFillColor(2)
#gStyle.SetLineWidth(1)
gStyle.SetHistFillStyle(2)

legend=TLegend(.13,.69,.37,.89)
legend.SetTextSize(0.038)

c=TCanvas()

def setHistStyle(h_temp,rebin, col):

    # h_temp=h_temp2.Rebin(len(bins)-1,"h_temp",array('d',bins))
    h_temp.SetLineWidth(1)
    h_temp.SetLineColor(col)
    # h_temp.SetBinContent(len(bins)-1,h_temp.GetBinContent(len(bins)-1)+h_temp.GetBinContent(len(bins))) #Add overflow bin content to last bin
    # h_temp.SetBinContent(len(bins),0.)
    h_temp.SetXTitle("N2")
    h_temp.SetYTitle("arbitary unit")
    h_temp.Rebin(rebin)
    h_temp.SetLineWidth(3)
    h_temp.Scale(1/h_temp.Integral())
    h_temp.GetXaxis().SetRangeUser(0,1500)
    #h_temp.SetMarkerColor(kBlack);
    #h_temp.SetMarkerStyle(2);
    return h_temp


path='/home/dekumar/t3store2/N2DDT_jobs/MonoH/bbDM/bbMET/BR_Condor_Farmout_N2DDT/hadd_outputs/'

files = [f for f in listdir(path) if isfile(join(path, f))]

axis=TAxis()
#print (files)
for file in files:
    if 'QCD_HT700to1000' in file:
        print (file)
        f1=TFile.Open(path+file)
        h_qcd_=f1.Get("h_N2")
        h_qcd=setHistStyle(h_qcd_,2,1)
        legend.AddEntry(h_qcd,"QCD_HT700to1000","L")
        #gr=TGraph(h_qcd)
        nbins=h_qcd.GetSize()-2
	h_total=h_qcd.Integral()
        print "maximum x range",h_qcd.GetXaxis().GetXmax();
        print "total no of bins", nbins
        XperBin=h_qcd.GetXaxis().GetXmax()/nbins
        print "X range per bin",XperBin 
        for i in range(nbins):
		eff=1-h_qcd.Integral(i,nbins)/h_qcd.Integral()
		if eff >= .02:
			print "efficince :", eff, "bin number",i
                        N2cut=i*XperBin
			print "N2CUT",N2cut
			break	
        #print "efficiency: " ,h_qcd.Integral(0,25)/h_qcd.Integral(), "  ", h_qcd.GetSize(), " ",h_qcd.FindBin(0.23)#.Integral(),GetXaxis().FindBin(pfMet)

    elif 'TT_TuneCUETP8M2T4' in file:
        print (file)
        f2=TFile.Open(path+file)
        h_TT_=f2.Get("h_N2")
        h_TT=setHistStyle(h_TT_,2,2)
        #legend.AddEntry(h_TT,"TT","L")



    elif '2HDMa_gg' in file:#'ZpBaryonic_MZp-500' in file:
        print (file)
        f3=TFile.Open(path+file)
        h_zp_=f3.Get("h_N2")
        h_zp=setHistStyle(h_zp_,2,3)
        legend.AddEntry(h_zp,'Signal','L')#"ZpBaryonic_MZp-500","L")



h_qcd.Draw('hist')
#h_TT.Draw('hist same')
h_zp.Draw('hist same')
legend.Draw()

c.SaveAs("N2_Combined.png")
c.SaveAs("N2_Combined.pdf")
