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
parser.add_argument('--name', type=str, help='either signal or background name')
parser.add_argument('--treename', type=str, help='tree name to save variables')
args = parser.parse_args()

try:
  input = raw_input
except:
  pass

if len(args.files) < 1:
  print(" Usage: Example1.py input_file")
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

# Tree to keep variables
treeName = args.treename
f = ROOT.TFile("./trees/" + treeName + ".root", "RECREATE")
tree_obj = ROOT.TTree(treeName, treeName+"tree")

# List of all variables to keep in the tree

# Jet variables
jetNo = array('l', [0])
jetPT = array('d')
jetPTleading = array('d', [0.])
jetETA = array('d')
jetPHI = array('d')

# bjet variables
bjetNo = array('l', [0])
bjetPT = array('d')

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
WMass = array('d', [0.])
SMTopMass = array('d', [0.])
nonSMTopMass = array('d', [0.])
newnonSMTopMass = array('d', [0.])

# Set tree branches
tree_obj.Branch("jetNo", jetNo, "jetNo/I")
tree_obj.Branch("jetPT", jetPT, "jetPT[jetNo]/D")
tree_obj.Branch("jetPTLeading", jetPTleading, "jetPTLeading/D")
tree_obj.Branch("jetETA", jetETA, "jetETA[jetNo]/D")
tree_obj.Branch("jetPHI", jetPHI, "jetPHI[jetNo]/D")

tree_obj.Branch("bjetNo", bjetNo, "bjetNo/I")
tree_obj.Branch("bjetPT", bjetPT, "jetPT/D")

tree_obj.Branch("elecNo", elecNo, "elecNo/I")
tree_obj.Branch("elecPT", elecPT, "elecPT[elecNo]/D")
tree_obj.Branch("elecPTLeading", PTleading, "elecPTLeading/D")
tree_obj.Branch("elecETA", elecETA, "elecETA[elecNo]/D")
tree_obj.Branch("elecPHI", elecPHI, "elecPHI[elecNo]/D")

tree_obj.Branch("dielecETA", dielecETA, "dielecETA/D")
tree_obj.Branch("dielecCOS", dielecCOS, "dielecCOS/D")
tree_obj.Branch("dielecMass", dielecMass, "dielecMass/D")
tree_obj.Branch("dielecR", dielecR, "dieleR/D")

tree_obj.Branch("WMass", WMass, "WMass/D")
tree_obj.Branch("TopMass", SMTopMass, "TopMass/D")
tree_obj.Branch("nonTopMass", nonSMTopMass, "nonTopMass/D")
tree_obj.Branch("newnonTopMass", newnonSMTopMass, "newnonTopMass/D")

# Loop over all events
print ("Total Num of Events {}".format(numberOfEntries))

# Event weight
#weight = 0.0004 * 300 * 1E3 / numberOfEntries   # for a specific event
#weight = 1
#yield_val = 0
#y2 = 0

# Jet variables
nEvent = 0
counter = 0
for entry in range(0, numberOfEntries):
  # Load selected branches with data from specified event
  #if (entry % 100 == 0 and entry != 0): break 
  #if (entry == 500): break 
  if (entry % 100000 == 0): print("Event Number:{}".format(entry))
  treeReader.ReadEntry(entry)

  # Preselections exactly 3 leptons with 1 OS and at least 2 jet with 1 b-tagged
  if (not(branchElectron.GetEntries() == 3 and branchJet.GetEntries() >=2)): continue
  bJetNo = 0
  for i in range(0, branchJet.GetEntries()):
    jet = branchJet.At(i)
    if (jet.BTag): bJetNo += 1
  if (not bJetNo == 1): continue
  ncharge = 0
  for i in range(0, branchElectron.GetEntries()):
    electron = branchElectron.At(i)      
    ncharge += electron.Charge
  if (ncharge == -3 or ncharge == 3): continue

  nEvent += 1

  #if (nEvent in range(0,10)): print("Jet No:{}\tbJetNo:{}\tElectronNo:{}".format(branchJet.GetEntries(), bJetNo, branchElectron.GetEntries()))

  # Loop over all jets in event  
  leading_jet_pt = 0 	# Leading non b-tagged jet pT
  leading_jet_index = 0 # Leading non b-tagged jet index
  for i in range(0, branchJet.GetEntries()):
    jet = branchJet.At(i)
    if (jet.PT > leading_jet_pt) and (jet.BTag == 0): 
       leading_jet_pt = jet.PT
       leading_jet_index = i
  histJetPTLead.Fill(leading_jet_pt)
    
  histJetNo.Fill(branchJet.GetEntries())

  # Loop over all bjets in events  
  for i in range(0, branchJet.GetEntries()):
    jet = branchJet.At(i)
    if (jet.BTag):
      histbJetPT.Fill(jet.PT)  
      bjet_index = i
  histbJetNo.Fill(bJetNo)

  # Loop over all electrons in event
  elec_eta = {}
  leading_elec_pt = 0	 # leading electron pT
  
  for i in range(0, branchElectron.GetEntries()):
    electron = branchElectron.At(i)  
    # Save positive and negative charge electron's Eta
    if (electron.Charge==1): elec_eta['+'+str(i)] = electron.Eta
    else: elec_eta['-'+str(i)] = electron.Eta
    histElectronPT.Fill(electron.PT)
    histElectronEta.Fill(electron.Eta)
    histElectronPhi.Fill(electron.Phi)
    if (electron.PT > leading_elec_pt): leading_elec_pt = electron.PT
       
  histElectronPTLead.Fill(leading_elec_pt)
  histElectronNo.Fill(branchElectron.GetEntries())
  
  # Delta Eta for lepton+ and lepton-
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
  
  histdiElectronEta.Fill(min_deltaEta)
  # deltaPhi or cosinePhi od Di-electron
  deltaPhi = abs(branchElectron.At(index[1]).Phi - branchElectron.At(index[-1]).Phi)
  deltaR = ROOT.sqrt((min_deltaEta * min_deltaEta) + (deltaPhi * deltaPhi))
  histdiElectronCosine.Fill(ROOT.cos(deltaPhi))
  histElectrondeltaR.Fill(deltaR)

  # Analyse missing ET, W boson and SM top mass
  if branchMET.GetEntries() >= 0:
      met = branchMET.At(0)
      histMET.Fill(met.MET)  
      met_vec = ROOT.TLorentzVector()
      elec_vec = ROOT.TLorentzVector()
      bjet_vec = ROOT.TLorentzVector()
      met_vec.SetPtEtaPhiE(met.MET, met.Eta, met.Phi, met.MET) 
      elec_ET = ROOT.TMath.Sqrt(branchElectron.At(index[0]).PT**2 + 0.005**2)
      #elec_vec.SetPtEtaPhiE(branchElectron.At(index[0]).PT, branchElectron.At(index[0]).Eta, branchElectron.At(index[0]).Phi, branchElectron.At(index[0]).PT)
      elec_vec.SetPtEtaPhiE(branchElectron.At(index[0]).PT, branchElectron.At(index[0]).Eta,
branchElectron.At(index[0]).Phi, elec_ET)
      bjet_ET = ROOT.TMath.Sqrt(branchJet.At(bjet_index).PT**2 + 4.67**2)
      bjet_vec.SetPtEtaPhiE(branchJet.At(bjet_index).PT, branchJet.At(bjet_index).Eta, branchJet.At(bjet_index).Phi, bjet_ET)
      W_vec = met_vec + elec_vec
      top_vec = met_vec + elec_vec + bjet_vec

      mW = W_vec.Mt()      
      histWmass.Fill(mW)
      mTop = top_vec.Mt()
      histTopmass.Fill(mTop)
      # W boson and Top quark mass
      #mW = (met.P4() + branchElectron.At(index[0]).P4()).Mt()
      #mW = (met.P4() + branchElectron.At(index[0]).P4())**2
      #mW = (met_vec + elec_vec).Mt()      
      #mTop = (branchJet.At(bjet_index).P4() + met.P4() + branchElectron.At(index[0]).P4()).Mt()
  
  # New algorithm gor ll selection
  leadjet_vec = ROOT.TLorentzVector()
  #leadjet_ET = ROOT.TMath.Sqrt(branchJet.At(leading_jet_index).PT**2 + branchJet.At(leading_jet_index).Mass)
  #leadjet_vec.SetPtEtaPhiE(branchJet.At(leading_jet_index).PT, branchJet.At(leading_jet_index).Eta, branchJet.At(leading_jet_index).Phi, leadjet_ET)
  leadjet_vec.SetPtEtaPhiM(branchJet.At(leading_jet_index).PT, branchJet.At(leading_jet_index).Eta, branchJet.At(leading_jet_index).Phi, branchJet.At(leading_jet_index).Mass)
  min_deltamass = 9999
  #noSMmTop_new = 0

  if (ncharge==+1):
      elec_first_vec = ROOT.TLorentzVector()
      elec_first_ET = ROOT.TMath.Sqrt(branchElectron.At(index[-1]).PT**2 + 0.005**2)
      elec_first_vec.SetPtEtaPhiE(branchElectron.At(index[-1]).PT, branchElectron.At(index[-1]).Eta,branchElectron.At(index[-1]).Phi, elec_first_ET)
      for i in index.keys():
          if (i != -1):
             elec_second_vec = ROOT.TLorentzVector()
             elec_second_ET = ROOT.TMath.Sqrt(branchElectron.At(index[i]).PT**2 + 0.005**2)
             elec_second_vec.SetPtEtaPhiE(branchElectron.At(index[i]).PT, branchElectron.At(index[i]).Eta,branchElectron.At(index[i]).Phi, elec_second_ET)
             newnoSMmTop = (elec_first_vec + elec_second_vec + leadjet_vec).Mt()
             delta_mass = abs(newnoSMmTop - 174)
             if (delta_mass < min_deltamass): 
                 min_deltamass = delta_mass
                 noSMmTop_new = newnoSMmTop

  if (ncharge==-1):
      elec_first_vec = ROOT.TLorentzVector()
      elec_first_ET = ROOT.TMath.Sqrt(branchElectron.At(index[1]).PT**2 + 0.005**2)
      elec_first_vec.SetPtEtaPhiE(branchElectron.At(index[1]).PT, branchElectron.At(index[1]).Eta,branchElectron.At(index[1]).Phi, elec_first_ET)
      for i in index.keys():
          if (i != 1):
             elec_second_vec = ROOT.TLorentzVector()
             elec_second_ET = ROOT.TMath.Sqrt(branchElectron.At(index[i]).PT**2 + 0.005**2)
             elec_second_vec.SetPtEtaPhiE(branchElectron.At(index[i]).PT, branchElectron.At(index[i]).Eta,branchElectron.At(index[i]).Phi, elec_second_ET)
             newnoSMmTop = (elec_first_vec + elec_second_vec + leadjet_vec).Mt()
             delta_mass = abs(newnoSMmTop - 174)
             if (delta_mass < min_deltamass): 
                 min_deltamass = delta_mass
                 noSMmTop_new = newnoSMmTop                 

  #print "NoSM Top mass:", noSMmTop_new
  histnewnoSMTopmass.Fill(noSMmTop_new)

  # Old algorithm to analyze non SM Top and mLL
  elec_first_vec = ROOT.TLorentzVector()
  elec_first_ET = ROOT.TMath.Sqrt(branchElectron.At(index[1]).PT**2 + 0.005**2)
  elec_second_vec = ROOT.TLorentzVector()  
  elec_second_ET = ROOT.TMath.Sqrt(branchElectron.At(index[-1]).PT**2 + 0.005**2)
  elec_first_vec.SetPtEtaPhiE(branchElectron.At(index[1]).PT, branchElectron.At(index[1]).Eta,branchElectron.At(index[1]).Phi, elec_first_ET)
  elec_second_vec.SetPtEtaPhiE(branchElectron.At(index[-1]).PT, branchElectron.At(index[-1]).Eta,branchElectron.At(index[-1]).Phi, elec_second_ET)
  leadjet_vec = ROOT.TLorentzVector()
  #leadjet_ET = ROOT.TMath.Sqrt(branchJet.At(leading_jet_index).PT**2 + branchJet.At(leading_jet_index).Mass)
  #leadjet_vec.SetPtEtaPhiE(branchJet.At(leading_jet_index).PT, branchJet.At(leading_jet_index).Eta, branchJet.At(leading_jet_index).Phi, leadjet_ET)
  leadjet_vec.SetPtEtaPhiM(branchJet.At(leading_jet_index).PT, branchJet.At(leading_jet_index).Eta, branchJet.At(leading_jet_index).Phi, branchJet.At(leading_jet_index).Mass)
  
  mLL = (elec_first_vec + elec_second_vec).Mt()
  noSMmTop = (elec_first_vec + elec_second_vec + leadjet_vec).Mt()
  
  histdiElectronMass.Fill(mLL)  
  histnoSMTopmass.Fill(noSMmTop)

name = args.name
for hist in hist_list:
    hist.Draw()
    save_name = './plots/' + name + '_' + hist.GetName() + '.pdf'
    c1.SaveAs(save_name)
    c1.Clear()

'''
# Yield value
#yield_val += weight
#y2 = weight * weight

print("Number of Events with more than two electrons {}".format(counter))
# Show resulting histograms
c1.cd(1)
histJetPT.Draw()
#input("Press Enter to continue...")
c1.cd(2)
histMass.Draw()
c1.cd(3)
histMET.Draw()
c1.cd(4)
histPhotonMass.Draw()

#print("Event yield: {} +/- {}".format(yield_val, y2))
#print("Selection Efficiency: {}".format(yield_val / (weight * numberOfEntries)))

c1.SaveAs("./test.pdf")
os.system("open test.pdf")
'''
