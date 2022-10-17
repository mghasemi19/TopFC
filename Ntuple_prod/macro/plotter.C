/*
Simple macro showing how to access branches from the delphes output root file,
loop over events, store histograms in a root file and print them as image files.

root -l examples/Example2.C'("delphes_output.root")'
*/

#include "TH1.h"
#include "TSystem.h"

#ifdef __CLING__
R__LOAD_LIBRARY(libDelphes)
#include "classes/DelphesClasses.h"
#include "external/ExRootAnalysis/ExRootTreeReader.h"
#include "external/ExRootAnalysis/ExRootResult.h"
#endif

//------------------------------------------------------------------------------

struct MyPlots
{
  TH1 *fJetPT;
  TH1 *fJetEta;
  TH1 *fJetNo;
  TH1 *fbJetPT;
  TH1 *fbJetNo;
  TH1 *fMissingET;
  TH1 *fElectronPT;
  TH1 *fElectronEta;
  TH1 *fElectronNo;
};

//------------------------------------------------------------------------------

class ExRootResult;
class ExRootTreeReader;

//------------------------------------------------------------------------------

void BookHistograms(ExRootResult *result, MyPlots *plots)
{
  THStack *stack;
  TLegend *legend;
  TPaveText *comment;

  // book 2 histograms for PT of 1st and 2nd leading jets

  /*
  plots->fJetPT[0] = result->AddHist1D(
    "jet_pt_0", "leading jet P_{T}",
    "jet P_{T}, GeV/c", "number of jets",
    50, 0.0, 100.0);

  plots->fJetPT[1] = result->AddHist1D(
    "jet_pt_1", "2nd leading jet P_{T}",
    "jet P_{T}, GeV/c", "number of jets",
    50, 0.0, 100.0);
  */  

  // Jet PT
  plots->fJetPT = result->AddHist1D(
    "jet_pt", "Jet P_{T}",
    "jet P_{T}, GeV/c", "number of jets",
    50, 0.0, 100.0);    
  //plots->fJetPT[0]->SetLineColor(kRed);
  //plots->fJetPT[1]->SetLineColor(kBlue);
  plots->fJetPT->SetLineColor(kBlue);    

  // Jet Eta
  plots->fJetEta = result->AddHist1D(
    "jet_eta", "Jet Eta",
    "jet Eta", "number of jets",
    50, -5, 5);
  plots->fJetEta->SetLineColor(kBlue);   

  // Jet Number
  plots->fJetNo = result->AddHist1D(
    "jet_number", "Jet Number",
    "jet number", "number of jets",
    12, 0, 12);
  plots->fJetNo->SetLineColor(kBlue);

  // Bjet PT
  plots->fbJetPT = result->AddHist1D(
    "bjet_pt", "B-Jet P_{T}",
    "bjet P_{T}, GeV/c", "number of b-jets",
    50, 0.0, 100.0);   
  plots->fbJetPT->SetLineColor(kBlue);
  
  // Bjet Number
  plots->fbJetNo = result->AddHist1D(
    "bjet_number", "B-Jet Number",
    "bjet number", "number of b-jets",
    12, 0, 12);
  plots->fbJetNo->SetLineColor(kBlue);     
 
  /*
  // book 1 stack of 2 histograms

  stack = result->AddHistStack("jet_pt_all", "1st and 2nd jets P_{T}");
  stack->Add(plots->fJetPT[0]);
  stack->Add(plots->fJetPT[1]);

  // book legend for stack of 2 histograms

  legend = result->AddLegend(0.72, 0.86, 0.98, 0.98);
  legend->AddEntry(plots->fJetPT[0], "leading jet", "l");
  legend->AddEntry(plots->fJetPT[1], "second jet", "l");

  // attach legend to stack (legend will be printed over stack in .eps file)

  result->Attach(stack, legend);
  */

  // book more histograms

  // Electron PT
  plots->fElectronPT = result->AddHist1D(
    "electron_pt", "electron P_{T}",
    "electron P_{T}, GeV/c", "number of electrons",
    50, 0.0, 100.0);
  plots->fElectronPT->SetLineColor(kBlue);

  // Electron Eta
  plots->fElectronEta = result->AddHist1D(
    "electron_eta", "Electron Eta",
    "electron Eta", "number of jets",
    50, -5, 5);
  plots->fElectronEta->SetLineColor(kBlue);  

  // Electron Number
  plots->fElectronNo = result->AddHist1D(
    "electron_number", "Electron Number",
    "electron number", "number of electrons",
    6, 0, 6);
  plots->fElectronNo->SetLineColor(kBlue);   

  // MET
  plots->fMissingET = result->AddHist1D(
    "missing_et", "Missing E_{T}",
    "Missing E_{T}, GeV", "number of events",
    60, 0.0, 30.0);
  plots->fMissingET->SetLineColor(kBlue);


  // book general comment

  //comment = result->AddComment(0.64, 0.86, 0.98, 0.98);
  //comment->AddText("demonstration plot");
  //comment->AddText("produced by Example2.C");

  // attach comment to single histograms

  //result->Attach(plots->fJetPT[0], comment);
  //result->Attach(plots->fJetPT[1], comment);
  //result->Attach(plots->fElectronPT, comment);

  // show histogram statisics for MissingET
  plots->fMissingET->SetStats();
}

//------------------------------------------------------------------------------

void AnalyseEvents(ExRootTreeReader *treeReader, MyPlots *plots)
{
  TClonesArray *branchJet = treeReader->UseBranch("Jet");
  TClonesArray *branchElectron = treeReader->UseBranch("Electron");
  TClonesArray *branchMissingET = treeReader->UseBranch("MissingET");

  Long64_t allEntries = treeReader->GetEntries();

  cout << "** Chain contains " << allEntries << " events" << endl;

  Jet *jet;
  MissingET *met;
  Electron *electron;

  Long64_t entry;

  Int_t i;
  Long64_t nEvent = 0;

  // Loop over all events
  for(entry = 0; entry < allEntries; ++entry)
  {
    // Load selected branches with data from specified event
    treeReader->ReadEntry(entry);

    // Preselections at least 3 leptons and 2 jet with 1 b-tagged
    if (!(branchElectron->GetEntries() >= 3 || branchJet->GetEntriesFast() >=2 )) continue;
    int bJetNo = 0;
    for(i = 0; i < branchJet->GetEntriesFast(); ++i)
    {
      if(jet->BTag) bJetNo ++;      
    }
    //cout << "Number of b-jet: " << bJetNo << endl;
    if(!(bJetNo >= 1)) continue;
    nEvent ++;
    
    int JetNo = branchJet->GetEntries();
    //plots->fJetNo->Fill(JetNo);
    int Jetcounter = 0;
    //if(branchJet->GetEntries() >= 3){cout << "Number of Jets: " << branchJet->GetEntries() << endl;}
    // Loop over all jets in event

    for(i = 0; i < branchJet->GetEntriesFast(); ++i)
    {
      jet = (Jet*) branchJet->At(i);
      plots->fJetPT->Fill(jet->PT);    
      plots->fJetEta->Fill(jet->Eta);
      Jetcounter ++;

      // Loop over bjets
      int bJetcounter = 0;
      if(jet->BTag){
        bJetcounter ++;
        plots->fbJetPT->Fill(jet->PT);
      }
      plots->fbJetNo->Fill(bJetcounter);
    }
    //if (entry <= 10){cout << branchJet->GetEntries() << "=" << Jetcounter << endl;}
    //plots->fJetNo->Fill(Jetcounter);

    // Analyse missing ET
    if(branchMissingET->GetEntriesFast() > 0)
    {
      met = (MissingET*) branchMissingET->At(0);
      plots->fMissingET->Fill(met->MET);
    }

    // Loop over all electrons in event
    for(i = 0; i < branchElectron->GetEntriesFast(); ++i)
    {
      electron = (Electron*) branchElectron->At(i);
      plots->fElectronPT->Fill(electron->PT);
      plots->fElectronEta->Fill(electron->Eta);

    }
  }
  cout << "Total number of events wich pass the preselection: " << nEvent << endl;
}

//------------------------------------------------------------------------------

void PrintHistograms(ExRootResult *result, MyPlots *plots)
{
  result->Print("png");
}

//------------------------------------------------------------------------------

void plotter(const char *inputFile)
{
  gSystem->Load("libDelphes");

  TChain *chain = new TChain("Delphes");
  chain->Add(inputFile);

  ExRootTreeReader *treeReader = new ExRootTreeReader(chain);
  ExRootResult *result = new ExRootResult();

  MyPlots *plots = new MyPlots;

  BookHistograms(result, plots);

  AnalyseEvents(treeReader, plots);

  PrintHistograms(result, plots);

  result->Write("results.root");

  cout << "** Exiting..." << endl;

  delete plots;
  delete result;
  delete treeReader;
  delete chain;
}

//------------------------------------------------------------------------------
