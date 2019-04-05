mv signal signal_old
mkdir signal
cd signal_old
for fl in *.root; do cp ../bkg_data/Output_crab_TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root ../signal/"$fl"; done
cd ..
