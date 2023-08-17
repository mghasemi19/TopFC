import os
import sys


#bkgs = {'ttbar': ['/data/mghasemi/samples/background/HLLHC*/Events/*/tag_1_delphes_events.root'], 'ttbarW':['/data/mghasemi/samples/background/ttbarW/Events/*/tag_1_delphes_events.root'], 'ttbarZ':['/data/mghasemi/samples/background/ttbarZ/Events/*/tag_1_delphes_events.root'], 'tttt':['/data/mghasemi/samples/background/tttt/Events/*/tag_1_delphes_events.root'], 'tZ':['/data/mghasemi/samples/background/tZ/Events/*/tag_1_delphes_events.root'], 'WZ':['/data/mghasemi/samples/background/ZW/Events/*/tag_1_delphes_events.root'], 'ZZ':['/data/mghasemi/samples/background/ZZ/Events/*/tag_1_delphes_events.root'], 'signal_tW_charm':['/data/mghasemi/samples/signals/tW_charm/Events/run_0*/tag_1_delphes_events.root'], 'signal_tW_up':['/data/mghasemi/samples/signals/tW_up/Events/run_0*/tag_1_delphes_events.root']}

#bkgs = {'ttbar': ['/data/mghasemi/samples/background/HLLHC*/Events/*/tag_1_delphes_events.root'], 'WZ':['/data/mghasemi/samples/background/ZW*/Events/*/tag_1_delphes_events.root']}

#bkgs = {'WZ':['/data/mghasemi/samples/background/ZW*/Events/*/tag_1_delphes_events.root']}
bkgs = {'signal_tW_charm_SRR':['/data/mghasemi/signal_coupling/tW_charm_SRR/Events/*/tag_1_delphes_events.root'], 'signal_tW_charm_VRR':['/data/mghasemi/signal_coupling/tW_charm_VRR/Events/*/tag_1_delphes_events.root'], 'signal_tW_charm_TRR':['/data/mghasemi/signal_coupling/tW_charm_TRR/Events/*/tag_1_delphes_events.root'], 'signal_tW_up_SRR':['/data/mghasemi/signal_coupling/tW_up_SRR/Events/*/tag_1_delphes_events.root'], 'signal_tW_up_VRR':['/data/mghasemi/signal_coupling/tW_up_VRR/Events/*/tag_1_delphes_events.root'], 'signal_tW_up_TRR':['/data/mghasemi/signal_coupling/tW_up_TRR/Events/*/tag_1_delphes_events.root']}

for bkg in bkgs.keys():   
   bkg_file = [bkgs[bkg][i] for i in range(len(bkgs[bkg]))]
   print ("python2 examples/tW_tree_maker.py --files {} --treename {}".format(bkg_file[0], bkg))
   os.system("python2 examples/tW_tree_maker.py --files {} --treename {}".format(bkg_file[0], bkg))
   print ("\n")
   
   '''
   if len(bkg_file) == 2:
     print ("python2 examples/tW_tree_maker.py --files {} {} --treename {}".format(bkg_file[0], bkg_file[1], bkg))
     os.system("python2 examples/tW_tree_maker.py --files {} {} --treename {}".format(bkg_file[0], bkg_file[1], bkg))
     print ("\n")
   if len(bkg_file) == 3:
     print ("python2 examples/tW_tree_maker.py --files {} {} {} --treename {}".format(bkg_file[0], bkg_file[1], bkg_file[2], bkg))
     os.system("python2 examples/tW_tree_maker.py --files {} {} {} --treename {}".format(bkg_file[0], bkg_file[1], bkg_file[2], bkg))
   '''


