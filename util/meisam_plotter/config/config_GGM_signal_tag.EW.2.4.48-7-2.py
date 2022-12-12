import glob, os
import plot_utils
from plot_utils import *

lumi = 36074.56 # Moriond 2017

remove_meff_corr=False
add_signal = False


folder_in="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-7-2/"


#name_infile_signal="../create_mini_tree/mini_trees_hh_v3_4btypes.root"
name_infile_signal=folder_in+"Sig_GGM_tagEW.2.4.28-7-2_SUSY7_nominal_all_2b2L_or_3b0L_loose.root"

name_infile_data=folder_in+"Data_tagEW.2.4.28-7-2_SUSY7_2b2L_or_3b0L_loose.root"
#name_infile_bkg=folder_in+"bkg_tagEW.2.4.28-1_nominal.root"
name_infile_bkg=folder_in+"Bkg_tagEW.2.4.28-7-2_SUSY7_METfilt_nominal_2b2L_or_3b0L_loose.root"
name_infile_QCD=folder_in+""


folder_out="./2017_07_13_SUSY7/"


if __name__ == "__main__":

    os.system("mkdir -p "+folder_out)

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
    #var_def += [{'def':("met",20,0.,1000),'leg':"E_{T}^{miss} [GeV]"}]

    #var_def += [{'def':("mTb_min",15,0,300),'leg':"m_{T}^{min}(b,MET) [GeV]"}]
    #var_def += [{'def':("jets_n",11, -0.5,10.5),'leg':"Number of jets"}]
    #var_def += [{'def':("met_sig",12,0,30),'leg':"MET/#sqrt{H_{T}}   [#sqrt{GeV}]"}]
    var_def += [{'def':("met",10,200.,700),'leg':"E_{T}^{miss} [GeV]"}]
    var_def += [{'def':("DeltaR_bb",15, 0,5),'leg':"dR(b,b)",'can':'dR_bb'}]
    var_def += [{'def':("mass_bb",15,50,200),'leg':"m(b,b) [GeV]"}]
    var_def += [{'def':("Z_mass",14,60,200),'leg':"m(l,l) [GeV]",'can':"mass_ll"}]
    var_def += [{'def':("Z_pt",10,50,550),'leg':"p_{T}(l,l) [GeV]",'can':"pt_ll"}]
    #var_def += [{'def':("bjets_n",4, 1.5,5.5),'leg':"Number of b-jets"}]
    #var_def += [{'def':("pt_bjet_1",20,0,1000),'leg':"p_{T} Leading b-jet [GeV]", "bvar":"pt_bjet_1_tt"}]
    #var_def += [{'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]

    #var_def += [{'def':("meff_incl",18, 200,2000),'leg':"m_{eff} [GeV]"}]
    #var_def += [{'def':("met+pt_lep_1+pt_bjet_1+pt_bjet_2",30, 0,3000),'leg':"m_{eff}^{2b,1L} [GeV]",'can':"meff_2b1L"}]

    #
    #var_def += [{'def':("mTb_min",20,0,500),'leg':"m_{T}^{b,min}  [GeV]", "bvar":"mTb_min_tt"}]
    #var_def += [{'def':("pt_bjet_2",20,0,1000),'leg':"p_{T} Sub-leading b-jet [GeV]", "bvar":"pt_bjet_2_tt"}]
    #var_def += [{'def':("meff_incl",60, 0,3000),'leg':"m_{eff} [GeV]"}]
    #var_def += [{'def':("jets_n",6, 3.5,9.5),'leg':"Number of jets"}]
    #var_def += [{'def':("pt_jet_1",20,0,1000),'leg':"p_{T} Leading jet [GeV]"}]
    #var_def += [{'def':("pt_jet_2",20,0,1000),'leg':"p_{T} Sub-leading jet [GeV]"}]
    #var_def += [{'def':("mass_h1_dR",30,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_dR"}]
    #var_def += [{'def':("mass_h2_dR",30,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_min_dR"}]
    #var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_dR"}] 
    #var_def += [{'def':("pt_bjet_3",20,0,1000),'leg':"p_{T} 3rd b-jet [GeV]", "bvar":"pt_bjet_3_tt"}]
    #var_def += [{'def':("pt_bjet_4",20,0,1000),'leg':"p_{T} 4th b-jet [GeV]", "bvar":"pt_bjet_4_tt"}]

    
    myslice = ["1"]

    for var in var_def:
        # list of things to write on the plot
        #print var['def']
        if "can" in var.keys():
            name_can = var['can']
        else:
            name_can = var['def'][0]

        sel="pass_MET && met>200 && jets_n>=2 && bjets_n_77==2 && signal_leptons_n==2 && Z_OSLeps"

        signals = ["GGM_Zh_300_Zhllbb","GGM_Zh_500_Zhllbb","GGM_Zh_800_Zhllbb"]
        labels_sig = ["m(#tilde{#chi}) = 300 GeV","m(#tilde{#chi}) = 500 GeV","m(#tilde{#chi}) = 800 GeV"]

        for m in signals:
            name_infile[m] = name_infile_signal        

        backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar"]
        for b in backgrounds:  
            name_infile[b]= name_infile_bkg  
        name_infile["Data"] = name_infile_data

        labels_bkg = ["diboson","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}"]

        #plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_Zh", do_scale=True, doLogY=False, write=write)

        #sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_Zh", signals, labels)


        weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
        myweights = "*".join(weights)
        print myweights
        write=["#bf{#it{ATLAS}} Internal","=2 OS-SF L, =2b, E_{T}^{miss}>200 GeV","36.1 fb^{-1}"]
        data_mc (var['def'], sel, myweights, backgrounds, name_infile, labels_bkg, var['leg'], lumi, True, write, folder_out, name_can, do_scale=False, add_signal = False)
