from ROOT import TGraph, TFile, TGraphAsymmErrors
from array import array
import os
import glob,math
import matplotlib.pyplot as plt

path='/Users/dekumar/Desktop/punzi_significance/*.root'

Mphi=['50','100','350','400','500','1000']
mchi=['1']
pT_cuts=[50,55,60,65,70]

bkgsr1=['jet1_pT_sr1','jet2_pT_sr1']
bkgsr2=['jet1_pT_sr2','jet1_pT_sr2']

Xrange=1000
Totalbins=200
perbin=(Xrange)/(Totalbins)
print (perbin)
setbins=[]
xjet1=[]
xjet2=[]
yjet1=[]
yjet2=[]

mphi50_sr1_jet1=[]
mphi50_sr1_jet2=[]
mphi50_sr2_jet1=[]
mphi50_sr2_jet2=[]

mphi100_sr1_jet1=[]
mphi100_sr1_jet2=[]
mphi100_sr2_jet1=[]
mphi100_sr2_jet2=[]

mphi350_sr1_jet1=[]
mphi350_sr1_jet2=[]
mphi350_sr2_jet1=[]
mphi350_sr2_jet2=[]

mphi400_sr1_jet1=[]
mphi400_sr1_jet2=[]
mphi400_sr2_jet1=[]
mphi400_sr2_jet2=[]

mphi500_sr1_jet1=[]
mphi500_sr1_jet2=[]
mphi500_sr2_jet1=[]
mphi500_sr2_jet2=[]

mphi1000_sr1_jet1=[]
mphi1000_sr1_jet2=[]
mphi1000_sr2_jet1=[]
mphi1000_sr2_jet2=[]

sr1_jet1=[]
sr1_jet2=[]
sr2_jet1=[]
sr2_jet2=[]

for i in pT_cuts:
    setbins.append((i)/(perbin))
    print (i/(perbin))


files = sorted(glob.glob(path))
print ("total files")
print (files)
for file in files:
    f=TFile.Open(file,'read')
    print ("selected file");f
    # bkgsum=f.Get("bkgSum")
    # a=bkgsum.Draw()
    for i in bkgsr1:
        if i in file.split('/')[-1]:

            if i==bkgsr1[0]:
                print (file)
                bkgsum=f.Get("bkgSum")
                a=bkgsum.Draw()
                print (bkgsum.Integral())
                for j in setbins:
                    print (bkgsum.Integral(int(j+1),201))
                    sr1_jet1.append(bkgsum.Integral(int(j+1),201))
            if i==bkgsr1[1]:
                bkgsum=f.Get("bkgSum")
                a=bkgsum.Draw()
                for j in setbins:
                    sr1_jet2.append(bkgsum.Integral(int(j+1),201))
    for i in bkgsr2:
        if i in file.split('/')[-1]:
            if i==bkgsr2[0]:
                bkgsum=f.Get("bkgSum")
                a=bkgsum.Draw()
                for j in setbins:
                    sr2_jet1.append(bkgsum.Integral(int(j+1),201))
            if i==bkgsr2[1]:
                for j in setbins:
                    sr2_jet2.append(bkgsum.Integral(int(j+1),201))


files = sorted(glob.glob(path))
print ("total files");files
for file in files:
    f=TFile.Open(file,'read')
    htotal=f.Get('h_total')
    #print ("selected file")
    #print (f)
    sr1_jet1_pT=f.Get('h_jet1_pT_sr1_')
    sr1_jet2_pT=f.Get('h_jet2_pT_sr1_')
    sr2_jet1_pT=f.Get('h_jet1_pT_sr2_')
    sr2_jet2_pT=f.Get('h_jet1_pT_sr2_')
    # n_sr1_jet1_pT=sr1_jet1_pT.Integral()
    # n_sr1_jet2_pT=
    # n_sr2_jet1_pT=
    # n_sr2_jet2_pT=

    for i in Mphi:
        #print (file.split('/')[-1])
        if '_Mphi-'+i+'.root' in file.split('/')[-1]:
            #print ("entering")
            if i==Mphi[0]:
                #print ("entering")
                for j in setbins:
                    mphi50_sr1_jet1.append((sr1_jet1_pT.Integral(int(j+1),201))/(htotal.Integral()))
                    mphi50_sr1_jet2.append(sr1_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi50_sr2_jet1.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi50_sr2_jet2.append(sr2_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))



            if i==Mphi[1]:
                #print ("entering")
                for j in setbins:
                    mphi100_sr1_jet1.append(sr1_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi100_sr1_jet2.append(sr1_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi100_sr2_jet1.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi100_sr2_jet2.append(sr2_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))

            if i==Mphi[2]:
                #print ("entering")
                for j in setbins:
                    mphi350_sr1_jet1.append(sr1_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi350_sr1_jet2.append(sr1_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi350_sr2_jet1.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi350_sr2_jet2.append(sr2_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))

            if i==Mphi[3]:
                #print ("entering")
                for j in setbins:
                    mphi400_sr1_jet1.append(sr1_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi400_sr1_jet2.append(sr1_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi400_sr2_jet1.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi400_sr2_jet2.append(sr2_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))

            if i==Mphi[4]:
                #print ("entering")
                for j in setbins:
                    mphi500_sr1_jet1.append(sr1_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi500_sr1_jet2.append(sr1_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi500_sr2_jet1.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi500_sr2_jet2.append(sr2_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))


            if i==Mphi[5]:
                #print ("entering")
                for j in setbins:
                    mphi1000_sr1_jet1.append(sr1_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi1000_sr1_jet2.append(sr1_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi1000_sr2_jet1.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi1000_sr2_jet2.append(sr2_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))

# for i in range(len(mphi50_sr2_jet2)):
#     print ("  jdsn")
#     print (mphi50_sr2_jet2[i])
#     print ("  jdsn")
#     print (mphi50_sr2_jet1[i])
#     print ("  jdsn")
#     print (mphi50_sr1_jet2[i])
#     print ("  jdsn")
#     print (mphi50_sr2_jet2[i])

EffMassSr1jet1=[]
EffMassSr1jet1=[]
EffMassSr1jet1=[]
EffMassSr1jet1=[]
EffMassSr1jet1=[]

EffMassSr1jet2=[]
EffMassSr1jet2=[]
EffMassSr1jet2=[]
EffMassSr1jet2=[]
EffMassSr1jet2=[]

EffMassSr2jet1=[]
EffMassSr2jet1=[]
EffMassSr2jet1=[]
EffMassSr2jet1=[]
EffMassSr2jet1=[]

EffMassSr2jet2=[]
EffMassSr2jet2=[]
EffMassSr2jet2=[]
EffMassSr2jet2=[]
EffMassSr2jet2=[]

y=[]

EffMassSr1jet1.append(mphi50_sr1_jet1)
EffMassSr1jet1.append(mphi100_sr1_jet1)
EffMassSr1jet1.append(mphi350_sr1_jet1)
EffMassSr1jet1.append(mphi400_sr1_jet1)
EffMassSr1jet1.append(mphi500_sr1_jet1)
EffMassSr1jet1.append(mphi1000_sr1_jet1)


EffMassSr1jet2.append(mphi50_sr1_jet2)
EffMassSr1jet2.append(mphi100_sr1_jet2)
EffMassSr1jet2.append(mphi350_sr1_jet2)
EffMassSr1jet2.append(mphi400_sr1_jet2)
EffMassSr1jet2.append(mphi500_sr1_jet2)
EffMassSr1jet2.append(mphi1000_sr1_jet2)


EffMassSr2jet1.append(mphi50_sr2_jet1)
EffMassSr2jet1.append(mphi100_sr2_jet1)
EffMassSr2jet1.append(mphi350_sr2_jet1)
EffMassSr2jet1.append(mphi400_sr2_jet1)
EffMassSr2jet1.append(mphi500_sr2_jet1)
EffMassSr2jet1.append(mphi1000_sr2_jet1)

EffMassSr2jet2.append(mphi50_sr2_jet2)
EffMassSr2jet2.append(mphi100_sr2_jet2)
EffMassSr2jet2.append(mphi350_sr2_jet2)
EffMassSr2jet2.append(mphi400_sr2_jet2)
EffMassSr2jet2.append(mphi500_sr2_jet2)
EffMassSr2jet2.append(mphi1000_sr2_jet2)

#print (sr2_jet2[0])
y2=[]
print (len(EffMassSr2jet2))
for pt in range(len(pT_cuts)):
    y=[]
    for i in range(len(EffMassSr2jet2)):
        y.append(((EffMassSr2jet2[i])[0])/(sr2_jet2[pt]))
        #print (y[0])
    plt.plot([50,100,350,400,500,1000],y,'o-',label='jet2_$p_{T}$='+str(pT_cuts[pt]))

plt.rc('axes', labelsize=20)
plt.xlabel(r'$M_{\phi}$')
plt.ylabel("Significance")
plt.legend()#ncol=3,title=r"tan$\beta$")
plt.title(r"Significance for SR2")
plt.savefig('sr2_jet2.pdf')
plt.savefig('sr2_jet2.png')

# for pt in range(len(pT_cuts)):
#     y=[]
#     for i in range(len(EffMassSr2jet1)):
#         y.append(((EffMassSr2jet1[i])[0])/(sr2_jet1[pt]))
#         #print (y[0])
#     plt.plot([50,100,350,400,500,1000],y,'o-',label='jet1_$p_{T}$='+str(pT_cuts[pt]))
#
# plt.rc('axes', labelsize=20)
# plt.xlabel(r'$M_{\phi}$')
# plt.ylabel("Significance")
# plt.legend()#ncol=3,title=r"tan$\beta$")
# plt.title(r"Significance for SR2")
# plt.savefig('sr2_jet1.pdf')
# plt.savefig('sr2_jet1.png')
#
# for pt in range(len(pT_cuts)):
#     y=[]
#     for i in range(len(EffMassSr2jet2)):
#         y.append(((EffMassSr2jet2[i])[0])/(sr2_jet2[pt]))
#         #print (y[0])
#     plt.plot([50,100,350,400,500,1000],y,'o-',label='jet2_$p_{T}$='+str(pT_cuts[pt]))
#
# plt.rc('axes', labelsize=20)
# plt.xlabel(r'$M_{\phi}$')
# plt.ylabel("Significance")
# plt.legend()#ncol=3,title=r"tan$\beta$")
# plt.title(r"Significance for SR2")
# plt.savefig('sr2_jet2.pdf')
# plt.savefig('sr2_jet2.png')
