import glob, os
import plot_utils
from plot_utils import *

lumi = 36074.56 # Moriond 2017

remove_meff_corr=False

pickle_sel="../../cuts_pickle/sel_wei_dict_presel.pickle"
pickle_sel_no_wei="../../cuts_pickle/sel_dict_presel.pickle"

folder_in="/afs/cern.ch/user/c/crizzi/storage/susy_EW/merge_HF_inputs/"

name_infile_data=folder_in+"Data_2.4.28-0-0_skim_2b.root"
#name_infile_bkg=folder_in+"bkg_tagEW.2.4.28-1_nominal.root"
name_infile_bkg="../eos/atlas/user/c/crizzi/susy_EW/bkg_tagEW.2.4.28-1_v3_nominal_aliases.root"
name_infile_QCD=folder_in+""
name_infile_signal="../create_mini_tree/mini_trees_hh_v4_4btypes_aliases.root"

outfolder="./2017_03_27/"

if __name__ == "__main__":

    os.system("mkdir -p "+outfolder)

    masses=["130","150","200","300","400","500","600","800"]
    weights=["weight_lumi","weight_mc"]
    name_infile = dict()
    for m in masses:
        name_infile[m] = name_infile_signal

    signals=["hh_200_hh4b","hh_300_hh4b", "hh_400_hh4b", "hh_500_hh4b", "hh_600_hh4b", "hh_700_hh4b", "hh_800_hh4b"]
    name_infile = dict()
    for s in signals:
        name_infile[s] = name_infile_signal

    backgrounds=["Zjets","Wjets","TopEW","SingleTop","ttbar"]
    #backgrounds=["ttbar"]
    for b in backgrounds:
        name_infile[b]= name_infile_bkg

    labels_sig = ["m(#tilde{#chi}) = 200 GeV","m(#tilde{#chi}) = 400 GeV","m(#tilde{#chi}) = 600 GeV","m(#tilde{#chi}) = 800 GeV"]
    labels_bkg = ["dijet","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}"]
    #labels_bkg = ["t#bar{t}"]


    #variables = ["(mass_h1_dR+mass_h2_dR)/2","fabs(mass_h1_dR-mass_h2_dR)","max(DeltaR_h1_dR,DeltaR_h2_dR)","met","met_sig","mTb_min","bjets_n_77","ht"]
    #labels_var = ["<m>","Dm","dR-max", "MET","MET/#sqrt{HT}","mtb", "N-b 77", "HT"]

    variables = ["mass_h1_dR","mass_h2_dR", "max(DeltaR_h1_min_diff,DeltaR_h2_min_diff)", "met", "mTb_min", "dphi_min", "jets_n", "bjets_n_77"]
    labels_var = ["m(h1)",    "m(h2)",       "dR-max",                                     "MET", "mTb",    "dphi-min",  "N-J",    "N-bJ"]

    #variables = ["met","met_sig","mTb_min","bjets_n_77","ht"]
    #labels_var = ["MET","MET/#sqrt{HT}","mtb", "N-b 77", "HT"]

    var_corr(variables, labels_var, backgrounds, name_infile, "correlation_bkg_v2.pdf")
    var_corr(variables, labels_var, ["hh_400_hh4b"], name_infile, "correlation_hh_400_v2.pdf")
    #var_corr(variables, labels_var, backgrounds, name_infile, "correlation_bkg.pdf")


    # +++++++++++++
    # Data/MC plots
    # +++++++++++++
    var_def=[]
    # 'def': variable to plot: (name, nbins, x-low, x-max)
    # 'leg': legend of the x-axis

    #var_def += [{'def':("fabs(mass_h1_min_diff-mass_h2_min_diff)",20,0,100),'leg':"|m1-m2| [GeV]",'can':"mass_diff_min_diff"}]
    #var_def += [{'def':("fabs(mass_h1_115-mass_h2_115)",20,0,100),'leg':"|m1-m2| [GeV]",'can':"mass_diff_115"}]
    #var_def += [{'def':("fabs(mass_h1_dR-mass_h2_dR)",20,0,100),'leg':"|m1-m2| [GeV]",'can':"mass_diff_min_dR"}]

    #var_def += [{'def':("met_sig",30,0,30),'leg':"MET/#sqrt{H_{T}}   [#sqrt{GeV}]"}]
    var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_dR"}] 
    var_def += [{'def':("max(DeltaR_h1_115,DeltaR_h2_115)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_115"}] 
    var_def += [{'def':("max(DeltaR_h1_min_diff,DeltaR_h2_min_diff)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_min_diff"}] 


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
    var_def += [{'def':("mass_h1_dR",30,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_dR"}]
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
    
    """
    var_def += [{'def':("mTb_min",15,0,300),'leg':"m_{T}^{min}(b,MET) [GeV]"}]
    var_def += [{'def':("jets_n",11, -0.5,10.5),'leg':"Number of jets"}]
    var_def += [{'def':("signal_leptons_n",5, -0.5,4.5),'leg':"Number of signal leptons"}]
    var_def += [{'def':("asymmetry",20, 0.,1.),'leg':"Asymmetry"}]
    var_def += [{'def':("bjets_n_85",6, -0.5,5.5),'leg':"Number of b-jets 85%"}]
    var_def += [{'def':("bjets_n_70",6, -0.5,5.5),'leg':"Number of b-jets 70%"}]
    var_def += [{'def':("bjets_n_77",6, -0.5,5.5),'leg':"Number of b-jets 77%"}]
    var_def += [{'def':("bjets_n_60",6, -0.5,5.5),'leg':"Number of b-jets 60%"}]
    var_def += [{'def':("pt_jet_1",16, 0,800),'leg':"1st jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_2",16, 0,800),'leg':"2nd jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_3",16, 0,800),'leg':"3rd jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_4",16, 0,800),'leg':"4th jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_5",16, 0,800),'leg':"5th jet p_{T} [GeV]"}]
    var_def += [{'def':("ht",20,0.,1000),'leg':"HT [GeV]"}]
    var_def += [{'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
    var_def += [{'def':("dphi_1jet",20,0,4),'leg':"#Delta#phi(j^{1},MET)"}]
    var_def += [{'def':("MJSum_rc_r08pt10",25,0,500),'leg':"MJSum [GeV]"}]
    """
    #var_def += [{'def':("dphi_mettrack_met",20,0,4),'leg':"#Delta#phi(MET^{track},MET)"}]

                



