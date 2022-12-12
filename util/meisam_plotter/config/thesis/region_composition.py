import os
from plot_utils import *

json_file = "json_example/strong_prod.json"

# luminosity (to scale MC)
lumi = 36100.0

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


# define the output folder (and create it if it doesn't exist)
folder_out="plots/tt_comp_36ifb/"
os.system("mkdir -p "+folder_out)
for sel in selections:
    os.system("mkdir -p "+folder_out+sel)
    for comp in compositions:
        os.system("mkdir -p "+folder_out+sel+"/"+comp)
"""
# backgrounds (names as in the input file, except removing "_NoSys")
#backgrounds_name=["multijet","diboson","Zjets_220","Wjets_220","TopEW","SingleTop","ttbar"]
backgrounds_name=["diboson","Zjets_220","Wjets_220","TopEW","SingleTop","ttbar"]
backgrounds = [b + "_NoSys" for b in backgrounds_name]
# backgrounds (as you want them in the legend)
#labels = ["Multijet","Diboson","Z+jets","W+jets","t#bar{t}+X","Single top","t#bar{t}"]
labels = ["Diboson","Z+jets","W+jets","t#bar{t}+X","Single top","t#bar{t}"]

# create the dictionaty that points to the correct input file for each background and for data

name_infile=dict()
for b in backgrounds:
    name_infile[b] = "/eos/atlas/user/c/crizzi/susy_multib/HFinputs_merged/SUSYHF_tag2.4.28-0-0/Bkg_2.4.28-0-0_skim_3b_with_wei.root"
name_infile['multijet_NoSys'] = "/eos/atlas/user/c/crizzi/susy_multib/HFinputs_merged/SUSYHF_tag2.4.28-0-0/Bkg_2.4.28-0-0_multijet_skim_3b_with_wei.root"
"""
name_infile["diboson"] = "/eos/atlas/user/c/crizzi/susy_multib/ntuples_HF/tag21.2.18_2b/Bkg_21.2.18_mc16a.diboson.root"
name_infile["Z_jets"] = "/eos/atlas/user/c/crizzi/susy_multib/ntuples_HF/tag21.2.18_2b/Bkg_21.2.18_mc16a.Z_jets.root"
name_infile["W_jets"] = "/eos/atlas/user/c/crizzi/susy_multib/ntuples_HF/tag21.2.18_2b/Bkg_21.2.18_mc16a.W_jets.root"
name_infile["topEW"] = "/eos/atlas/user/c/crizzi/susy_multib/ntuples_HF/tag21.2.18_2b/Bkg_21.2.18_mc16a.topEW.root"
name_infile["singletop"] = "/eos/atlas/user/c/crizzi/susy_multib/ntuples_HF/tag21.2.18_2b/Bkg_21.2.18_mc16a.singletop.root"
name_infile["ttbar"] = "/eos/atlas/user/c/crizzi/susy_multib/ntuples_HF/tag21.2.18_2b/Bkg_21.2.18_mc16a.ttbar.root"
"""
name_infile_data="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.2.4.33-2-0/Data_tag.2.4.33-2-0.root"

name_infile_signal="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.2.4.33-2-0/Sig_GGM_tag.2.4.33-2-0_nominal_3b_0L_met_all.root" # not used in this version

name_infile["Data"] = ["/eos/atlas/user/c/crizzi/susy_multib/ntuples_HF/tag21.2.18_2b/Data_21.2.18_20152016.root"]
#,"/eos/atlas/user/c/crizzi/susy_multib/ntuples_HF/tag21.2.18_2b/Data_21.2.18_2017.root"]

# create myweights, a *single* string with the weights to be used sepatated by a *
weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2*seednom*weight_qcd_scale"]
myweights = "*".join(weights)

"""
region_sel = "CR_Gtt_1L_B,VR1_Gtt_1L_B,VR2_Gtt_1L_B,SR_Gtt_1L_B,CR_Gtt_1L_M,VR1_Gtt_1L_M,VR2_Gtt_1L_M,SR_Gtt_1L_M,CR_Gtt_1L_C,VR1_Gtt_1L_C,VR2_Gtt_1L_C,SR_Gtt_1L_C"
region_composition(json_file,  backgrounds,myweights, name_infile, labels, slices=["1"], region=region_sel, name_can="Gtt_1L_bkg", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")

region_sel = "CR_Gtt_0L_B,VR_Gtt_0L_B,SR_Gtt_0L_B,CR_Gtt_0L_M,VR_Gtt_0L_M,SR_Gtt_0L_M,CR_Gtt_0L_C,VR_Gtt_0L_C,SR_Gtt_0L_C"
region_composition(json_file, ["multijet_NoSys"]+backgrounds, myweights, name_infile, ["Multijet"]+labels, slices=["1"], region=region_sel, name_can="Gtt_0L_bkg", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")

region_sel = "CR_Gbb_B,VR_Gbb_B,SR_Gbb_B,CR_Gbb_M,VR_Gbb_M,SR_Gbb_M,CR_Gbb_C,VR_Gbb_C,SR_Gbb_C,CR_Gbb_VC,VR_Gbb_VC,SR_Gbb_VC"
region_composition(json_file, ["multijet_NoSys"]+backgrounds, myweights, name_infile, ["Multijet"]+labels, slices=["1"], region=region_sel, name_can="Gbb_bkg", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")

region_sel = "CR_Hnj_Hmeff,VR0L_Hnj_Hmeff,VR1L_Hnj_Hmeff,SR0L_Hnj_Hmeff,SR1L_Hnj_Hmeff,CR_Hnj_Imeff,VR0L_Hnj_Imeff,VR1L_Hnj_Imeff,SR0L_Hnj_Imeff,SR1L_Hnj_Imeff,CR_Hnj_Lmeff,VR0L_Hnj_Lmeff,VR1L_Hnj_Lmeff,SR0L_Hnj_Lmeff,SR1L_Hnj_Lmeff"
region_composition(json_file, ["multijet_NoSys"]+backgrounds, myweights, name_infile, ["Multijet"]+labels, slices=["1"], region=region_sel, name_can="Hnj_bkg", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")

region_sel = "CR_Inj_Imeff,VR0L_Inj_Imeff,VR1L_Inj_Imeff,SR0L_Inj_Imeff,SR1L_Inj_Imeff,CR_Inj_Lmeff,VR0L_Inj_Lmeff,VR1L_Inj_Lmeff,SR0L_Inj_Lmeff,SR1L_Inj_Lmeff"
region_composition(json_file, ["multijet_NoSys"]+backgrounds, myweights, name_infile, ["Multijet"]+labels, slices=["1"], region=region_sel, name_can="Inj_bkg", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")

region_sel = "CR_Lnj_Hmeff,VR0L_Lnj_Hmeff,SR0L_Lnj_Hmeff,CR_Lnj_Imeff,VR0L_Lnj_Imeff,SR0L_Lnj_Imeff,CR_Lnj_Lmeff,VR0L_Lnj_Lmeff,SR0L_Lnj_Lmeff,CR_IStR,VR0L_IStR,SR0L_IStR"
region_composition(json_file, ["multijet_NoSys"]+backgrounds, myweights, name_infile, ["Multijet"]+labels, slices=["1"], region=region_sel, name_can="Lnj_bkg", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")

myslice=["ttbar_class==0","ttbar_class<0","ttbar_class>0"]
backgrounds=["ttbar_NoSys"]
labels = ["t#bar{t} + light","t#bar{t} + #geq 1 c","t#bar{t} + #geq 1 b"]

region_sel = "CR_Gtt_1L_B,VR1_Gtt_1L_B,VR2_Gtt_1L_B,SR_Gtt_1L_B,CR_Gtt_1L_M,VR1_Gtt_1L_M,VR2_Gtt_1L_M,SR_Gtt_1L_M,CR_Gtt_1L_C,VR1_Gtt_1L_C,VR2_Gtt_1L_C,SR_Gtt_1L_C"
region_composition(json_file,  backgrounds,myweights, name_infile, labels, slices=myslice, region=region_sel, name_can="Gtt_1L_HF", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")

region_sel = "CR_Gtt_0L_B,VR_Gtt_0L_B,SR_Gtt_0L_B,CR_Gtt_0L_M,VR_Gtt_0L_M,SR_Gtt_0L_M,CR_Gtt_0L_C,VR_Gtt_0L_C,SR_Gtt_0L_C"
region_composition(json_file, backgrounds, myweights, name_infile, labels, slices=myslice, region=region_sel, name_can="Gtt_0L_HF", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")

region_sel = "CR_Gbb_B,VR_Gbb_B,SR_Gbb_B,CR_Gbb_M,VR_Gbb_M,SR_Gbb_M,CR_Gbb_C,VR_Gbb_C,SR_Gbb_C,CR_Gbb_VC,VR_Gbb_VC,SR_Gbb_VC"
region_composition(json_file, backgrounds, myweights, name_infile, labels, slices=myslice, region=region_sel, name_can="Gbb_HF", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")

region_sel = "CR_Hnj_Hmeff,VR0L_Hnj_Hmeff,VR1L_Hnj_Hmeff,SR0L_Hnj_Hmeff,SR1L_Hnj_Hmeff,CR_Hnj_Imeff,VR0L_Hnj_Imeff,VR1L_Hnj_Imeff,SR0L_Hnj_Imeff,SR1L_Hnj_Imeff,CR_Hnj_Lmeff,VR0L_Hnj_Lmeff,VR1L_Hnj_Lmeff,SR0L_Hnj_Lmeff,SR1L_Hnj_Lmeff"
region_composition(json_file, backgrounds, myweights, name_infile, labels, slices=myslice, region=region_sel, name_can="Hnj_HF", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")

region_sel = "CR_Inj_Imeff,VR0L_Inj_Imeff,VR1L_Inj_Imeff,SR0L_Inj_Imeff,SR1L_Inj_Imeff,CR_Inj_Lmeff,VR0L_Inj_Lmeff,VR1L_Inj_Lmeff,SR0L_Inj_Lmeff,SR1L_Inj_Lmeff"
region_composition(json_file, backgrounds, myweights, name_infile, labels, slices=myslice, region=region_sel, name_can="Inj_HF", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")

region_sel = "CR_Lnj_Hmeff,VR0L_Lnj_Hmeff,SR0L_Lnj_Hmeff,CR_Lnj_Imeff,VR0L_Lnj_Imeff,SR0L_Lnj_Imeff,CR_Lnj_Lmeff,VR0L_Lnj_Lmeff,SR0L_Lnj_Lmeff,CR_IStR,VR0L_IStR,SR0L_IStR"
region_composition(json_file, backgrounds, myweights, name_infile, labels, slices=myslice, region=region_sel, name_can="Lnj_HF", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")

"""

#name_infile["ttbar_NoSys"] = "/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.2.4.37/tag.2.4.37-0-X_skim/ttbar_tag.2.4.37-0-X_useMET300400_3b_0L_met_br_wei.root"
name_infile["ttbar_NoSys"] = "/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.2.4.37/Bkg_tag.2.4.37-0-X_nominal_and_qcd3b.root"
myslice = ["ttbar_decay_type==0", "ttbar_decay_type==1", "ttbar_decay_type==2", "ttbar_decay_type==3", "ttbar_decay_type==4", "ttbar_decay_type==5","ttbar_decay_type>=6 && ttbar_decay_type<=9", "ttbar_decay_type>=10 && ttbar_decay_type<=13", "ttbar_decay_type>=14 && ttbar_decay_type<=17"]

labels = ["ee","e#mu", "e#tau", "#mu#mu", "#mu#tau","#tau#tau","e+jets","#mu+jets","#tau+jets"]
backgrounds=["ttbar_NoSys"]
weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
myweights = "*".join(weights)


region_sel = "CR_Gtt_1L_B,VR1_Gtt_1L_B,VR2_Gtt_1L_B,SR_Gtt_1L_B,CR_Gtt_1L_M,VR1_Gtt_1L_M,VR2_Gtt_1L_M,SR_Gtt_1L_M,CR_Gtt_1L_C,VR1_Gtt_1L_C,VR2_Gtt_1L_C,SR_Gtt_1L_C"
region_composition(json_file,  backgrounds,myweights, name_infile, labels, slices=myslice, region=region_sel, name_can="Gtt_1L_tt", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")

#region_sel = "CR_Gtt_0L_B,VR_Gtt_0L_B,SR_Gtt_0L_B,CR_Gtt_0L_M,VR_Gtt_0L_M,SR_Gtt_0L_M,CR_Gtt_0L_C,VR_Gtt_0L_C,SR_Gtt_0L_C"
#region_composition(json_file, backgrounds, myweights, name_infile, labels, slices=myslice, region=region_sel, name_can="Gtt_0L_tt", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")

#region_sel = "CR_Gbb_B,VR_Gbb_B,SR_Gbb_B,CR_Gbb_M,VR_Gbb_M,SR_Gbb_M,CR_Gbb_C,VR_Gbb_C,SR_Gbb_C,CR_Gbb_VC,VR_Gbb_VC,SR_Gbb_VC"
#region_composition(json_file, backgrounds, myweights, name_infile, labels, slices=myslice, region=region_sel, name_can="Gbb_tt", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")

region_sel = "CR_Hnj_Hmeff,VR0L_Hnj_Hmeff,VR1L_Hnj_Hmeff,SR0L_Hnj_Hmeff,SR1L_Hnj_Hmeff,CR_Hnj_Imeff,VR0L_Hnj_Imeff,VR1L_Hnj_Imeff,SR0L_Hnj_Imeff,SR1L_Hnj_Imeff,CR_Hnj_Lmeff,VR0L_Hnj_Lmeff,VR1L_Hnj_Lmeff,SR0L_Hnj_Lmeff,SR1L_Hnj_Lmeff"
region_composition(json_file, backgrounds, myweights, name_infile, labels, slices=myslice, region=region_sel, name_can="Hnj_tt", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")

region_sel = "CR_Inj_Imeff,VR0L_Inj_Imeff,VR1L_Inj_Imeff,SR0L_Inj_Imeff,SR1L_Inj_Imeff,CR_Inj_Lmeff,VR0L_Inj_Lmeff,VR1L_Inj_Lmeff,SR0L_Inj_Lmeff,SR1L_Inj_Lmeff"
region_composition(json_file, backgrounds, myweights, name_infile, labels, slices=myslice, region=region_sel, name_can="Inj_tt", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")

region_sel = "CR_Lnj_Hmeff,VR0L_Lnj_Hmeff,SR0L_Lnj_Hmeff,CR_Lnj_Imeff,VR0L_Lnj_Imeff,SR0L_Lnj_Imeff,CR_Lnj_Lmeff,VR0L_Lnj_Lmeff,SR0L_Lnj_Lmeff,CR_IStR,VR0L_IStR,SR0L_IStR"
region_composition(json_file, backgrounds, myweights, name_infile, labels, slices=myslice, region=region_sel, name_can="Lnj_tt", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots/")


# plot_var to compare the shapes of different backgrounds
# compare to compare with also ratio panel - but doesn't allow comparing different selections of the same backgrounds

"""
# lsit of things to write on the plot
write_1L=["#bf{#it{ATLAS}} Internal, 21.2.18","1L, #geq2b, #geq4J, E_{T}^{miss}>200 GeV","36.1 fb^{-1}"]
write_0L=["#bf{#it{ATLAS}} Internal, 21.2.18","0L, #geq2b, #geq4J, E_{T}^{miss}>200 GeV, D#phi>0.4","36.1 fb^{-1}"]
# Here I organize the vatiables that I want to plot in a list that I can loop on. This is not strictly necessary but can be useful
# I've chosen to have a list of dictionaries, that put together different arguments of data_mc associated to the same variable. Also this is not mandatory
var_def=[]
var_def += [{'def':("pt_lep_1",20,0,1000),'leg':"p_{T} Leading lepton [GeV]"}]
var_def += [{'def':("meff_incl",30, 0,3000),'leg':"m_{eff} [GeV]"}]
var_def += [{'def':("bjets_n",4, 1.5,5.5),'leg':"Number of b-jets"}]
var_def += [{'def':("mT",20,0,500),'leg':"m_{T}  [GeV]"}]
var_def += [{'def':("jets_n",6, 3.5,9.5),'leg':"Number of jets"}]
var_def += [{'def':("met",18,200.,1000),'leg':"E_{T}^{miss} [GeV]"}]
var_def += [{'def':("mTb_min",20,0,500),'leg':"m_{T}^{b,min}  [GeV]"}]
var_def += [{'def':("pt_jet_1",20,0,1000),'leg':"p_{T} Leading jet [GeV]"}]
var_def += [{'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
var_def += [{'def':("pt_bjet_1",20,0,1000),'leg':"p_{T} Leading b-jet [GeV]", "bvar":"pt_bjet_1_tt"}]
var_def += [{'def':("pt_bjet_2",20,0,1000),'leg':"p_{T} Sub-leading b-jet [GeV]", "bvar":"pt_bjet_2_tt"}]
var_def += [{'def':("pt_jet_2",20,0,1000),'leg':"p_{T} Sub-leading jet [GeV]"}]
var_def += [{'def':("pt_jet_3",20,0,1000),'leg':"p_{T} 3-rd jet [GeV]"}]
var_def += [{'def':("pt_jet_4",20,0,1000),'leg':"p_{T} 4th jet [GeV]"}]
var_def += [{'def':("MJSum_rc_r08pt10",32,0,800),'leg':"MJSum"}]

# loop on all the variables that you want to plot
for var in var_def:
    # this is just to define the name of the pdf file: if the key 'can' is in the dictionaly that will be the name, otherwise the name of the variable is used
    if "can" in var.keys():
        name_can = var['can']
    else:
        name_can = var['def'][0]
    # fianlly, the data_mc finction is called

    for sel in selections:
        if "1L" in sel:
            write = write_1L
        else:
            write = write_0L
        for comp in compositions:
            data_mc (var['def'], selections[sel], myweights, backgrounds, name_infile, compositions[comp][1], var['leg'], lumi, logY, write, folder_out+sel+"/"+comp+"/", name_can, do_scale=False, add_signal = False, slices=compositions[comp][0])
    #plot_var(var['def'], sel+"*("+myweights+")", backgrounds, name_infile, labels, var['leg'], "1", folder_out, name_can, lumi, logY, write)

"""
