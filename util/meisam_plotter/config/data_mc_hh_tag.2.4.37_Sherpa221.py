import os
from plot_utils import *

# selection to be applied 
# luminosity (to scale MC)
lumi = 36074.56
# produce plots with log scale on Y axis
logY = True
do_scale = False # doesn't do anything for now!

# define the output folder (and create it if it doesn't exist)
folder_out="plots/data_mc_2.4.37_ZCR/"
os.system("mkdir -p "+folder_out)

# backgrounds (names as in the input file, except removing "_NoSys")
backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar"]
# backgrounds (as you want them in the legend)
labels = ["diboson","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}"]

# create the dictionaty that points to the correct input file for each background and for data
name_infile=dict()
name_infile_bkg = "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.37-0-X_tmp/Bkg_tag.2.4.37-0-X_nominal_and_qcd.root"
#name_infile_bkg = "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.37-0-X_Sherpa221/Bkg_tag.2.4.37-0-X_nominal.root"
name_infile_data= "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.37-0-X_tmp/Data_tag.2.4.37-0-X.root"

for b in backgrounds:
    print b
    name_infile[b] = name_infile_bkg
    name_infile[b+"_NoSys"] = name_infile_bkg
name_infile["Data"] = name_infile_data

# create myweights, a *single* string with the weights to be used sepatated by a *
sel="(((signal_muon_trig_pass && signal_muons_n==2) || (signal_electron_trig_pass && signal_electrons_n==2)) && pt_lep_1>60 && jets_n>=4 && bjets_n>=2 && signal_leptons_n==2 && ZCR_met>200 && fabs(Z_mass-91.2)<5 && Z_OSLeps && ZCR_meff_4bj>700 && max(DeltaR_h1_dR,DeltaR_h2_dR)<3)"
myweights="(weight_mc*weight_lumi*weight_btag*weight_elec*weight_muon*weight_jvt*weight_WZ_2_2*weight_elec_trigger*weight_muon_trigger)"


# lsit of things to write on the plot
write=["#bf{#it{ATLAS}} Internal","36.1 fb^{-1}"]

# Here I organize the vatiables that I want to plot in a list that I can loop on. This is not strictly necessary but can be useful
# I've chosen to have a list of dictionaries, that put together different arguments of data_mc associated to the same variable. Also this is not mandatory
var_def=[]
var_def += [{'def':("bjets_n",4, 1.5,5.5),'leg':"Number of b-jets"}]
var_def += [{'def':("jets_n",6, 3.5,9.5),'leg':"Number of jets"}]
var_def += [{'def':("met",18,200.,1000),'leg':"E_{T}^{miss} [GeV]"}]
var_def += [{'def':("ZCR_met",18,200.,1000),'leg':"E_{T}^{miss} [GeV]"}]
var_def += [{'def':("mTb_min",20,0,500),'leg':"m_{T}^{b,min}  [GeV]"}]
var_def += [{'def':("ZCR_mTb_min",20,0,500),'leg':"m_{T}^{b,min}  [GeV]"}]
var_def += [{'def':("meff_incl",30, 0,3000),'leg':"m_{eff} [GeV]"}]
var_def += [{'def':("ZCR_meff_incl",60, 0,3000),'leg':"m_{eff} [GeV]"}]
var_def += [{'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
var_def += [{'def':("ZCR_dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_dR"}]
var_def += [{'def':("meff_4bj",20,300,1300),'leg':"meff 4b [GeV]"}]
var_def += [{'def':("ZCR_meff_4bj",10,600,1300),'leg':"meff 4b [GeV]"}]
var_def += [{'def':("pt_jet_1",10,0,1000),'leg':"p_{T} Leading jet [GeV]"}]
var_def += [{'def':("pt_bjet_1",10,0,1000),'leg':"p_{T} Leading b-jet [GeV]", "bvar":"pt_bjet_1_tt"}]
var_def += [{'def':("pt_bjet_2",10,0,1000),'leg':"p_{T} Sub-leading b-jet [GeV]", "bvar":"pt_bjet_2_tt"}]
var_def += [{'def':("pt_jet_1",10,0,1000),'leg':"p_{T} Leading jet [GeV]"}]
var_def += [{'def':("pt_jet_2",10,0,1000),'leg':"p_{T} Sub-leading jet [GeV]"}]
var_def += [{'def':("pt_jet_3",10,0,1000),'leg':"p_{T} 3-rd jet [GeV]"}]
var_def += [{'def':("pt_jet_4",10,0,1000),'leg':"p_{T} 4th jet [GeV]"}]
var_def += [{'def':("mass_h1_dR",15,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_dR"}]
var_def += [{'def':("mass_h2_dR",15,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_min_dR"}]
var_def += [{'def':("met_sig",15,0,30),'leg':"MET/#sqrt{H_{T}}   [#sqrt{GeV}]"}]


# loop on all the variables that you want to plot
for var in var_def:
    # this is just to define the name of the pdf file: if the key 'can' is in the dictionaly that will be the name, otherwise the name of the variable is used
    if "can" in var.keys():
        name_can = var['can']
    else:
        name_can = var['def'][0]
    #name_can+="_Vjets221"
    # fianlly, the data_mc finction is called
    data_mc (var['def'], sel, myweights, backgrounds, name_infile, labels, var['leg'], lumi, logY, write, folder_out, name_can, do_scale=False, add_signal = False)


