#!/usr/bin/env python

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


# Book histograms
c1 = ROOT.TCanvas("c1","c1",1100,900);
c1.Divide(1,4)
histJetPT = ROOT.TH1F("jet_pt", "jet P_{T}", 100, 0.0, 100.0)
histMass = ROOT.TH1F("mass", "M_{inv}(e_{1}, e_{2})", 100, 40.0, 140.0)
histPhotonMass = ROOT.TH1F("DiPhotoMass", "M_{inv}(a_{1})(a_{2})", 100, 110.0, 140.0)
histMET = ROOT.TH1F("MET", "MET", 100, 0.0, 300.0)

# Loop over all events
print ("Num of Events {}".format(numberOfEntries))

# Event weight
weight = 0.0004 * 300 * 1E3 / numberOfEntries
yield_val = 0
y2 = 0

counter = 0
for entry in range(0, numberOfEntries):
  # Load selected branches with data from specified event
  treeReader.ReadEntry(entry)

  # If event contains at least 1 jet
  if branchJet.GetEntries() > 0:
    # Take first jet
    jet = branchJet.At(0)

    # Plot jet transverse momentum
    histJetPT.Fill(jet.PT, weight)

    # Print jet transverse momentum
    #print(jet.PT)

  # If event contains at least 2 electrons
  if branchElectron.GetEntries() > 1:
    counter += 1
    # Take first two electrons
    elec1 = branchElectron.At(0)
    elec2 = branchElectron.At(1)

    # Plot their invariant mass
    histMass.Fill(((elec1.P4()) + (elec2.P4())).M(), weight)

  # If event contains any MET
  if branchMET.GetEntries() > 0:
      met = branchMET.At(0)
      histMET.Fill(met.MET, weight)

   # If event contains at least 2 photons
  if branchPhoton.GetEntries() > 1:
    # Take first two photons
    phot1 = branchPhoton.At(0)
    phot2 = branchPhoton.At(1)

    if (phot1.PT < 20 or phot2.PT < 20 or abs(phot1.Eta) > 2.5 or abs(phot2.Eta) > 2.5): continue
    # Plot their invariant mass
    histPhotonMass.Fill(((phot1.P4()) + (phot2.P4())).M(), weight)

  # Yield value
  yield_val += weight
  y2 = weight * weight

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

print("Event yield: {} +/- {}".format(yield_val, y2))
print("Selection Efficiency: {}".format(yield_val / (weight * numberOfEntries)))

c1.SaveAs("./test.pdf")
os.system("open test.pdf")




