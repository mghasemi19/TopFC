import glob, os
from plot_utils import *

# luminosity (to scale MC)
lumi = 36074.56 # Moriond 2017
# produce plots with log scale on Y axis
logY = True
do_scale = False # doesn't do anything for now!

# define the output folder (and create it if it doesn't exist)
outfolder="./plots_example_sig_vs_bkg/"
os.system("mkdir -p "+outfolder)

# backgrounds (names as in the input file, except removing "_NoSys")
backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar"]
# backgrounds (as you want them in the legend)
labels_bkg = ["diboson","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}"]
# same for signal
signals=["GGM_hh_400_hhall","GGM_hh_800_hhall"]
labels_sig = ["m(#tilde{#chi}) = 400 GeV","m(#tilde{#chi}) = 800 GeV"]

# create the dictionaty that points to the correct input file for each background and for signals
name_infile = dict()
# note: these files have a >=3b skim
folder_in="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.2.4.33-5-0_3b/"
name_infile_bkg=folder_in+"Bkg_tag.2.4.33-5-0_3b.root"
name_infile_signal=folder_in+"Sig_GGM_tag.2.4.33-5-0_3bAll.root"
for b in backgrounds:
    name_infile[b]= name_infile_bkg
for s in signals:
    name_infile[s] = name_infile_signal
    
# selection to be applied. NOTE: it includes the weights!!
sel="(pass_MET && met>200 && jets_n>=4 && bjets_n>=3 && (baseline_electrons_n+baseline_muons_n)==0)*(weight_mc*weight_lumi*weight_btag*weight_elec*weight_muon*weight_jvt*weight_WZ_2_2)"
# lsit of things to write on the plot
write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}"]

    
# Here I organize the vatiables that I want to plot in a list that I can loop on. This is not strictly necessary but can be useful
# I've chosen to have a list of dictionaries, that put together different arguments of data_mc associated to the same variable. Also this is not mandatory
var_def=[]
var_def += [{'def':("bjets_n",4, 1.5,5.5),'leg':"Number of b-jets"}]
var_def += [{'def':("meff_4bj",20,300,1300),'leg':"meff 4b [GeV]"}]
var_def += [{'def':("mTb_min",20,0,500),'leg':"m_{T}^{b,min}  [GeV]", "bvar":"mTb_min_tt"}]
var_def += [{'def':("pt_bjet_1",20,0,1000),'leg':"p_{T} Leading b-jet [GeV]", "bvar":"pt_bjet_1_tt"}]
var_def += [{'def':("pt_bjet_2",20,0,1000),'leg':"p_{T} Sub-leading b-jet [GeV]", "bvar":"pt_bjet_2_tt"}]
var_def += [{'def':("met",20,0.,1000),'leg':"E_{T}^{miss} [GeV]"}]
var_def += [{'def':("jets_n",6, 3.5,9.5),'leg':"Number of jets"}]
var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_dR"}] 

# loop on all the variables that you want to plot
for var in var_def:
    # this is just to define the name of the pdf file: if the key 'can' is in the dictionaly that will be the name, otherwise the name of the variable is used
    if "can" in var.keys():
        name_can = var['can']
    else:
        name_can = var['def'][0]
        # fianlly, the sig_bkg finction is called
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, logY, write, do_scale, outfolder, name_can, signals, labels_sig)     
