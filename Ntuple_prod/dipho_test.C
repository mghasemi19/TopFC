#include <iostream>
#include <TClonesArray.h>
#include <TH1.h>
#include <TTree.h>
//#include </home/zwang/Downloads/MG5_aMC_v2_4_0/ExRootAnalysis/ExRootAnalysis/ExRootTreeReader.h>

using namespace std;

void dipho_test(){
  gSystem->Load("/home/zwang/Downloads/MG5_aMC_v2_4_0/Delphes/libDelphes");
//  gSystem->Load("/home/Downloads/MG5_aMC_v2_4_0/ExRootAnalysis/libExRootAnalysis");

  TChain chain("Delphes");
  chain.Add("tag_1_delphes_events.root");
 // chain.Add("/storage/aaaaa/bkttbar/run_06/tag_1_delphes_events.root");
  
//  chain.Print();

  ExRootTreeReader *treeReader = new ExRootTreeReader(&chain);
  Long64_t numberOfEntries = treeReader->GetEntries();

//  TClonesArray *branchParticle = treeReader->UseBranch("Particle");
  TClonesArray *branchElectron = treeReader->UseBranch("Electron");
  TClonesArray *branchMuon = treeReader->UseBranch("Muon");
  TClonesArray *branchJet = treeReader->UseBranch("Jet");
  TClonesArray *branchMET = treeReader->UseBranch("MissingET");
  TClonesArray *branchPhoton = treeReader->UseBranch("Photon");

  //new tree file
  double JetM=0;
  double JetPt=0;
  double photonM=0;
  double photonPt=0;
  double MET=0;
  double mas=0;
  double mH=0;
  double lepM=0;
  double lepPt=0;
/*
  TFile *newfile = new TFile("sig_lja_1.root", "recreate");
  TTree *tree = new TTree("T","Delphes");

  tree->Branch("diJetPt",&JetPt);
  tree->Branch("diJetM",&JetM);
  tree->Branch("diPhoPt",&photonPt);
  tree->Branch("diPhoM",&photonM);
  tree->Branch("MissingET",&MET);
  tree->Branch("dilepM",&lepM);
*/
  TCanvas * canvas1 = new TCanvas("canvas1");
  TH1 *histDiPhotMass = new TH1F("DiPhotMass", "M_{inv}(a_{1}, a_{2})", 100, 0.0, 300.0); 

 
 //Loop over all events
 for(Int_t entry = 0; entry < numberOfEntries; entry++){
   //Load selected branches with data from specified event
   treeReader->ReadEntry(entry);
   printf("process%d\n",entry);
   Electron *elec1;
   Muon *mu1;
   Jet *jet1 *jet2 *jet0;
   MissingET *MET1;
   Photon *pho1 *pho2;

   TLorentzVector Jet1P4,Jet2P4,pho1P4,pho2P4,lepP4,lep1P4,lep2P4;

   int jet=0;
   int pho=0;
   int lep=0;
//Pre-selection

    //At least 2 jets

  for(int a=0; a < branchPhoton->GetEntries();a++){
    pho1= (Photon *) branchPhoton->At(a);
    if(pho1->PT<15||fabs(pho1->Eta)>2.5) continue;
    pho++;
  }

  if(pho<2) continue;


// Find first two photons with largest PT
   int c=0;
   for(int i=0; i < branchPhoton->GetEntries(); i++){
    pho1= (Photon *) branchPhoton->At(i);
    if(pho1->PT<15||fabs(pho1->Eta)>2.5) continue;
    if(c==0) pho1P4=pho1->P4();
    if(c==1) pho2P4=pho1->P4();
    c++;
   }
   
     TLorentzVector phoP4 = pho1P4+pho2P4;
     Double_t diPhoPtVal = sqrt(phoP4.Px()*phoP4.Px()+phoP4.Py()*phoP4.Py());

     photonPt=diPhoPtVal;
     photonM=phoP4.M();

     histDiPhotMass->Fill(photonM);

  //write a new tree~~~~
//  tree->Fill();  

}

    canvas1->cd();
    histDiPhotMass->Draw();
//  tree->Write();
//  newfile->Close();
}


