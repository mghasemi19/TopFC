/// \file
/// \ingroup tutorial_roostats
/// \notebook -nodraw
/// 'Number Counting Utils' RooStats tutorial
///
/// This tutorial shows an example of the RooStats standalone
/// utilities that calculate the p-value or Z value (eg. significance in
/// 1-sided Gaussian standard deviations) for a number counting experiment.
/// This is a hypothesis test between background only and signal-plus-background.
/// The background estimate has uncertainty derived from an auxiliary or sideband
/// measurement.
///
/// Documentation for these utilities can be found here:
/// http://root.cern.ch/root/html/RooStats__NumberCountingUtils.html
///
///
/// This problem is often called a proto-type problem for high energy physics.
/// In some references it is referred to as the on/off problem.
///
/// The problem is treated in a fully frequentist fashion by
/// interpreting the relative background uncertainty as
/// being due to an auxiliary or sideband observation
/// that is also Poisson distributed with only background.
/// Finally, one considers the test as a ratio of Poisson means
/// where an interval is well known based on the conditioning on the total
/// number of events and the binomial distribution.
/// For more on this, see
///  - http://arxiv.org/abs/0905.3831
///  - http://arxiv.org/abs/physics/physics/0702156
///  - http://arxiv.org/abs/physics/0511028
///
///
/// \macro_image
/// \macro_output
/// \macro_code
///
/// \author Kyle Cranmer

#include "RooStats/RooStatsUtils.h"
#include <iostream>

using namespace RooFit;
using namespace RooStats; // the utilities are in the RooStats namespace
using namespace std;

void significance_compute()
{

   // From the root prompt, you can see the full list of functions by using tab-completion
   // ~~~{.bash}
   // root [0] RooStats::NumberCountingUtils::  <tab>
   // BinomialExpZ
   // BinomialWithTauExpZ
   // BinomialObsZ
   // BinomialWithTauObsZ
   // BinomialExpP
   // BinomialWithTauExpP
   // BinomialObsP
   // BinomialWithTauObsP
   // ~~~

   // For each of the utilities you can inspect the arguments by tab completion
   // ~~~{.bash}
   // root [1] NumberCountingUtils::BinomialExpZ( <tab>
   // Double_t BinomialExpZ(Double_t sExp, Double_t bExp, Double_t fractionalBUncertainty)
   // ~~~

   // -------------------------------------------------
   // Here we see common usages where the experimenter
   // has a relative background uncertainty, without
   // explicit reference to the auxiliary or sideband
   // measurement

   // -------------------------------------------------------------
   // Expected p-values and significance with background uncertainty   
   // simple NN stats
   //double ttcharm_sExpected_list[] = {399.1, 292.6, 184.3};       
   //double ttcharm_bExpected_list[] = {269.1, 180.8, 105.3};

   // optimized NN stats
   //double ttcharm_sExpected_list[] = {567.2, 487.0, 387.7};       
   //double ttcharm_bExpected_list[] = {337.9, 246.6, 160.1};   

   // optimized NN with dropout stats
   double ttcharm_sExpected_list[] = {570.8, 492.8, 397.1};       
   double ttcharm_bExpected_list[] = {240.7, 173.9, 116.7};   

   double relativeBkgUncert[] = {0.25, 0.5, 1};
   double ttcharm_pval_25[3][9];
   double ttcharm_zval_25[3][9];
   double ttcharm_pval_50[3][9];
   double ttcharm_zval_50[3][9];
   double ttcharm_pval_100[3][9];
   double ttcharm_zval_100[3][9];

   double mu_sig[] = {1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3};
   
   for (int i=0; i<3; i++){         // loop over sig/bkg events
      for (int k=0; k<3; k++){      // loop over bkguncert
         for (int j=0; j<9; j++){   // loop over mu_sig
	         double pExp = NumberCountingUtils::BinomialExpP(ttcharm_sExpected_list[i]*mu_sig[j], ttcharm_bExpected_list[i], relativeBkgUncert[k]);
	         double zExp = NumberCountingUtils::BinomialExpZ(ttcharm_sExpected_list[i]*mu_sig[j], ttcharm_bExpected_list[i], relativeBkgUncert[k]);
            //cout << "expected p-value =" << pExp << "  Z value (Gaussian sigma) = " << zExp << endl;
            if (relativeBkgUncert[k]==0.25){              
               ttcharm_pval_25[i][j] = pExp;
               ttcharm_zval_25[i][j] = zExp;
            }
            if (relativeBkgUncert[k]==0.5){
               ttcharm_pval_50[i][j] = pExp;
               ttcharm_zval_50[i][j] = zExp;
            }
            if (relativeBkgUncert[k]==1){
               ttcharm_pval_100[i][j] = pExp;
               ttcharm_zval_100[i][j] = zExp;
            }                        
	         //cout << "\nnSig = " << ttcharm_sExpected_list[i] << " * " << mu_sig[j] << "  nBkg = " << ttcharm_bExpected_list[i] << "  Bkg_unc = " << relativeBkgUncert[k] << endl; 
	         //cout << "expected p-value =" << pExp << "  Z value (Gaussian sigma) = " << zExp << endl;	    
	      }
         //cout << "------------------" << endl;
      }   
	//cout << "------------------" << endl;
   }
   
   cout << "P-val for ttcharm_pval_25:" << endl;
   for (auto &row : ttcharm_pval_25){
      for (auto &col : row) {cout << col << endl;}
   }     
   cout << "Z-val for ttcharm_zval_25:" << endl;
   for (auto &row : ttcharm_zval_25){
      for (auto &col : row) {cout << col << endl;}
   }     

   cout << "P-val for ttcharm_pval_50:" << endl;
   for (auto &row : ttcharm_pval_50){
      for (auto &col : row) {cout << col << endl;}
   }     
   cout << "Z-val for ttcharm_zval_50:" << endl;
   for (auto &row : ttcharm_zval_50){
      for (auto &col : row) {cout << col << endl;}
   }

   cout << "P-val for ttcharm_pval_100:" << endl;
   for (auto &row : ttcharm_pval_100){
      for (auto &col : row) {cout << col << endl;}
   }     
   cout << "Z-val for ttcharm_zval_100:" << endl;
   for (auto &row : ttcharm_zval_100){
      for (auto &col : row) {cout << col << endl;}
   }   
   
// -------------------------------------------------------------
   /*
   // Expected p-values and significance with background uncertainty   
   double ttup_sExpected_list[] = {496.9, 379.2, 252.1};
   double ttup_bExpected_list[] = {348.4, 242.4, 141.2};
   //double relativeBkgUncert[] = {0.25, 0.5, 1};
   double ttup_pval_25[3][9];
   double ttup_zval_25[3][9];
   double ttup_pval_50[3][9];
   double ttup_zval_50[3][9];
   double ttup_pval_100[3][9];
   double ttup_zval_100[3][9];

   //double mu_sig[] = {1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3};
   
   for (int i=0; i<3; i++){         // loop over sig/bkg events
      for (int k=0; k<3; k++){      // loop over bkguncert
         for (int j=0; j<9; j++){   // loop over mu_sig
	         double pExp = NumberCountingUtils::BinomialExpP(ttup_sExpected_list[i]*mu_sig[j], ttup_bExpected_list[i], relativeBkgUncert[k]);
	         double zExp = NumberCountingUtils::BinomialExpZ(ttup_sExpected_list[i]*mu_sig[j], ttup_bExpected_list[i], relativeBkgUncert[k]);
            //cout << "expected p-value =" << pExp << "  Z value (Gaussian sigma) = " << zExp << endl;
            if (relativeBkgUncert[k]==0.25){              
               ttup_pval_25[i][j] = pExp;
               ttup_zval_25[i][j] = zExp;
            }
            if (relativeBkgUncert[k]==0.5){
               ttup_pval_50[i][j] = pExp;
               ttup_zval_50[i][j] = zExp;
            }
            if (relativeBkgUncert[k]==1){
               ttup_pval_100[i][j] = pExp;
               ttup_zval_100[i][j] = zExp;
            }                        
	         //cout << "\nnSig = " << ttcharm_sExpected_list[i] << " * " << mu_sig[j] << "  nBkg = " << ttcharm_bExpected_list[i] << "  Bkg_unc = " << relativeBkgUncert[k] << endl; 
	         //cout << "expected p-value =" << pExp << "  Z value (Gaussian sigma) = " << zExp << endl;	    
	      }
         //cout << "------------------" << endl;
      }   
	//cout << "------------------" << endl;
   }
   cout << "P-val for ttup_pval_25:" << endl;
   for (auto &row : ttup_pval_25){
      for (auto &col : row) {cout << col << endl;}
   }     
   cout << "Z-val for ttcharm_zval_25:" << endl;
   for (auto &row : ttup_zval_25){
      for (auto &col : row) {cout << col << endl;}
   }     

   cout << "P-val for ttup_pval_50:" << endl;
   for (auto &row : ttup_pval_50){
      for (auto &col : row) {cout << col << endl;}
   }     
   cout << "Z-val for ttup_zval_50:" << endl;
   for (auto &row : ttup_zval_50){
      for (auto &col : row) {cout << col << endl;}
   }

   cout << "P-val for ttup_pval_100:" << endl;
   for (auto &row : ttup_pval_100){
      for (auto &col : row) {cout << col << endl;}
   }     
   cout << "Z-val for ttup_zval_100:" << endl;
   for (auto &row : ttup_zval_100){
      for (auto &col : row) {cout << col << endl;}
   }   
   */
}
