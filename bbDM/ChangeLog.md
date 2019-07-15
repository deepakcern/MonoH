# Change log for the monoH boosted category

## 1. base code:

we will keep log from here

[https://github.com/deepakcern/MonoH/blob/e2c92323b87e5f1b1419742ab38a3e227ccd9b50/bbDM/bbDM/bbMET/bbMETBranchReader.py](https://github.com/deepakcern/MonoH/blob/e2c92323b87e5f1b1419742ab38a3e227ccd9b50/bbDM/bbDM/bbMET/bbMETBranchReader.py)


plots from base code(middle plots): 

[https://drive.google.com/file/d/1IgtXQXbxUBmRXoGS4cvcMYrUSMm-YYdJ/view](https://drive.google.com/file/d/1IgtXQXbxUBmRXoGS4cvcMYrUSMm-YYdJ/view)



#### Note: In above plots we used SDMass Corr from Raman's code

## 2. Next Change:

---
#### BugFound: ??
#### What is bug: ??
#### Fixed in this iteration: ??
---
### Other updates in the code[w.r.t previous version]:

Here I have updated code for SDMaa corr. This time I used Benedik's root file for SDMass corr.

#### Plots:
Here are the plots(old slides):
[http://dekumar.web.cern.ch/dekumar/My_Slides/Updates/monoH_Boosted_category_18062019.pdf](http://dekumar.web.cern.ch/dekumar/My_Slides/Updates/monoH_Boosted_category_18062019.pdf)

#### Conclusion:
- In this iteration SDMass plots are not good in all CRs, they are not matching with 2016 Analysis.
- Top CR has more stats than 2016
- Not looking ZCR for now

## 3. Next change:

---
#### BugFound ?: *Yes*
#### What is bug ?: *I was cleaning FatJet against lepton with DeltaR < 0.4 but it has to be DeltaR < 1.5*
#### Fixed in this iteration ?: *Yes*
---
#####################################################################################

---
I realised that there are few selections which I need to update in my code:

1. **In 2016 they used vetoID for electron veto**
2. **According to 2016 AN, tau ID was same as in my code, they are using following things[with pT > 18 GeV and eta < 2.3 selection] to select tau**:
   - **New DecayModeFinding**
   - **byVLooseIsolationMVArun2v1DBnewDMwLT**
  
3. In 2016 monoH paper, it is written that AK4 Jets are cleaned against CA15Jets, but it is not written in AN and also not mentioned in the preapproval slides.

4. In 2016 monoH paper, it is mentioned to remove electron in transition region but not written in AN.

---
#####################################################################################

---
In my framework I was using following things [with pT > 18 GeV and eta < 2.3] to select tau:
- New DecayModeFinding
- byLooseIsolationMVA3oldDMwLT


further in my framework I was using following selections to select tau properly against leptons [not sure it was used in 2016Analysis or not], these selections I was using in monoH resolved same as bbDM so didn't removed in monoH boosted category:
- disc_againstElectronLooseMVA5
- disc_againstElectronTightMVA5
- disc_againstMuonLoose3 
- disc_againstMuonTight3

**Not sure about these variables needs to confirm with Raman**

---
### Other updates in the code[w.r.t previous version]:
Note: 
I did a mistake in this iteration,I made many changes in this iteration, I should not do many changes in one time, then it becomes very hard to know which change is dominating in the final output. Be carefull in future.

There are few changes in this iteration:

- Updated electron looseID to electronVetoID
- Updated tau selection for tau veto. Removed disc_againstElectron/Muon variables only kept **New DecayModeFinding** and **byVLooseIsolationMVArun2v1DBnewDMwLT** for tau veto
- Updated EWK and QCD K-factor as monoH2016
- Cleaned AK4Jets against CA15jet [given in monoH 2016 paper]
- removed electron in transition region

#### Plots:
Here are the plots from this iteration: [http://dekumar.web.cern.ch/dekumar/My_Slides/Updates/monoH_boosted_changeNo3.pdf](http://dekumar.web.cern.ch/dekumar/My_Slides/Updates/monoH_boosted_changeNo3.pdf)

#### gitLink:
https://github.com/deepakcern/MonoH/blob/9853137d9f254fd0216214744214e00895a9951c/bbDM/bbDM/bbMET/bbMETBranchReader.py

#### Conclusion:
- We have very less events now [specially in electron region]
- Something is wrong in lepton veto condition
- need to cross check again
---

## 4. Next change:

---
#### BugFound: ??
#### What is bug: ??
#### Fixed in this iteration: ??
---
### Other updates in the code[w.r.t previous version]:
Tau disc variables were causing events reduction so in this iteration I have added again tau disc varible:
**Why?**: I think because in monoH 2016 paper it is written that they put tau[hadronic] veto not all the taus so we need to keep tau descriminator against lepton:

#### Code:
https://github.com/deepakcern/MonoH/blob/3dc2b7f0b558c858295ea4d2aa86a3a04c6b3189/bbDM/bbDM/bbMET/bbMETBranchReader.py

#### Plots:
N/A


## 5. Next change:

---
#### BugFound: Yes
#### What is bug: fixed eta bug in electron region [it came in step 3]
#### Fixed in this iteration: Yes
---
### Other updates in the code[w.r.t previous version]:

We used tau veto against loose lepton in all CR. Ititially it was tight

#### Code: https://github.com/deepakcern/MonoH/blob/dbe2287c6f9b33b4b426e34b32a632119cae3fe4/bbDM/bbDM/bbMET/bbMETBranchReader.py

#### Plots: http://dekumar.web.cern.ch/dekumar/figs/boosted_category_fixed_eta_08072019/

#### Slides comparing with step2 : http://dekumar.web.cern.ch/dekumar/My_Slides/Updates/Boosted_category_08072019.pdf


## 6. Next change:
---
#### BugFound: ??
#### What is bug: ??
#### Fixed in this iteration: ??
---

### Other updates in the code[w.r.t previous version]:

In this iteration I changed AK4Jet cleaning ordering.

First we select CA15 jet with all selections [pT, eta, double B tagger]

Then we do AK4Jet cleaning against CA15Jet

Here I also applied photon veto and remoded eta < 2.4 for tight electron now it is 2.5 for all electron.


#### code:https://github.com/deepakcern/MonoH/blob/c06de916069a350cb24502428d49cfaceb4f5ea3/bbDM/bbDM/bbMET/bbMETBranchReader.py
