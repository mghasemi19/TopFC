#include <iostream>

// Fill tree with gaus random numbers
void gaus_tree(){
   TTree *tree = new TTree("tree", "Test tree");
   double num;
   tree->Branch("number", &num, "num/D");
   TH1F *h = new TH1F("h", "h", 100, -5, 5); 
   h->FillRandom("gaus", 1000);
   for (int i=0; i<h->GetEntries(); i++){
     num = 0; num = h->GetRandom();
     tree->Fill();
   }
   tree->Draw("number");
}

// Loop through a tree and do simple comparison between bkg and sig branches
void loop_tree(){
  TFile *infile = new TFile("/Users/mghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/mlpHiggs.root");
  TTree *bkg_tree = (TTree*) infile->Get("bg_filtered");  
  TTree *sig_tree = (TTree*) infile->Get("sig_filtered");
  bkg_tree->Print("Toponly");

  float pt_bkg, pt_sig;
  bkg_tree->SetBranchAddress("ptsumf", &pt_bkg);
  sig_tree->SetBranchAddress("ptsumf", &pt_sig);
  
  std::cout << "Total number of events:" << bkg_tree->GetEntries() << std::endl;
  for (int n=0; n<bkg_tree->GetEntries();n++){    
    bkg_tree->GetEntry(n);
    sig_tree->GetEntry(n);
    if (pt_bkg > pt_sig) std::cout << "Bkg_pT:" << pt_bkg << std::endl;
    if (pt_bkg == pt_sig) std::cout << "Bkg_pT = Sig_pT:" << pt_bkg << std::endl;
    if (pt_bkg < pt_sig) std::cout << "Sig_pT:" << pt_sig << std::endl;
  }
}

// Advance way to loop over trees via iterators
void loop_Iter(){
   //TFile *infile = new TFile("/Users/meisamghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/mlpHiggs.root");
   TFile *infile = new TFile("/Users/mghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/mlpHiggs.root");
   infile->GetListOfKeys()->Print();

   TIter next(infile->GetListOfKeys());
   TKey *key;

   TObjArray obj(0);
   while ((key=(TKey*)next())) {
       TH1F *htest = new TH1F("htest", "hist", 50, 0, 0.5);
       printf("key: %s points to an object of class: %s\n", key->GetName(), key->GetClassName());
       if (key->GetName() == "Tot_tree") continue;
       //if (key->GetClassName() != "TTree") continue;
       TTree *tree = (TTree*)infile->Get(key->GetName());
       //tree->Draw("ptsumf>>htest");
       //key->Print();
       tree->Draw("ptsumf>>htest", "", "goff"); 
       std::cout << htest->GetMean() << std::endl;
       htest->SetTitle(key->GetName());
       htest->SetName(key->GetName());

       obj.Add(htest);
       htest->Delete();
   }
   TFile *ofile = new TFile("wow.root", "RECREATE");
   obj.Write();
   ofile->Close();
}

// Copy trees with selections
void copy_tree(){
  TFile *infile = new TFile("/Users/mghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/mlpHiggs.root");
  TTree *bkg_tree = (TTree*) infile->Get("bg_filtered");
  TTree *sig_tree = (TTree*) infile->Get("sig_filtered");
  bkg_tree->Print("Toponly");
 
  TCanvas *c = new TCanvas("c", "c", 600, 300);
  c->Divide(2,1);
  c->cd(1); bkg_tree->Draw("ptsumf");
  TFile *f2 = new TFile("/Users/mghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/ForTest.root","recreate");
  //f2->cd();
  TTree *sub_bkg = bkg_tree->CopyTree("ptsumf > 0.1");  
  TTree *sub_sig = sig_tree->CopyTree("ptsumf > 0.1");  
  c->Update();
  c->cd(2); sub_bkg->Draw("ptsumf");

  sub_bkg->Write();
  sub_sig->Write();

  f2->Close();
}

// Add tree to a file
void add_tree(){
  TFile *infile = new TFile("/Users/mghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/mlpHiggs_test.root", "update");
  TTree *bkg_tree = (TTree*) infile->Get("bg_filtered");
  TTree *sig_tree = (TTree*) infile->Get("sig_filtered");   
  TTree *tot_tree = new TTree("Tot_tree", "Tree");
  
  float bkg_pt, sig_pt, tot_pt;
  bkg_tree->SetBranchAddress("ptsumf", &bkg_pt);
  sig_tree->SetBranchAddress("ptsumf", &sig_pt);
  tot_tree->Branch("tot_ptsumf", &tot_pt);

  for (int n=0; n<bkg_tree->GetEntries();n++){
    bkg_tree->GetEntry(n);
    sig_tree->GetEntry(n);  
    tot_pt = bkg_pt + sig_pt;
    tot_tree->Fill();
  }
  bkg_tree->Scan(0); 
  sig_tree->Scan(0); 
  tot_tree->Scan(0); 
  tot_tree->Write();
  infile->Close();
}

// Merge with chain class
void merge_tree(){
  TChain chain("bg_filtered");
  //chain.Add("../mlp/ForTest.root");
  chain.Add("../mlp/mlpHiggs.root");
  std::cout << chain.GetEntries() << std::endl;
  chain.Add("../mlp/ForTest.root");
  std::cout << chain.GetEntries() << std::endl;

  //chain.Draw("ptsumf");
  //std::cout << chain.GetEntries();
  //chain.Scan(1350);
  TFile *ofile = new TFile("chain.root", "RECREATE");
  chain.SetName("twobg_filter");
  chain.Write();
  ofile->Close();
}

// Merge with MergeTrees class
void Merge_Tree(){
  TFile *infile = new TFile("/Users/mghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/mlpHiggs.root");    
  TTree *bkg_tree = (TTree*)infile->Get("bg_filtered"); bkg_tree->Print(); 
  std::cout << bkg_tree->GetEntries() << std::endl;
  TTree *sig_tree = (TTree*)infile->Get("sig_filtered"); sig_tree->Print();
  std::cout << sig_tree->GetEntries() << std::endl;
  TFile *ofile = new TFile("/Users/mghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/total.root", "RECREATE");
  TList *list = new TList;
  list->Add(bkg_tree);
  list->Add(sig_tree);
  TTree *new_tree = TTree::MergeTrees(list);
  new_tree->SetName("tot_filtered"); new_tree->Print();
  std::cout << new_tree->GetEntries() << std::endl;
  std::cout << new_tree->GetDirectory()->GetName() << std::endl;

  new_tree->Write();
  infile->Close();
  ofile->Close();
}

// Add a branch to tree
void update_tree(){
  TFile *infile = new TFile("/Users/mghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/mlpHiggs.root", "update");
  TTree *bkg_tree = (TTree*) infile->Get("bg_filtered");
  float test, pt, m;
  TBranch *br = bkg_tree->Branch("test", &test, "test/F");
  //bkg_tree->Branch("test", &test, "test/F");
  bkg_tree->SetBranchAddress("msumf", &m);
  bkg_tree->SetBranchAddress("ptsumf", &pt);
  for (int i=0; i<bkg_tree->GetEntries(); i++){
    bkg_tree->GetEntry(i);
    test = pt+m;
    br->Fill();
    //bkg_tree->Fill();
  }
  bkg_tree->Print();
  bkg_tree->Write();
  //infile->Write("", TObject.kOverwrite);
  delete infile;
}
 
// Simply remove a tree from a file
void removeTree(){

  std::string file_name="/Users/mghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/mlpHiggs.root";
  TFile *file=new TFile((file_name).c_str(),"update");
  //std::string object_to_remove="sig_filtered;4";
  std::string object_to_remove2="bg_filtered;2";
  //the object can be a tree, a histogram, etc, in this case "test1" is a TTree
  //notice the ";1" which means cycle 1; to remove all cycles do ";*"
  //if your object is not at the top directory, but in a directory in the .root file, called foo
  // you do first
  //file->cd("foo");
  //then continue with the Delete command which is only applied to the current gDirectory
  //gDirectory->Delete(object_to_remove.c_str());
  gDirectory->Delete(object_to_remove2.c_str());

  file->Close();
}

// Simply remove a branch in tree
void remove_branch(){
   TFile f("/Users/meisamghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/mlpHiggs.root","update");
   TTree *T = (TTree*)f.Get("sig_filtered;1");
   TBranch *b = T->GetBranch("test");
   T->GetListOfBranches()->Remove(b);
   T->Write();
   f.Close();

   /*
   TTree *T = (TTree*)f.Get("CollectionTree");
   TBranch* b= T->GetBranch("StreamESD_ref");
   T->GetListOfBranches()->Remove(b);
   TLeaf* l= T->GetLeaf("StreamESD_ref");
   T->GetListOfLeaves()->Remove(l);
   T->Write();
   */
}

// turn of some of the branches
void turnoof_branch(){
   //TString dir = "$ROOTSYS/test/Event.root";
   //gSystem->ExpandPathName(dir);
   //const auto filename = gSystem->AccessPathName(dir) ? "./Event.root" : "$ROOTSYS/test/Event.root";

   TString filename = "./tree1.root";
   TFile oldfile(filename);
   TTree *oldtree;
   oldfile.GetObject("t1", oldtree);

   // Deactivate all branches
   oldtree->SetBranchStatus("*", 0);

   // Activate only four of them
   //for (auto activeBranchName : {"event", "fNtrack", "fNseg", "fH"})
   for (auto activeBranchName : {"pz", "py", "px"})
      oldtree->SetBranchStatus(activeBranchName, 1);

   // Create a new file + a clone of old tree in new file
   TFile newfile("small.root", "recreate");
   auto newtree = oldtree->CloneTree();

   newtree->Print();
   newfile.Write();
}

// Better way to merge Trees
void mergeTree_adv() {
  TFile *infile = new TFile("/Users/meisamghasemi/Desktop/Code-factory/Root/root-6.18.04/tutorials/mlp/mlpHiggs.root");
  TTree *bkg_tree = (TTree*)infile->Get("bg_filtered"); bkg_tree->Print();
  std::cout << bkg_tree->GetEntries() << std::endl;
  TTree *sig_tree = (TTree*)infile->Get("sig_filtered"); sig_tree->Print();

   //TFile *f = new TFile("treeparent.root", "update");
   //TTree *T  = (TTree*)f->Get("T");
   //TFile *ff = new TFile("treefriend.root");
   //TTree *TF = (TTree*)ff->Get("TF");
   TList* treeList = new TList;
   treeList->Add(bkg_tree); treeList->Add(sig_tree);
   TTree* outTree = TTree::MergeTrees(treeList);
   outTree->SetName("Test");
   outTree->Print();
   //f->cd();
   //outTree->Write(0, TObject::kOverwrite);
   //delete f;
}

void tree_basic(){
   //gaus_tree();
   //loop_tree();
   //add_tree();
   //copy_tree();
   //merge_tree();
   //update_tree();
   removeTree();
   //loop_Iter();
   //Merge_Tree();
   //remove_branch();
}
   
