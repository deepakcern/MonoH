## 1. Running Locally

To run the code locally:

```
cmsrel CMSSW_9_X
cd CMSSW_9_X/src
git clone git@github.com:deepakcern/MonoH.git
cd MonoH/TriggerTurnOn/BR_Condor_Farmout
f_TriggerEfficiencyPlotter_.py -i /eos/cms/store/group/phys_exotica/bbMET/2018_ntuples/MET/DM_Search/190114_175917/0000/NCUGlobalTuples_100.root -D . -o Output.root
```


##condor job:
```
cmsrel CMSSW_9_X
cd CMSSW_9_X/src

git clone git@github.com:deepakcern/MonoH.git
cd MonoH/TriggerTurnOn/BR_Condor_Farmout
. submitjobs.sh
```
