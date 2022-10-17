#!/usr/bin/env python

from http.client import HTTP_VERSION_NOT_SUPPORTED
import sys
import os
import ROOT

try:
  input = raw_input
except:
  pass

if len(sys.argv) < 2:
  print(" Usage: Example1.py input_file")
  sys.exit(1)

ROOT.gSystem.Load("libDelphes")

try:
  ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
  ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
except:
  pass

inputFile = sys.argv[1]

# Create chain of root trees
chain = ROOT.TChain("Delphes")
chain.Add(inputFile)

# Create object of class ExRootTreeReader
treeReader = ROOT.ExRootTreeReader(chain)
numberOfEntries = treeReader.GetEntries()

# Get pointers to branches used in this analysis
branchJet = treeReader.UseBranch("Jet")
branchElectron = treeReader.UseBranch("Electron")
branchPhoton = treeReader.UseBranch("Photon")
branchMET = treeReader.UseBranch("MissingET")

# Book Canvas
c1 = ROOT.TCanvas("c1","c1",1100,900);
#c1.Divide(1,4)

# All histograms for objects
histJetPT = ROOT.TH1F("jet_pt", "jet P_{T}", 50, 0.0, 100.0)
histJetEta = ROOT.TH1F("jet_eta", "jet Eta", 50, -5.0, 5.0)
histJetNo = ROOT.TH1F("jet_number", "jet Number", 12, 0.0, 12.0)
histbJetPT = ROOT.TH1F("bjet_pt", "b-jet P_{T}", 50, 0.0, 100.0)
histbJetNo = ROOT.TH1F("bjet_number", "b-jet Number", 5, 0.0, 5.0)
histElectronPT = ROOT.TH1F("electron_pt", "electron P_{T}", 50, 0.0, 100.0)
histElectronEta = ROOT.TH1F("electron_eta", "electron Eta", 50, -5.0, 5.0)
histElectronNo = ROOT.TH1F("electron_number", "electron Number", 12, 0.0, 12.0)
histMET = ROOT.TH1F("MET", "MET", 100, 0.0, 300.0)

#dict_hist = {}

# Loop over all events
print ("Total Num of Events {}".format(numberOfEntries))

# Event weight
#weight = 0.0004 * 300 * 1E3 / numberOfEntries   # for a specific event
#weight = 1
#yield_val = 0
#y2 = 0

nEvent = 0
counter = 0
for entry in range(0, numberOfEntries):
  # Load selected branches with data from specified event
  treeReader.ReadEntry(entry)

  # Preselections exactly 3 leptons and at least 2 jet with 1 b-tagged
  if (not(branchElectron.GetEntries() == 3 and branchJet.GetEntries() >=2)): continue
  bJetNo = 0
  for i in range(0, branchJet.GetEntries()):
    jet = branchJet.At(i)
    if (jet.BTag): bJetNo += 1
  if (not bJetNo >= 1): continue
  nEvent += 1
  if (nEvent in range(0,10)): print("Jet No:{}\tbJetNo:{}\tElectronNo:{}".format(branchJet.GetEntries(), bJetNo, branchElectron.GetEntries()))

  # Loop over all jets in event
  for i in range(0, branchJet.GetEntries()):
    jet = branchJet.At(i)
    histJetPT.Fill(jet.PT)
    histJetEta.Fill(jet.Eta)
  histJetNo.Fill(branchJet.GetEntries())

  # Loop over all bjets in events
  for i in range(0, branchJet.GetEntries()):
    jet = branchJet.At(i)
    if (jet.BTag):
      histbJetPT.Fill(jet.PT)  
  histbJetNo.Fill(bJetNo)

  # Loop over all electrons in event
  for i in range(0, branchElectron.GetEntries()):
    electron = branchElectron.At(i)  
    histElectronPT.Fill(electron.PT)
    histElectronEta.Fill(electron.Eta)
  histElectronNo.Fill(branchElectron.GetEntries())

  # Analyse missing ET
  if branchMET.GetEntries() >= 0:
      met = branchMET.At(0)
      histMET.Fill(met.MET)

print("Number of events which pass the preselection: {}".format(nEvent))

histbJetNo.Draw()
c1.SaveAs('test.pdf')
os.system('open test.pdf')

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