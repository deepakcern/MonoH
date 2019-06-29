# change log for the monoH boosted category

## 1. base code:
we will keep log from here

[https://github.com/deepakcern/MonoH/blob/e2c92323b87e5f1b1419742ab38a3e227ccd9b50/bbDM/bbDM/bbMET/bbMETBranchReader.py](https://github.com/deepakcern/MonoH/blob/e2c92323b87e5f1b1419742ab38a3e227ccd9b50/bbDM/bbDM/bbMET/bbMETBranchReader.py)


plots from base code(middle plots): 

[https://drive.google.com/file/d/1IgtXQXbxUBmRXoGS4cvcMYrUSMm-YYdJ/view](https://drive.google.com/file/d/1IgtXQXbxUBmRXoGS4cvcMYrUSMm-YYdJ/view)

#### Note: In above plots we used SDMass Corr from Raman's code

## 2. Next Change:
Here I have updated code for SDMaa corr. This time I used benedik's root file for SDMass corr.

Here are the plots(old slides):
[http://dekumar.web.cern.ch/dekumar/My_Slides/Updates/monoH_Boosted_category_18062019.pdf](http://dekumar.web.cern.ch/dekumar/My_Slides/Updates/monoH_Boosted_category_18062019.pdf)


## 3. Next change:

I realised that there are few selections which I should update:
1. In 2016 they used vetoID for electron veto
2. According to 2016 AN, tau ID was same as in my code, they are using following things[with pT > 18 GeV and eta < 2.3 selection] to select tau:
  - New DecayModeFinding
  - byVLooseIsolationMVArun2v1DBnewDMwLT
  
In my framework I was using following things [with pT > 18 GeV and eta < 2.3] to select tau:
- New DecayModeFinding
- byLooseIsolationMVA3oldDMwLT

further in my framework I was using these tau selections to tau properly against leptons [not sure it was used in 2016Analysis or not], these selections I was using in monoH resolved same as bbDM so didn't removed in monoH boosted.:
- disc_againstElectronLooseMVA5
- disc_againstElectronMediumMVA5
- disc_againstElectronTightMVA5
- disc_againstMuonLoose3 
- disc_againstMuonTight3

**Not sure about these variables needs to confirm with Raman**
