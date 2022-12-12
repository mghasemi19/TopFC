import glob, os
import plot_utils
from plot_utils import *

lumi = 36074.56 # Moriond 2017

remove_meff_corr=False
add_signal = False

pickle_sel="../../cuts_pickle/sel_wei_dict_presel.pickle"
pickle_sel_no_wei="../../cuts_pickle/sel_dict_presel.pickle"

folder_in="../../input/eos/atlas/user/c/crizzi/susy_multib/HFinputs_merged/SUSYHF_tag2.4.28-0-0/"

name_infile_data=folder_in+"Data_2.4.28-0-0_skim_2b.root"
name_infile=folder_in+"Bkg_2.4.28-0-0_skim_2b_NoSys_with_wei.root"
name_infile_QCD=folder_in+"Bkg_2.4.28-0-0_multijet_skim_2b_NoSys_with_wei.root"
#kbest_match_if_match_possible.pdf"
#name_infile_signal="../create_mini_tree/mini_trees_hh_v3_4btypes.root"
name_infile_signal="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-0-3_TOPQ1_mini_tree/mini_ntuples_v6_all_types.root"

outfolder="./2017_06_19/"


if __name__ == "__main__":

    os.system("mkdir -p "+outfolder)

    masses=["130","150","200","300","400","500","600","800"]
    weights=["weight_lumi","weight_mc"]
    name_infile = dict()
    for m in masses:
        name_infile[m] = name_infile_signal

    num_sel=["bjets_n_60>=3","bjets_n_70>=3","bjets_n_77>=3","bjets_n_85>=3"]
    legend = ["#geq 3b 60","#geq 3b 70","#geq 3b 77","#geq 3b 85"]
    den_sel = "is_hh_4b"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_3bjets_hh4b.pdf")

    num_sel=["bjets_n_60>=4","bjets_n_70>=4","bjets_n_77>=4","bjets_n_85>=4"]
    legend = ["#geq 4b 60","#geq 4b 70","#geq 4b 77","#geq 4b 85"]
    den_sel = "is_hh_4b"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_4bjets_hh4b.pdf")

    num_sel=["bjets_n_60>=3","bjets_n_70>=3","bjets_n_77>=3","bjets_n_85>=3"]
    legend = ["#geq 3b 60","#geq 3b 70","#geq 3b 77","#geq 3b 85"]
    den_sel = "is_hh_4b && met>200"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_3bjets_hh4b_met200.pdf")

    num_sel=["bjets_n_60>=4","bjets_n_70>=4","bjets_n_77>=4","bjets_n_85>=4"]
    legend = ["#geq 4b 60","#geq 4b 70","#geq 4b 77","#geq 4b 85"]
    den_sel = "is_hh_4b && met>200"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_4bjets_hh4b_met200.pdf")

    """
    num_sel=["good_match_115","good_match_min_diff", "good_match_min_dR", "good_match_max_pt"]
    legend = ["115", "min-diff", "min-dR","max-pT"]
    den_sel = "is_hh_4b && match_possible && pass_MET && met>180 && jets_n>=4 && bjets_85_n>=3 && dphi_min>0.4"
    signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "best_match_if_match_possible_presel.pdf")

    num_sel=["jets_n>=4","match_possible","match_possible && lead_mv2_matched"]
    legend = ["#geq 4 jets", "match possible", "leading mv2 matched"]
    den_sel = "is_hh_4b"
    signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "match_possible.pdf")

    num_sel=["pass_MET && met>180","jets_n>=4","bjets_85_n>=2","dphi_min>0.4"," pass_MET && met>180 && jets_n>=4 && bjets_85_n>=2 && dphi_min>0.4"]
    legend = ["met>180 & trig","#geq 4 jets","#geq 2 b 85%", "dphi>0.4", "all"]
    den_sel = "is_hh_4b"
    signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_presel.pdf")

    num_sel=["pass_MET && met>180","jets_n>=4","bjets_85_n>=3","dphi_min>0.4"," pass_MET && met>180 && jets_n>=4 && bjets_85_n>=3 && dphi_min>0.4"]
    legend = ["met>180 & trig","#geq 4 jets","#geq 3 b 85%", "dphi>0.4", "all"]
    den_sel = "is_hh_4b"
    signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_presel_3b.pdf")

    num_sel=["pass_MET && met>180","jets_n>=4","bjets_85_n>=2","dphi_min>0.4"," pass_MET && met>180 && jets_n>=4 && bjets_85_n>=2 && dphi_min>0.4"]
    legend = ["met>180 & trig","#geq 4 jets","#geq 2 b 85%", "dphi>0.4", "all"]
    den_sel = "1"
    signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_presel_on_all.pdf")

    num_sel=["pass_MET && met>180","jets_n>=4","bjets_85_n>=3","dphi_min>0.4"," pass_MET && met>180 && jets_n>=4 && bjets_85_n>=3 && dphi_min>0.4"]
    legend = ["met>180 & trig","#geq 4 jets","#geq 3 b 85%", "dphi>0.4", "all"]
    den_sel = "1"
    signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_presel_3b_on_all.pdf")

    num_sel=["pass_MET && met>180","pass_MET && met>200","pass_MET && met>250"]
    legend = ["met>180","met>200","met>250"]
    den_sel = "is_hh_4b"
    signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_met.pdf")

    num_sel=["pass_MET && met>180","pass_MET && met>200","pass_MET && met>250"]
    legend = ["met>180","met>200","met>250"]
    den_sel = "is_hh_4b && jets_n>=4"
    signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_met_after4j.pdf")

    num_sel=["jets_n>=4","jets_n>=4 && pt_jet_4 > 25","jets_n>=4 && pt_jet_4 > 30"]
    legend = ["4 jets 20","4 jets 25","4 jets 30"]
    den_sel = "is_hh_4b"
    signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_4j.pdf")

    num_sel=["jets_n>=4","jets_n>=4 && pt_jet_4 > 25","jets_n>=4 && pt_jet_4 > 30"]
    legend = ["4 jets 20","4 jets 25","4 jets 30"]
    den_sel = "is_hh_4b && pass_MET && met>180"
    signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_4j_after_met.pdf")

    num_sel=["is_hh_4b"]
    legend = ["hh #rightarrow 4b"]
    den_sel = "1"
    signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "is_hh_4b.pdf")

    """

    # +++++++++++++
    # Data/MC plots
    # +++++++++++++
    var_def=[]
    # 'def': variable to plot: (name, nbins, x-low, x-max)
    # 'leg': legend of the x-axis
    #var_def += [{'def':("met",20,0.,800),'leg':"E_{T}^{miss} [GeV]"}]
    #var_def += [{'def':("(met/sqrt(ht_had))",10,0,30),'leg':"MET/#sqrt{H_{T}}   [#sqrt{GeV}]",'can':"met_sig"}]
    #var_def += [{'def':("max(dR_h2_min_dR,dR_h1_min_dR)",15,0,5), 'leg':'max( dR(b1_{h1},b2_{h1}), dR(b1_{h2},b2_{h2}) )','can':"dRmax_min_dR"}]
    #var_def += [{'def':("m_h1_min_dR",30,50,200),'leg':"<m> [GeV]",'can':"mass_h1_min_dR"}]
    #var_def += [{'def':("m_h2_min_dR",30,50,200),'leg':"<m> [GeV]",'can':"mass_h2_min_dR"}]
    #var_def += [{'def':("dR_h1_min_dR",15,0,5), 'leg':'dR(b_{1}, b_{2}) h_{1}'}]
    #var_def += [{'def':("dR_h2_min_dR",15,0,5), 'leg':'dR(b_{1}, b_{2}) h_{2}'}]
    #var_def += [{'def':("fabs(m_h1_min_dR-m_h2_min_dR)",10,0,50),'leg':"|m1-m2| [GeV]",'can':"mass_diff_min_dR"}]
    #var_def += [{'def':("(m_h1_min_dR+m_h2_min_dR)/2",30,50,200),'leg':"<m> [GeV]",'can':"mass_average_min_dR"}]

    #var_def += [{'def':("m_h1_min_diff",30,50,200),'leg':"m(1) [GeV]",'can':"mass_h1_min_diff"}]
    #var_def += [{'def':("m_h2_min_diff",30,50,200),'leg':"m(2) [GeV]",'can':"mass_h2_min_diff"}]

    var_def += [{'def':("m_bb",30,50,200),'leg':"m(bb) [GeV]"}]
    var_def += [{'def':("m_ll",30,50,200),'leg':"m(ll) [GeV]"}]

    #var_def += [{'def':("max(dR_h2_min_diff,dR_h1_min_diff)",30,0,5), 'leg':'max( dR(b1_{h1},b2_{h1}), dR(b1_{h2},b2_{h2}) )','can':"dRmax_min_diff"}]
    #var_def += [{'def':("(m_h1_min_diff+m_h2_min_diff)/2",30,50,200),'leg':"<m> [GeV]",'can':"mass_average_min_diff"}]
    #var_def += [{'def':("mtb_min",15,0,300),'leg':"m_{T}^{min}(b,MET) [GeV]"}]
    #var_def += [{'def':("bjets_77_n",6, -0.5,5.5),'leg':"Number of b-jets 77%"}]
    #var_def += [{'def':("fabs(m_h1_min_diff-m_h2_min_diff)",50,0,50),'leg':"|m1-m2| [GeV]",'can':"mass_diff_min_diff"}]


    #var_def += [{'def':("bjets_85_n",6, -0.5,5.5),'leg':"Number of b-jets 85%"}]
    """
    var_def += [{'def':("max(dR_h2_115,dR_h1_115)",30,0,5), 'leg':'max( dR(b1_{h1},b2_{h1}), dR(b1_{h2},b2_{h2}) )','can':"dRmax_115"}]
    var_def += [{'def':("max(dR_h2_max_pt,dR_h1_max_pt)",30,0,5), 'leg':'max( dR(b1_{h1},b2_{h1}), dR(b1_{h2},b2_{h2}) )','can':"dRmax_max_pt"}]

    var_def += [{'def':("m_h1_min_diff",30,50,200),'leg':"<m> [GeV]",'can':"mass_h1_min_diff"}]
    var_def += [{'def':("m_h2_min_diff",30,50,200),'leg':"<m> [GeV]",'can':"mass_h2_min_diff"}]
    var_def += [{'def':("dR_h1_min_diff",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{1}'}]
    var_def += [{'def':("dR_h2_min_diff",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{2}'}]


    var_def += [{'def':("fabs(m_h1_115-m_h2_115)",50,0,50),'leg':"|m1-m2| [GeV]",'can':"mass_diff_115"}]
    var_def += [{'def':("(m_h1_115+m_h2_115)/2",30,50,200),'leg':"<m> [GeV]",'can':"mass_average_115"}]
    var_def += [{'def':("m_h1_115",30,50,200),'leg':"<m> [GeV]",'can':"mass_h1_115"}]
    var_def += [{'def':("m_h2_115",30,50,200),'leg':"<m> [GeV]",'can':"mass_h2_115"}]
    var_def += [{'def':("dR_h1_115",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{1}'}]
    var_def += [{'def':("dR_h2_115",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{2}'}]

    var_def += [{'def':("fabs(m_h1_max_pt-m_h2_max_pt)",50,0,50),'leg':"|m1-m2| [GeV]",'can':"mass_diff_max_pt"}]
    var_def += [{'def':("(m_h1_max_pt+m_h2_max_pt)/2",30,50,200),'leg':"<m> [GeV]",'can':"mass_average_max_pt"}]
    var_def += [{'def':("m_h1_max_pt",30,50,200),'leg':"<m> [GeV]",'can':"mass_h1_max_pt"}]
    var_def += [{'def':("m_h2_max_pt",30,50,200),'leg':"<m> [GeV]",'can':"mass_h2_max_pt"}]
    var_def += [{'def':("dR_h1_max_pt",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{1}'}]
    var_def += [{'def':("dR_h2_max_pt",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{2}'}]

    var_def += [{'def':("fabs(m_h1_true_match-m_h2_true_match)",50,0,50),'leg':"|m1-m2| [GeV]",'can':"mass_diff_true_match"}]
    var_def += [{'def':("(m_h1_true_match+m_h2_true_match)/2",30,50,200),'leg':"<m> [GeV]",'can':"mass_average_true_match"}]
    var_def += [{'def':("m_h1_true_match",30,50,200),'leg':"<m> [GeV]",'can':"mass_h1_true_match"}]
    var_def += [{'def':("m_h2_true_match",30,50,200),'leg':"<m> [GeV]",'can':"mass_h2_true_match"}]
    var_def += [{'def':("dR_h1_true_match",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{1}'}]
    var_def += [{'def':("dR_h2_true_match",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{2}'}]

    var_def += [{'def':("pt_trueb1_h1",16, 0,800),'leg':"true-b_{1} from h_{1} p_{T} [GeV]"}]
    var_def += [{'def':("pt_trueb2_h1",16, 0,800),'leg':"true-b_{2} from h_{1} p_{T} [GeV]"}]
    var_def += [{'def':("pt_trueb1_h2",16, 0,800),'leg':"true-b_{1} from h_{2} p_{T} [GeV]"}]
    var_def += [{'def':("pt_trueb2_h2",16, 0,800),'leg':"true-b_{2} from h_{2} p_{T} [GeV]"}]

    var_def += [{'def':("eta_trueb1_h1",40,-4,4),'leg':"true-b_{1} from h_{1} #eta"}]
    var_def += [{'def':("eta_trueb2_h1",40,-4,4),'leg':"true-b_{2} from h_{1} #eta"}]
    var_def += [{'def':("eta_trueb1_h2",40,-4,4),'leg':"true-b_{1} from h_{2} #eta"}]
    var_def += [{'def':("eta_trueb2_h2",40,-4,4),'leg':"true-b_{2} from h_{2} #eta"}]

    var_def += [{'def':("jets_n",11, -0.5,10.5),'leg':"Number of jets"}]
    var_def += [{'def':("signal_leptons_n",5, -0.5,4.5),'leg':"Number of signal leptons"}]
    var_def += [{'def':("asymmetry",20, 0.,1.),'leg':"Asymmetry"}]
    var_def += [{'def':("bjets_70_n",6, -0.5,5.5),'leg':"Number of b-jets 70%"}]
    var_def += [{'def':("bjets_60_n",6, -0.5,5.5),'leg':"Number of b-jets 60%"}]
    var_def += [{'def':("pt_jet_1",16, 0,800),'leg':"1st jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_2",16, 0,800),'leg':"2nd jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_3",16, 0,800),'leg':"3rd jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_4",16, 0,800),'leg':"4th jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_5",16, 0,800),'leg':"5th jet p_{T} [GeV]"}]
    var_def += [{'def':("ht_had",20,0.,1000),'leg':"HT [GeV]"}]
    var_def += [{'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
    var_def += [{'def':("dphi_1jet",20,0,4),'leg':"#Delta#phi(j^{1},MET)"}]

    var_def += [{'def':("MJSum_R08PT10",25,0,500),'leg':"MJSum [GeV]"}]
    var_def += [{'def':("dphi_mettrack_met",20,0,4),'leg':"#Delta#phi(MET^{track},MET)"}]
    """
    
    myslice = ["1"]
    #signals = ["hh_130","hh_150","hh_200","hh_300","hh_400","hh_500","hh_600","hh_800"]
    #labels = ["130","150","200","300","400","500","600","800"]
    #signals = ["hh_150","hh_300","hh_500","hh_600","hh_800"]
    
    signals = ["hh_150","hh_200","hh_500","hh_800"]
    labels = ["m(#tilde{#chi}) = 150 GeV","m(#tilde{#chi}) = 200 GeV","m(#tilde{#chi}) = 500 GeV","m(#tilde{#chi}) = 800 GeV"]

    for m in signals:
        name_infile[m] = name_infile_signal

    for var in var_def:
        # list of things to write on the plot
        #print var['def']
        if "can" in var.keys():
            name_can = var['can']
        else:
            name_can = var['def'][0]

        sel="(jets_n>=4 && pass_MET && bjets_n_77>=3)*(weight_mc*weight_lumi)"
        write=["#bf{#it{ATLAS}} Internal","#geq 4 jets, 3b77, passMET"]

        signals = ["hh_300_hh4b","Zh_300_Zh4b"]
        labels = ["300, hh 4b","300, Zh 4b"]
        for m in signals:
            name_infile[m] = name_infile_signal        
        #plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_300_4j_3b_passMET", do_scale=True, doLogY=False, write=write)

        signals = ["hh_500_hh4b","Zh_500_Zh4b"]
        labels = ["500, hh 4b","500, Zh 4b"]
        for m in signals:
            name_infile[m] = name_infile_signal        
        #plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_500_4j_3b_passMET", do_scale=True, doLogY=False, write=write)


        signals = ["hh_600_hh4b","Zh_600_Zh4b"]
        labels = ["600, hh 4b","600, Zh 4b"]
        for m in signals:
            name_infile[m] = name_infile_signal        
        #plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_600_4j_3b_passMET", do_scale=True, doLogY=False, write=write)


        signals = ["hh_800_hh4b","Zh_800_Zh4b"]
        labels = ["800, hh 4b","800, Zh 4b"]
        for m in signals:
            name_infile[m] = name_infile_signal        
        #plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_800_4j_3b_passMET", do_scale=True, doLogY=False, write=write)



        sel="(jets_n>=2 && pass_MET && bjets_n_77==2 && TwoSFlep)*(weight_mc*weight_lumi)"
        write=["#bf{#it{ATLAS}} Internal","#geq 2 jets, 2b77, 2SF lep, passMET"]

        signals = ["Zh_300_ZZllbb","Zh_300_Zhllbb"]
        labels = ["300, ZZ bbll","300, Zh bbll"]
        for m in signals:
            name_infile[m] = name_infile_signal        
        plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_300_2j_2b_2L_passMET", do_scale=True, doLogY=False, write=write)

        signals = ["Zh_500_ZZllbb","Zh_500_Zhllbb"]
        labels = ["500, ZZ bbll","500, Zh bbll"]
        for m in signals:
            name_infile[m] = name_infile_signal        
        plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_500_2j_2b_2L_passMET", do_scale=True, doLogY=False, write=write)


        signals = ["Zh_600_ZZllbb","Zh_600_Zhllbb"]
        labels = ["600, ZZ bbll","600, Zh bbll"]
        for m in signals:
            name_infile[m] = name_infile_signal        
        #plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_600_2j_2b_2L_passMET", do_scale=True, doLogY=False, write=write)


        signals = ["Zh_800_ZZllbb","Zh_800_Zhllbb"]
        labels = ["800, ZZ bbll","800, Zh bbll"]
        for m in signals:
            name_infile[m] = name_infile_signal        
        plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_800_2j_2b_2L_passMET", do_scale=True, doLogY=False, write=write)


        #if "true_match" in var['def'][0]:
        #    sel="(is_hh_4b && match_possible)*(weight_mc*weight_lumi)"
        #    write=["#bf{#it{ATLAS}} Internal","hh #rightarrow 4b, true match"]
        #    plot_var(var['def'], sel, signals, name_infile, name_infile, labels,var['leg'], myslice, outfolder, name_can+"_true_match", lumi, do_scale=False, doLogY=True, write=write)
        #    plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_true_match", do_scale=True, doLogY=False, write=write)

        #sel="(is_hh_4b)*(weight_mc*weight_lumi)"
        #write=["#bf{#it{ATLAS}} Internal","hh #rightarrow 4b"]
        #plot_var(var['def'], sel, signals, name_infile, labels,var['leg'], myslice, outfolder,name_can, do_scale=False, doLogY=True, write=write)
        #plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can, do_scale=True, doLogY=False, write=write)

        #sel="(is_hh_4b && pass_MET && met>180 && jets_n>=4 && bjets_85_n>=2 && dphi_min>0.4)*(weight_mc*weight_lumi)"
        #write=["#bf{#it{ATLAS}} Internal","hh #rightarrow 4b, Preselection"]
        #plot_var(var['def'], sel, signals, name_infile, labels,var['leg'], myslice, outfolder,name_can+"_presel", do_scale=False, doLogY=True, write=write)
        #plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_presel", do_scale=True, doLogY=False, write=write)
        """
            
        signals = ["hh_300_hh4b","hh_500_hh4b","hh_800_hh4b", "Zh_300_Zh4b","Zh_500_Zh4b","Zh_800_Zh4b", "Zh_300_ZZ4b","Zh_500_ZZ4b","Zh_800_ZZ4b"]
        labels = ["300, hh 4b", "500, hh4b", "800, hh 4b", "300, Zh 4b", "500, Zh4b", "800, Zh 4b", "300, ZZ 4b", "500, ZZ4b", "800, ZZ 4b"]
        for m in signals:
            name_infile[m] = name_infile_signal        

        sel="(jets_n>=4 && pass_MET && bjets_77_n>=2)*(weight_mc*weight_lumi)"
        write=["#bf{#it{ATLAS}} Internal","#geq 4 jets, 2b77, passMET"]
        #plot_var(var['def'], sel, signals, name_infile, labels,var['leg'], myslice, outfolder,name_can+"_4j", do_scale=False, doLogY=True, write=write)
        plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_4j_2b_passMET", do_scale=True, doLogY=False, write=write)

        signals = ["hh_300_hh4b","hh_500_hh4b","hh_800_hh4b"]
        labels = ["300, hh 4b", "500, hh4b", "800, hh 4b"]
        sel="(m_h2_min_dR>100 && m_h2_min_dR<140 && m_h1_min_dR>100 && m_h1_min_dR<140 && jets_n>=4 && pass_MET && bjets_77_n>=2)*(weight_mc*weight_lumi)"
        write=["#bf{#it{ATLAS}} Internal","#geq 4 jets, 2b77, passMET, hh-mass"]
        plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_4j_2b_passMET_hhmass", do_scale=True, doLogY=False, write=write)

        signals = ["Zh_300_Zh4b","Zh_500_Zh4b","Zh_800_Zh4b"]
        labels = ["300, Zh 4b", "500, Zh4b", "800, Zh 4b"]
        sel="(m_h2_min_dR>70 && m_h2_min_dR<100 && m_h1_min_dR>100 && m_h1_min_dR<140 && jets_n>=4 && pass_MET && bjets_77_n>=2)*(weight_mc*weight_lumi)"
        write=["#bf{#it{ATLAS}} Internal","#geq 4 jets, 2b77, passMET, Zh-mass"]
        plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_4j_2b_passMET_Zhmass", do_scale=True, doLogY=False, write=write)

        signals = ["Zh_300_ZZ4b","Zh_500_ZZ4b","Zh_800_ZZ4b"]
        labels = ["300, ZZ 4b", "500, ZZ4b", "800, ZZ 4b"]
        sel="(m_h2_min_dR>70 && m_h2_min_dR<100 && m_h1_min_dR>70 && m_h1_min_dR<100 && jets_n>=4 && pass_MET && bjets_77_n>=2)*(weight_mc*weight_lumi)"
        write=["#bf{#it{ATLAS}} Internal","#geq 4 jets, 2b77, passMET, ZZ-mass"]
        plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_4j_2b_passMET_ZZmass", do_scale=True, doLogY=False, write=write)

        signals = ["hh_300_hh4b","hh_500_hh4b","hh_800_hh4b", "Zh_300_Zh4b","Zh_500_Zh4b","Zh_800_Zh4b", "Zh_300_ZZ4b","Zh_500_ZZ4b","Zh_800_ZZ4b"]
        labels = ["300, hh 4b", "500, hh4b", "800, hh 4b", "300, Zh 4b", "500, Zh4b", "800, Zh 4b", "300, ZZ 4b", "500, ZZ4b", "800, ZZ 4b"]

        sel="(met>180 && jets_n>=4 && pass_MET && bjets_77_n>=2)*(weight_mc*weight_lumi)"
        write=["#bf{#it{ATLAS}} Internal","#geq 4 jets, 2b77, passMET, met 180"]
        #plot_var(var['def'], sel, signals, name_infile, labels,var['leg'], myslice, outfolder,name_can+"_4j", do_scale=False, doLogY=True, write=write)
        plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_4j_2b_met180_passMET", do_scale=True, doLogY=False, write=write)

        signals = ["hh_300_hh4b","hh_500_hh4b","hh_800_hh4b"]
        labels = ["300, hh 4b", "500, hh4b", "800, hh 4b"]
        sel="(met>180 && m_h2_min_dR>100 && m_h2_min_dR<140 && m_h1_min_dR>100 && m_h1_min_dR<140 && jets_n>=4 && pass_MET && bjets_77_n>=2)*(weight_mc*weight_lumi)"
        write=["#bf{#it{ATLAS}} Internal","#geq 4 jets, 2b77, passMET, met 180", "hh-mass"]
        plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_4j_2b_met180_passMET_hhmass", do_scale=True, doLogY=False, write=write)

        signals = ["Zh_300_Zh4b","Zh_500_Zh4b","Zh_800_Zh4b"]
        labels = ["300, Zh 4b", "500, Zh4b", "800, Zh 4b"]
        sel="(met>180 && m_h2_min_dR>70 && m_h2_min_dR<100 && m_h1_min_dR>100 && m_h1_min_dR<140 && jets_n>=4 && pass_MET && bjets_77_n>=2)*(weight_mc*weight_lumi)"
        write=["#bf{#it{ATLAS}} Internal","#geq 4 jets, 2b77, passMET, met 180", "Zh-mass"]
        plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_4j_2b_met180_passMET_Zhmass", do_scale=True, doLogY=False, write=write)

        signals = ["Zh_300_ZZ4b","Zh_500_ZZ4b","Zh_800_ZZ4b"]
        labels = ["300, ZZ 4b", "500, ZZ4b", "800, ZZ 4b"]
        sel="(met>180 && m_h2_min_dR>70 && m_h2_min_dR<100 && m_h1_min_dR>70 && m_h1_min_dR<100 && jets_n>=4 && pass_MET && bjets_77_n>=2)*(weight_mc*weight_lumi)"
        write=["#bf{#it{ATLAS}} Internal","#geq 4 jets, 2b77, passMET, met 180","ZZ-mass"]
        plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_4j_2b_met180_passMET_ZZmass", do_scale=True, doLogY=False, write=write)

        """
