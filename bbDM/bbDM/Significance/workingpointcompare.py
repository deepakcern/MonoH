from ROOT import TGraph, TFile, TGraphAsymmErrors
from array import array
import os
import glob,math
import matplotlib.pyplot as plt

path_loose='/Users/dekumar/MEGA/Fullwork/punzi_significance/forloose/*.root'


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

mphi50_sr1_jet1_loose=[]
mphi50_sr1_jet2_loose=[]
mphi50_sr2_jet1_loose=[]
mphi50_sr2_jet2_loose=[]

mphi100_sr1_jet1_loose=[]
mphi100_sr1_jet2_loose=[]
mphi100_sr2_jet1_loose=[]
mphi100_sr2_jet2_loose=[]

mphi350_sr1_jet1_loose=[]
mphi350_sr1_jet2_loose=[]
mphi350_sr2_jet1_loose=[]
mphi350_sr2_jet2_loose=[]

mphi400_sr1_jet1_loose=[]
mphi400_sr1_jet2_loose=[]
mphi400_sr2_jet1_loose=[]
mphi400_sr2_jet2_loose=[]

mphi500_sr1_jet1_loose=[]
mphi500_sr1_jet2_loose=[]
mphi500_sr2_jet1_loose=[]
mphi500_sr2_jet2_loose=[]

mphi1000_sr1_jet1_loose=[]
mphi1000_sr1_jet2_loose=[]
mphi1000_sr2_jet1_loose=[]
mphi1000_sr2_jet2_loose=[]

sr1_jet1_loose=[]
sr1_jet2_loose=[]
sr2_jet1_loose=[]
sr2_jet2_loose=[]

for i in pT_cuts:
    setbins.append((i)/(perbin))
    print (i/(perbin))


files_loose = sorted(glob.glob(path_loose))
print ("total files")
print (files_loose)
for file_b in files_loose:
    f=TFile.Open(file_b,'read')
    #print ("selected file");f
    # bkgsum=f.Get("bkgSum")
    # a=bkgsum.Draw()
    for i in bkgsr1:
        if i in file_b.split('/')[-1]:

            if i==bkgsr1[0]:
                print (file_b)
                bkgsum=f.Get("bkgSum")
                a=bkgsum.Draw()
                print (bkgsum.Integral())
                for j in setbins:
                    print (bkgsum.Integral(int(j+1),201))
                    sr1_jet1_loose.append(bkgsum.Integral(int(j+1),201))
            if i==bkgsr1[1]:
                bkgsum=f.Get("bkgSum")
                a=bkgsum.Draw()
                for j in setbins:
                    sr1_jet2_loose.append(bkgsum.Integral(int(j+1),201))
    for i in bkgsr2:
        if i in file_b.split('/')[-1]:
            if i==bkgsr2[0]:
                bkgsum=f.Get("bkgSum")
                a=bkgsum.Draw()
                for j in setbins:
                    sr2_jet1_loose.append(bkgsum.Integral(int(j+1),201))
            if i==bkgsr2[1]:
                for j in setbins:
                    sr2_jet2_loose.append(bkgsum.Integral(int(j+1),201))


files_loose = sorted(glob.glob(path_loose))
print ("total files");files_loose
for file in files_loose:
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
                    mphi50_sr1_jet1_loose.append((sr1_jet1_pT.Integral(int(j+1),201))/(htotal.Integral()))
                    mphi50_sr1_jet2_loose.append(sr1_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi50_sr2_jet1_loose.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi50_sr2_jet2_loose.append(sr2_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))



            if i==Mphi[1]:
                #print ("entering")
                for j in setbins:
                    mphi100_sr1_jet1_loose.append(sr1_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi100_sr1_jet2_loose.append(sr1_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi100_sr2_jet1_loose.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi100_sr2_jet2_loose.append(sr2_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))

            if i==Mphi[2]:
                #print ("entering")
                for j in setbins:
                    mphi350_sr1_jet1_loose.append(sr1_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi350_sr1_jet2_loose.append(sr1_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi350_sr2_jet1_loose.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi350_sr2_jet2_loose.append(sr2_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))

            if i==Mphi[3]:
                #print ("entering")
                for j in setbins:
                    mphi400_sr1_jet1_loose.append(sr1_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi400_sr1_jet2_loose.append(sr1_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi400_sr2_jet1_loose.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi400_sr2_jet2_loose.append(sr2_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))

            if i==Mphi[4]:
                #print ("entering")
                for j in setbins:
                    mphi500_sr1_jet1_loose.append(sr1_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi500_sr1_jet2_loose.append(sr1_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi500_sr2_jet1_loose.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi500_sr2_jet2_loose.append(sr2_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))


            if i==Mphi[5]:
                #print ("entering")
                for j in setbins:
                    mphi1000_sr1_jet1_loose.append(sr1_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi1000_sr1_jet2_loose.append(sr1_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi1000_sr2_jet1_loose.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi1000_sr2_jet2_loose.append(sr2_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))

# for i in range(len(mphi50_sr2_jet2)):
#     print ("  jdsn")
#     print (mphi50_sr2_jet2[i])
#     print ("  jdsn")
#     print (mphi50_sr2_jet1[i])
#     print ("  jdsn")
#     print (mphi50_sr1_jet2[i])
#     print ("  jdsn")
#     print (mphi50_sr2_jet2[i])


EffMassSr1jet1_loose=[]
EffMassSr1jet2_loose=[]
EffMassSr2jet1_loose=[]
EffMassSr2jet2_loose=[]

EffMassSr1jet1_loose.append(mphi50_sr1_jet1_loose)
EffMassSr1jet1_loose.append(mphi100_sr1_jet1_loose)
EffMassSr1jet1_loose.append(mphi350_sr1_jet1_loose)
EffMassSr1jet1_loose.append(mphi400_sr1_jet1_loose)
EffMassSr1jet1_loose.append(mphi500_sr1_jet1_loose)
EffMassSr1jet1_loose.append(mphi1000_sr1_jet1_loose)


EffMassSr1jet2_loose.append(mphi50_sr1_jet2_loose)
EffMassSr1jet2_loose.append(mphi100_sr1_jet2_loose)
EffMassSr1jet2_loose.append(mphi350_sr1_jet2_loose)
EffMassSr1jet2_loose.append(mphi400_sr1_jet2_loose)
EffMassSr1jet2_loose.append(mphi500_sr1_jet2_loose)
EffMassSr1jet2_loose.append(mphi1000_sr1_jet2_loose)


EffMassSr2jet1_loose.append(mphi50_sr2_jet1_loose)
EffMassSr2jet1_loose.append(mphi100_sr2_jet1_loose)
EffMassSr2jet1_loose.append(mphi350_sr2_jet1_loose)
EffMassSr2jet1_loose.append(mphi400_sr2_jet1_loose)
EffMassSr2jet1_loose.append(mphi500_sr2_jet1_loose)
EffMassSr2jet1_loose.append(mphi1000_sr2_jet1_loose)

EffMassSr2jet2_loose.append(mphi50_sr2_jet2_loose)
EffMassSr2jet2_loose.append(mphi100_sr2_jet2_loose)
EffMassSr2jet2_loose.append(mphi350_sr2_jet2_loose)
EffMassSr2jet2_loose.append(mphi400_sr2_jet2_loose)
EffMassSr2jet2_loose.append(mphi500_sr2_jet2_loose)
EffMassSr2jet2_loose.append(mphi1000_sr2_jet2_loose)


########################################################################
#This section id for medium working points

path='/Users/dekumar/Desktop/punzi_significance/*.root'


mphi50_sr1_jet1_medium=[]
mphi50_sr1_jet2_medium=[]
mphi50_sr2_jet1_medium=[]
mphi50_sr2_jet2_medium=[]

mphi100_sr1_jet1_medium=[]
mphi100_sr1_jet2_medium=[]
mphi100_sr2_jet1_medium=[]
mphi100_sr2_jet2_medium=[]

mphi350_sr1_jet1_medium=[]
mphi350_sr1_jet2_medium=[]
mphi350_sr2_jet1_medium=[]
mphi350_sr2_jet2_medium=[]

mphi400_sr1_jet1_medium=[]
mphi400_sr1_jet2_medium=[]
mphi400_sr2_jet1_medium=[]
mphi400_sr2_jet2_medium=[]

mphi500_sr1_jet1_medium=[]
mphi500_sr1_jet2_medium=[]
mphi500_sr2_jet1_medium=[]
mphi500_sr2_jet2_medium=[]

mphi1000_sr1_jet1_medium=[]
mphi1000_sr1_jet2_medium=[]
mphi1000_sr2_jet1_medium=[]
mphi1000_sr2_jet2_medium=[]

sr1_jet1_medium=[]
sr1_jet2_medium=[]
sr2_jet1_medium=[]
sr2_jet2_medium=[]

# for i in pT_cuts:
#     setbins.append((i)/(perbin))
#     print (i/(perbin))


files = sorted(glob.glob(path))
print ("total files")
print (files)
for file in files:
    f=TFile.Open(file,'read')
    #print ("selected file");f
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
                    sr1_jet1_medium.append(bkgsum.Integral(int(j+1),201))
            if i==bkgsr1[1]:
                bkgsum=f.Get("bkgSum")
                a=bkgsum.Draw()
                for j in setbins:
                    sr1_jet2_medium.append(bkgsum.Integral(int(j+1),201))
    for i in bkgsr2:
        if i in file.split('/')[-1]:
            if i==bkgsr2[0]:
                bkgsum=f.Get("bkgSum")
                a=bkgsum.Draw()
                for j in setbins:
                    sr2_jet1_medium.append(bkgsum.Integral(int(j+1),201))
            if i==bkgsr2[1]:
                for j in setbins:
                    sr2_jet2_medium.append(bkgsum.Integral(int(j+1),201))


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
                    mphi50_sr1_jet1_medium.append((sr1_jet1_pT.Integral(int(j+1),201))/(htotal.Integral()))
                    mphi50_sr1_jet2_medium.append(sr1_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi50_sr2_jet1_medium.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi50_sr2_jet2_medium.append(sr2_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))



            if i==Mphi[1]:
                #print ("entering")
                for j in setbins:
                    mphi100_sr1_jet1_medium.append(sr1_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi100_sr1_jet2_medium.append(sr1_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi100_sr2_jet1_medium.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi100_sr2_jet2_medium.append(sr2_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))

            if i==Mphi[2]:
                #print ("entering")
                for j in setbins:
                    mphi350_sr1_jet1_medium.append(sr1_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi350_sr1_jet2_medium.append(sr1_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi350_sr2_jet1_medium.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi350_sr2_jet2_medium.append(sr2_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))

            if i==Mphi[3]:
                #print ("entering")
                for j in setbins:
                    mphi400_sr1_jet1_medium.append(sr1_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi400_sr1_jet2_medium.append(sr1_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi400_sr2_jet1_medium.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi400_sr2_jet2_medium.append(sr2_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))

            if i==Mphi[4]:
                #print ("entering")
                for j in setbins:
                    mphi500_sr1_jet1_medium.append(sr1_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi500_sr1_jet2_medium.append(sr1_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi500_sr2_jet1_medium.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi500_sr2_jet2_medium.append(sr2_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))


            if i==Mphi[5]:
                #print ("entering")
                for j in setbins:
                    mphi1000_sr1_jet1_medium.append(sr1_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi1000_sr1_jet2_medium.append(sr1_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi1000_sr2_jet1_medium.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi1000_sr2_jet2_medium.append(sr2_jet2_pT.Integral(int(j+1),201)/(htotal.Integral()))

# for i in range(len(mphi50_sr2_jet2)):
#     print ("  jdsn")
#     print (mphi50_sr2_jet2[i])
#     print ("  jdsn")
#     print (mphi50_sr2_jet1[i])
#     print ("  jdsn")
#     print (mphi50_sr1_jet2[i])
#     print ("  jdsn")
#     print (mphi50_sr2_jet2[i])


EffMassSr1jet1_medium=[]
EffMassSr1jet2_medium=[]
EffMassSr2jet1_medium=[]
EffMassSr2jet2_medium=[]


EffMassSr1jet1_medium.append(mphi50_sr1_jet1_medium)
EffMassSr1jet1_medium.append(mphi100_sr1_jet1_medium)
EffMassSr1jet1_medium.append(mphi350_sr1_jet1_medium)
EffMassSr1jet1_medium.append(mphi400_sr1_jet1_medium)
EffMassSr1jet1_medium.append(mphi500_sr1_jet1_medium)
EffMassSr1jet1_medium.append(mphi1000_sr1_jet1_medium)


EffMassSr1jet2_medium.append(mphi50_sr1_jet2_medium)
EffMassSr1jet2_medium.append(mphi100_sr1_jet2_medium)
EffMassSr1jet2_medium.append(mphi350_sr1_jet2_medium)
EffMassSr1jet2_medium.append(mphi400_sr1_jet2_medium)
EffMassSr1jet2_medium.append(mphi500_sr1_jet2_medium)
EffMassSr1jet2_medium.append(mphi1000_sr1_jet2_medium)


EffMassSr2jet1_medium.append(mphi50_sr2_jet1_medium)
EffMassSr2jet1_medium.append(mphi100_sr2_jet1_medium)
EffMassSr2jet1_medium.append(mphi350_sr2_jet1_medium)
EffMassSr2jet1_medium.append(mphi400_sr2_jet1_medium)
EffMassSr2jet1_medium.append(mphi500_sr2_jet1_medium)
EffMassSr2jet1_medium.append(mphi1000_sr2_jet1_medium)

EffMassSr2jet2_medium.append(mphi50_sr2_jet2_medium)
EffMassSr2jet2_medium.append(mphi100_sr2_jet2_medium)
EffMassSr2jet2_medium.append(mphi350_sr2_jet2_medium)
EffMassSr2jet2_medium.append(mphi400_sr2_jet2_medium)
EffMassSr2jet2_medium.append(mphi500_sr2_jet2_medium)
EffMassSr2jet2_medium.append(mphi1000_sr2_jet2_medium)




######################################################################

EffMassSr2jet2=[]
EffMassSr2jet1=[]
EffMassSr1jet2=[]
EffMassSr1jet1=[]
sr2_jet2=[]
sr2_jet1=[]
sr1_jet1=[]


EffMassSr2jet2.append(EffMassSr2jet2_loose)
EffMassSr2jet2.append(EffMassSr2jet2_medium)
EffMassSr2jet1.append(EffMassSr2jet2_loose)
EffMassSr2jet1.append(EffMassSr2jet2_medium)
EffMassSr1jet1.append(EffMassSr2jet2_loose)
EffMassSr1jet1.append(EffMassSr2jet2_medium)

sr2_jet2.append(sr2_jet2_loose)
sr2_jet2.append(sr2_jet2_medium)
sr2_jet1.append(sr2_jet2_loose)
sr2_jet1.append(sr2_jet2_medium)
sr1_jet1.append(sr2_jet2_loose)
sr1_jet1.append(sr2_jet2_medium)

WP=['LWP','MWP']
#print (sr2_jet2[0])
print (len(EffMassSr1jet1))
for pt in range(len(pT_cuts)):
    for i in range(len(EffMassSr2jet1)):
        y=[]
        for j in range(len(EffMassSr2jet1[0])):
            a=EffMassSr2jet2[i]
            b=sr2_jet2[i]
            print (((a)[j][pt])/(b[pt]))
            y.append((((a)[j][pt])/(b[pt])))
            #print (y[0])
        plt.plot([50,100,350,400,500,1000],y,'o-',label='jet2_$p_{T}$='+str(pT_cuts[pt])+'GeV : '+(WP[i]))

    #plt.rc('axes', labelsize=20)
    plt.xlabel(r'$M_{\phi}$')
    plt.ylabel("Significance")
    plt.legend()#ncol=3,title=r"tan$\beta$")
    plt.title(r"Significance for SR2: LWP Vs MWP ")
    plt.savefig('sr2_jet2_pT_'+str(pT_cuts[pt])+'.pdf')
    plt.savefig('sr2_jet2_pT_'+str(pT_cuts[pt])+'.png')
    plt.clf()
    plt.cla()
    plt.close('all')

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
