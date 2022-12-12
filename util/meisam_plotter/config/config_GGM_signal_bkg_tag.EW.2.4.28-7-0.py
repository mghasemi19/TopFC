import glob, os
import plot_utils
from plot_utils import *

lumi = 36074.56 # Moriond 2017

remove_meff_corr=False

pickle_sel="../../cuts_pickle/sel_wei_dict_presel.pickle"
pickle_sel_no_wei="../../cuts_pickle/sel_dict_presel.pickle"

folder_in="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-7-0/"

name_infile_data=folder_in+"Data_2.4.28-0-0_skim_2b.root"
#name_infile_bkg=folder_in+"bkg_tagEW.2.4.28-1_nominal.root"
name_infile_bkg=folder_in+"Bkg_tagEW.2.4.28-7-0_SUSY10_METfilt_nominal_2b.root"
name_infile_QCD=folder_in+""
name_infile_signal=folder_in+"Sig_GGM_tagEW.2.4.28-7-0_SUSY10_nominal_all.root"

outfolder="./2017_06_26_sig_bkg/"

if __name__ == "__main__":

    os.system("mkdir -p "+outfolder)

    masses=["130","150","200","300","400","500","600","800"]
    weights=["weight_lumi","weight_mc"]
    name_infile = dict()
    for m in masses:
        name_infile[m] = name_infile_signal

    num_sel=["is_hh_4b"]
    legend = ["hh #rightarrow 4b"]
    den_sel = "1"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "is_hh_4b.pdf")

    num_sel=["is_hh_4b","hh_type==1","hh_type==2","hh_type==3","hh_type!=1 &&hh_type!=2 && hh_type!=3"]
    legend = ["hh #rightarrow 4b","hh #rightarrow 4b test","hh #rightarrow max 2b","hh #rightarrow 0b","no hh"]
    den_sel = "(signal_leptons_n)==0"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "is_hh_4b_test.pdf")


    num_sel=["bjets_n_85>=3","bjets_n_77>=3","bjets_n_70>=3","bjets_n>=3"]
    legend = ["3b 85", "3b 77", "3b 70","3b 77 flat"]
    den_sel = "(signal_leptons_n)==0 && jets_n>=4 && met>200 && pass_MET && hh_type==10"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, "./", "bjet_efficiency_3b_met200_4j.pdf")

    num_sel=["bjets_n_85>=4","bjets_n_77>=4","bjets_n_70>=4","bjets_n>=4"]
    legend = ["4b 85", "4b 77", "4b 70","4b 77 flat"]
    den_sel = "(signal_leptons_n)==0 && jets_n>=4 && met>200 && pass_MET && hh_type==10"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, "./", "bjet_efficiency_4b_met200_4j.pdf")

    num_sel=["bjets_n_85>=3","bjets_n_77>=3","bjets_n_70>=3","bjets_n>=3"]
    legend = ["3b 85", "3b 77", "3b 70","3b 77 flat"]
    den_sel = "hh_type==10"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, "./", "bjet_efficiency_3b_hh4b.pdf")

    num_sel=["bjets_n_85>=4","bjets_n_77>=4","bjets_n_70>=4","bjets_n>=4"]
    legend = ["4b 85", "4b 77", "4b 70","4b 77 flat"]
    den_sel = "hh_type==10"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, "./", "bjet_efficiency_4b_hh4b.pdf")

    num_sel=["jets_n>=4"]
    legend = [">= 4 jets"]
    den_sel = "hh_type==10"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, "./", "4j_efficiency_4b_hh4b.pdf")



    # +++++++++++++
    # Data/MC plots
    # +++++++++++++
    var_def=[]
    var_def += [{'def':("meff_4bj",20,300,1300),'leg':"meff 4b [GeV]"}]    
    var_def += [{'def':("mTb_min",15,0,300),'leg':"m_{T}^{min}(b,MET) [GeV]"}]
    var_def += [{'def':("met_sig",30,0,30),'leg':"MET/#sqrt{H_{T}}   [#sqrt{GeV}]"}]
    var_def += [{'def':("met",20,0.,1000),'leg':"E_{T}^{miss} [GeV]"}]
    var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_dR"}] 
    var_def += [{'def':("jets_n",11, -0.5,10.5),'leg':"Number of jets"}]
    var_def += [{'def':("bjets_n",4, 1.5,5.5),'leg':"Number of b-jets 77%"}]
    var_def += [{'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]

    """
    var_def += [{'def':("DeltaR_bb",25, 0,5),'leg':"dR(b,b)",'can':'dR_bb'}]
    var_def += [{'def':("mass_bb",30,50,200),'leg':"m(b,b) [GeV]"}]
    var_def += [{'def':("Z_mass",20,50,250),'leg':"m(l,l) [GeV]",'can':"mass_ll"}]

    #var_def += [{'def':("mass_h1_dR",40,50,250),'leg':"m(h1) [GeV]",'can':"mass_h1_min_dR"}]
    #var_def += [{'def':("mass_h2_dR",40,50,250),'leg':"m(h2) [GeV]",'can':"mass_h2_min_dR"}]
    #var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_dR"}] 
    #var_def += [{'def':("mass_h1_min_diff",40,50,250),'leg':"m(h1) [GeV]",'can':"mass_h1_min_diff"}]
    #var_def += [{'def':("mass_h2_min_diff",40,50,250),'leg':"m(h2) [GeV]",'can':"mass_h2_min_diff"}]
    var_def += [{'def':("bjets_n_77",4, 1.5,5.5),'leg':"Number of b-jets 77%"}]
    var_def += [{'def':("pt_jet_1",16, 0,800),'leg':"1st jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_2",16, 0,800),'leg':"2nd jet p_{T} [GeV]"}]
    #var_def += [{'def':("pt_jet_3",16, 0,800),'leg':"3rd jet p_{T} [GeV]"}]
    #var_def += [{'def':("pt_jet_4",16, 0,800),'leg':"4th jet p_{T} [GeV]"}]
    #var_def += [{'def':("dphi_1jet",20,0,4),'leg':"#Delta#phi(j^{1},MET)"}]
    var_def += [{'def':("pt_bjet_1",16, 0,800),'leg':"1st b-jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_bjet_2",16, 0,800),'leg':"2nd b-jet p_{T} [GeV]"}]

    var_def += [{'def':("bjets_n_85",4, 1.5,5.5),'leg':"Number of b-jets 85%"}]
    var_def += [{'def':("bjets_n_70",4, 1.5,5.5),'leg':"Number of b-jets 70%"}]
    var_def += [{'def':("bjets_n",4, 1.5,5.5),'leg':"Number of b-jets 77% Flat Eff"}]

    var_def += [{'def':("met_sig",30,0,30),'leg':"MET/#sqrt{H_{T}}   [#sqrt{GeV}]"}]
    var_def += [{'def':("met",20,0.,1000),'leg':"E_{T}^{miss} [GeV]"}]


    #var_def += [{'def':("DeltaR_jj",25, 0,5),'leg':"dR(j,j)"}]
    #var_def += [{'def':("mass_jj",30,50,200),'leg':"m(j,j) [GeV]"}]

    var_def += [{'def':("mTb_min",15,0,300),'leg':"m_{T}^{min}(b,MET) [GeV]"}]
    var_def += [{'def':("jets_n",11, -0.5,10.5),'leg':"Number of jets"}]
    var_def += [{'def':("asymmetry",20, 0.,1.),'leg':"Asymmetry"}]
    var_def += [{'def':("pt_jet_1",16, 0,800),'leg':"1st jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_2",16, 0,800),'leg':"2nd jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_3",16, 0,800),'leg':"3rd jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_4",16, 0,800),'leg':"4th jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_5",16, 0,800),'leg':"5th jet p_{T} [GeV]"}]
    var_def += [{'def':("ht",20,0.,1000),'leg':"HT [GeV]"}]
    var_def += [{'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
    var_def += [{'def':("dphi_1jet",20,0,4),'leg':"#Delta#phi(j^{1},MET)"}]
    var_def += [{'def':("pt_bjet_1",16, 0,800),'leg':"1st b-jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_bjet_2",16, 0,800),'leg':"2nd b-jet p_{T} [GeV]"}]

    var_def += [{'def':("pt_jet_5",16, 0,800),'leg':"5th jet p_{T} [GeV]"}]
    #var_def += [{'def':("max(DeltaR_h1_min_diff,DeltaR_h2_min_diff)",15,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_min_diff"}] 
    #var_def += [{'def':("(mass_h1_min_diff+mass_h2_min_diff)/2",15,50,200),'leg':"<m> [GeV]",'can':"mass_average_min_diff"}]
    
    #var_def += [{'def':("signal_leptons_n",5, -0.5,4.5),'leg':"Number of signal leptons"}]
    #var_def += [{'def':("(baseline_muons_n+baseline_electrons_n)",5, -0.5,4.5),'leg':"Number of baseline leptons","can":"baseline_leptons_n"}]
    var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_dR"}] 
    #var_def += [{'def':("mass_h1_dR",30,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_dR"}]
    #var_def += [{'def':("mass_h2_dR",30,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_min_dR"}]

    #var_def += [{'def':("MJSum_rc_r08pt10",25,0,500),'leg':"MJSum [GeV]"}]

    #var_def += [{'def':("dphi_mettrack_met",20,0,4),'leg':"#Delta#phi(MET^{track},MET)"}]

    #var_def += [{'def':("mass_h1_min_diff",15,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_diff"}]
    # 'def': variable to plot: (name, nbins, x-low, x-max)
    # 'leg': legend of the x-axis

    #var_def += [{'def':("fabs(mass_h1_min_diff-mass_h2_min_diff)",20,0,100),'leg':"|m1-m2| [GeV]",'can':"mass_diff_min_diff"}]
    #var_def += [{'def':("fabs(mass_h1_115-mass_h2_115)",20,0,100),'leg':"|m1-m2| [GeV]",'can':"mass_diff_115"}]
    #var_def += [{'def':("fabs(mass_h1_dR-mass_h2_dR)",20,0,100),'leg':"|m1-m2| [GeV]",'can':"mass_diff_min_dR"}]

    #var_def += [{'def':("met_sig",30,0,30),'leg':"MET/#sqrt{H_{T}}   [#sqrt{GeV}]"}]
    
    #var_def += [{'def':("max(DeltaR_h1_115,DeltaR_h2_115)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_115"}] 

    var_def += [{'def':("mass_h1_115",30,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_115"}]
    var_def += [{'def':("mass_h2_115",30,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_115"}]
    var_def += [{'def':("(mass_h1_115+mass_h2_115)/2",30,50,200),'leg':"<m> [GeV]",'can':"mass_average_115"}]
    var_def += [{'def':("DeltaR_h1_115",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{1}'}]
    var_def += [{'def':("DeltaR_h2_115",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{2}'}]

    var_def += [{'def':("(mass_h1_min_diff+mass_h2_min_diff)/2",30,50,200),'leg':"<m> [GeV]",'can':"mass_average_min_diff"}]
    var_def += [{'def':("mass_h1_min_diff",30,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_diff"}]
    var_def += [{'def':("mass_h2_min_diff",30,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_min_diff"}]
    var_def += [{'def':("DeltaR_h1_min_diff",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{1}'}]
    var_def += [{'def':("DeltaR_h2_min_diff",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{2}'}]

    var_def += [{'def':("(mass_h1_dR+mass_h2_dR)/2",30,50,200),'leg':"<m> [GeV]",'can':"mass_average_min_dR"}]
    """

    #var_def += [{'def':("(mass_h1_min_diff>100 && mass_h1_min_diff<140) + (mass_h2_min_diff>100 && mass_h2_min_diff<140)",3,-0.5,2.5),'leg':"Number of higgs candidates",'can':"h_cand_n_min_diff"}]
    #var_def += [{'def':("(mass_h1_115>100 && mass_h1_115<140) + (mass_h2_115>100 && mass_h2_115<140)",3,-0.5,2.5),'leg':"Number of higgs candidates",'can':"h_cand_n_115"}]
    #var_def += [{'def':("(mass_h1_max_pt>100 && mass_h1_max_pt<140) + (mass_h2_max_pt>100 && mass_h2_max_pt<140)",3,-0.5,2.5),'leg':"Number of higgs candidates",'can':"h_cand_n_max_pt"}]
    #var_def += [{'def':("(mass_h1_dR>100 && mass_h1_dR<140) + (mass_h2_dR>100 && mass_h2_dR<140)",3,-0.5,2.5),'leg':"Number of higgs candidates",'can':"h_cand_n_min_dR"}]

    """
    var_def += [{'def':("mass_h2_dR",30,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_min_dR"}]
    var_def += [{'def':("DeltaR_h1_dR",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{1}'}]
    var_def += [{'def':("DeltaR_h2_dR",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{2}'}]
    """
    #var_def += [{'def':("fabs(m_h1_max_pt-mass_h2_max_pt)",20,0,50),'leg':"|m1-m2| [GeV]",'can':"mass_diff_max_pt"}]
    #var_def += [{'def':("(m_h1_max_pt+mass_h2_max_pt)/2",30,50,200),'leg':"<m> [GeV]",'can':"mass_average_max_pt"}]

    #var_def += [{'def':("mass_h1_max_pt",30,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_max_pt"}]
    #var_def += [{'def':("mass_h2_max_pt",30,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_max_pt"}]
    #var_def += [{'def':("DeltaR_h1_max_pt",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{1}'}]
    #var_def += [{'def':("DeltaR_h2_max_pt",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{2}'}]

    #var_def += [{'def':("fabs(mass_h1_true_match-mass_h2_true_match)",50,0,50),'leg':"|m1-m2| [GeV]",'can':"mass_diff_true_match"}]
    #var_def += [{'def':("(mass_h1_true_match+mass_h2_true_match)/2",30,50,200),'leg':"<m> [GeV]",'can':"mass_average_true_match"}]
    #var_def += [{'def':("mass_h1_true_match",30,50,200),'leg':"<m> [GeV]",'can':"mass_h1_true_match"}]
    #var_def += [{'def':("mass_h2_true_match",30,50,200),'leg':"<m> [GeV]",'can':"mass_h2_true_match"}]
    #var_def += [{'def':("DeltaR_h1_true_match",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{1}'}]
    #var_def += [{'def':("DeltaR_h2_true_match",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{2}'}]

    #var_def += [{'def':("pt_trueb1_h1",16, 0,800),'leg':"true-b_{1} from h_{1} p_{T} [GeV]"}]
    #var_def += [{'def':("pt_trueb2_h1",16, 0,800),'leg':"true-b_{2} from h_{1} p_{T} [GeV]"}]
    #var_def += [{'def':("pt_trueb1_h2",16, 0,800),'leg':"true-b_{1} from h_{2} p_{T} [GeV]"}]
    #var_def += [{'def':("pt_trueb2_h2",16, 0,800),'leg':"true-b_{2} from h_{2} p_{T} [GeV]"}]

    #var_def += [{'def':("eta_trueb1_h1",40,-4,4),'leg':"true-b_{1} from h_{1} #eta"}]
    #var_def += [{'def':("eta_trueb2_h1",40,-4,4),'leg':"true-b_{2} from h_{1} #eta"}]
    #var_def += [{'def':("eta_trueb1_h2",40,-4,4),'leg':"true-b_{1} from h_{2} #eta"}]
    #var_def += [{'def':("eta_trueb2_h2",40,-4,4),'leg':"true-b_{2} from h_{2} #eta"}]


                

    #signals=["GGM_hh_130","GGM_hh_150","GGM_hh_200","GGM_hh_300","GGM_hh_400","GGM_hh_500","GGM_hh_600","GGM_hh_800"]
    signals=["GGM_hh_300_hh4b","GGM_hh_500_hh4b","GGM_hh_800_hh4b"]
    #signals=["GGM_Zh_150","GGM_Zh_200","GGM_Zh_500","GGM_Zh_800"]
    name_infile = dict()
    for s in signals:
        name_infile[s] = name_infile_signal

    backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar"]
        #backgrounds=["Zjets","Wjets","SingleTop","ttbar"]
    #backgrounds=["ttbar"]
    for b in backgrounds:
        name_infile[b]= name_infile_bkg

    labels_sig = ["m(#tilde{#chi}) = 300 GeV","m(#tilde{#chi}) = 500 GeV","m(#tilde{#chi}) = 800 GeV"]
    labels_bkg = ["diboson","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}"]
    #labels_bkg = ["Z+jets","W+jets","single top","t#bar{t}"]
    #labels_bkg = ["t#bar{t}"]


    for var in var_def:
        if "can" in var.keys():
            name_can = var['can']
        else:
            name_can = var['def'][0]

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, #geq 4j, #geq 3b, mhh","hh #rightarrow 4b"]
        sel="(mTb_min>140 && jets_n<=6 && max(DeltaR_h1_dR,DeltaR_h2_dR)>1.5 && mass_h1_dR>100 && mass_h1_dR<150 && mass_h2_dR>90 && mass_h2_dR<140 && met>200 && jets_n>=4 && bjets_n>=3 && signal_leptons_n==0 && dphi_min>0.4 && signal_leptons_n==0)*(weight_mc*weight_lumi*weight_btag*weight_elec*weight_muon*weight_jvt*weight_WZ_2_2)"
        #sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_hh_mhh_highdR_highMET", signals, labels_sig)
        plot_var(var['def'], sel, signals, name_infile, labels_sig, var['leg'], ["1"], outfolder,name_can+"_hh", do_scale=True, doLogY=False, write=write)
