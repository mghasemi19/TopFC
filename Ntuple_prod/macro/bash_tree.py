import os
import sys

#bkgs = {'ttbar': ['/data/mghasemi/samples/background/HLLHC*/Events/*/tag_1_delphes_events.root', '/data/mghasemi/samples/background/HLLHCttbar/Events/run_02/tag_1_delphes_events.root'], 'ttbarW':['/data/mghasemi/samples/background/ttbarW/Events/run_01/tag_1_delphes_events.root', '/data/mghasemi/samples/background/ttbarW/Events/run_02/tag_1_delphes_events.root'], 'ttbarZ':['/data/mghasemi/samples/background/ttbarZ/Events/run_01/tag_1_delphes_events.root', '/data/mghasemi/samples/background/ttbarZ/Events/run_02/tag_1_delphes_events.root'], 'tttt':['/data/mghasemi/samples/background/tttt/Events/run_01/tag_1_delphes_events.root', '/data/mghasemi/samples/background/tttt/Events/run_02/tag_1_delphes_events.root'], 'tZ':['/data/mghasemi/samples/background/tZ/Events/run_01/tag_1_delphes_events.root', '/data/mghasemi/samples/background/tZ/Events/run_02/tag_1_delphes_events.root'], 'WZ':['/data/mghasemi/samples/background/ZW/Events/run_01/tag_1_delphes_events.root', '/data/mghasemi/samples/background/ZW/Events/run_02/tag_1_delphes_events.root'], 'ZZ':['/data/mghasemi/samples/background/ZZ/Events/run_01/tag_1_delphes_events.root', '/data/mghasemi/samples/background/ZZ/Events/run_02/tag_1_delphes_events.root'], 'signal_charm':['/data/mghasemi/IPM_test_signalcharm/Events/run_01/tag_1_delphes_events.root', '/data/mghasemi/IPM_test_signalcharm2/Events/run_01/tag_1_delphes_events.root', '/data/mghasemi/IPM_test_signalcharm3/Events/run_01/tag_1_delphes_events.root'], 'signal_up':['/data/mghasemi/IPM_test_signalup/Events/run_01/tag_1_delphes_events.root', '/data/mghasemi/IPM_test2_signalup/Events/run_01/tag_1_delphes_events.root', '/data/mghasemi/IPM_test3_signalup/Events/run_01/tag_1_delphes_events.root']}

#bkgs = {'ttbar': ['/data/mghasemi/samples/background/HLLHC*/Events/*/tag_1_delphes_events.root'], 'WZ':['/data/mghasemi/samples/background/ZW*/Events/*/tag_1_delphes_events.root']}
#bkgs = {'WZ':['/data/mghasemi/samples/background/ZW*/Events/*/tag_1_delphes_events.root']}

#bkgs = {'ttbar': ['/data/mghasemi/samples/background/HLLHC*/Events/*/tag_1_delphes_events.root'], 'ttbarW':['/data/mghasemi/samples/background/ttbarW/Events/*/tag_1_delphes_events.root'], 'ttbarZ':['/data/mghasemi/samples/background/ttbarZ/Events/*/tag_1_delphes_events.root'], 'tttt':['/data/mghasemi/samples/background/tttt/Events/*/tag_1_delphes_events.root'], 'tZ':['/data/mghasemi/samples/background/tZ/Events/*/tag_1_delphes_events.root'], 'WZ':['/data/mghasemi/samples/background/ZW*/Events/*/tag_1_delphes_events.root'], 'ZZ':['/data/mghasemi/samples/background/ZZ/Events/*/tag_1_delphes_events.root'], 'signal_charm':['/data/mghasemi/IPM_test_signalcharm*/Events/run_0*/tag_1_delphes_events.root'], 'signal_up':['/data/mghasemi/IPM_test_signalup*/Events/run_0*/tag_1_delphes_events.root']}

bkgs = {'signal_charm_SRR':['/data/mghasemi/signal_coupling/ttbar_charm_SRR/Events/*/tag_1_delphes_events.root'], 'signal_charm_VRR':['/data/mghasemi/signal_coupling/ttbar_charm_VRR/Events/*/tag_1_delphes_events.root'], 'signal_charm_TRR':['/data/mghasemi/signal_coupling/ttbar_charm_TRR/Events/*/tag_1_delphes_events.root'], 'signal_up_SRR':['/data/mghasemi/signal_coupling/ttbar_up_SRR/Events/*/tag_1_delphes_events.root'], 'signal_up_VRR':['/data/mghasemi/signal_coupling/ttbar_up_VRR/Events/*/tag_1_delphes_events.root'], 'signal_up_TRR':['/data/mghasemi/signal_coupling/ttbar_up_TRR/Events/*/tag_1_delphes_events.root']}

for bkg in bkgs.keys():
   bkg_file = [bkgs[bkg][i] for i in range(len(bkgs[bkg]))]
   print ("python2 examples/tree_maker.py --files {} --treename {}".format(bkg_file[0], bkg))
   os.system("python2 examples/tree_maker.py --files {} --treename {}".format(bkg_file[0], bkg))
   print ("\n")

'''
for bkg in bkgs.keys():   
   bkg_file = [bkgs[bkg][i] for i in range(len(bkgs[bkg]))]
   #print bkg_file
   if len(bkg_file) == 2:
     print ("python2 examples/tree_maker.py --files {} {} --treename {}".format(bkg_file[0], bkg_file[1], bkg))
     os.system("python2 examples/tree_maker.py --files {} {} --treename {}".format(bkg_file[0], bkg_file[1], bkg))
     print ("\n")
   if len(bkg_file) == 3:
     print ("python2 examples/tree_maker.py --files {} {} {} --treename {}".format(bkg_file[0], bkg_file[1], bkg_file[2], bkg))
     os.system("python2 examples/tree_maker.py --files {} {} {} --treename {}".format(bkg_file[0], bkg_file[1], bkg_file[2], bkg))
     print ("\n")
'''

