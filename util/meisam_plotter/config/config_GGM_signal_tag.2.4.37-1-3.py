import glob, os
import plot_utils
from plot_utils import *

lumi = 36074.56 # Moriond 2017

remove_meff_corr=False
add_signal = False

pickle_sel="../../cuts_pickle/sel_wei_dict_presel.pickle"
pickle_sel_no_wei="../../cuts_pickle/sel_dict_presel.pickle"

folder_in="/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.37-1-3/"

name_infile_data=folder_in
name_infile=folder_in
name_infile_QCD=folder_in

name_infile_signal=folder_in+"Sig_GGM_tag.2.4.37-1-3_nominal.root"

outfolder="./2018_06_07/"


if __name__ == "__main__":

    os.system("mkdir -p "+outfolder)

    #masses=["130","150","200","250","300","400","500","600","700","800","900","1000"]
    masses=["200","300","400","500","600","700","800","900","1000"]
    weights=["weight_lumi","weight_mc"]
    name_infile = dict()
    for m in masses:
        name_infile[m] = name_infile_signal

    new_sel_h1 = "((pt_h1_dR<189 && mass_h1_dR>105 && mass_h1_dR<135) || (pt_h1_dR>189 && pt_h1_dR<225 && mass_h1_dR>110 && mass_h1_dR<135) || (pt_h1_dR>225 && pt_h1_dR<261 && mass_h1_dR>115 && mass_h1_dR<135) || (pt_h1_dR>261 && pt_h1_dR<297 && mass_h1_dR>115 && mass_h1_dR<135) || (pt_h1_dR>297 && pt_h1_dR<333 && mass_h1_dR>110 && mass_h1_dR<135) || (pt_h1_dR>333 && pt_h1_dR<369 && mass_h1_dR>115 && mass_h1_dR<130) || (pt_h1_dR>369 && pt_h1_dR<423 && mass_h1_dR>120 && mass_h1_dR<135) || (pt_h1_dR>423 && pt_h1_dR<427 && mass_h1_dR>120 && mass_h1_dR<135) || (pt_h1_dR>427 && pt_h1_dR<549 && mass_h1_dR>120 && mass_h1_dR<135) || (pt_h1_dR>549 && mass_h1_dR>120 && mass_h1_dR<135))"

    new_sel_h2 = "((pt_h2_dR<117 && mass_h2_dR>65 && mass_h2_dR<115) || (pt_h2_dR>117 && pt_h2_dR<153 && mass_h2_dR>70 && mass_h2_dR<120) || (pt_h2_dR>153 && pt_h2_dR<189 && mass_h1_dR>75 && mass_h2_dR<125) || (pt_h2_dR>189 && pt_h2_dR<225 && mass_h2_dR>80 && mass_h2_dR<125) || (pt_h2_dR>225 && pt_h2_dR<261 && mass_h2_dR>85 && mass_h2_dR<125) || (pt_h2_dR>261 && pt_h2_dR<297 && mass_h1_dR>90 && mass_h2_dR<125) || (pt_h2_dR>297 && pt_h2_dR<333 && mass_h2_dR>95 && mass_h2_dR<125) || (pt_h2_dR>333 && pt_h2_dR<387 && mass_h2_dR>95 && mass_h2_dR<125) || (pt_h2_dR>387 && pt_h2_dR<441 && mass_h2_dR>105 && mass_h2_dR<125) || (pt_h2_dR>441 && pt_h2_dR<531 && mass_h2_dR>110 && mass_h2_dR<130) || (pt_h2_dR>531 && mass_h2_dR>110 && mass_h2_dR<135))"

    old_sel_h1 = "mass_h1_dR>110 && mass_h1_dR<150"
    old_sel_h2 = "mass_h2_dR>90 && mass_h2_dR<140"

    num_sel=[old_sel_h1, new_sel_h1]
    legend = ["old sel h1","new sel h1"]
    den_sel = "hh_type==10 && met>200 && bjets_n>=3 && jets_n>=4"
    signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "h1_hh4b_met200_4j_3b.pdf")

    num_sel=[old_sel_h2, new_sel_h2]
    legend = ["old sel h2","new sel h2"]
    den_sel = "hh_type==10 && met>200 && bjets_n>=3 && jets_n>=4"
    signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "h2_hh4b_met200_4j_3b.pdf")

    num_sel=["("+old_sel_h1+") && ("+old_sel_h2+")", "("+new_sel_h1+") && ("+new_sel_h2+")"]
    legend = ["old sel h1 and h2","new sel h1 and h2"]
    den_sel = "hh_type==10 && met>200 && bjets_n>=3 && jets_n>=4"
    signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "h1_h2_hh4b_met200_4j_3b.pdf")


    # +++++++++++++
    # Data/MC plots
    # +++++++++++++
    var_def=[]
    # 'def': variable to plot: (name, nbins, x-low, x-max)
    # 'leg': legend of the x-axis
    #var_def += [{'def':("meff_4bj",20,300,1300),'leg':"meff 4b [GeV]"}]
    #var_def += [{'def':("mTb_min",20,0,500),'leg':"m_{T}^{b,min}  [GeV]", "bvar":"mTb_min_tt"}]
    #var_def += [{'def':("met",18,200.,1000),'leg':"E_{T}^{miss} [GeV]"}]
    #var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_dR"}] 
    #var_def += [{'def':("met_sig",20,0.,20),'leg':"E_{T}^{miss}/#sqrt{HT}"}]

    #var_def += [{'def':("bjets_n",4, 1.5,5.5),'leg':"Number of b-jets"}]
    #var_def += [{'def':("mTb_min",20,0,500),'leg':"m_{T}^{b,min}  [GeV]", "bvar":"mTb_min_tt"}]
    #var_def += [{'def':("pt_bjet_1",20,0,1000),'leg':"p_{T} Leading b-jet [GeV]", "bvar":"pt_bjet_1_tt"}]
    #var_def += [{'def':("pt_bjet_2",20,0,1000),'leg':"p_{T} Sub-leading b-jet [GeV]", "bvar":"pt_bjet_2_tt"}]
    #var_def += [{'def':("meff_incl",60, 0,3000),'leg':"m_{eff} [GeV]"}]
    #var_def += [{'def':("jets_n",6, 3.5,9.5),'leg':"Number of jets"}]
    #var_def += [{'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
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

        sel="(jets_n>=4 && pass_MET && bjets_n_77>=3)*(weight_mc*weight_lumi*weight_btag)"
        write=["#bf{#it{ATLAS}} Internal","#geq 4 jets, 3b77, passMET"]

        signals = ["GGM_hh_300_hh4b","GGM_hh_500_hh4b","GGM_hh_800_hh4b"]
        labels = ["m(#tilde{#chi}) = 300 GeV","m(#tilde{#chi}) = 500 GeV","m(#tilde{#chi}) = 800 GeV"]
        for m in signals:
            name_infile[m] = name_infile_signal        
        plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_hh", do_scale=True, doLogY=False, write=write)

        signals = ["GGM_Zh_300_Zh4b","GGM_Zh_500_Zh4b","GGM_Zh_800_Zh4b"]
        labels = ["m(#tilde{#chi}) = 300 GeV","m(#tilde{#chi}) = 500 GeV","m(#tilde{#chi}) = 800 GeV"]
        for m in signals:
            name_infile[m] = name_infile_signal        
        #plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_Zh", do_scale=True, doLogY=False, write=write)

        signals = ["GGM_Zh_300_ZZ4b","GGM_Zh_500_ZZ4b","GGM_Zh_800_ZZ4b"]
        labels = ["m(#tilde{#chi}) = 300 GeV","m(#tilde{#chi}) = 500 GeV","m(#tilde{#chi}) = 800 GeV"]
        for m in signals:
            name_infile[m] = name_infile_signal        
        #plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_ZZ", do_scale=True, doLogY=False, write=write)
