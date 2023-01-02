# Ntuple production for Signal and Backgrounds

To produce signal and background samples we use [Madgraph](http://madgraph.phys.ucl.ac.be/) as the main ME generator.
Then the ouptput will be inserted to [Pythia8](https://pythia.org/) for parton showering and hadronisation, and finally
[Delphes](https://cp3.irmp.ucl.ac.be/projects/delphes) (which is a C++ framework) will be used to simulate the interactions
between particles and detector materials. To produce signal samples (for both charm and up), need to run the MG script 
as the following:
```
./bin/mg5_aMC /path/to/script/signal/file
```
which will handle the whole process (ME, PS+Had, detector Sim) with the appropirate model and run parameters. 
The same can be run for background sample generaton:
```
./bin/mg5_aMC /path/to/script/background/file
```

There are several useful scripts for plotting in macro folder. We can get all the analysis plots by running:
 ```
 python2 ./macro/plotter.py --file ./tag_1_delphes_events.root 2>&1 | tee output.log
 ```

To make analysis trees for both signal and background, [tree_maker.py](https://github.com/mghasemi19/TopFC/blob/main/Ntuple_prod/macro/tree_maker.py) can be used as below:
```
python2 examples/tree_maker.py --files /data/mghasemi/IPM_test_signalup/Events/run_01/tag_1_delphes_events.root --treename upsignal
```
