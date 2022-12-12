import glob, os
import plot_utils
from plot_utils import *

lumi = 36074.56 # Moriond 2017


json_name="../macro_yields/json_final/chiara_17_06_28_dRUnc40_v3.json"
#json_name="../macro_yields/json_to_compare/chiara_17_06_28_nodR_forPie.json"

folder_in="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-6-2/"
name_infile_data=folder_in+"Data_2.4.28-0-0_skim_2b.root"
name_infile_bkg=folder_in+"Bkg_tagEW.2.4.28-6-2_SUSY10_METfilt_nominal_3b_0L_met200.root"
name_infile_signal=folder_in+"Sig_GGM_tagEW.2.4.28-6-2_SUSY10_nominal_all.root"


outfolder="./2017_07_31/"

if __name__ == "__main__":

    os.system("mkdir -p "+outfolder)

    name_infile = dict()
    #backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar_light","ttbar_cc","ttbar_bb"]
    #backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar","QCD"]
    #backgrounds=["ttbar_light","ttbar_cc","ttbar_bb"]
    backgrounds=["ttbar"]
    labels_bkg = ["t#bar{t}+light","t#bar{t}+cc","t#bar{t}+bb"]   
    #labels_bkg = ["diboson","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}","QCD"]
    #labels_bkg = ["QCD","non-QCD"]

    for b in backgrounds:
        name_infile[b]= name_infile_bkg

    weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
    myweights = "*".join(weights)
    #myslice=["weight_lumi>2.081e-08 && weight_lumi<2.082e-08","!(weight_lumi>2.081e-08 && weight_lumi<2.082e-08)"]
    #myslice=["(is_QCD)","(!is_QCD)"]
    myslice=["ttbar_class==0","ttbar_class<0","ttbar_class>0"]

    plot_pie (json_name, myweights, backgrounds, name_infile, labels_bkg, myslice, outfolder, "pie_HF", region="CR_3b_meff4", do_scale=False)



