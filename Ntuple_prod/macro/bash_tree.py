import os
import sys

bkgs = {'ttbar': ['/data/mghasemi/samples/background/HLLHCttbar/Events/run_01/tag_1_delphes_events.root', '/data/mghasemi/samples/background/HLLHCttbar/Events/run_02/tag_1_delphes_events.root'], 'ttbarW':['/data/mghasemi/samples/background/ttbarW/Events/run_01/tag_1_delphes_events.root', '/data/mghasemi/samples/background/ttbarW/Events/run_02/tag_1_delphes_events.root'], 'ttbarZ':['/data/mghasemi/samples/background/ttbarZ/Events/run_01/tag_1_delphes_events.root', '/data/mghasemi/samples/background/ttbarZ/Events/run_02/tag_1_delphes_events.root'], 'tttt':['/data/mghasemi/samples/background/tttt/Events/run_01/tag_1_delphes_events.root', '/data/mghasemi/samples/background/tttt/Events/run_02/tag_1_delphes_events.root'], 'tZ':['/data/mghasemi/samples/background/tZ/Events/run_01/tag_1_delphes_events.root', '/data/mghasemi/samples/background/tZ/Events/run_02/tag_1_delphes_events.root'], 'WZ':['/data/mghasemi/samples/background/ZW/Events/run_01/tag_1_delphes_events.root', '/data/mghasemi/samples/background/ZW/Events/run_02/tag_1_delphes_events.root'], 'ZZ':['/data/mghasemi/samples/background/ZZ/Events/run_01/tag_1_delphes_events.root', '/data/mghasemi/samples/background/ZZ/Events/run_02/tag_1_delphes_events.root']}

for bkg in bkgs.keys():
   bkg_file = [bkgs[bkg][i] for i in range(len(bkgs[bkg]))]
   #print bkg_file
   if len(bkg_file) == 2:
     print ("python2 examples/tree_maker.py --files {} {} --treename {}".format(bkg_file[0], bkg_file[1], bkg))
     os.system("python2 examples/tree_maker.py --files {} {} --treename {}".format(bkg_file[0], bkg_file[1], bkg))
   


