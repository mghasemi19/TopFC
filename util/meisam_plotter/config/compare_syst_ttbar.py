import os
from plot_utils import *

# selection to be applied 
#sel = "(dphi_min>0.4) && (jets_n>=4) && (jets_n<=6) &&  (met>200) && (baseline_electrons_n+baseline_muons_n==0) && pass_MET && bjets_n>=3"
sel = "(dphi_min>0.4) && (jets_n>=4) &&  (met>200) && pass_MET && bjets_n>=3"
# luminosity (to scale MC)
lumi = 36074.56
# produce plots with log scale on Y axis
logY = True
do_scale = False # doesn't do anything for now!

# define the output folder (and create it if it doesn't exist)
folder_out="plots/ttbar_syst_with_data/"
os.system("mkdir -p "+folder_out)

# lsit of things to write on the plot
#write=["#bf{#it{ATLAS}} Internal","#geq3b, #geq4J, E_{T}^{miss}>200 GeV, D#phi>0.4","36.1 fb^{-1}"]
write=["#bf{#it{ATLAS}} Internal","0L, #geq3b, #geq4J, E_{T}^{miss}>200 GeV, D#phi>0.4","36.1 fb^{-1}"]

# Here I organize the vatiables that I want to plot in a list that I can loop on. This is not strictly necessary but can be useful
# I've chosen to have a list of dictionaries, that put together different arguments of data_mc associated to the same variable. Also this is not mandatory
var_def=[]
#var_def += [{'def':("baseline_electrons_n+baseline_muons_n",4, -0.5,3.5),'leg':"Number of baseline leptons", 'can':"lep_n"}]
var_def += [{'def':("met",10,200.,700),'leg':"E_{T}^{miss} [GeV]"}]
var_def += [{'def':("jets_n",6, 3.5,9.5),'leg':"Number of jets"}]
"""
var_def += [{'def':("bjets_n",4, 1.5,5.5),'leg':"Number of b-jets"}]
#var_def += [{'def':("gen_filt_met",18,200.,1000),'leg':"E_{T}^{miss} Gen [GeV]"}]
#var_def += [{'def':("gen_filt_ht",18,200.,1000),'leg':"H_{T}^{miss} Gen [GeV]"}]
var_def += [{'def':("mTb_min",20,0,500),'leg':"m_{T}^{b,min}  [GeV]"}]
var_def += [{'def':("meff_incl",60, 0,3000),'leg':"m_{eff} [GeV]"}]
var_def += [{'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
var_def += [{'def':("pt_jet_1",10,0,1000),'leg':"p_{T} Leading jet [GeV]"}]
var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",15,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_dR"}]
var_def += [{'def':("meff_4bj",20,300,1300),'leg':"meff 4b [GeV]"}]
var_def += [{'def':("pt_bjet_1",10,0,1000),'leg':"p_{T} Leading b-jet [GeV]", "bvar":"pt_bjet_1_tt"}]
var_def += [{'def':("pt_bjet_2",10,0,1000),'leg':"p_{T} Sub-leading b-jet [GeV]", "bvar":"pt_bjet_2_tt"}]
var_def += [{'def':("pt_jet_1",10,0,1000),'leg':"p_{T} Leading jet [GeV]"}]
var_def += [{'def':("pt_jet_2",10,0,1000),'leg':"p_{T} Sub-leading jet [GeV]"}]
var_def += [{'def':("mass_h1_dR",15,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_dR"}]
var_def += [{'def':("mass_h2_dR",15,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_min_dR"}]
var_def += [{'def':("met_sig",15,0,30),'leg':"MET/#sqrt{H_{T}}   [#sqrt{GeV}]"}]
"""
#labels=["nominal","ttbar_rad_high","ttbar_rad_low","ttbar_PhHppEG","ttbar_MGPy8EG","ttbar_aMcAtNlo","ttbar_PhPy8EG","ttbar_PhHppEG_H7UE","ttbar_Sherpa_221","ttbar_Sherpa_220"]
#to_compare=[["ttbar"],["ttbar_rad_high"],["ttbar_rad_low"],["ttbar_PhHppEG"],["ttbar_MGPy8EG"],["ttbar_aMcAtNlo"],["ttbar_PhPy8EG"],["ttbar_PhHppEG_H7UE"],["ttbar_Sherpa_221"],["ttbar_Sherpa_220"]]

common=["diboson_NoSys","Zjets_NoSys","Wjets_NoSys","TopEW_NoSys","SingleTop_NoSys"]
labels=["Data","nominal","rad_high","rad_low"]#,"PhHppEG","aMcAtNlo","PhPy8EG"]#,"PhHppEG_H7UE","Sherpa_221","Sherpa_220"]
to_compare=[["Data"],common+["ttbar_NoSys"],common+["ttbar_rad_high_NoSys"],common+["ttbar_rad_low_NoSys"]]#  ,common+["ttbar_PhHppEG"],common+["ttbar_aMcAtNlo"],common+["ttbar_PhPy8EG"]]#,["ttbar_PhHppEG_H7UE"],["ttbar_Sherpa_221"],["ttbar_Sherpa_220"]]


# create myweights, a *single* string with the weights to be used sepatated by a *
wei_list=[]
weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
myweights = "*".join(weights)
for i in range(len(labels)):
    if i ==0:
        wei_list.append("1")
    else:
        wei_list.append(myweights)

name_infile_bkg = "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.33-5-0_3b/Bkg_tag.2.4.33-5-0_3b.root"
name_infile_data= "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.33-5-0_3b/Data_tag.2.4.33-5-0_3b.root"
name_infile_tt_syst="/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.33-5-0_3b_ttbar_syst/ttbar_syst_and_nom_tag.2.4.33-5-0_3b_useMET300400_nominal.root"
name_infile_tt_nom= "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.33-5-0_3b/Bkg_tag.2.4.33-5-0_3b.root"
# create the dictionaty that points to the correct input file for each background and for data
name_infile_list=[]
for i in range(len(labels)):
    name_infile_1=dict()
    if i ==0:
        name_infile_1[to_compare[i][0]]=name_infile_data
    elif i==1:
        for tc in to_compare[i]:
            if "ttbar" in tc:
                name_infile_1[tc] = name_infile_tt_nom
            else:            
                name_infile_1[tc] = name_infile_bkg
    else:
        for tc in to_compare[i]:
            if "ttbar" in tc:
                name_infile_1[tc] = name_infile_tt_syst
            else:            
                name_infile_1[tc] = name_infile_bkg
    name_infile_list.append(name_infile_1)

# loop on all the variables that you want to plot
for var in var_def:
    # this is just to define the name of the pdf file: if the key 'can' is in the dictionaly that will be the name, otherwise the name of the variable is used
    if "can" in var.keys():
        name_can = var['can']
    else:
        name_can = var['def'][0]
    name_can += "_ttbar_syst_3b"
    # fianlly, the data_mc finction is called
    compare (var['def'], sel, wei_list, to_compare, name_infile_list, labels, var['leg'], lumi, logY, write, folder_out, name_can, do_scale=False, is_first_data=True)


