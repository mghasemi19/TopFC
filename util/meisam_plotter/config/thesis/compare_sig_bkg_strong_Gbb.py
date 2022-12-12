import os
from plot_utils import *

sel_1 = "((jets_n>=4) &&  (met>200) && (signal_electrons_n+signal_muons_n>=1) && pass_MET && bjets_n>=3)"
label_sel_1 = "1L_3b"

sel_2 = "((dphi_min>0.4) && (jets_n>=4) &&  (met>200) && (signal_electrons_n+signal_muons_n==0) && pass_MET && bjets_n>=3)"
label_sel_2 = "0L_3b"

sel_3 = "((jets_n>=4) &&  (met>200) && ((signal_electrons_n+signal_muons_n==0 && (dphi_min>0.4)) || signal_electrons_n+signal_muons_n>=1) && pass_MET && bjets_n>=3)"
label_sel_3 = "01L_3b"

selections = dict()
selections[label_sel_1] = sel_1
selections[label_sel_2] = sel_2
selections[label_sel_3] = sel_3

# luminosity (to scale MC)
lumi = 36074.56
# produce plots with log scale on Y axis
logY = True
do_scale = False # doesn't do anything for now!

# lsit of things to write on the plot
#write=["#bf{#it{ATLAS}} Internal","#geq3b, #geq4J, E_{T}^{miss}>200 GeV, D#phi>0.4","36.1 fb^{-1}"]
#write_1L=["C. Rizzi PhD Thesis, Simulation, 36.1 fb^{-1}","#geq 1 lepton, #geq 3 b-jets, #geq 4 jets,", "E_{T}^{miss}>200 GeV"]
#write_0L=["C. Rizzi PhD Thesis, Simulation, 36.1 fb^{-1}","0 lepton, #geq 3 b-jets, #geq 4 jets,", "E_{T}^{miss} > 200 GeV, #Delta#phi^{4j}_{min}>0.4"]
write_1L=["C. Rizzi PhD Thesis","Simulation, #sqrt{s}=13 TeV, 36.1 fb^{-1}","#geq 1 lepton, #geq 3 b-jets, #geq 4 jets,", "E_{T}^{miss}>200 GeV","Gbb model"]
write_0L=["C. Rizzi PhD Thesis","Simulation, #sqrt{s}=13 TeV, 36.1 fb^{-1}","0 lepton, #geq 3 b-jets, #geq 4 jets,", "E_{T}^{miss} > 200 GeV, #Delta#phi^{4j}_{min}>0.4","Gbb model"]
write_01L=["C. Rizzi PhD Thesis","Simulation, #sqrt{s}=13 TeV, 36.1 fb^{-1}","#geq 3 b-jets, #geq 4 jets, E_{T}^{miss} > 200 GeV,","#Delta#phi^{4j}_{min}>0.4 if 0L","Gbb model"]


# Here I organize the vatiables that I want to plot in a list that I can loop on. This is not strictly necessary but can be useful
# I've chosen to have a list of dictionaries, that put together different arguments of data_mc associated to the same variable. Also this is not mandatory
var_def=[]
var_def += [{'def':("baseline_electrons_n+baseline_muons_n",4, -0.5,3.5),'leg':"Number of baseline leptons", 'can':"lep_n"}]
var_def += [{'def':("met",8,200.,1000),'leg':"E_{T}^{miss} [GeV]"}]
var_def += [{'def':("jets_n",8, 3.5, 11.5),'leg':"Number of jets"}]
#var_def += [{'def':("pt_jet_1",10,0,1000),'leg':"p_{T} Leading jet [GeV]"}]
var_def += [{'def':("bjets_n",4, 1.5,5.5),'leg':"Number of b-jets"}]
var_def += [{'def':("mTb_min",20,0,500),'leg':"m_{T}^{b,min}  [GeV]"}]
var_def += [{'def':("meff_incl",22, 500,4000),'leg':"m_{eff} [GeV]"}]
var_def += [{'def':("dphi_min",10,0,3.4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
var_def += [{'def':("dphi_1jet",17,0,3.4),'leg':"#Delta#phi^{min}(j-1,MET)"}]
var_def += [{'def':("pt_jet_1",13,0,1300),'leg':"p_{T} jet 1 [GeV]"}]
var_def += [{'def':("pt_jet_2",13,0,1300),'leg':"p_{T} jet 2 [GeV]"}]
var_def += [{'def':("pt_jet_3",13,0,1300),'leg':"p_{T} jet 3 [GeV]"}]
var_def += [{'def':("pt_jet_4",26,0,1300),'leg':"p_{T} jet 4 [GeV]"}]
var_def += [{'def':("pt_bjet_1",40,0,2000),'leg':"p_{T} b-jet 1 [GeV]"}]
var_def += [{'def':("pt_bjet_2",28,0,1400),'leg':"p_{T} b-jet 2 [GeV]"}]
var_def += [{'def':("MJSum_rc_r08pt10",20,0,1000),'leg':"M_{J}^{#Sigma} [GeV]"}]
var_def += [{'def':("pt_lep_1",40,0,2000),'leg':"p_{T} lepton 1 [GeV]"}]
var_def += [{'def':("mT",24,0,1200),'leg':"m_{T}  [GeV]"}]
var_def += [{'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
var_def += [{'def':("pt_bjet_1",10,0,1000),'leg':"p_{T} Leading b-jet [GeV]", "bvar":"pt_bjet_1_tt"}]
var_def += [{'def':("pt_bjet_2",10,0,1000),'leg':"p_{T} Sub-leading b-jet [GeV]", "bvar":"pt_bjet_2_tt"}]
var_def += [{'def':("pt_jet_2",10,0,1000),'leg':"p_{T} Sub-leading jet [GeV]"}]

"""
#var_def += [{'def':("gen_filt_met",18,200.,1000),'leg':"E_{T}^{miss} Gen [GeV]"}]
#var_def += [{'def':("gen_filt_ht",18,200.,1000),'leg':"H_{T}^{miss} Gen [GeV]"}]
var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",15,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_dR"}]
var_def += [{'def':("meff_4bj",20,300,1300),'leg':"meff 4b [GeV]"}]
var_def += [{'def':("pt_bjet_1",10,0,1000),'leg':"p_{T} Leading b-jet [GeV]", "bvar":"pt_bjet_1_tt"}]
var_def += [{'def':("pt_bjet_2",10,0,1000),'leg':"p_{T} Sub-leading b-jet [GeV]", "bvar":"pt_bjet_2_tt"}]
var_def += [{'def':("pt_jet_2",10,0,1000),'leg':"p_{T} Sub-leading jet [GeV]"}]
var_def += [{'def':("mass_h1_dR",15,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_dR"}]
var_def += [{'def':("mass_h2_dR",15,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_min_dR"}]
var_def += [{'def':("met_sig",15,0,30),'leg':"MET/#sqrt{H_{T}}   [#sqrt{GeV}]"}]
"""
#labels=["nominal","ttbar_rad_high","ttbar_rad_low","ttbar_PhHppEG","ttbar_MGPy8EG","ttbar_aMcAtNlo","ttbar_PhPy8EG","ttbar_PhHppEG_H7UE","ttbar_Sherpa_221","ttbar_Sherpa_220"]
#to_compare=[["ttbar"],["ttbar_rad_high"],["ttbar_rad_low"],["ttbar_PhHppEG"],["ttbar_MGPy8EG"],["ttbar_aMcAtNlo"],["ttbar_PhPy8EG"],["ttbar_PhHppEG_H7UE"],["ttbar_Sherpa_221"],["ttbar_Sherpa_220"]]

#common=["diboson_NoSys","Zjets_NoSys","Wjets_NoSys","TopEW_NoSys","SingleTop_NoSys"]
common=[]

# put to true the one you want to plot
folder_out="plots/sig_bkg_strong/"
if True:
    labels=["Background","m(#tilde{g})=2.1 TeV, m(#tilde{#chi}^{0})=1 GeV","m(#tilde{g})=1.9 TeV, m(#tilde{#chi}^{0})=600 GeV"," m(#tilde{g})=1.9 TeV,m(#tilde{#chi}^{0})=1.8 TeV"]
    to_compare=[["ttbar_NoSys","Wjets_220_NoSys","Zjets_220_NoSys","diboson_NoSys","SingleTop_NoSys","TopEW_NoSys"],["Gbb_2100_1_NoSys"],["Gbb_1900_600_NoSys"],["Gbb_1900_1800_NoSys"]]


# define the output folder (and create it if it doesn't exist)
os.system("mkdir -p "+folder_out)
for sel in selections:
    os.system("mkdir -p "+folder_out+sel)


# create myweights, a *single* string with the weights to be used sepatated by a *
wei_list=[]
weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
myweights = "*".join(weights)
for i in range(len(labels)):
    if i ==-1:
        wei_list.append("1")
    else:
        wei_list.append(myweights)

name_infile_bkg = "/nfs/pic.es/user/c/crizzi/scratch2/susy_multib/HF_inputs/SUSYHF_tag2.4.28/Bkg_2.4.28-0-0_skim_3b_meffRw_ttHFweight.root"
name_infile_data= "/nfs/pic.es/user/c/crizzi/scratch2/susy_multib/HF_inputs/SUSYHF_tag2.4.28/Data_2.4.28-0-0_skim_2b.root"
name_infile_sig = "/nfs/pic.es/user/c/crizzi/scratch2/susy_multib/HF_inputs/SUSYHF_tag2.4.28/Sig_2.4.28-0-0_with_wei.root"
# create the dictionaty that points to the correct input file for each background and for data
name_infile_list=[]
for i in range(len(labels)):
    name_infile_1=dict()
    for tc in to_compare[i]:
        if i ==0:
            name_infile_1[tc] = name_infile_bkg
        else:            
            name_infile_1[tc] = name_infile_sig
    name_infile_list.append(name_infile_1)

# loop on all the variables that you want to plot
for var in var_def:
    # this is just to define the name of the pdf file: if the key 'can' is in the dictionaly that will be the name, otherwise the name of the variable is used
    if "can" in var.keys():
        name_can = var['can']
    else:
        name_can = var['def'][0]
    name_can = "Gbb_compare_"+name_can
    # fianlly, the data_mc finction is called

    for sel in selections:
        print sel
        if "1L" in sel:
            write = write_1L            
        elif "0L" in sel:
            write = write_0L
        else:
            write = write_01L
        compare (var['def'], selections[sel], wei_list, to_compare, name_infile_list, labels, var['leg'], lumi, logY, write, folder_out+sel+"/", name_can, do_scale=False, is_first_data=False, x1leg = 0.49 , y1leg = 0.63, do_ratio=False, scale_max = 3,leg_size=17, text_size=20)


