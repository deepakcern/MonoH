## 1. Running Locally

To run the code locally:

```
f_TriggerEfficiencyPlotter_.py -i /eos/cms/store/group/phys_exotica/bbMET/2018_ntuples/MET/DM_Search/190114_175917/0000/NCUGlobalTuples_100.root -D . -o Output.root
```


##condor job:
```
cmsrel CMSSW_8_0_21
cd CMSSW_8_0_21/src

git clone git@github.com:deepakcern/MonoH.git
cd MonoH/TriggerTurnOn/BR_Condor_Farmout
. submitjobs.sh
```
