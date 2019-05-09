# monoHbb
### Full Workflow:

![alt text](http://spmondal.web.cern.ch/spmondal/bbMETFlow.png)


# 1. Run DMAnalyzer

First step is to generate ntuples.

1.Follow instructions from https://github.com/deepakcern/DMAnaRun2/tree/80X_puppi+deepCSV (only 80X_puppi+deepCSV branch) to setup DelPanj within CMSSW.

# 2. Run SkimTree 
#### Note: (Ntuples Location: /afs/cern.ch/work/d/dekumar/public/monoH/Filelists/2016_Ntuples)

Clone this repository in a location from where HTCondor jobs can be submitted (```login.uscms.org``` for example). We shall refer to this location as the working directory for this section.
```
cmsrel CMSSW_8_0_26_patch1
cd CMSSW_8_0_26_patch1/src
git clone https://github.com/deepakcern/MonoH.git
git checkout monoH_boosted
cd monoH/bbDM/bbMET
```
## 2.1. Running Locally

SkimTree can be run using:
```bash
python SkimTree.py path_to_ntuple_file
```
##### Example:
```bash
python SkimTree.py root://eoscms.cern.ch//eos/cms/store/group/phys_exotica/bbMET/monoHbb_data12042019/monoH_2016data_20190412/SingleElectron/SingleElectron-Run2016H-03Feb2017_ver3-v1/190412_050220/0000/NCUGlobalTuples_9.root
```
## 2.2. Running on HTCondor

***SkimTree jobs are numerous is number, hence using a Condor network with large number of cores is recommended. Recommended submit node: uscms.***

### 2.2.1. Running SkimTree Condor Jobs

1. Navigate to workingdir/`bbMET/bbMET/ST_Condor/`.
2. Open `runAnalysis.sh` to edit.
3. Line 19 contains an exemplar path to a T2 location. The SkimTree outputs (Skimmed Trees) will be stored in this location. Edit this path (remember to change the username) and specify where you wish to store the outputs. The directory does not necessarily have to exist, it will be created if non-existent. Make sure you have write access to the specified directory.
4. Initiate your voms-proxy using `voms-proxy-init --voms cms --valid 192:00`.
5. Submit jobs using
    ```bash
    . submitjobs.sh
    ```
6. To monitor the job submission process, use:
    ```bash
    tail -f logsubmit.txt
    ```
7. To monitor status of jobs, use `condor_q username`.

### 2.2.2. Outputs 


The SkimTree outputs (Skimmed Trees) are saved to the location that was specified in the `runAnalysis.sh` file. These will be used while running BranchReader (next section).

**(SkimTree jobs for all data and background may take upto 1 day to finish.)**

# 3. Run BranchReader

#### Note: [New location of input filelists:/afs/cern.ch/work/d/dekumar/public/monoH/Filelists/NewSkimmed ]

Clone this repository in a location from where HTCondor jobs can be submitted (```user@login.uscms.org``` for example). We shall refer to this location as the working directory for this section.

```
cmsrel CMSSW_8_0_26_patch1
cd CMSSW_8_0_26_patch1/src
git clone https://github.com/deepakcern/MonoH.git
git checkout monoH_boosted
cd MonoH/bbDM/bbMET
```

## 3.1. Running Locally

* BranchReader can be run using:
```bash
python bbMETBranchReader.py -a -i path_to_skimmed_tree -D . --csv
```
* The "farmout" mode can be used to combine multiple input root files in one go. If all the root files are listed in a text file named input.txt, one can use:
```bash
python bbMETBranchReader.py -a -F -i input.txt -D . --csv
```
Note: Initiate your voms-proxy using voms-proxy-init --voms cms --valid 192:00

## 3.2. Running on HTCondor

***The number of BranchReader jobs can be adjusted by combining suitable number of input files in the Farmout mode.***
***Note: If you submit condor jobs using `lxplus` then open `submit_multi.sub` file and add these two line:
```
Proxy_filename = x509up
Proxy_path = /afs/cern.ch/user/d/dekumar/private/$(Proxy_filename)
request_cpus = 4
+JobFlavour = "nextweek"
```
and open `.bashrc` file and add:
```
alias voms='voms-proxy-init --voms cms --valid 192:00 && cp -v /tmp/x509up_u104803 /afs/cern.ch/user/d/dekumar/private/x509up'
```

Remove this line `python bbMETBranchReader.py -a -F -i "$1" -D . -o BROutput.root --csv` in runAnalysis.sh and add these lines:
```
export X509_USER_PROXY=$1
voms-proxy-info -all
voms-proxy-info -all -file $1

python bbMETBranchReader.py -a -F -i "$2" -D . -o BROutput.root --csv
```
##### Note: do not use --deepcsv

Now open `MultiSubmit.py` replace line 26 with  `submittemp.write("arguments = $(Proxy_path) "+tempfile.split('/')[1]+'\n')`

Initiate your voms-proxy using `voms`.

#### Note: you can find lxplus condor files here: /afs/cern.ch/work/d/dekumar/public/monoH/lxplus_condor_monoH/bbDM/bbMET/BR_Condor_Farmout

### 3.2.1. Running BranchReader Condor Jobs

1. Navigate to workingdir/`MonoH/bbDM/bbDM/bbMET/BR_Condor_Farmout/`.
2. This framework automatically combines multiple skimmed_tree root files in one job. The number of root files to be combined in each job can be specified by editing L4 of MultiSubmit.py (`maxfilesperjob=100`).
3. Initiate your voms-proxy using `voms-proxy-init --voms cms --valid 192:00`.
4. Submit jobs using
    ```bash
    . submitjobs.sh
    ```
5. To monitor the job submission process, use:
    ```bash
    tail -f logsubmit.txt
    ```
6. To monitor status of jobs, use `condor_q username`.
7. If jobs are in `held` then use the command:
```
python releaseJobs.py
```

### 3.2.2. Retrieving Outputs

1. Once all BranchReader Condor jobs are complete, one needs to combine the output .root files for each sample. This can be achieved by using the `hadd` command. If no CMSSW or ROOT instance is sourced by default in your working area, go to a CMSSW release base and run `cmsenv`, otherwise the `hadd` command may not work.
2. Navigate to `MonoH/bbDM/bbDM/bbMET/BR_Condor_Farmout/` and run
    ```bash
    python HADD_multi_Farmout.py
    ```
    The outputs .root files are stitched on a per sample basis and one .root file per sample is produced inside `bbMET/bbMET/BR_Condor_Farmout/hadd_outputs`.
3. These .root files inside `hadd_outputs` can be used directly as inputs to the plotting code and will henceforth be referred to as **BranchReader outputs**.ch
4. 
```
cd file_structure
. mk_bkg_data.sh [make bkg_data directory]
. hadd_data.sh
. makesig.sh [to make dummy files]
```


# 4. Run Plotting Script

1. [This is the step to make CRs plots]
2. Clone this repository
```
cd CMSSW_8_0_26_patch1/src
git clone https://github.com/deepakcern/bbMETplot.git
```
2. Open `bbMETplot/Scripts/bbMET_StackFactory_withSM.py` and edit L306 to suit the current working directory. Edit L375[`give the path of bkg_data dir`], L352[`give the path of signal directory`], and L395[`give the path of bkg_data directory`] to the path(s) where the BranchReader outputs are stored.
3. Navigate to `bbMETplot/Scripts/test` and run
```
python ../bbMET_StackFactory_withSM.py -d MET -s -m -q
python ../bbMET_StackFactory_withSM.py -d SE -e
python ../bbMET_StackFactory_withSM.py -d SP -p [not needed]
```
The boolean flags are explained as follows:

* s: Signal Regions (only MC plots)
* m: Muon Control Regions
* q: QCD Control Regions
* e: Electron Control Regions
* p: Photon Control Regions
* The `-d` flag is used to select the appropriate primary dataset for each region.

