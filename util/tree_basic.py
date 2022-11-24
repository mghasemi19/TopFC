#!/usr/bin/env python

import ROOT
import numpy as np
from array import array 
import random


def gaus_tree():
  tree = ROOT.TTree("T", "T")
  px = array('d', [0,0])
  #px = array('d', [0])
  tree.Branch("px", px, "px/D")
  hist = ROOT.TH1F("hist", "gaus", 100, -5, 5)
  hist.FillRandom("gaus", 1000)

  for i in range(1000): 
    px[0] = hist.GetRandom()
    px[1] = hist.GetRandom() + 1
    if i==0:
      print("px[0]:{}".format(px[0]))
      print("px[1]:{}".format(px[1]))

    tree.Fill()
  #tree.Draw("px")
  tree.Print()
  tree.Show(0)
  tree.StartViewer()
  raw_input("STOP")

def make_tree():
  f = ROOT.TFile("my_tree.root", "RECREATE")
  tree = ROOT.TTree("valid", "An Example Tree")
  pt = array('f', [0.])
  ptRef = array('f', [0.])
  rsp = array('f', [0.])
  tree.Branch("pt", pt, 'pt/F')
  tree.Branch("ptRef", ptRef,'ptRef/F')
  tree.Branch("rsp", rsp, 'rsp/F')
  for i in range(1000000):
    pt[0] = (i+1) * 1.0
    ptRef[0] = (i+1) * 1.0
    rsp[0] = 1. * pt[0] / ptRef[0]
    tree.Fill()
  tree.Write("", ROOT.TObject.kOverwrite);
  f.Close() 

def loop_tree():
  infile = ROOT.TFile("/Users/meisamghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/mlpHiggs.root")
  for tree in infile.GetListOfKeys():
    #print ("tree_name:{}".format(tree.GetName()))
    if "bg" in tree.GetName(): bg_tree = infile.Get("bg_filtered")
    if "sig" in tree.GetName(): sig_tree = infile.Get("sig_filtered")
  bg_tree.Print()
  tot_tree = ROOT.TTree("tot_Tree", "Tree")
  tot_pt = array('f', [0.])
  tot_tree.Branch("Tot_pt", tot_pt, "tot_pt/F")
  for i in range(bg_tree.GetEntries()):
    bg_tree.GetEntry(i)
    sig_tree.GetEntry(i)
    tot_pt[0] = bg_tree.ptsumf + sig_tree.ptsumf
    #print ("tot_pt:", tot_pt)
    tot_tree.Fill()
    #print ("tot_ptsumf:{}".format(tot_tree.Tot_pt))
  tot_tree.Draw("Tot_pt")
  raw_input("STOP")

def merge_tree():
  infile = ROOT.TFile("/Users/mghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/mlpHiggs.root")
  bkg_tree = infile.Get("bg_filtered")
  bkg_tree.Print()
  sig_tree = infile.Get("sig_filtered") 
  sig_tree.Print()
  ofile = ROOT.TFile("/Users/mghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/python_total.root", "RECREATE")
  tree_list = ROOT.TList()
  tree_list.Add(bkg_tree)
  tree_list.Add(sig_tree)
  new_tree = ROOT.TTree.MergeTrees(tree_list)
  new_tree.SetName("tot_filtered")
  new_tree.SetTitle("Total background (WW) events")
  new_tree.Write()
  infile.Close()
  ofile.Close()

def update_tree():
  #infile = ROOT.TFile("/Users/meisamghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/mlpHiggs.root", "update")
  infile = ROOT.TFile("/Users/meisamghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/ForTest.root", "update")
  bkg_tree = infile.Get("sig_filtered")
  test = array('f', [0.])
  br = bkg_tree.Branch("pt_m", test, "test/F")
  for i in range(bkg_tree.GetEntries()):
    bkg_tree.GetEntry(i)
    test[0] = bkg_tree.ptsumf + bkg_tree.msumf
    print ("test:{}".format(test[0]))
    br.Fill()
  
  #bkg_tree.Print()
  infile.Write("", ROOT.TObject.kOverwrite)
  infile.Close()
  
# not working
def remove_branch():
   #f = ROOT.TFile("/Users/meisamghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/mlpHiggs.root","update")
   f = ROOT.TFile("/Users/meisamghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/ForTest.root","update")
   T = f.Get("sig_filtered;1")
   b = T.GetBranch("pt_m")
   T.GetListOfBranches().Remove(b)
   #T.Write();
   f.Write("", ROOT.TObject.kOverwrite)
   f.Close();
    
if __name__ == "__main__":
  #gaus_tree()
  #make_tree
  #loop_tree()
  merge_tree()
  #update_tree()
  #remove_branch()
  

