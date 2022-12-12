import glob, os
import plot_utils
from plot_utils import *

lumi = 36074.56 # Moriond 2017

name_infile_signal="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-0-3_TOPQ1_mini_tree/mini_ntuples_v6.root"

outfolder="./2017_07_05/"


if __name__ == "__main__":

    os.system("mkdir -p "+outfolder)

    #+++++++++++++++++
    # EFFICIENCY PLOTS
    #+++++++++++++++++

    # produce a plot in which on the x axis there are the different signal mases, on the y-axis the efficiency of a certain selection (all the ones in num_sel, and the plot will have one line for each) with respect to a common selection (the one in den_sel)
    
    # these are the masses that will be on the x-axis
    masses=["130","150","200","300","400","500","600","800"]
    # event weights (do not change)
    weights=["weight_lumi","weight_mc","weight_btag"]
    name_infile = dict()
    # tell the code where to find the input file (do not change)
    for m in masses:
        name_infile[m] = name_infile_signal

    # in this case I want to see the fraction of times that I have a certain number of b-jets
    num_sel=["bjets_n_60>=3","bjets_n_70>=3","bjets_n_77>=3","bjets_n_85>=3"]
    legend = ["#geq 3b 60","#geq 3b 70","#geq 3b 77","#geq 3b 85"]
    den_sel = "is_hh_4b"
    signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "eff_3bjets_hh4b.pdf")

    # in this case I want to see the fraction of times that a certain reconstruction algorithm gives the correct matching (once you have implemented the new algorithms, you will need to add them here)
    num_sel=["good_match_min_diff", "good_match_min_dR", "good_match_max_pt"]
    legend = ["min-diff", "min-dR","max-pT"]
    den_sel = "is_hh_4b && match_possible && pass_MET && met>180 && jets_n>=4 && bjets_n_85>=3 && dphi_min>0.4"
    signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "best_match_if_match_possible_presel.pdf")


    # ++++++++++++++
    # DISTRIBUTIONS
    # ++++++++++++++

    # here I want to check what some variables look like for some signal masses

    # list that contains all the variables that I want to plot
    var_def=[]
    # 'def': variable to plot: (name, nbins, x-low, x-max)
    # 'leg': label of the x-axis
    # 'can': name of the canvas (without .pdf). If not present, will be the same one as 'def'. Necessary only when 'def' has a formula in it

    # to add new variables, just add another line with var_def += ... and just follow this schema :)
    var_def += [{'def':("met",20,0.,800),'leg':"E_{T}^{miss} [GeV]"}]
    var_def += [{'def':("bjets_n_77",6, -0.5,5.5),'leg':"Number of b-jets 77%"}]
    var_def += [{'def':("max(dR_h2_min_dR,dR_h1_min_dR)",15,0,5), 'leg':'max( dR(b1_{h1},b2_{h1}), dR(b1_{h2},b2_{h2}) )','can':"dRmax_min_dR"}]
    var_def += [{'def':("m_h1_min_diff",30,50,200),'leg':"m(1) [GeV]",'can':"mass_h1_min_diff"}]
    var_def += [{'def':("pt_trueb1_h1",16, 0,800),'leg':"true-b_{1} from h_{1} p_{T} [GeV]"}]


    myslice = ["1"]
    # which signals to plot
    signals = ["hh_150","hh_200","hh_500","hh_800"]
    # labels for the legend (mind the order, has to be same as above)
    labels = ["m(#tilde{#chi}) = 150 GeV","m(#tilde{#chi}) = 200 GeV","m(#tilde{#chi}) = 500 GeV","m(#tilde{#chi}) = 800 GeV"]

    # tell the code where to find each signal, this doesn't need to be changed
    for m in signals:
        name_infile[m] = name_infile_signal

    for var in var_def:
        if "can" in var.keys():
            name_can = var['can']
        else:
            name_can = var['def'][0]

        # selection to be applied before plotting the variables
        # note: weight_mc*weight_lumi is essential
        sel="(jets_n>=4 && pass_MET && bjets_n_77>=3)*(weight_mc*weight_lumi)"
        # list of things to write on the plot
        write=["#bf{#it{ATLAS}} Internal","#geq 4 jets, 3b77, passMET"]
        plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_300_4j_3b_passMET", do_scale=True, doLogY=False, write=write)

