 #include <iostream>
 #include <math.h>
 #define PI 3.1415927

 void b_dR(const char *inputFile){

     //remember to change the lib directory of your Delphes
     gSystem->Load("/home/zwang/Downloads/MG5_aMC_v2_4_0/Delphes/libDelphes");
	   
     TChain chain("Delphes");
     chain.Add(inputFile);
     chain.Print();
		  
     ExRootTreeReader *treeReader = new ExRootTreeReader(&chain);
     Long64_t numberOfEntries = treeReader->GetEntries();
		     
     TClonesArray *branchElectron = treeReader->UseBranch("Electron");
     TClonesArray *branchMuon = treeReader->UseBranch("Muon");
     TClonesArray *branchJet = treeReader->UseBranch("Jet");
     TClonesArray *branchParticle = treeReader->UseBranch("Particle");
			   
      TH1 *dR = new TH1F("dR","dR",500,0,5);
      Int_t k2=0;   //number of re-constructed Jets
      Int_t k3=0;   //number of parton bottoms
      for(Int_t entry = 0; entry < numberOfEntries; entry++){
			      
        treeReader->ReadEntry(entry);
			      
	Jet *Jet0,*Jet1,*Jet2;
	GenParticle *par,*par1;

//the number of  bottoms k1
        Int_t k1=0;
        Int_t a1=branchJet->GetEntries();
        for(Int_t i=0;i<a1;i++){
            Jet0=(Jet *) branchJet->At(i);
            if(Jet0->BTag==1&&Jet0->PT>40) {k1++;}
             }
    
   
//Count parton bottom k4
        Int_t k4=0; 
	for( Int_t i=0; i<branchParticle->GetEntries() ; i++){
	    par = (GenParticle *) branchParticle->At(i);
	    if ((par->PID ==-5||par->PID==5)&&par->Status==3&&par->PT>40) {k3++;k4++;}
       }
       
       if (k4==0) continue;
//       if (k1==0) continue;

       for(Int_t i=0;i<branchParticle->GetEntries();i++){

         //set par1 to be the parton level bottom
         par1=(GenParticle*) branchParticle->At(i);
	 if (!((par1->PID ==-5||par1->PID==5)&&par1->Status==3&&par1->PT>40)) continue;

	 double deltaR;
	 double minR=10;
	 Int_t b=-1; //id of closest jet

	 for(Int_t j=0;j<branchJet->GetEntries();j++){
           //set Jet1 to be the reco level bottom
	   Jet1 = (Jet *) branchJet->At(j);
	   if(!(Jet1->PT>40&&Jet1->BTag==1)) continue;

           double deltaPhi;
	   if(fabs(Jet1->Phi-par1->Phi)<=PI) deltaPhi=Jet1->Phi-par1->Phi;
	   else if(Jet1->Phi-par1->Phi>PI) deltaPhi=Jet1->Phi-par1->Phi-2*PI;
	   else deltaPhi=Jet1->Phi-par1->Phi+2*PI;

           deltaR=sqrt(deltaPhi*deltaPhi+(Jet1->Eta-par1->Eta)*(Jet1->Eta-par1->Eta));
           //find the closed reco bottom to the parton level bottom
	   if(deltaR<minR) { minR=deltaR;b=j; }
	   }
	   
	 if(b==-1) continue;
       
         //find in the delta R
         dR->Fill(minR);
	 }
       }
       TCanvas *c = new TCanvas("haha");
       c->cd();
       dR->Draw();
       }

