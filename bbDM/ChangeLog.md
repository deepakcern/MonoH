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
- In 2016 they used vetoID for electron veto
- According to 2016 AN, tau ID was same as in my code, they are using following things to select tau:
  -New DecayModeFinding
  -byVLooseIsolationMVArun2v1DBnewDMwLT

