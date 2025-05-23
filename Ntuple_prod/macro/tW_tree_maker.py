# TopFC analysis tree making framework. This makes trees with analysis variables as branches
#!/usr/bin/env python

#from http.client import HTTP_VERSION_NOT_SUPPORTED
import sys
import os
import ROOT
import argparse
import numpy as np
from array import array

parser = argparse.ArgumentParser(
                description='Produce TopFC Analysis variables.'
                )
parser.add_argument('--files', type=str, nargs='+', help='tree files want to be merged')
parser.add_argument('--treename', type=str, help='tree name to save variables')
args = parser.parse_args()

try:
  input = raw_input
except:
  pass

if len(args.files) < 1:
  print(" Usage: python2 treemaker.py --files input_file --treename name")
  sys.exit(1)

ROOT.gSystem.Load("libDelphes")

try:
  ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
  ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
except:
  pass

inputFile = [f for f in args.files]

# Create chain of root trees
chain = ROOT.TChain("Delphes")
for f in inputFile: chain.Add(f)

# Create object of class ExRootTreeReader
treeReader = ROOT.ExRootTreeReader(chain)
numberOfEntries = treeReader.GetEntries()

# Get pointers to branches used in this analysis
branchJet = treeReader.UseBranch("Jet")
branchElectron = treeReader.UseBranch("Electron")
branchMuon = treeReader.UseBranch("Muon")
branchPhoton = treeReader.UseBranch("Photon")
branchMET = treeReader.UseBranch("MissingET")

# weights for signal and backgrounds based on MG5 xsec
#weights = {'ttbarZ': 0.004368240427953154, 'tZ': 0.00375, 'tttt': 2.795205553087607e-05, 'ZZ': 0.67125, 'ttbar': 0.742304347826087, 'ttbarW': 0.00015, 'WZ': 0.02715,'signal_charm': 0.01376, 'signal_up': 0.01376, 'test':1, 'signal_tW_charm':7e-4, 'signal_tW_up':7e-4}

weights = {'signal_tW_charm_SRR': 1.2e-5, 'signal_tW_charm_VRR':4.8e-5 , 'signal_tW_charm_TRR': 0.0005, 'signal_tW_up_SRR': 1.8e-5, 'signal_tW_charm_VRR':7.2e-05 , 'signal_tW_charm_TRR': 0.000765}

# Tree to keep variables
treeName = args.treename
f = ROOT.TFile("./tW_trees/" + treeName + ".root", "RECREATE")
tree_obj = ROOT.TTree(treeName, treeName+"tree")

# List of all variables to keep in the tree

# Jet variables
jetNo = array('l', [0])
jetPT = array('d')
jetPTleading = array('d', [0.])
jetETA = array('d')
jetPHI = array('d')

# Electron variables
elecNo = array('l', [0])
elecPT = array('d')
elecPTleading = array('d', [0.])
elecETA = array('d')
elecPHI = array('d')

# Di-electron variables
dielecETA = array('d', [0.])
dielecCOS = array('d', [0.])
dielecMass = array('d', [0.])
dielecR = array('d', [0.])

# W-boson and SM and nonSM Top-quark Mass
Met = array('d', [0.])
WMass = array('d', [0.])
newWMass = array('d', [0.])
newSMTopMass = array('d', [0.])
nonSMTopMass = array('d', [0.])        # delta Eta algorithm
newnonSMTopMass = array('d', [0.])     # min top mass with leading jet
testnonSMTopMass = array('d', [0.])    # min top mass with all jets included

# Weights 
weight = array('d', [0.])

# Set tree branches
tree_obj.Branch("jetNo", jetNo, "jetNo/I")
tree_obj.Branch("jetPT", jetPT, "jetPT[jetNo]/D")
tree_obj.Branch("jetPTLeading", jetPTleading, "jetPTLeading/D")
tree_obj.Branch("jetETA", jetETA, "jetETA[jetNo]/D")
tree_obj.Branch("jetPHI", jetPHI, "jetPHI[jetNo]/D")

tree_obj.Branch("elecNo", elecNo, "elecNo/I")
tree_obj.Branch("elecPT", elecPT, "elecPT[elecNo]/D")
tree_obj.Branch("elecPTLeading", elecPTleading, "elecPTLeading/D")
tree_obj.Branch("elecETA", elecETA, "elecETA[elecNo]/D")
tree_obj.Branch("elecPHI", elecPHI, "elecPHI[elecNo]/D")

tree_obj.Branch("dielecETA", dielecETA, "dielecETA/D")
tree_obj.Branch("dielecCOS", dielecCOS, "dielecCOS/D")
tree_obj.Branch("dielecMass", dielecMass, "dielecMass/D")
tree_obj.Branch("dielecR", dielecR, "dieleR/D")

tree_obj.Branch("met", Met, "met/D")
tree_obj.Branch("WMass", WMass, "WMass/D")
tree_obj.Branch("newWMass", newWMass, "newWMass/D")
tree_obj.Branch("newTopMass", newSMTopMass, "newTopMass/D")
tree_obj.Branch("nonTopMass", nonSMTopMass, "nonTopMass/D")
tree_obj.Branch("newnonTopMass", newnonSMTopMass, "newnonTopMass/D")
tree_obj.Branch("testnonTopMass", testnonSMTopMass, "testnonTopMass/D")

tree_obj.Branch("weight", weight, "weight/D")

# Loop over all events
print ("Total Num of Events {}".format(numberOfEntries))
#quit()

# Event weight
# weight = xsec * lumi * eff / numberOfEntries 
#weight = 0.0004 * 300 * 1E3 / numberOfEntries   # for a specific event (H to bbar)

# Event numbers
nEvent = 0
counter = 0
for entry in range(0, numberOfEntries):
  # Load selected branches with data from specified event
  #if (entry % 100 == 0 and entry != 0): break 
  #if (entry == 500000): break 
  if (entry % 100000 == 0): print("Event Number:{}".format(entry))
  treeReader.ReadEntry(entry)

  # Trigger and Preselections exactly 3 leptons with 1 OS and at least 2 jet with 1 b-tagged
  if (not(branchElectron.GetEntries() == 3 and branchJet.GetEntries() >=1)): continue
  nonbJetNo = 0
  bJetNo = 0
  for i in range(0, branchJet.GetEntries()):
    jet = branchJet.At(i)
    # Di-lepton HLT --->>> jetPT>30 GeV and jetETA<5 (for non-btagged)
    # Di-lepton HLT --->>> jetPT>30 GeV and jetETA<3 (for btagged)
    if ((int(jet.BTag)==0) and (jet.PT>=30.) and (abs(jet.Eta)<=5.)): 
       nonbJetNo += 1
       #print("loop PT:", int(jet.PT))
       #print("loop eta:", int(jet.Eta))
    if ((int(jet.BTag)==1) and (jet.PT>=30.) and (abs(jet.Eta)<=3.)): 
       bJetNo += 1
       #print("loop PT:", int(jet.PT))
       #print("loop eta:", int(jet.Eta))
    #print("Btag:", int(jet.BTag))
    #print("PT:", int(jet.PT))
    #print("Eta:", int(jet.Eta))
  
  #print("nonbJetNo:", nonbJetNo)
  #print("branchJet.GetEntries():", branchJet.GetEntries())
  #print(">>>>>>>>>>>>")
  if (not nonbJetNo+bJetNo == branchJet.GetEntries()): continue
  if (not bJetNo == 0): continue

  ncharge = 0
  nelectron = 0
  for i in range(0, branchElectron.GetEntries()):
    electron = branchElectron.At(i)      
    # Di-lepton HLT --->>> jetPT>20 GeV and jetETA<3 (for electron)
    if (electron.PT>=20 and electron.Eta<=3): nelectron += 1
    ncharge += electron.Charge
  if (ncharge == -3 or ncharge == 3): continue
  if (not nelectron == branchElectron.GetEntries()): continue

 
  #if (nEvent == 21): break
  #if (nEvent == 1): break
  nEvent += 1
  #print("nonbJetNo:", nonbJetNo)
  #print("branchJet.GetEntries():", branchJet.GetEntries())
  
  #if (nEvent in range(0,10)): print("Jet No:{}\tbJetNo:{}\tElectronNo:{}".format(branchJet.GetEntries(), bJetNo, branchElectron.GetEntries()))

  # 1) Loop over all jets in event  
  leading_jet_pt = 0 	# Leading non b-tagged jet pT
  leading_jet_index = 0 # Leading non b-tagged jet index

  jetNo[0] = branchJet.GetEntries()
  jetPT = array( 'd')
  jetETA = array( 'd')
  jetPHI = array( 'd')

  for i in range(0, branchJet.GetEntries()):    
    jet = branchJet.At(i)
    #print "jet", i, " pT:", jet.PT
    jetPT.append(jet.PT)
    jetETA.append(jet.Eta)
    jetPHI.append(jet.Phi)
    if (jet.PT > leading_jet_pt) and (jet.BTag == 0): 
       leading_jet_pt = jet.PT
       leading_jet_index = i    
  jetPTleading[0] = leading_jet_pt

  # 2) Loop over all bjets in events  (no bjet for tW signal)
  
  # 3) Loop over all electrons in event
  elec_eta = {}
  leading_elec_pt = 0	 # leading electron pT
  leading_electron_index = 0  # Leading electron index
  
  elecNo[0] = branchElectron.GetEntries()
  elecPT = array( 'd')
  elecETA = array( 'd')
  elecPHI = array( 'd')

  for i in range(0, branchElectron.GetEntries()):  
    electron = branchElectron.At(i)  
    elecPT.append(electron.PT)
    elecETA.append(electron.Eta)
    elecPHI.append(electron.Phi)    
    # Save positive and negative charge electron's Eta
    if (electron.Charge==1): elec_eta['+'+str(i)] = electron.Eta
    else: elec_eta['-'+str(i)] = electron.Eta
    if (electron.PT > leading_elec_pt): 
       leading_elec_pt = electron.PT
       leading_electron_index = i
  elecPTleading[0] = leading_elec_pt
       
  # Delta Eta algorithm to select (OS) lepton+ and lepton-
  min_deltaEta = 999
  index = {}
  if (ncharge==-1):
      for i in elec_eta.keys():
          if i.startswith('+'):
              for j in elec_eta.keys():
                  if (i != j): 
                      tmp_eta = elec_eta[i] - elec_eta[j]
                      if (abs(tmp_eta) <= min_deltaEta): 
                        min_deltaEta = tmp_eta
                        index[1] = abs(int(i))
                        index[-1] = abs(int(j))                        
  if (ncharge==+1):
      for i in elec_eta.keys():
          if i.startswith('-'):
              for j in elec_eta.keys():
                  if (i != j): 
                      tmp_eta = elec_eta[i] - elec_eta[j]
                      if (abs(tmp_eta) <= min_deltaEta): 
                        min_deltaEta = tmp_eta
                        index[-1] = abs(int(i))
                        index[1] = abs(int(j))  
  index[0] = [k for k in range(0,3) if not (k==index[-1] or k==index[+1])][0]
  # index [-1, 1] corresponds to l- and l+ coming from non-SM top vertex
  # index[0] depends on the ncharge and coming from SM top vertex
 
  '''
  print(ncharge)
  for i in range(0, branchElectron.GetEntries()):
    electron = branchElectron.At(i)
    print(i, ":", electron.Charge)
  print(index)
  '''
  
  # 4) Fill Di-electron variables based on min delta ETA
  deltaPhi = abs(branchElectron.At(index[1]).Phi - branchElectron.At(index[-1]).Phi)
  deltaR = ROOT.sqrt((min_deltaEta * min_deltaEta) + (deltaPhi * deltaPhi))
  
  dielecETA[0] = min_deltaEta
  dielecCOS[0] = ROOT.cos(deltaPhi)
  dielecR[0] = deltaR 

  # 5) Analyse missing ET and W boson 
  #    (based on min delta ETA algorithm --->>> index[0] -- SM top vertex)
  if branchMET.GetEntries() >= 0:
      met = branchMET.At(0)
      met_vec = ROOT.TLorentzVector()
      elec_vec = ROOT.TLorentzVector()
      #met_vec.SetPtEtaPhiE(met.MET, met.Eta, met.Phi, met.MET) 
      met_vec.SetPtEtaPhiM(met.MET, met.Eta, met.Phi, 0) 
      elec_ET = ROOT.TMath.Sqrt(branchElectron.At(index[0]).PT**2 + 0.005**2)
      #elec_vec.SetPtEtaPhiE(branchElectron.At(index[0]).PT, branchElectron.At(index[0]).Eta,
      elec_vec.SetPtEtaPhiM(branchElectron.At(index[0]).PT, branchElectron.At(index[0]).Eta,
branchElectron.At(index[0]).Phi, 0.005)
      W_vec = met_vec + elec_vec
      mW = W_vec.Mt()      

      Met[0] = met.MET
      WMass[0] = mW
  
  # 6) New algorithm for (OS) lepton selection (mll - mtop with leading jet)
  newindex = {}  # new index for OS selection
  leadjet_vec = ROOT.TLorentzVector()
  leadjet_vec.SetPtEtaPhiM(branchJet.At(leading_jet_index).PT, branchJet.At(leading_jet_index).Eta, branchJet.At(leading_jet_index).Phi, branchJet.At(leading_jet_index).Mass)
  min_deltamass = 9999

  if (ncharge==+1):
      newindex[-1] = index[-1]
      elec_first_vec = ROOT.TLorentzVector()
      elec_first_ET = ROOT.TMath.Sqrt(branchElectron.At(index[-1]).PT**2 + 0.005**2)
      #elec_first_vec.SetPtEtaPhiE(branchElectron.At(index[-1]).PT, branchElectron.At(index[-1]).Eta,branchElectron.At(index[-1]).Phi, elec_first_ET)
      elec_first_vec.SetPtEtaPhiM(branchElectron.At(index[-1]).PT, branchElectron.At(index[-1]).Eta,branchElectron.At(index[-1]).Phi, 0.005)
      for i in index.keys():
          if (i != -1):
             elec_second_vec = ROOT.TLorentzVector()
             elec_second_ET = ROOT.TMath.Sqrt(branchElectron.At(index[i]).PT**2 + 0.005**2)
             #elec_second_vec.SetPtEtaPhiE(branchElectron.At(index[i]).PT, branchElectron.At(index[i]).Eta,branchElectron.At(index[i]).Phi, elec_second_ET)
             elec_second_vec.SetPtEtaPhiM(branchElectron.At(index[i]).PT, branchElectron.At(index[i]).Eta,branchElectron.At(index[i]).Phi, 0.005)
             newnoSMmTop = (elec_first_vec + elec_second_vec + leadjet_vec).Mt()
             delta_mass = abs(newnoSMmTop - 174)
             if (delta_mass < min_deltamass): 
                 newindex[1] = index[i]
                 min_deltamass = delta_mass
                 noSMmTop_new = newnoSMmTop
      newindex[0] = [k for k in range(0,3) if not (k==newindex[-1] or k==newindex[+1])][0]

  if (ncharge==-1):
      newindex[1] = index[1]
      elec_first_vec = ROOT.TLorentzVector()
      elec_first_ET = ROOT.TMath.Sqrt(branchElectron.At(index[1]).PT**2 + 0.005**2)
      #elec_first_vec.SetPtEtaPhiE(branchElectron.At(index[1]).PT, branchElectron.At(index[1]).Eta,branchElectron.At(index[1]).Phi, elec_first_ET)
      elec_first_vec.SetPtEtaPhiM(branchElectron.At(index[1]).PT, branchElectron.At(index[1]).Eta,branchElectron.At(index[1]).Phi, 0.005)
      for i in index.keys():
          if (i != 1):
             elec_second_vec = ROOT.TLorentzVector()
             elec_second_ET = ROOT.TMath.Sqrt(branchElectron.At(index[i]).PT**2 + 0.005**2)
             #elec_second_vec.SetPtEtaPhiE(branchElectron.At(index[i]).PT, branchElectron.At(index[i]).Eta,branchElectron.At(index[i]).Phi, elec_second_ET)
             elec_second_vec.SetPtEtaPhiM(branchElectron.At(index[i]).PT, branchElectron.At(index[i]).Eta,branchElectron.At(index[i]).Phi, 0.005)
             newnoSMmTop = (elec_first_vec + elec_second_vec + leadjet_vec).Mt()
             delta_mass = abs(newnoSMmTop - 174)
             if (delta_mass < min_deltamass): 
                 newindex[-1] = index[i]
                 min_deltamass = delta_mass
                 noSMmTop_new = newnoSMmTop                 

      newindex[0] = [k for k in range(0,3) if not (k==newindex[-1] or k==newindex[+1])][0]

  #print(newindex)
  newnonSMTopMass[0] = noSMmTop_new


  # 7) New algorithm for (OS) lepton selection with Jet selection as an extra degree of freedome
  newindex = {}  # new index for OS selection
  min_deltamass = 9999

  if (ncharge==+1):
      newindex[-1] = index[-1]
      elec_first_vec = ROOT.TLorentzVector()
      elec_first_ET = ROOT.TMath.Sqrt(branchElectron.At(index[-1]).PT**2 + 0.005**2)
      #elec_first_vec.SetPtEtaPhiE(branchElectron.At(index[-1]).PT, branchElectron.At(index[-1]).Eta,branchElectron.At(index[-1]).Phi, elec_first_ET)
      elec_first_vec.SetPtEtaPhiM(branchElectron.At(index[-1]).PT, branchElectron.At(index[-1]).Eta,branchElectron.At(index[-1]).Phi, 0.005)
      for i in index.keys():
          if (i != -1):
             elec_second_vec = ROOT.TLorentzVector()
             elec_second_ET = ROOT.TMath.Sqrt(branchElectron.At(index[i]).PT**2 + 0.005**2)
             #elec_second_vec.SetPtEtaPhiE(branchElectron.At(index[i]).PT, branchElectron.At(index[i]).Eta,branchElectron.At(index[i]).Phi, elec_second_ET)
             elec_second_vec.SetPtEtaPhiM(branchElectron.At(index[i]).PT, branchElectron.At(index[i]).Eta,branchElectron.At(index[i]).Phi, 0.005)
             for j in range(0, branchJet.GetEntries()):
		 if (branchJet.At(j).BTag == 0):
		    jet_vec = ROOT.TLorentzVector()
		    jet_vec.SetPtEtaPhiM(branchJet.At(j).PT, branchJet.At(j).Eta, branchJet.At(j).Phi, branchJet.At(j).Mass)
		    #print("jet_vec.M", jet_vec.M())
                    newnoSMmTop = (elec_first_vec + elec_second_vec + jet_vec).Mt()
                    delta_mass = abs(newnoSMmTop - 174)
                    #print("newnoSMmTop", newnoSMmTop)
                    #print(i, index[i])
                    if (delta_mass < min_deltamass): 
                       newindex[1] = index[i]
                       min_deltamass = delta_mass
                       noSMmTop_new = newnoSMmTop
      newindex[0] = [k for k in range(0,3) if not (k==newindex[-1] or k==newindex[+1])][0]

  if (ncharge==-1):
      newindex[1] = index[1]
      elec_first_vec = ROOT.TLorentzVector()
      elec_first_ET = ROOT.TMath.Sqrt(branchElectron.At(index[1]).PT**2 + 0.005**2)
      #elec_first_vec.SetPtEtaPhiE(branchElectron.At(index[1]).PT, branchElectron.At(index[1]).Eta,branchElectron.At(index[1]).Phi, elec_first_ET)
      elec_first_vec.SetPtEtaPhiM(branchElectron.At(index[1]).PT, branchElectron.At(index[1]).Eta,branchElectron.At(index[1]).Phi, 0.005)
      for i in index.keys():
          if (i != 1):
             elec_second_vec = ROOT.TLorentzVector()
             elec_second_ET = ROOT.TMath.Sqrt(branchElectron.At(index[i]).PT**2 + 0.005**2)
             #elec_second_vec.SetPtEtaPhiE(branchElectron.At(index[i]).PT, branchElectron.At(index[i]).Eta,branchElectron.At(index[i]).Phi, elec_second_ET)
             elec_second_vec.SetPtEtaPhiM(branchElectron.At(index[i]).PT, branchElectron.At(index[i]).Eta,branchElectron.At(index[i]).Phi, 0.005)
             for j in range(0, branchJet.GetEntries()):
		 if (branchJet.At(j).BTag == 0):
                    jet_vec = ROOT.TLorentzVector()
                    jet_vec.SetPtEtaPhiM(branchJet.At(j).PT, branchJet.At(j).Eta, branchJet.At(j).Phi, branchJet.At(j).Mass)
                    newnoSMmTop = (elec_first_vec + elec_second_vec + jet_vec).Mt()  
                    delta_mass = abs(newnoSMmTop - 174)
                    if (delta_mass < min_deltamass): 
                       newindex[-1] = index[i]
                       min_deltamass = delta_mass
                       noSMmTop_new = newnoSMmTop                 

      newindex[0] = [k for k in range(0,3) if not (k==newindex[-1] or k==newindex[+1])][0]

  #print(newindex)
  testnonSMTopMass[0] = noSMmTop_new

  # 8) W boson mass with new algorithm (based on newindex[0] -- SM top vertex)
  if branchMET.GetEntries() >= 0:
      met = branchMET.At(0)
      met_vec = ROOT.TLorentzVector()
      elec_vec = ROOT.TLorentzVector()
      #met_vec.SetPtEtaPhiE(met.MET, met.Eta, met.Phi, met.MET)
      met_vec.SetPtEtaPhiM(met.MET, met.Eta, met.Phi, 0)
      elec_ET = ROOT.TMath.Sqrt(branchElectron.At(newindex[0]).PT**2 + 0.005**2)
      #elec_vec.SetPtEtaPhiE(branchElectron.At(index[0]).PT, branchElectron.At(index[0]).Eta,
      elec_vec.SetPtEtaPhiM(branchElectron.At(newindex[0]).PT, branchElectron.At(newindex[0]).Eta,
branchElectron.At(newindex[0]).Phi, 0.005)
      W_vec = met_vec + elec_vec

      mW = W_vec.Mt()

      newWMass[0] = mW

  # 9) Old algorithm (delta ETA) to analyze non SM Top and mLL
  elec_first_vec = ROOT.TLorentzVector()
  elec_first_ET = ROOT.TMath.Sqrt(branchElectron.At(index[1]).PT**2 + 0.005**2)
  elec_second_vec = ROOT.TLorentzVector()  
  elec_second_ET = ROOT.TMath.Sqrt(branchElectron.At(index[-1]).PT**2 + 0.005**2)
  #elec_first_vec.SetPtEtaPhiE(branchElectron.At(index[1]).PT, branchElectron.At(index[1]).Eta,branchElectron.At(index[1]).Phi, elec_first_ET)
  elec_first_vec.SetPtEtaPhiM(branchElectron.At(index[1]).PT, branchElectron.At(index[1]).Eta,branchElectron.At(index[1]).Phi, 0.005)
  #elec_second_vec.SetPtEtaPhiE(branchElectron.At(index[-1]).PT, branchElectron.At(index[-1]).Eta,branchElectron.At(index[-1]).Phi, elec_second_ET)
  elec_second_vec.SetPtEtaPhiM(branchElectron.At(index[-1]).PT, branchElectron.At(index[-1]).Eta,branchElectron.At(index[-1]).Phi, 0.005)
  leadjet_vec = ROOT.TLorentzVector()
  leadjet_vec.SetPtEtaPhiM(branchJet.At(leading_jet_index).PT, branchJet.At(leading_jet_index).Eta, branchJet.At(leading_jet_index).Phi, branchJet.At(leading_jet_index).Mass)
  
  mLL = (elec_first_vec + elec_second_vec).Mt()
  noSMmTop = (elec_first_vec + elec_second_vec + leadjet_vec).Mt()
  
  dielecMass[0] = mLL  
  nonSMTopMass[0] = noSMmTop

  # Weight for the sample
  weight[0] = float("{:.4f}".format(weights[treeName]))
  #print weight[0]
 
  # Set branches address back to their origin
  tree_obj.SetBranchAddress("jetPT", jetPT)  
  tree_obj.SetBranchAddress("jetETA", jetETA)  
  tree_obj.SetBranchAddress("jetPHI", jetPHI)  
  tree_obj.SetBranchAddress("elecPT", elecPT)  
  tree_obj.SetBranchAddress("elecETA", elecETA)  
  tree_obj.SetBranchAddress("elecPHI", elecPHI) 

  tree_obj.Fill() 
    
f.cd()
tree_obj.Write()
#tree_obj.Scan("weight")
print("./tW_trees/couplings" + treeName + ".root is created")
f.Close()


'''
# Yield value
#yield_val += weight
#y2 = weight * weight

#print("Event yield: {} +/- {}".format(yield_val, y2))
#print("Selection Efficiency: {}".format(yield_val / (weight * numberOfEntries)))

'''
