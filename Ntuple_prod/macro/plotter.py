#!/usr/bin/env python

#from http.client import HTTP_VERSION_NOT_SUPPORTED
import sys
import os
import ROOT
import argparse

parser = argparse.ArgumentParser(
                description='Produce Analysis variables.'
                )
parser.add_argument('--file', type=str, nargs='+', help='tree files want to be merged')
args = parser.parse_args()

try:
  input = raw_input
except:
  pass

if len(args.file) < 1:
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
inputFile = [f for f in args.file]

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

# All histograms for objects
histJetPT = ROOT.TH1F("jet_pt", "jet P_{T}", 50, 0.0, 100.0)
histJetEta = ROOT.TH1F("jet_eta", "jet Eta", 50, -5.0, 5.0)
histJetNo = ROOT.TH1F("jet_number", "jet Number", 12, 0.0, 12.0)
histbJetPT = ROOT.TH1F("bjet_pt", "b-jet P_{T}", 50, 0.0, 100.0)
histbJetNo = ROOT.TH1F("bjet_number", "b-jet Number", 5, 0.0, 5.0)
histElectronPT = ROOT.TH1F("electron_pt", "electron P_{T}", 50, 0.0, 100.0)
histElectronEta = ROOT.TH1F("electron_eta", "electron Eta", 50, -5.0, 5.0)
histdiElectronEta = ROOT.TH1F("dielectron_delta eta", "dielectron delta Eta", 50, -5.0, 5.0)
histdiElectronCosine = ROOT.TH1F("dielectron_cos", "dielectron Cosine", 14, 0.0, 7.0)
histElectrondeltaR = ROOT.TH1F("dielectron_R", "dielectron delta R", 16, 0.0, 8.0)
histElectronNo = ROOT.TH1F("electron_number", "electron Number", 12, 0.0, 12.0)
histMuonPT = ROOT.TH1F("muon_pt", "muon P_{T}", 50, 0.0, 100.0)
histMuonEta = ROOT.TH1F("muon_eta", "muon Eta", 50, -5.0, 5.0)
histMuonNo = ROOT.TH1F("muon_number", "muon Number", 12, 0.0, 12.0)
histMET = ROOT.TH1F("MET", "MET", 100, 0.0, 300.0)
histWmass = ROOT.TH1F("Wmass", "Wboson Mass", 20, 50, 150)
histTopmass = ROOT.TH1F("Topmass", "Top Mass", 50, 100, 300)

#hist_list = [histJetPT, histJetEta, histJetNo, histbJetPT, histbJetNo, histElectronPT, histElectronEta, histdiElectronEta, histdiElectronCosine, histElectrondeltaR, histElectronNo, histMET, histWmass, histTopmass]
hist_list = [histWmass, histTopmass]

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
  #if (entry % 100000 == 0): break 
  if (entry % 50000 == 0): print("Event Number:{}".format(entry))
  treeReader.ReadEntry(entry)

  # Preselections exactly 3 leptons and at least 2 jet with 1 b-tagged
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
  histdiElectronCosine.Fill(deltaPhi)
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

      #mW = (met.P4() + branchElectron.At(index[0]).P4()).Mt()
      #mW = (met.P4() + branchElectron.At(index[0]).P4())**2
      mW = W_vec.Mt()
      
      #mW = (met_vec + elec_vec).Mt()      
      #mTop = (branchJet.At(bjet_index).P4() + met.P4() + branchElectron.At(index[0]).P4()).Mt()
      mTop = top_vec.Mt()
    
      histWmass.Fill(mW)
      histTopmass.Fill(mTop)


print("Number of events which pass the preselection: {}".format(nEvent))


#histTopmass.Draw()
for hist in hist_list:
    hist.Draw()
    save_name = hist.GetName() + '.pdf'
    c1.SaveAs(save_name)
#os.system('open test.pdf')

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
