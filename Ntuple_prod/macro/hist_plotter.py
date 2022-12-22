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

'''
if len(sys.argv) < 2:
  print(" Usage: Example1.py input_file")
  sys.exit(1)
'''

ROOT.gSystem.Load("libDelphes")

try:
  ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
  ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
except:
  pass

#inputFile = sys.argv[1]
inputFile = [f for f in args.files]

# Create chain of root trees
chain = ROOT.TChain("Delphes")
for f in inputFile: chain.Add(f)
#chain.Add(inputFile)

# Create object of class ExRootTreeReader
treeReader = ROOT.ExRootTreeReader(chain)
numberOfEntries = treeReader.GetEntries()

# Get pointers to branches used in this analysis
branchJet = treeReader.UseBranch("Jet")
branchElectron = treeReader.UseBranch("Electron")
branchMuon = treeReader.UseBranch("Muon")
branchPhoton = treeReader.UseBranch("Photon")
branchMET = treeReader.UseBranch("MissingET")

# Book Canvas
c1 = ROOT.TCanvas("c1","c1",1100,900);
#c1.Divide(1,4)

# Tree to keep variables
treeName = args.treename
tree_obj = ROOT.TTree(treeName, treeName+"tree")

# All histograms for objects
histJetPT = ROOT.TH1F("jet_pt", "jet P_{T}", 50, 0.0, 500.0)
histJetEta = ROOT.TH1F("jet_eta", "jet Eta", 50, -5.0, 5.0)
histJetPhi = ROOT.TH1F("jet_phi", "jet Phi", 16, -4.0, 4.0)
histJetNo = ROOT.TH1F("jet_number", "jet Number", 12, 0.0, 12.0)
histbJetPT = ROOT.TH1F("bjet_pt", "b-jet P_{T}", 50, 0.0, 500.0)
histbJetNo = ROOT.TH1F("bjet_number", "b-jet Number", 5, 0.0, 5.0)
histElectronPT = ROOT.TH1F("electron_pt", "electron P_{T}", 50, 0.0, 500.0)
histElectronEta = ROOT.TH1F("electron_eta", "electron Eta", 50, -5.0, 5.0)
histElectronPhi = ROOT.TH1F("electron_phi", "electron Phi", 16, -4.0, 4.0)
histdiElectronEta = ROOT.TH1F("dielectron_delta eta", "dielectron delta Eta", 50, -5.0, 5.0)
histdiElectronCosine = ROOT.TH1F("dielectron_cos", "dielectron Cosine", 14, 0.0, 7.0)
histdiElectronMass = ROOT.TH1F("dielectron_mass", "dielectron Mass", 6, 500.0, 3500.0)
histElectrondeltaR = ROOT.TH1F("dielectron_R", "dielectron delta R", 16, 0.0, 8.0)
histElectronNo = ROOT.TH1F("electron_number", "electron Number", 12, 0.0, 12.0)
histMuonPT = ROOT.TH1F("muon_pt", "muon P_{T}", 50, 0.0, 500.0)
histMuonEta = ROOT.TH1F("muon_eta", "muon Eta", 50, -5.0, 5.0)
histMuonNo = ROOT.TH1F("muon_number", "muon Number", 12, 0.0, 12.0)
histMET = ROOT.TH1F("MET", "MET", 100, 0.0, 300.0)
histWmass = ROOT.TH1F("Wmass", "Wboson Mass", 20, 50, 150)
histTopmass = ROOT.TH1F("Topmass", "Top Mass", 50, 100, 300)

#hist_list = [histJetPT, histJetEta, histJetPhi, histJetNo, histbJetPT, histbJetNo, histElectronPT, histElectronEta, histElectronPhi, histdiElectronEta, histdiElectronCosine, histElectrondeltaR, histdiElectronMass, histElectronNo, histMET, histWmass, histTopmass]
#hist_list = [histJetPT, histWmass, histTopmass]
#hist_list = [histJetPT, histJetEta, histJetPhi, histJetNo]
hist_list = [histdiElectronMass]

#dict_hist = {}

# Loop over all events
print ("Total Num of Events {}".format(numberOfEntries))

# Event weight
#weight = 0.0004 * 300 * 1E3 / numberOfEntries   # for a specific event
#weight = 1
#yield_val = 0
#y2 = 0

# Jet variables
#njet = int(branchJet.GetEntries())
njet = 5
print("Number of jets:", njet)

nEvent = 0
counter = 0
for entry in range(0, numberOfEntries):
  # Load selected branches with data from specified event
  #if (entry % 100 == 0 and entry != 0): break 
  #if (entry == 1): break 
  if (entry % 50000 == 0): print("Event Number:{}".format(entry))
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
  for i in range(0, branchJet.GetEntries()):
    jet = branchJet.At(i)
    histJetPT.Fill(jet.PT)
    histJetEta.Fill(jet.Eta)
    histJetPhi.Fill(jet.Phi)    
    
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
  for i in range(0, branchElectron.GetEntries()):
    electron = branchElectron.At(i)  
    # Save positive and negative charge electron's Eta
    if (electron.Charge==1): elec_eta['+'+str(i)] = electron.Eta
    else: elec_eta['-'+str(i)] = electron.Eta
    histElectronPT.Fill(electron.PT)
    histElectronEta.Fill(electron.Eta)
    histElectronPhi.Fill(electron.Phi)
  histElectronNo.Fill(branchElectron.GetEntries())
  #print(elec_eta)
  
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
  #print(index)
  
  histdiElectronEta.Fill(min_deltaEta)
  # deltaPhi or cosinePhi
  deltaPhi = abs(branchElectron.At(index[1]).Phi - branchElectron.At(index[-1]).Phi)
  deltaR = ROOT.sqrt((min_deltaEta * min_deltaEta) + (deltaPhi * deltaPhi))
  histdiElectronCosine.Fill(ROOT.cos(deltaPhi))
  histElectrondeltaR.Fill(deltaR)

  # Analyse missing ET
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

      # W boson and Top quark mass
      #mW = (met.P4() + branchElectron.At(index[0]).P4()).Mt()
      #mW = (met.P4() + branchElectron.At(index[0]).P4())**2
      mW = W_vec.Mt()      
      #mW = (met_vec + elec_vec).Mt()      
      #mTop = (branchJet.At(bjet_index).P4() + met.P4() + branchElectron.At(index[0]).P4()).Mt()
      mTop = top_vec.Mt()
    
      histWmass.Fill(mW)
      histTopmass.Fill(mTop)

  elec_first_vec = ROOT.TLorentzVector()
  elec_first_ET = ROOT.TMath.Sqrt(branchElectron.At(index[1]).PT**2 + 0.005**2)
  elec_second_vec = ROOT.TLorentzVector()  
  elec_second_ET = ROOT.TMath.Sqrt(branchElectron.At(index[-1]).PT**2 + 0.005**2)
  elec_first_vec.SetPtEtaPhiE(branchElectron.At(index[1]).PT, branchElectron.At(index[1]).Eta,
branchElectron.At(index[1]).Phi, elec_first_ET)
  elec_second_vec.SetPtEtaPhiE(branchElectron.At(index[-1]).PT, branchElectron.At(index[-1]).Eta,
branchElectron.At(index[-1]).Phi, elec_second_ET)
  mLL = (elec_first_vec + elec_second_vec).Mt()
  histdiElectronMass.Fill(mLL)  

  #tree_obj.Fill()

#histTopmass.Draw()
name = args.name
for hist in hist_list:
    hist.Draw()
    save_name = './plots/' + name + '_' + hist.GetName() + '.pdf'
    c1.SaveAs(save_name)
    c1.Clear()
f = ROOT.TFile("./trees/" + treeName + ".root", "RECREATE")
f.cd()
#tree_obj.Write('./trees/' + treeName + '.root', ROOT.TObject.kOverwrite)
#tree_obj.Write("", ROOT.TObject.kOverwrite)
#tree_obj.Scan("jetpT")
#tree_obj.Draw("jetPT")
#os.system('open test.pdf')
f.Close()

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
