import os
from plot_utils import *

json_file = "json_example/hh_regions.json"

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
backgrounds=["multijet_NoSys","diboson_NoSys","Zjets_NoSys","Wjets_NoSys","TopEW_NoSys","SingleTop_NoSys","ttbar_NoSys"]
# backgrounds (as you want them in the legend)
labels = ["Multijet","Diboson","Z+jets","W+jets","t#bar{t}+X","Single top","t#bar{t}"]

# create the dictionaty that points to the correct input file for each background and for data

name_infile=dict()
for b in backgrounds:
    name_infile[b] = "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.37-0-X_skim/Bkg_tag.2.4.37-0-X_useMET300400_3b_0L_met_br_wei.root"
name_infile['multijet_NoSys'] = "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/qcd_trisha_from_calum/qcd_br_wei.root"

# create myweights, a *single* string with the weights to be used sepatated by a *
weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
myweights = "*".join(weights)

###################
# bkg composition #
###################

region_sel = "CR_3b_meff1,VR_3b_meff1_A,SR_3b_meff1_A,CR_3b_meff2,VR_3b_meff2_A,SR_3b_meff2_A,CR_3b_meff3,VR_3b_meff3_A,SR_3b_meff3_A"
#region_composition(json_file,  backgrounds,myweights, name_infile, labels, slices=["1"], region=region_sel, name_can="hh_3b_bkg", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots_ewk/")

region_sel = "CR_4b_meff1,VR_4b_meff1_A,SR_4b_meff1_A,SR_4b_meff1_A_disc,VR_4b_meff1_B,SR_4b_meff1_B,CR_4b_meff2,VR_4b_meff2_A,SR_4b_meff2_A,VR_4b_meff2_B,SR_4b_meff2_B"
#region_composition(json_file,  backgrounds,myweights, name_infile, labels, slices=["1"], region=region_sel, name_can="hh_4b_bkg", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots_ewk/")

#####################
# HF classification #
#####################

myslice=["ttbar_class==0","ttbar_class<0","ttbar_class>0"]
backgrounds=["ttbar_NoSys"]
labels = ["t#bar{t} + light","t#bar{t} + #geq 1 c","t#bar{t} + #geq 1 b"]

region_sel = "CR_3b_meff1,VR_3b_meff1_A,SR_3b_meff1_A,CR_3b_meff2,VR_3b_meff2_A,SR_3b_meff2_A,CR_3b_meff3,VR_3b_meff3_A,SR_3b_meff3_A"
#region_composition(json_file,  backgrounds,myweights, name_infile, labels, slices=myslice, region=region_sel, name_can="hh_3b_HF", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots_ewk/")

region_sel = "CR_4b_meff1,VR_4b_meff1_A,SR_4b_meff1_A,SR_4b_meff1_A_disc,VR_4b_meff1_B,SR_4b_meff1_B,CR_4b_meff2,VR_4b_meff2_A,SR_4b_meff2_A,VR_4b_meff2_B,SR_4b_meff2_B"
#region_composition(json_file,  backgrounds,myweights, name_infile, labels, slices=myslice, region=region_sel, name_can="hh_4b_HF", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots_ewk/")

##############
# decay type #
##############

myslice = ["ttbar_decay_type==0", "ttbar_decay_type==1", "ttbar_decay_type==2", "ttbar_decay_type==3", "ttbar_decay_type==4", "ttbar_decay_type==5","ttbar_decay_type>=6 && ttbar_decay_type<=9", "ttbar_decay_type>=10 && ttbar_decay_type<=13", "ttbar_decay_type>=14 && ttbar_decay_type<=17"]

labels = ["ee","e#mu", "e#tau", "#mu#mu", "#mu#tau","#tau#tau","e+jets","#mu+jets","#tau+jets"]
backgrounds=["ttbar_NoSys"]
weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
myweights = "*".join(weights)

region_sel = "CR_3b_meff1,VR_3b_meff1_A,SR_3b_meff1_A,CR_3b_meff2,VR_3b_meff2_A,SR_3b_meff2_A,CR_3b_meff3,VR_3b_meff3_A,SR_3b_meff3_A"
region_composition(json_file,  backgrounds,myweights, name_infile, labels, slices=myslice, region=region_sel, name_can="hh_3b_tt", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots_ewk/")

region_sel = "CR_4b_meff1,VR_4b_meff1_A,SR_4b_meff1_A,SR_4b_meff1_A_disc,VR_4b_meff1_B,SR_4b_meff1_B,CR_4b_meff2,VR_4b_meff2_A,SR_4b_meff2_A,VR_4b_meff2_B,SR_4b_meff2_B"
region_composition(json_file,  backgrounds,myweights, name_infile, labels, slices=myslice, region=region_sel, name_can="hh_4b_tt", write=["C. Rizzi PhD Thesis"], outfolder="./comp_plots_ewk/")
