import glob, os
import plot_utils
from plot_utils import *

lumi = 36074.56 # Moriond 2017

name_infile_signal = "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.37-0-X/Sig_GGM_tag.2.4.37-0-X.root"
name_infile_bkg = "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.37-0-X_tmp/Bkg_tag.2.4.37-0-X_nominal_and_qcd.root"
name_infile_data= "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.37-0-X_tmp/Data_tag.2.4.37-0-X.root"


outfolder="./sig_bkg_2.4.37/"

if __name__ == "__main__":

    os.system("mkdir -p "+outfolder)

    masses=["130","150","200","300","400","500","600","800"]
    weights=["weight_lumi","weight_mc"]
    name_infile = dict()
    for m in masses:
        name_infile[m] = name_infile_signal

    num_sel=["hh_type==10"]
    legend = ["hh #rightarrow 4b"]
    den_sel = "1"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_is_hh_4b.pdf")

    num_sel=["hh_type==10","hh_type==1","hh_type==2","hh_type==3","hh_type!=1 &&hh_type!=2 && hh_type!=3"]
    legend = ["hh #rightarrow 4b","hh #rightarrow 4b test","hh #rightarrow max 2b","hh #rightarrow 0b","no hh"]
    den_sel = "(signal_leptons_n)==0"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_is_hh_4b_test.pdf")

    num_sel=["bjets_n_85>=3","bjets_n_77>=3","bjets_n_70>=3","bjets_n>=3"]
    legend = ["3b 85", "3b 77", "3b 70","3b 77 flat"]
    den_sel = "(signal_leptons_n)==0 && jets_n>=4 && met>200 && pass_MET && hh_type==10"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_3b_met200_4j.pdf")

    num_sel=["bjets_n_85>=4","bjets_n_77>=4","bjets_n_70>=4","bjets_n>=4"]
    legend = ["4b 85", "4b 77", "4b 70","4b 77 flat"]
    den_sel = "(signal_leptons_n)==0 && jets_n>=4 && met>200 && pass_MET && hh_type==10"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_4b_met200_4j.pdf")

    num_sel=["bjets_n_85>=3","bjets_n_77>=3","bjets_n_70>=3","bjets_n>=3"]
    legend = ["3b 85", "3b 77", "3b 70","3b 77 flat"]
    den_sel = "hh_type==10"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_3b_hh4b.pdf")

    num_sel=["bjets_n_85>=4","bjets_n_77>=4","bjets_n_70>=4","bjets_n>=4"]
    legend = ["4b 85", "4b 77", "4b 70","4b 77 flat"]
    den_sel = "hh_type==10"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_4b_hh4b.pdf")

    num_sel=["jets_n>=4"]
    legend = [">= 4 jets"]
    den_sel = "hh_type==10"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_4j_4b_hh4b.pdf")



    # +++++++++++++
    # Signal/bkg plots
    # +++++++++++++
    var_def=[]

    #var_def += [{'def':("mass_h1_dR",40,50,250),'leg':"m(h1) [GeV]"}]
    #var_def += [{'def':("mass_h2_dR",40,50,250),'leg':"m(h2) [GeV]"}]
    #var_def += [{'def':("mass_bb",40,50,250),'leg':"m(b,b) [GeV]"}]
    var_def += [{'def':("fabs(pt_jet_1-pt_bjet_1)<0.001",2,-0.5,1.5),'leg':"lead_tagged",'can':'lead_tagged'}]
    """
    var_def += [{'def':("meff_4bj",20,300,1300),'leg':"meff 4b [GeV]"}]
    var_def += [{'def':("mTb_min",15,0,300),'leg':"m_{T}^{min}(b,MET) [GeV]"}]
    var_def += [{'def':("jets_n",11, -0.5,10.5),'leg':"Number of jets"}]
    var_def += [{'def':("met_sig",30,0,30),'leg':"MET/#sqrt{H_{T}}   [#sqrt{GeV}]"}]
    var_def += [{'def':("met",20,0.,1000),'leg':"E_{T}^{miss} [GeV]"}]
    var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_dR"}] 
    #var_def += [{'def':("mass_h1_min_diff",40,50,250),'leg':"m(h1) [GeV]",'can':"mass_h1_min_diff"}]
    #var_def += [{'def':("mass_h2_min_diff",40,50,250),'leg':"m(h2) [GeV]",'can':"mass_h2_min_diff"}]
    var_def += [{'def':("bjets_n_77",4, 1.5,5.5),'leg':"Number of b-jets 77%"}]
    var_def += [{'def':("pt_jet_1",16, 0,800),'leg':"1st jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_2",16, 0,800),'leg':"2nd jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_3",16, 0,800),'leg':"3rd jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_4",16, 0,800),'leg':"4th jet p_{T} [GeV]"}]
    var_def += [{'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
    #var_def += [{'def':("dphi_1jet",20,0,4),'leg':"#Delta#phi(j^{1},MET)"}]
    var_def += [{'def':("pt_bjet_1",16, 0,800),'leg':"1st b-jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_bjet_2",16, 0,800),'leg':"2nd b-jet p_{T} [GeV]"}]
    """

    signals=["GGM_hh_300","GGM_hh_500","GGM_hh_800"]
    name_infile = dict()
    for s in signals:
        name_infile[s] = name_infile_signal

    backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar"]
    for b in backgrounds:
        name_infile[b]= name_infile_bkg

    #labels_sig = ["m(#tilde{#chi}) = 150 GeV","m(#tilde{#chi}) = 200 GeV","m(#tilde{#chi}) = 500 GeV","m(#tilde{#chi}) = 800 GeV"]
    labels_sig = ["m(#tilde{#chi}) = 300 GeV","m(#tilde{#chi}) = 500 GeV","m(#tilde{#chi}) = 800 GeV"]
    labels_bkg = ["diboson","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}"]

    for var in var_def:
        if "can" in var.keys():
            name_can = var['can']
        else:
            name_can = var['def'][0]

        name_can = name_can+"_hh"

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j, 2b, met>200","hh(4b)"]
        sel="(meff_4bj>800 && jets_n>=4 && jets_n<=5 && bjets_n>=3 && baseline_leptons_n==0 && pass_MET && dphi_min>0.4 && met>200)*(weight_mc*weight_lumi*weight_elec*weight_muon*weight_jvt*weight_WZ_2_2)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j_2b_0l_met200", signals, labels_sig,"hh_type==10")





