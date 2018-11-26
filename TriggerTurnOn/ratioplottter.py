from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TFile, TGraphAsymmErrors,TLatex,TLine,gStyle,TLegend
from ROOT import kBlack, kBlue, kRed
from array import array


f = TFile.Open('test.root')
gStyle.SetFrameLineWidth(3)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
gStyle.SetLegendBorderSize(0)
gStyle.SetFillColor(2)
gStyle.SetLineWidth(1)
gStyle.SetHistFillStyle(2)

bins=[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,160,170,180,190,200,220,240,260,280,300,350,400,500,600,700,800,1000,1200,1500]

def setHistStyle(h_temp2,bins):

    h_temp=h_temp2.Rebin(len(bins)-1,"h_temp",array('d',bins))
    h_temp.SetLineWidth(1)
    h_temp.SetBinContent(len(bins)-1,h_temp.GetBinContent(len(bins)-1)+h_temp.GetBinContent(len(bins))) #Add overflow bin content to last bin
    h_temp.SetBinContent(len(bins),0.)
    h_temp.GetXaxis().SetRangeUser(0,1500)
    h_temp.SetMarkerColor(kBlack);
    h_temp.SetMarkerStyle(2);
    return h_temp



def createRatio(h1, h2):
     h3 = h1.Clone("h3")
     h3.SetLineColor(kBlack)
     h3.SetMarkerStyle(20)
     h3.SetTitle("")
     h3.SetMinimum(0.1)
     h3.SetMaximum(1.35)

     # Set up plot for markers and errors
     h3.Sumw2()
     h3.SetStats(0)
     h3.Divide(h2)

     # Adjust y-axis settings
     y = h3.GetYaxis()
     y.SetTitle("Trigger efficiency ")
     # y.SetNdivisions(505)
     # y.SetTitleSize(20)
     # y.SetTitleFont(43)
     # y.SetTitleOffset(1.55)
     # y.SetLabelFont(43)
     # y.SetLabelSize(15)

     # Adjust x-axis settings
     x = h3.GetXaxis()
     x.SetTitleSize(20)
     x.SetTitleFont(43)
     x.SetTitleOffset(4.0)
     x.SetLabelFont(43)
     x.SetLabelSize(15)
     x.SetRangeUser(0,100)

     return h3


def createCanvasPads():
    c = TCanvas("c", "canvas", 800, 800)
    # Upper histogram plot is pad1
    pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0)  # joins upper and lower plot
    pad1.SetGridx()
    pad1.Draw()
    # Lower ratio plot is pad2
    c.cd()  # returns to main canvas before defining pad2
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
    pad2.SetTopMargin(0)  # joins upper and lower plot
    pad2.SetBottomMargin(0.2)
    pad2.SetGridx()
    pad2.Draw()

    return c, pad1, pad2

def getLegend():
    legend=TLegend(.50,.59,.87,.89)
    legend.SetTextSize(0.038)

    return legend

def getLatex():
    latex =  TLatex()
    latex.SetNDC();
    latex.SetTextSize(0.04);
    latex.SetTextAlign(31);
    latex.SetTextAlign(11);
    return latex


def combineHist(hists,leg_label,leg):

    myhists=[]
    for i in range(len(hists)):
        print (hists[i])
        myhists.append(f.Get(hists[i]))
    for i in range(len(myhists)):
        if i==0:
            myhists[i].SetXTitle("Recoil [GeV]")
            myhists[i].SetYTitle("Events")
            myhists[i].Rebin(20)
            #myhists[i].setHistStyle(hists[i],bins)
            myhists[i].SetLineColor(i+1)
            myhists[i].SetLineWidth(3)
            myhists[i].GetXaxis().SetRangeUser(0,1500)
            leg.AddEntry(myhists[i],leg_label[i],"L")
            myhists[i].Draw('hist')
        else:
            myhists[i].SetXTitle("Recoil [GeV]")
            myhists[i].SetYTitle("Events")
            myhists[i].Rebin(20)
            #myhists[i].setHistStyle(hists[i],bins)
            myhists[i].SetLineColor(i+1)
            myhists[i].SetLineWidth(3)
            myhists[i].GetXaxis().SetRangeUser(0,1500)
            leg.AddEntry(myhists[i],leg_label[i],"L")
            myhists[i].Draw('hist same')


def ratioplot():
     # create required parts

     leg=getLegend()
     latex=getLatex()
     c=TCanvas()
     c.SetLogy()

#Draw input histograms
     hists=['h_frac_recoil_','h_full_recoil_']
     label=['recoil with MET triggers','recoil without MET triggers']
     combineHist(hists,label,leg)
     #leg.Draw()
     #c.SaveAs("Combinehists_D.pdf")

     ratio=[]
     h1=f.Get('h_frac_recoil_')
     #h1=setHistStyle(h1,bins)
     h2=f.Get('h_full_recoil_')
     #h2=setHistStyle(h2,bins)

     h3 = createRatio(h1, h2)
     gr=TGraphAsymmErrors(h1,h2)
     gr.GetXaxis().SetRangeUser(0,1500)
     gr.GetYaxis().SetRangeUser(0,1.2)
     gr.SetMarkerStyle(20)
     gr.SetMarkerSize(0.5)
     gr.SetLineColor(1)
     gr.GetYaxis().SetTitle("Trigger Efficiency")
     gr.GetXaxis().SetTitle("Recoil [GeV]")
     gr.SetTitle("")


    # print ("ratio",ratio )
     # c, pad1, pad2 = createCanvasPads()
     #
     # # draw everything
     # pad1.cd()
     # h1.Draw()
     # h2.Draw("same")
     # to avoid clipping the bottom zero, redraw a small axis
     # h1.GetYaxis().SetLabelSize(0.0)
     # axis = TGaxis(-5, 20, -5, 220, 20, 220, 510, "")
     # axis.SetLabelFont(43)
     # axis.SetLabelSize(15)
     # axis.Draw()
     # pad2.cd()
     gr.Draw()
     latex.DrawLatex(0.41, 0.93, "Trigger Efficincy in MET Run2017E")
     xmin=0.0
     line = TLine(max(xmin,gr.GetXaxis().GetXmin()),1,1500,1)
     line.SetLineColor(1)
     line.SetLineWidth(1)
     line.SetLineStyle(7)
     line.Draw()
     #h3.Draw('pl')
     c.SaveAs("test.pdf")

if __name__ == "__main__":
     ratioplot()
