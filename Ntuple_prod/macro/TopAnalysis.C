/*
created Jun 10 2013, T. Andeen
Based on example/Example2.C
*/

#include <iostream>
#include "TH1.h"
#include "TSystem.h"
#include "TMath.h"
#include "THStack.h"
#include "TLegend.h"
#include "TPaveText.h"
#include "TMinuit.h"
#include "TClonesArray.h"
#include "TLorentzVector.h"
#include "TObject.h"
#include "external/ExRootAnalysis/ExRootResult.h"
#include "external/ExRootAnalysis/ExRootTreeReader.h"
#include "classes/DelphesClasses.h"

bool m_debug=false; 
//------------------------------------------------------------------------------

struct MyPlots
{
  TH1 *fJetPT[2];
  TH1 *fMissingET;
  TH1 *fHiggsM;
  TH1 *fTopM;
  TH1 *fTtildeM;
  TH1 *fSelectedHiggsM;
  TH1 *fSelectedTopM;
  TH1 *fSelectedTtildeM;
  TH1 *fSelectedTbjM;
  TH1 *fTbjM;
  TH1 *fElectronPT;
};

//------------------------------------------------------------------------------
//Simple functions: 
float ConvertEtaToTheta(float eta){return 2.0*atan( exp(-1.0*eta) );};
float MinDeltaPhi(float phi1, float phi2) {
  float dphi = phi1 - phi2;
  while (dphi < -M_PI) dphi += 2*M_PI;
  while (dphi >  M_PI) dphi -= 2*M_PI;
  return dphi;
}
float DeltaR(float eta1, float phi1, float eta2, float phi2) {
  float dphi = MinDeltaPhi(phi1, phi2);
  float deta = eta1 - eta2;
  float dr = sqrt(pow(dphi,2) + pow(deta,2));
  return dr;
}

float DeltaR(TLorentzVector *tlv1, TLorentzVector *tlv2) {
  float phi1 = tlv1->Phi();
  float phi2 = tlv2->Phi();
  float eta1 = tlv1->Eta();
  float eta2 = tlv2->Eta();
  return DeltaR(eta1, phi1, eta2, phi2);
}


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

  plots->fJetPT[0] = result->AddHist1D(
    "jet_pt_0", "leading jet P_{T}",
    "jet P_{T}, GeV/c", "number of jets",
    50, 0.0, 100.0);

  plots->fJetPT[1] = result->AddHist1D(
    "jet_pt_1", "2nd leading jet P_{T}",
    "jet P_{T}, GeV/c", "number of jets",
    50, 0.0, 100.0);

  plots->fJetPT[0]->SetLineColor(kRed);
  plots->fJetPT[1]->SetLineColor(kBlue);

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

  // book more histograms

  plots->fElectronPT = result->AddHist1D(
    "electron_pt", "electron P_{T}",
    "electron P_{T}, GeV/c", "number of electrons",
    50, 0.0, 100.0);

  plots->fMissingET = result->AddHist1D(
    "missing_et", "Missing E_{T}",
    "Missing E_{T}, GeV", "number of events",
    60, 0.0, 30.0);

  plots->fHiggsM = result->AddHist1D(
    "higgs_M", "Higgs M",
    "Higgs Mass, GeV", "number of events",
    730, 0.0, 730.0);

  plots->fTopM = result->AddHist1D(
    "Top_M", "Top M",
    "Top Mass, GeV", "number of events",
    200, 100.0, 300.0);

  plots->fTtildeM = result->AddHist1D(
    "Ttilde_M", "Ttilde M",
    "Ttilde Mass, GeV", "number of events",
    400, 0.0, 4000.0);
  
  plots->fSelectedHiggsM = result->AddHist1D(
    "Selectedhiggs_M", "Higgs M",
    "Higgs Mass, GeV", "number of events",
    730, 0.0, 730.0);

  plots->fSelectedTopM = result->AddHist1D(
    "SelectedTop_M", "Top M",
    "Top Mass, GeV", "number of events",
    200, 100.0, 300.0);

  plots->fSelectedTtildeM = result->AddHist1D(
    "SelectedTtilde_M", "Ttilde M",
    "Ttilde Mass, GeV", "number of events",
    40, 0.0, 4000.0);

  plots->fSelectedTbjM = result->AddHist1D(
    "SelectedTbj_M", "Selected Tbj M",
    "Selected Tbj Mass, GeV", "number of events",
    400, 0.0, 4000.0);


  plots->fTbjM = result->AddHist1D(
    "Tbj_M", "Tbj M",
    "Tbj Mass, GeV", "number of events",
    400, 0.0, 4000.0);


  // book general comment

  comment = result->AddComment(0.64, 0.86, 0.98, 0.98);
  comment->AddText("validation plot");
  comment->AddText("produced by TTilde.C");

  // attach comment to single histograms

  result->Attach(plots->fJetPT[0], comment);
  result->Attach(plots->fJetPT[1], comment);
  result->Attach(plots->fElectronPT, comment);
  result->Attach(plots->fHiggsM, comment);
  result->Attach(plots->fTopM, comment);

  // show histogram statisics for MissingET
  plots->fMissingET->SetStats();
}

//_________________________________________________________________________________________________
void delta2_fcn(Int_t& npar, Double_t* grad, Double_t& f, Double_t* par, Int_t iflag){
    
  Double_t delta2 = 0;
  Double_t alpha = par[0];
  Double_t r = par[1];
  Double_t dphi = par[2];
  Double_t l_pt = par[3];
  Double_t l_m = par[4];
  Double_t n_px = par[5];
  Double_t n_py = par[6];
  r /= sqrt(l_pt * l_pt + l_m * l_m) - l_pt * cos(dphi + alpha);
  TLorentzVector *neut = new TLorentzVector(n_px, n_py, 0., 0.);
  neut->SetE(neut->P());
  
  TLorentzVector *neut_new = new TLorentzVector(r * neut->P() * cos(neut->Phi() + alpha), r * neut->P() * sin(neut->Phi() + alpha), 0., 0.);
  neut_new->SetE(neut_new->P());
  
  delta2 = pow((neut_new->Px() - neut->Px()), 2)  + pow((neut_new->Py() - neut->Py()), 2);
  r *= sqrt(l_pt * l_pt + l_m * l_m) - l_pt * cos(dphi + alpha);
  delete neut;
  delete neut_new;
  f = delta2;
}

//_________________________________________________________________________________________________
double fitAlpha(const TLorentzVector* L, const Double_t met, const Double_t metphi){
  if(m_debug>0) std::cout << "entering fitAlpha()" << std::endl;

  // initialize
  double m_mWpdg = 80.4 * 1000; //MeV
  Double_t pxNu = met * cos(metphi);
  Double_t pyNu = met * sin(metphi);
  Double_t ptNu = met;

  TMinuit *fit = new TMinuit(7);
  fit->SetFCN(delta2_fcn);
  int ierr = 0;
  double arglist[1] = {-1};
  fit->mnexcm("SET PRIN",arglist,1,ierr);
  // Initialise the parameters
  std::string par_name[7] = {"alpha", "r", "dphi", "l_pt", "l_m", "n_px", "n_py"};
  Double_t par_ival[7] = {0., (m_mWpdg * m_mWpdg - L->M() * L->M()) / (2 * ptNu), metphi - L->Phi(), L->Pt(), L->M(), pxNu, pyNu};
  Double_t par_step[7] = {0.1, 0., 0., 0., 0., 0., 0.};
  Double_t par_min[7] = {-3.15, 0., -3.15, 0., 0., -10000., -10000.};
  Double_t par_max[7] = {3.15, 1., 3.15, 10000., 80., 10000., 10000.};
  for (Int_t i = 0; i < 7; i++){
    fit->DefineParameter(i,par_name[i].c_str(),par_ival[i],par_step[i],par_min[i],par_max[i]);
    if (i != 0){
      fit->FixParameter(i);
    }
  }
  fit->SetPrintLevel(-1);
  fit->Migrad();
  Double_t a, e_a;
  Int_t ret = fit->GetParameter(0, a, e_a);
  delete fit;
  if (ret > 0){
    return a;
  }
  else {
    std::cout << "Error in fit of alpha for met correction" << std::endl;
    return 0.;
  }
  
}

//_________________________________________________________________________________________________
std::vector<TLorentzVector*> candidatesFromWMass_Rotation(const TLorentzVector* L, const Double_t met, const Double_t metphi, const bool useSmallestPz){

  if(m_debug>0) std::cout << "entering candidatesFromWMassRotation()" << std::endl;
  
  // initialize
  Double_t m_mWpdg = 80.4 * 1000; //MeV
  Double_t pxNu = met * cos(metphi);
  Double_t pyNu = met * sin(metphi);
  
  Double_t pzNu = -1000000;
  Double_t ptNu = met;
  Double_t eNu;
  
  std::vector<TLorentzVector*> NC;
    
  Double_t c1 = m_mWpdg * m_mWpdg - L->M() * L->M() + 2 * (L->Px() * pxNu + L->Py() * pyNu);
  Double_t b1 = 2 * L->Pz();
    
  Double_t A = 4 * pow(L->E(), 2) - b1 * b1;
  Double_t B = -2 * c1 * b1;
  Double_t C = 4 * pow(L->E(), 2) * ptNu * ptNu - c1 * c1;
  Double_t discr = B*B - 4*A*C;
  Double_t r = 1;
  
  Double_t sol1, sol2;
  if (discr > 0){
    sol1 = (-B + sqrt(discr)) / (2*A);
    sol2 = (-B - sqrt(discr)) / (2*A);
  }
  else { 
    Double_t alpha = fitAlpha(L, met, metphi);
    //cout<<"alpha "<<alpha<<" L "<<L<<endl;
    Double_t dphi = metphi - L->Phi();
    r = ( pow(m_mWpdg,2) - pow(L->M(),2) ) / (2 * ptNu * (sqrt(pow(L->Pt(),2) + pow(L->M(),2)) - L->Pt() * cos(dphi + alpha)));
    
    Double_t old_p = ptNu;
    Double_t old_phi = metphi;
    pxNu = r * old_p * cos(old_phi + alpha);
    pyNu = r * old_p * sin(old_phi + alpha);
    ptNu = sqrt (pxNu*pxNu + pyNu*pyNu);
    
    c1 = m_mWpdg * m_mWpdg - pow(L->M(),2) + 2 * (L->Px() * pxNu + L->Py() * pyNu);
    B = -2 * c1 * b1;
    C = 4 * pow(L->E(),2) * ptNu * ptNu - c1 * c1;
    discr = B*B - 4*A*C;
    
    sol1 = -B / (2*A);
    sol2 = -B / (2*A);
  }
  
  if (useSmallestPz){
    
    pzNu = (fabs(sol1) > fabs(sol2)) ? sol2 : sol1;
    
    eNu  = sqrt(pxNu*pxNu + pyNu*pyNu + pzNu*pzNu);
    TLorentzVector *nu1 = new TLorentzVector(pxNu,pyNu,pzNu,eNu);
    NC.push_back(nu1);
    
  }else{
    
    pzNu = sol1;
    eNu  = sqrt(pxNu*pxNu + pyNu*pyNu + pzNu*pzNu);
    TLorentzVector *nu1 = new TLorentzVector(pxNu,pyNu,pzNu,eNu);
    pzNu = sol2;
    eNu = sqrt(pxNu*pxNu + pyNu*pyNu + pzNu*pzNu);
    TLorentzVector *nu2 = new TLorentzVector(pxNu,pyNu,pzNu,eNu);
    NC.push_back(nu1);
    NC.push_back(nu2);
    
  }
  
  if(m_debug>0) std::cout << "quitting NeutrinoBuilder::candidatesFromWMassRotation() : " << NC.size() << std::endl;
  return NC;
}

//------------------------------------------------------------------------------

void AnalyseEvents(ExRootTreeReader *treeReader, MyPlots *plots)
{
  TClonesArray *branchJet = treeReader->UseBranch("Jet");
  TClonesArray *branchElectron = treeReader->UseBranch("Electron");
  TClonesArray *branchMuon = treeReader->UseBranch("Muon");
  TClonesArray *branchMissingET = treeReader->UseBranch("MissingET");
  
  Long64_t allEntries = treeReader->GetEntries();

  cout << "** Chain contains " << allEntries << " events" << endl;

  std::vector<Jet*> jets;
  std::vector<Electron*> electrons;
  std::vector<Muon*> muons;

  MissingET *met;
  Electron *electron;
  Muon *muon;
  Jet *ajet;
  Long64_t entry;

  Int_t i;

  // Loop over all events
  for(entry = 0; entry < allEntries; ++entry)
  {
    // Load selected branches with data from specified event
    treeReader->ReadEntry(entry);

    jets.clear();
    electrons.clear();
    muons.clear();

    /*
    // Analyse three leading jets
    if(branchJet->GetEntriesFast() >= 3)
    {
      jet[0] = (Jet*) branchJet->At(0);
      jet[1] = (Jet*) branchJet->At(1);

      plots->fJetPT[0]->Fill(jet[0]->Mass);
      plots->fJetPT[1]->Fill(jet[1]->Mass);

    }
    */

    // Loop over all jets in event and select >pt 30 and |eta|<5
    // and count btags. 

    int iselected=0;
    int btags=0;

    for(i = 0; i < branchJet->GetEntriesFast(); ++i) {
      //pt ordered jets. 
      //cout<<"i "<<i<<endl;
      ajet = (Jet*) branchJet->At(i);
      
      if ((ajet->PT >= 30.0) && (fabs(ajet->Eta) <= 5.0)){
	//cout<<"ajet pt "<<ajet->PT<<endl;
	jets.push_back((Jet*) branchJet->At(i));
	iselected++;
	if (ajet->BTag==1){
	  btags++;
	}
	//cout<<"iselected "<<iselected<<endl;
      }
    }

    // Loop over all electrons in event
    for(i = 0; i < branchElectron->GetEntriesFast(); ++i) {
      electron = (Electron*) branchElectron->At(i);
      plots->fElectronPT->Fill(electron->PT);
      if( (electron->PT>=30.0) && (fabs(electron->Eta)<2.5) ){
	electrons.push_back( (Electron*) branchElectron->At(i));
      }
    }
    
    // Loop over all muons in event
    for(i = 0; i < branchMuon->GetEntriesFast(); ++i) {
      muon = (Muon*) branchMuon->At(i);
      //plots->fMuonPT->Fill(muon->PT);      
      if( (muon->PT>=30.0) && (fabs(muon->Eta)<2.5) ){
	muons.push_back( (Muon*) branchMuon->At(i));
      }
    }
    
    // Get missing ET
    double theMET = 0.0; 
    double theMETPhi=0.0;
    if(branchMissingET->GetEntriesFast() > 0)
    {
      met = (MissingET*) branchMissingET->At(0);
      plots->fMissingET->Fill(met->MET);
      theMET = met->MET;
      theMETPhi = met->Phi;
    }

    //cout<<"found "<<jets.size()<<" jets "<< electrons.size() <<" electrons "<< muons.size() <<" muons "<<endl;
    //"met" selection:
    if (theMET<30.0) { continue; }
    
    //jet selection:
    if (jets.size()<5) { continue; }
    if (btags<2) { continue; }
    
    //lepton selection:
    if (electrons.size()<1 && muons.size()<1) { continue; }
    if (electrons.size()>=1 && muons.size()>=1) { continue; }
    TLorentzVector theLepton;
    if (electrons.size()>0) {
      double theta = 2 * TMath::ATan( TMath::Exp(-electrons.at(0)->Eta) );
      double P = electrons.at(0)->PT * TMath::CosH(electrons.at(0)->Eta);
      double pz = P*TMath::Cos(theta);
      
      if(m_debug)cout<<"elec pt "<<electrons.at(0)->PT<<", eta "<<electrons.at(0)->Eta<<", phi "<<electrons.at(0)->Phi<<" theta "<<theta<<" pz "<<pz<<endl;
      theLepton.SetPtEtaPhiM(electrons.at(0)->PT, electrons.at(0)->Eta, electrons.at(0)->Phi, 0.5/1000);
    } else {     
      if(m_debug)cout<<"muons pt "<<muons.at(0)->PT<<", eta "<<muons.at(0)->Eta<<", phi "<<muons.at(0)->Phi<<endl;
      theLepton.SetPtEtaPhiM(muons.at(0)->PT, muons.at(0)->Eta, muons.at(0)->Phi, 105.7/1000);

    }
    if(m_debug>0) cout<<"lep pt "<<theLepton.Pt()<<", eta "<<theLepton.Eta()<<", phi "<<theLepton.Phi()<<" mass "<<theLepton.M()<<" energy "<<theLepton.E()<<endl;

    //left out isolation. 
    if(m_debug>0) cout<<"event selected, now do tagging "<<endl;
    if(m_debug>0) cout<<"selected "<<jets.size()<<" jets "<< electrons.size() <<" electrons "<< muons.size() <<" muons "<<endl;

    //now tag the jets:
    
    //tag light jet: 
    float hiEta=0.;
    int lightjetIndex = -1;
    for (int ij =0; ij<jets.size(); ij++){
      if ( fabs(jets.at(ij)->Eta) > hiEta ) {
	hiEta = fabs(jets.at(ij)->Eta);
	lightjetIndex = ij;
      }
    }
    TLorentzVector lightjet;
    lightjet.SetPtEtaPhiM(jets.at(lightjetIndex)->PT, jets.at(lightjetIndex)->Eta, jets.at(lightjetIndex)->Phi,  0.0);

    if(m_debug>0) cout<<"hi eta jet "<<hiEta<<endl;
    
    int topbIndex = -1;

    //Mw constraint to get nu pz 

    TLorentzVector theLeptonMeV;
    theLeptonMeV.SetPxPyPzE(theLepton.Px()*1000, theLepton.Py()*1000, theLepton.Pz()*1000, theLepton.E()*1000);
    
    if(m_debug)cout<<"build neutrino, lep mass "<<theLeptonMeV.M()<<endl;

    std::vector<TLorentzVector*> neutrino = candidatesFromWMass_Rotation(&theLeptonMeV, 1000*theMET, theMETPhi, true);
    TLorentzVector tmp;
    std::vector<TLorentzVector*> leptonicW;
    TLorentzVector leptonicTop;
	
    for(int n=0; n<neutrino.size(); n++) {
      if(m_debug)cout<<"the nu "<<neutrino.at(n)->Px()<<" the nu pt "<<neutrino.at(n)->Pt() <<" met "<< theMET<<endl;

      if(m_debug)cout<<"build leptonic Top nu "<<n<<endl;
      neutrino.at(n)->SetPxPyPzE(neutrino.at(n)->Px()/1000,neutrino.at(n)->Py()/1000 , neutrino.at(n)->Pz()/1000  , neutrino.at(n)->E()/1000 );
      
      if(m_debug)cout<<"build leptonic Top nu "<<n<<endl;

      tmp=*neutrino.at(n)+theLepton;
      
      if(m_debug)cout<<"build leptonic Top W "<<n<<" mass "<<tmp.M()<< endl;
      
      leptonicW.push_back( new TLorentzVector( tmp )  );
      if(m_debug)cout<<"build leptonic Top all "<<n<<endl;

      //find best jet to make the top mass closest to 175

      float deltaM=1000000.;

      for (int ij =0; ij<jets.size(); ij++){
	if (ij == lightjetIndex) { continue; }
	TLorentzVector tmp_jet;
	tmp_jet.SetPtEtaPhiM(jets.at(ij)->PT, jets.at(ij)->Eta, jets.at(ij)->Phi, 0.0);
	TLorentzVector tmp_top;
	tmp_top =  *neutrino.at(n) + theLepton + tmp_jet;
	//cout<<" test top mass " <<tmp_top.M() <<endl;
	if ( fabs(174.0 - tmp_top.M()) < deltaM ){
	  deltaM =  fabs(174.0 - tmp_top.M());
	  topbIndex=ij;
	  leptonicTop = tmp_top;
	}
      }

      if(m_debug)cout<<"finished building leptonic Top "<<n<<endl;
    } //end solving for nu, W, top, found top jet. 
    
    if(m_debug>0) cout<<"best top mass "<< leptonicTop.M() <<endl;
    plots->fTopM->Fill(leptonicTop.M());
	

    //tag Tjb b jet: 
    float nextHiEta=0.;
    int bjetIndex = -1;
    for (int ij =0; ij<jets.size(); ij++){
      if ( ij == topbIndex || ij == lightjetIndex) { continue; }
      if ( fabs(jets.at(ij)->Eta) > nextHiEta ) {
	nextHiEta = fabs(jets.at(ij)->Eta);
	bjetIndex = ij;
      }
    }
    TLorentzVector bjet;
    bjet.SetPtEtaPhiM(jets.at(bjetIndex)->PT, jets.at(bjetIndex)->Eta, jets.at(bjetIndex)->Phi, 0.0);

    //the 2 highest pt jets are the higgs
	
    TLorentzVector hbjet1;
    int bH1jetIndex = -1;
    for (int ij =0; ij<jets.size(); ij++){
      if ( ij == topbIndex || ij == lightjetIndex || ij == bjetIndex) { continue; }
      bH1jetIndex=ij;
      hbjet1.SetPtEtaPhiM(jets.at(ij)->PT, jets.at(ij)->Eta, jets.at(ij)->Phi, 0.0);
      break;
    }

    TLorentzVector hbjet2;
    int bH2jetIndex = -1;
    for (int ij =0; ij<jets.size(); ij++){
      if ( ij == topbIndex || ij == lightjetIndex || ij == bjetIndex || ij == bH1jetIndex) { continue; }
      bH2jetIndex=ij;
      hbjet2.SetPtEtaPhiM(jets.at(ij)->PT, jets.at(ij)->Eta, jets.at(ij)->Phi,   0.0);
      break;
    }

    TLorentzVector higgs = hbjet1+hbjet2;
    plots->fHiggsM->Fill(higgs.M());
    TLorentzVector ttilde = higgs+leptonicTop;
    plots->fTtildeM->Fill(ttilde.M());
    TLorentzVector tbj = ttilde+bjet+lightjet;
    plots->fTbjM->Fill(ttilde.M());
    
    //Now selections on the reconstructed objects: 
    float jbDeltaR = DeltaR(jets.at(bjetIndex)->Eta, jets.at(bjetIndex)->Phi
			    , jets.at(lightjetIndex)->Eta, jets.at(lightjetIndex)->Phi);
    float bhDeltaR = DeltaR(jets.at(bjetIndex)->Eta, jets.at(bjetIndex)->Phi
			    , higgs.Eta(), higgs.Phi());
    float higgsbbDeltaR = DeltaR(jets.at(bH1jetIndex)->Eta, jets.at(bH1jetIndex)->Phi
				 , jets.at(bH2jetIndex)->Eta, jets.at(bH2jetIndex)->Phi);
    if(m_debug>0) cout<<"jbDeltaR "<<jbDeltaR << " bhDeltaR "<< bhDeltaR<<" higgsbbDeltaR "<<higgsbbDeltaR<<endl;

    //M_ttilde dependent: // hi mass selection, could be tighter? 
    bool Mt1000 = true;
    bool Mt1500 = false;
    
    if (Mt1000){
      if (leptonicTop.Pt() < 230.0 ) { continue;}
      if (higgs.Pt() < 230.0 ) { continue;}
      if (jets.at(0)->PT < 250.0) {continue;}
      if (tbj.M() < 1700.0 ) { continue;}
    } else if (Mt1500) {
      if (leptonicTop.Pt() < 270.0 ) { continue;}
      if (higgs.Pt() < 270.0 ) { continue;}
      if (jets.at(0)->PT < 320.0) {continue;}
      if (tbj.M() < 2100.0 ) { continue;}
    }
    
    //constant:
    if (lightjet.E() < 230.0) { continue; }
    if (fabs( lightjet.Eta()) < 2.1) { continue; }
    if (fabs( bjet.Eta()) < 0.9 ) { continue; }
    if (jbDeltaR<2) { continue; }
    if (bhDeltaR<1.8) { continue; }
    //add higgs constitutent jet mass cut

    plots->fSelectedTopM->Fill(leptonicTop.M());
    plots->fSelectedHiggsM->Fill(higgs.M());
    plots->fSelectedTtildeM->Fill(ttilde.M());
    plots->fSelectedTbjM->Fill(tbj.M());

  } //end event loop
}

//------------------------------------------------------------------------------

void PrintHistograms(ExRootResult *result, MyPlots *plots)
{
  result->Print("png");
}

//------------------------------------------------------------------------------

//void Ttilde(const char *inputFile)
void Ttilde(TChain *chain)
{
  gSystem->Load("libDelphes");

  //TChain *chain = new TChain("Delphes");
  //chain->Add(inputFile);

  ExRootTreeReader *treeReader = new ExRootTreeReader(chain);
  ExRootResult *result = new ExRootResult();

  MyPlots *plots = new MyPlots;

  BookHistograms(result, plots);

  AnalyseEvents(treeReader, plots);

  PrintHistograms(result, plots);

  result->Write("results.root");

  std::cout << "** Exiting..." << endl;

  delete plots;
  delete result;
  delete treeReader;
  //delete chain;
}

