# monoHbb
### Full Workflow:

![alt text](http://spmondal.web.cern.ch/spmondal/bbMETFlow.png)


# 1. Run DMAnalyzer

First step is to generate ntuples.

1.Follow instructions from https://github.com/deepakcern/DMAnaRun2/tree/80X_puppi+deepCSV (only 80X_puppi+deepCSV branch) to setup DelPanj within CMSSW.

# 2. Run SkimTree

Clone this repository in a location from where HTCondor jobs can be submitted (```login.uscms.org``` for example). We shall refer to this location as the working directory for this section.

## 2.1. Running Locally

SkimTree can be run using:
```bash
python SkimTree.py path_to_ntuple_file
```
##### Example:
```bash
python SkimTree.py root://se01.indiacms.res.in:1094//dpm/indiacms.res.in/home/cms/store/user/zabai/t3store2/bbDM_bkg/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328/180202_114154/0001/NCUGlobalTuples_1009.root
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

Clone this repository in a location from where HTCondor jobs can be submitted (```ui.indiacms.res.in``` for example). We shall refer to this location as the working directory for this section.

## 3.1. Running Locally

* BranchReader can be run using:
```bash
python bbMETBranchReader.py -a -i path_to_skimmed_tree -D . --csv
```
* The "farmout" mode can be used to combine multiple input root files in one go. If all the root files are listed in a text file named input.txt, one can use:
```bash
python bbMETBranchReader.py -a -F -i input.txt -D . --csv
```
## 3.2. Running on HTCondor

***The number of BranchReader jobs can be adjusted by combining suitable number of input files in the Farmout mode.***


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
3. These .root files inside `BR_Outputs` can be used directly as inputs to the plotting code and will henceforth be referred to as **BranchReader outputs**.ch


# 4. Run Plotting Script

1. Copy all the outputs from BranchReader (in `hadd_outputs` directory) to a directory (or, optionally, segregate the files in separate directories named `data`, `bkg`, and `signal`).
2. Open `bbMETplot/Scripts/bbMET_StackFactory.py` and edit L92 to suit the current working directory. Edit L160, L229, and L272 to the path(s) where the BranchReader outputs are stored.
3. Navigate to `bbMETplot/Scripts/test` and run
```
python ../bbMET_StackFactory.py -d MET -s -m -q
python ../bbMET_StackFactory.py -d SE -e
python ../bbMET_StackFactory.py -d SP -p
```
The boolean flags are explained as follows:

* s: Signal Regions (only MC plots)
* m: Muon Control Regions
* q: QCD Control Regions
* e: Electron Control Regions
* p: Photon Control Regions
* The `-d` flag is used to select the appropriate primary dataset for each region.

