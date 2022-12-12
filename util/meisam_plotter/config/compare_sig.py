import os
from plot_utils import *

# selection to be applied 
#sel = "(dphi_min>0.4) && (jets_n>=4) && (jets_n<=6) &&  (met>200) && (baseline_electrons_n+baseline_muons_n==0) && pass_MET && bjets_n>=3"
sel = "(jets_n>=4) &&  (met>200) && signal_leptons_n>=1 && bjets_n>=2"
# luminosity (to scale MC)
lumi = 36074.56
# produce plots with log scale on Y axis
logY = False
do_scale = False # doesn't do anything for now!

# define the output folder (and create it if it doesn't exist)
folder_out="plots/tt_signal/"
os.system("mkdir -p "+folder_out)

# lsit of things to write on the plot
#write=["#bf{#it{ATLAS}} Internal","#geq3b, #geq4J, E_{T}^{miss}>200 GeV, D#phi>0.4","36.1 fb^{-1}"]
#write=["#bf{#it{ATLAS}} Internal","0L, #geq2b, #geq4J, E_{T}^{miss}>200 GeV, D#phi>0.4","36.1 fb^{-1}"]
write=["#geq 4 jets, E_{T}^{miss}>200 GeV, #geq 1L, #geq 2b","Normalized to unit area"] 

# Here I organize the vatiables that I want to plot in a list that I can loop on. This is not strictly necessary but can be useful
# I've chosen to have a list of dictionaries, that put together different arguments of data_mc associated to the same variable. Also this is not mandatory
var_def=[]
#var_def += [{'def':("baseline_electrons_n+baseline_muons_n",4, -0.5,3.5),'leg':"Number of baseline leptons", 'can':"lep_n"}]
var_def += [{'def':("bjets_n",4, 1.5,5.5),'leg':"Number of b-jets"}]
#var_def += [{'def':("jets_n",6, 3.5,9.5),'leg':"Number of jets"}]
var_def += [{'def':("met",18,200.,1000),'leg':"E_{T}^{miss} [GeV]"}]
#var_def += [{'def':("gen_filt_met",18,200.,1000),'leg':"E_{T}^{miss} Gen [GeV]"}]
#var_def += [{'def':("gen_filt_ht",18,200.,1000),'leg':"H_{T}^{miss} Gen [GeV]"}]
var_def += [{'def':("mTb_min",20,0,500),'leg':"m_{T}^{b,min}  [GeV]"}]
var_def += [{'def':("mT",20,0,500),'leg':"m_{T}  [GeV]"}]
var_def += [{'def':("meff_incl",60, 0,3000),'leg':"m_{eff} [GeV]"}]
#var_def += [{'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
#var_def += [{'def':("pt_jet_1",20,0,1000),'leg':"p_{T} Leading jet [GeV]"}]
#var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_dR"}]
#var_def += [{'def':("meff_4bj",20,300,1300),'leg':"meff 4b [GeV]"}]
#var_def += [{'def':("pt_bjet_1",20,0,1000),'leg':"p_{T} Leading b-jet [GeV]", "bvar":"pt_bjet_1_tt"}]
#var_def += [{'def':("pt_bjet_2",20,0,1000),'leg':"p_{T} Sub-leading b-jet [GeV]", "bvar":"pt_bjet_2_tt"}]
#var_def += [{'def':("pt_jet_1",20,300,1300),'leg':"p_{T} Leading jet [GeV]"}]
#var_def += [{'def':("pt_jet_2",20,0,1000),'leg':"p_{T} Sub-leading jet [GeV]"}]
#var_def += [{'def':("mass_h1_dR",30,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_dR"}]
#var_def += [{'def':("mass_h2_dR",30,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_min_dR"}]
#var_def += [{'def':("met_sig",30,0,30),'leg':"MET/#sqrt{H_{T}}   [#sqrt{GeV}]"}]

#labels=["nominal","ttbar_rad_high","ttbar_rad_low","ttbar_PhHppEG","ttbar_MGPy8EG","ttbar_aMcAtNlo","ttbar_PhPy8EG","ttbar_PhHppEG_H7UE","ttbar_Sherpa_221","ttbar_Sherpa_220"]
#to_compare=[["ttbar"],["ttbar_rad_high"],["ttbar_rad_low"],["ttbar_PhHppEG"],["ttbar_MGPy8EG"],["ttbar_aMcAtNlo"],["ttbar_PhPy8EG"],["ttbar_PhHppEG_H7UE"],["ttbar_Sherpa_221"],["ttbar_Sherpa_220"]]

#common=["diboson","Zjets","Wjets","TopEW","SingleTop"]
#labels=["Data","PP6, no RW","PP6, RW"]
#to_compare=[["Data"],common+["ttbar"],common+["ttbar"]]

labels=["Gtt 2000,1 GeV","t#bar{t}"]
to_compare=[["Gtt_2000_5000_1"],["ttbar"]]

# create myweights, a *single* string with the weights to be used sepatated by a *
wei_list=[]
weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
myweights = "*".join(weights)
for i in range(len(labels)):
    #if i ==0:
    #    wei_list.append("1")
    #elif i==1:
    #    wei_list.append(myweights+"*weight_ttbar_NNLO")
    #else:
    wei_list.append(myweights)

name_infile_sig = "/eos/user/g/gstark/MBJ/Sig_21.2.18_mc16a.Gtt.root"
name_infile_tt= "/eos/user/g/gstark/MBJ/Bkg_21.2.18_mc16a.ttbar.root"

# create the dictionaty that points to the correct input file for each background and for data
name_infile_list=[]
for i in range(len(labels)):
    name_infile_1=dict()
    if i ==0:
        name_infile_1[to_compare[i][0]]=name_infile_sig
    else:
        for tc in to_compare[i]:
            name_infile_1[tc] = name_infile_tt
    #name_infile_list.append(name_infile_1)
    name_infile_list.append(name_infile_1)

# loop on all the variables that you want to plot
for var in var_def:
    # this is just to define the name of the pdf file: if the key 'can' is in the dictionaly that will be the name, otherwise the name of the variable is used
    if "can" in var.keys():
        name_can = var['can']
    else:
        name_can = var['def'][0]
    #name_can += "_ttbar_rw"
    # fianlly, the data_mc finction is called
    compare (var['def'], sel, wei_list, to_compare, name_infile_list, labels, var['leg'], lumi, logY, write, folder_out, name_can, do_scale=True, is_first_data=False)


