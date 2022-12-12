import glob, os
import plot_utils
from plot_utils import *

lumi = 36074.56 # Moriond 2017

remove_meff_corr=False

pickle_sel="../../cuts_pickle/sel_wei_dict_presel.pickle"
pickle_sel_no_wei="../../cuts_pickle/sel_dict_presel.pickle"

folder_in="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-4-1/"

name_infile_data=folder_in+"Data_tagEW.2.4.28-4-1_SUSY10_2b.root"
name_infile_bkg=folder_in+"Bkg_tagEW.2.4.28-4-1_SUSY10_METfilt_nominal_3b.root"
name_infile_QCD=folder_in+""
name_infile_signal=folder_in+"Sig_GGM_tagEW.2.4.28-4-1_SUSY10_nominal_4b.root"
#name_infile_signal=folder_in+"Sig_GGM_tagEW.2.4.28-4-1_SUSY10_nominal_4b.root"

outfolder="./2017_06_21/"

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
    var_def += [{'def':("meff_4bj",20,300,1300),'leg':"meff 4b [GeV]"}]
    var_def += [{'def':("mTb_min",15,0,300),'leg':"m_{T}^{min}(b,MET) [GeV]"}]
    var_def += [{'def':("jets_n",11, -0.5,10.5),'leg':"Number of jets"}]
    var_def += [{'def':("met_sig",30,0,30),'leg':"MET/#sqrt{H_{T}}   [#sqrt{GeV}]"}]
    var_def += [{'def':("met",20,0.,1000),'leg':"E_{T}^{miss} [GeV]"}]
    var_def += [{'def':("mass_h1_dR",40,50,250),'leg':"m(h1) [GeV]",'can':"mass_h1_min_dR"}]
    var_def += [{'def':("mass_h2_dR",40,50,250),'leg':"m(h2) [GeV]",'can':"mass_h2_min_dR"}]
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
    var_def += [{'def':("m_rho300_1",40,50,250),'leg':"m(j1) #rho 300 [GeV]",'can':"mass_VRj1_rho300"}]
    var_def += [{'def':("m_rho300_2",40,50,250),'leg':"m(j2) #rho 300 [GeV]",'can':"mass_VRj2_rho300"}]
    var_def += [{'def':("m_rho400_1",40,50,250),'leg':"m(j1) #rho 400 [GeV]",'can':"mass_VRj1_rho400"}]
    var_def += [{'def':("m_rho400_2",40,50,250),'leg':"m(j2) #rho 400 [GeV]",'can':"mass_VRj2_rho400"}]
    var_def += [{'def':("m_rho500_1",40,50,250),'leg':"m(j1) #rho 500 [GeV]",'can':"mass_VRj1_rho500"}]
    var_def += [{'def':("m_rho500_2",40,50,250),'leg':"m(j2) #rho 500 [GeV]",'can':"mass_VRj2_rho500"}]
    """

    #var_def += [{'def':("bjets_n_85",4, 1.5,5.5),'leg':"Number of b-jets 85%"}]
    #var_def += [{'def':("bjets_n_70",4, 1.5,5.5),'leg':"Number of b-jets 70%"}]
    #var_def += [{'def':("bjets_n",4, 1.5,5.5),'leg':"Number of b-jets 77% Flat Eff"}]
    """

    #var_def += [{'def':("DeltaR_bb",25, 0,5),'leg':"dR(b,b)"}]
    #var_def += [{'def':("DeltaR_jj",25, 0,5),'leg':"dR(j,j)"}]
    #var_def += [{'def':("mass_bb",30,50,200),'leg':"m(b,b) [GeV]"}]
    #var_def += [{'def':("mass_jj",30,50,200),'leg':"m(j,j) [GeV]"}]

    var_def += [{'def':("asymmetry",20, 0.,1.),'leg':"Asymmetry"}]
    var_def += [{'def':("pt_jet_5",16, 0,800),'leg':"5th jet p_{T} [GeV]"}]
    var_def += [{'def':("ht",20,0.,1000),'leg':"HT [GeV]"}]

    var_def += [{'def':("pt_jet_5",16, 0,800),'leg':"5th jet p_{T} [GeV]"}]
    #var_def += [{'def':("max(DeltaR_h1_min_diff,DeltaR_h2_min_diff)",15,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_min_diff"}] 
    #var_def += [{'def':("(mass_h1_min_diff+mass_h2_min_diff)/2",15,50,200),'leg':"<m> [GeV]",'can':"mass_average_min_diff"}]
    
    #var_def += [{'def':("signal_leptons_n",5, -0.5,4.5),'leg':"Number of signal leptons"}]
    #var_def += [{'def':("(baseline_muons_n+baseline_electrons_n)",5, -0.5,4.5),'leg':"Number of baseline leptons","can":"baseline_leptons_n"}]
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
    """
    """
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

    #backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar_light","ttbar_cc","ttbar_bb"]
    backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar"]
        #backgrounds=["Zjets","Wjets","SingleTop","ttbar"]
    #backgrounds=["ttbar"]
    for b in backgrounds:
        name_infile[b]= name_infile_bkg

    #labels_sig = ["m(#tilde{#chi}) = 150 GeV","m(#tilde{#chi}) = 200 GeV","m(#tilde{#chi}) = 500 GeV","m(#tilde{#chi}) = 800 GeV"]
    labels_sig = ["m(#tilde{#chi}) = 300 GeV","m(#tilde{#chi}) = 500 GeV","m(#tilde{#chi}) = 800 GeV"]
    #labels_bkg = ["diboson","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}+light", "t#bar{t}+cc", "t#bar{t}+bb"]
    labels_bkg = ["diboson","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}"]
    #labels_bkg = ["Z+jets","W+jets","single top","t#bar{t}"]
    #labels_bkg = ["t#bar{t}"]


    for var in var_def:
        if "can" in var.keys():
            name_can = var['can']
        else:
            name_can = var['def'][0]

        name_can = name_can+"_hh"

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j, 2b, met>200","hh(4b)"]
        sel="(mass_h1_dR>100 && mass_h1_dR<140 && mass_h2_dR>100 && mass_h2_dR<140 && jets_n>=4 && jets_n<=7 && bjets_n>=2 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>200)*(weight_mc*weight_lumi*weight_elec*weight_muon*weight_jvt*weight_WZ_2_2)"
        #sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j_2b_0l_met200", signals, labels_sig,"hh_type==10")

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j, 3b, met>200","hh(4b)"]
        #sel="(mass_h1_dR>100 && mass_h1_dR<140 && mass_h2_dR>100 && mass_h2_dR<140 && jets_n>=4 && jets_n<=7 && bjets_n>=3 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>200)*(weight_mc*weight_lumi*weight_elec*weight_muon*weight_jvt*weight_WZ_2_2)"
        #sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j_3b_0l_met200", signals, labels_sig,"hh_type==10")

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j, 4b, met>200","hh(4b)"]
        sel="(mass_h1_dR>100 && mass_h1_dR<140 && mass_h2_dR>100 && mass_h2_dR<140 && jets_n>=4 && jets_n<=7 && bjets_n>=4 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>200)*(weight_mc*weight_lumi*weight_elec*weight_muon*weight_jvt*weight_WZ_2_2)"
        #sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j_4b_0l_met200", signals, labels_sig, "hh_type==10")

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4-7j, #geq 3b, met>200","hh(4b)"]
        sel="(jets_n>=4 && jets_n<=7 && bjets_n>=3 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>200)*(weight_mc*weight_lumi*weight_elec*weight_muon*weight_jvt*weight_WZ_2_2*weight_btag)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4_7j_3b_0l_met200_hh", signals, labels_sig)

            
        """

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","2-OS-L, L-trig, 2j, ex2b L-trig","Zh/ZZ #rightarrow llbb"]
        sel="(jets_n>=2 && bjets_n_77==2 && signal_leptons_n>=2 && Z_OSLeps && pt_lep_1>27 && (signal_electron_trig_pass || signal_muon_trig_pass))*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_2j_ex2b_2l_lep_trig", signals, labels_sig, "hh_type==32 || hh_type==22")

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","2-OS-L, L-trig, 2j, ex2b ","Zh #rightarrow llbb"]
        sel="(jets_n>=2 && bjets_n_77==2 && signal_leptons_n>=2 && Z_OSLeps && pt_lep_1>27 && (signal_electron_trig_pass || signal_muon_trig_pass) && mass_bb > 100 && mass_bb<140 && Z_mass>70 && Z_mass<100)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_2j_ex2b_2l_lep_trig_mZ_mh", signals, labels_sig, "hh_type==22")

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","2-OS-L, L-trig, 2j, ex2b ","ZZ #rightarrow llbb"]
        sel="(jets_n>=2 && bjets_n_77==2 && signal_leptons_n>=2 && Z_OSLeps && pt_lep_1>27 && (signal_electron_trig_pass || signal_muon_trig_pass) && mass_bb > 70 && mass_bb<100 && Z_mass>70 && Z_mass<100)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j_ex2b_0l_lep_trig_mZ_mZ", signals, labels_sig, "hh_type==32")

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","2-OS-L, 2j, ex2b, L-trig, met>100 ","Zh/ZZ #rightarrow llbb"]
        sel="(met>100 && jets_n>=2 && bjets_n_77==2 && signal_leptons_n>=2 && Z_OSLeps && pt_lep_1>27 && (signal_electron_trig_pass || signal_muon_trig_pass))*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_2j_ex2b_2l_lep_trig_met100", signals, labels_sig, "hh_type==32 || hh_type==22")

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","2-OS-L, L-trig, 2j, ex2b, met>100","Zh #rightarrow llbb"]
        sel="(met>100 && jets_n>=2 && bjets_n_77==2 && signal_leptons_n>=2 && Z_OSLeps && pt_lep_1>27 && (signal_electron_trig_pass || signal_muon_trig_pass) && mass_bb > 100 && mass_bb<140 && Z_mass>70 && Z_mass<100)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_2j_ex2b_2l_lep_trig_met100_mZ_mh", signals, labels_sig, "hh_type==22")

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","2-OS-L, L-trig, 2j, ex2b, met>100 ","ZZ #rightarrow llbb"]
        sel="(met>100 && jets_n>=2 && bjets_n_77==2 && signal_leptons_n>=2 && Z_OSLeps && pt_lep_1>27 && (signal_electron_trig_pass || signal_muon_trig_pass) && mass_bb > 70 && mass_bb<100 && Z_mass>70 && Z_mass<100)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_2j_ex2b_2l_lep_trig_met100_mZ_mZ", signals, labels_sig, "hh_type==32")


        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","2-OS-L, 2j, ex2b, met>180","Zh/ZZ #rightarrow llbb"]
        sel="(jets_n>=2 && bjets_n_77==2 && signal_leptons_n>=2 && Z_OSLeps && pass_MET && met>180)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_2j_ex2b_2l_met180", signals, labels_sig, "hh_type==32 || hh_type==22")

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","2-OS-L, 2j, ex2b, met>180","Zh #rightarrow llbb"]
        sel="(jets_n>=2 && bjets_n_77==2 && signal_leptons_n>=2 && Z_OSLeps && pass_MET && met>180 && mass_bb > 100 && mass_bb<140 && Z_mass>70 && Z_mass<100)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_2j_ex2b_2l_met180_mZ_mh", signals, labels_sig, "hh_type==22")

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","2-OS-L, 2j, ex2b, met>180","ZZ #rightarrow llbb"]
        sel="(jets_n>=2 && bjets_n_77==2 && signal_leptons_n>=2 && Z_OSLeps && pass_MET && met>180 && mass_bb > 70 && mass_bb<100 && Z_mass>70 && Z_mass<100)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_2j_ex2b_2l_met180_mZ_mZ", signals, labels_sig, "hh_type==32")


        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j, ex2b, met>180","Zh/ZZ #rightarrow qqbb"]
        sel="(jets_n>=4 && bjets_n_77==2 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>180)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j_ex2b_0l_met180", signals, labels_sig, "hh_type==33 || hh_type==23")

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j, ex2b, met>180, mZ, mh","Zh #rightarrow qqbb"]
        sel="(jets_n>=4 && bjets_n_77==2 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>180 && mass_bb > 100 && mass_bb<140 && mass_jj>70 && mass_jj<100)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j_ex2b_0l_met180_mZ_mh", signals, labels_sig, "hh_type==23")

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j, ex2b, met>180, mZ, mZ","ZZ #rightarrow qqbb"]
        sel="(jets_n>=4 && bjets_n_77==2 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>180 && mass_bb>70 && mass_bb<100 && mass_jj>70 && mass_jj<100)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j_ex2b_0l_met180_mZ_mZ", signals, labels_sig, "hh_type==33")
        """
        """

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}"," 0L, #geq 3b, met>180, mh, mh ","hh #rightarrow 4b"]
        sel="(jets_n>=4 && bjets_n_77>=3 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>180 && mass_h2_dR>100 && mass_h2_dR<140 && mass_h1_dR>100 && mass_h1_dR<140)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j_in3b_0l_met180_mh_mh", signals, labels_sig, "hh_type==10")

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}"," 0L, #geq 3b, met>400 ","hh #rightarrow 4b"]
        sel="(met>400 && jets_n>=4 && bjets_n_77>=3 && signal_leptons_n==0 && pass_MET && dphi_min>0.4)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j_in3b_0l_met400", signals, labels_sig, "hh_type==10")


        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}"," 0L, #geq 3b, 250<met<400 ","hh #rightarrow 4b"]
        sel="(met>250 && met<400 && jets_n>=4 && bjets_n_77>=3 && signal_leptons_n==0 && pass_MET && dphi_min>0.4)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j_in3b_0l_met250_400", signals, labels_sig, "hh_type==10")


        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}"," 0L, #geq 3b, 180<met<250 ","hh #rightarrow 4b"]
        sel="(met>180 && met<250 && jets_n>=4 && bjets_n_77>=3 && signal_leptons_n==0 && pass_MET && dphi_min>0.4)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j_in3b_0l_met180_250", signals, labels_sig, "hh_type==10")



        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}"," 0L, met>180, mh, mh ","hh #rightarrow 4b"]
        sel="(jets_n>=4 &&  signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>180 && mass_h2_dR>100 && mass_h2_dR<140 && mass_h1_dR>100 && mass_h1_dR<140)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j_0l_met180_mh_mh", signals, labels_sig, "hh_type==10")

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}"," 0L, met>400 ","hh #rightarrow 4b"]
        sel="(met>400 && jets_n>=4 &&  signal_leptons_n==0 && pass_MET && dphi_min>0.4)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j_0l_met400", signals, labels_sig, "hh_type==10")


        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}"," 0L, 250<met<400 ","hh #rightarrow 4b"]
        sel="(met>250 && met<400 && jets_n>=4 &&  signal_leptons_n==0 && pass_MET && dphi_min>0.4)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j_0l_met250_400", signals, labels_sig, "hh_type==10")


        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}"," 0L, 180<met<250 ","hh #rightarrow 4b"]
        sel="(met>180 && met<250 && jets_n>=4 &&  signal_leptons_n==0 && pass_MET && dphi_min>0.4)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j_0l_met180_250", signals, labels_sig, "hh_type==10")


        """






