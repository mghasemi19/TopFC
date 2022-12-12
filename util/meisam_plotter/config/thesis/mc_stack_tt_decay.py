import os
from plot_utils import *

json_file = "json_example/strong_prod.json"


# selection to be applied 
sel_1 = "((jets_n>=4) &&  (met>200) && (signal_electrons_n+signal_muons_n>=1) && pass_MET && bjets_n>=3)"
label_sel_1 = "1L_3b"

sel_2 = "((dphi_min>0.4) && (jets_n>=4) &&  (met>200) && (signal_electrons_n+signal_muons_n==0) && pass_MET && bjets_n>=3)"
label_sel_2 = "0L_3b"

selections = dict()
selections[label_sel_1] = sel_1
selections[label_sel_2] = sel_2

# luminosity (to scale MC)
lumi = 36100.0
# produce plots with log scale on Y axis
logY = True
do_scale = False # doesn't do anything for now!


"""
ttbar_channel = "(channel_number==407342 || channel_number==407343 || channel_number==407344 || channel_number==410470)"
myslice_1 = ["!"+ttbar_channel, "ttbar_decay_type<6 &&"+ttbar_channel,"ttbar_decay_type>=6 && "+ttbar_channel] # ttbar_decay_type >5 --> singke lep, ttbar_decay_type <= 5 --> dilepton
labels_slice_1 = ["non-t#bar{t}", "t#bar{t} dilep","t#bar{t} sin-lep"]
label_comp_1 = "semilep_dilep"

myslice_2 = ["!"+ttbar_channel, "ttbar_decay_type<6 &&"+ttbar_channel, "ttbar_decay_type>=6 && ttbar_decay_type<=9 &&"+ttbar_channel, "ttbar_decay_type>=10 && ttbar_decay_type<=13 &&"+ttbar_channel, "ttbar_decay_type>=14 && ttbar_decay_type<=17 &&"+ttbar_channel]
labels_slice_2 = ["non-t#bar{t}", "t#bar{t} dilep","e+jets","#mu+jets","#tau+jets"]
label_comp_2 = "semilep_comp"

compositions = dict()
#compositions[label_comp_1]=[myslice_1, labels_slice_1]
compositions[label_comp_2]=[myslice_2, labels_slice_2]
"""

ttbar_channel = "(channel_number==410000 || channel_number==407009 || channel_number==407010 || channel_number==407011 || channel_number==407012 || channel_number==407322 || channel_number==407323)" 

myslice_tt = [ttbar_channel+" && "+"ttbar_decay_type==0", ttbar_channel+" && "+"ttbar_decay_type==1", ttbar_channel+" && "+"ttbar_decay_type==2", ttbar_channel+" && "+"ttbar_decay_type==3", ttbar_channel+" && "+"ttbar_decay_type==4", ttbar_channel+" && "+"ttbar_decay_type==5",ttbar_channel+" && "+"ttbar_decay_type>=6 && ttbar_decay_type<=9", ttbar_channel+" && "+"ttbar_decay_type>=10 && ttbar_decay_type<=13", ttbar_channel+" && "+"ttbar_decay_type>=14 && ttbar_decay_type<=17", "!"+ttbar_channel]
labels_slice_tt = ["ee","e#mu", "e#tau", "#mu#mu", "#mu#tau","#tau#tau","e+jets","#mu+jets","#tau+jets","Non t#bar{t}"]
label_comp_tt = "tt_dec"

backgrounds_name=["multijet","diboson","Zjets","Wjets","TopEW","SingleTop","ttbar"]
backgrounds = [b + "_NoSys" for b in backgrounds_name]

compositions = dict()
compositions[label_comp_tt]=[myslice_tt, labels_slice_tt]


# define the output folder (and create it if it doesn't exist)
folder_out="plots/mc_stack_strong/"
os.system("mkdir -p "+folder_out)
for sel in selections:
    os.system("mkdir -p "+folder_out+sel)
    for comp in compositions:
        os.system("mkdir -p "+folder_out+sel+"/"+comp)

# create the dictionaty that points to the correct input file for each background and for data

name_infile=dict()
for b in backgrounds:
#    name_infile[b] = "/eos/atlas/user/c/crizzi/susy_multib/HFinputs_merged/SUSYHF_tag2.4.28-0-0/Bkg_2.4.28-0-0_skim_2b_with_wei.root"
#name_infile['multijet_NoSys'] = "/eos/atlas/user/c/crizzi/susy_multib/HFinputs_merged/SUSYHF_tag2.4.28-0-0/Bkg_2.4.28-0-0_multijet_skim_2b_NoSys_with_wei.root"
    name_infile[b] = "/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.2.4.37/Bkg_tag.2.4.37-0-X_nominal_and_qcd3b.root"
name_infile_data="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.2.4.33-2-0/Data_tag.2.4.33-2-0.root"
name_infile_signal="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.2.4.33-2-0/Sig_GGM_tag.2.4.33-2-0_nominal_3b_0L_met_all.root" # not used in this version
name_infile["Data"] = ["/eos/atlas/user/c/crizzi/susy_multib/ntuples_HF/tag21.2.18_2b/Data_21.2.18_20152016.root"]
#,"/eos/atlas/user/c/crizzi/susy_multib/ntuples_HF/tag21.2.18_2b/Data_21.2.18_2017.root"]

# create myweights, a *single* string with the weights to be used sepatated by a *
weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
myweights = "*".join(weights)
#region_composition(json_file, ["multijet_NoSys"]+backgrounds, myweights, name_infile, ["Multijet"]+labels, slices=["1"], region=region_sel, name_can="Gbb_bkg", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")



# lsit of things to write on the plot
write_1L=["C. Rizzi PhD Thesis, Simulation, 36.1 fb^{-1}","#geq 1 lepton, #geq 3 b-jets, #geq 4 jets,", "E_{T}^{miss}>200 GeV"]
write_0L=["C. Rizzi PhD Thesis, Simulation, 36.1 fb^{-1}","0 lepton, #geq 3 b-jets, #geq 4 jets,", "E_{T}^{miss} > 200 GeV, #Delta#phi^{4j}_{min}>0.4"]
# Here I organize the vatiables that I want to plot in a list that I can loop on. This is not strictly necessary but can be useful
# I've chosen to have a list of dictionaries, that put together different arguments of data_mc associated to the same variable. Also this is not mandatory
var_def=[]
#var_def += [{'def':("pt_lep_1",20,0,1000),'leg':"p_{T} Leading lepton [GeV]"}]
#var_def += [{'def':("meff_incl",30, 0,3000),'leg':"m_{eff} [GeV]"}]
#var_def += [{'def':("bjets_n",4, 1.5,5.5),'leg':"Number of b-jets"}]
var_def += [{'def':("mT",20,0,500),'leg':"m_{T}  [GeV]"}]
#var_def += [{'def':("jets_n",6, 3.5,9.5),'leg':"Number of jets"}]
#var_def += [{'def':("met",18,200.,1000),'leg':"E_{T}^{miss} [GeV]"}]
var_def += [{'def':("mTb_min",20,0,500),'leg':"m_{T}^{b,min}  [GeV]"}]
#var_def += [{'def':("pt_jet_1",20,0,1000),'leg':"p_{T} Leading jet [GeV]"}]
#var_def += [{'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
#var_def += [{'def':("pt_bjet_1",20,0,1000),'leg':"p_{T} Leading b-jet [GeV]", "bvar":"pt_bjet_1_tt"}]
#var_def += [{'def':("pt_bjet_2",20,0,1000),'leg':"p_{T} Sub-leading b-jet [GeV]", "bvar":"pt_bjet_2_tt"}]
#var_def += [{'def':("pt_jet_2",20,0,1000),'leg':"p_{T} Sub-leading jet [GeV]"}]
#var_def += [{'def':("pt_jet_3",20,0,1000),'leg':"p_{T} 3-rd jet [GeV]"}]
#var_def += [{'def':("pt_jet_4",20,0,1000),'leg':"p_{T} 4th jet [GeV]"}]
#var_def += [{'def':("MJSum_rc_r08pt10",32,0,800),'leg':"MJSum"}]

# loop on all the variables that you want to plot
for var in var_def:
    # this is just to define the name of the pdf file: if the key 'can' is in the dictionaly that will be the name, otherwise the name of the variable is used
    if "can" in var.keys():
        name_can = var['can']
    else:
        name_can = var['def'][0]
    # fianlly, the data_mc finction is called

    for sel in selections:
        _backgrounds=backgrounds
        if "1L" in sel:
            write = write_1L            
        else:
            write = write_0L
        if "0L" in sel and compositions[comp][0][0]=="1":
            _labels = ['Multijet']+labels
        else:
            _labels = compositions[comp][1]
        for comp in compositions:
            mc_stack(var['def'], selections[sel], myweights, _backgrounds, name_infile, _labels, var['leg'], lumi, logY, write, folder_out+sel+"/"+comp+"/", name_can, do_scale=False, add_signal = False, slices=compositions[comp][0])
    #plot_var(var['def'], sel+"*("+myweights+")", backgrounds, name_infile, labels, var['leg'], "1", folder_out, name_can, lumi, logY, write)


