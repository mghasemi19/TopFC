import glob, os
import plot_utils
from plot_utils import *

lumi = 36074.56 # Moriond 2017

remove_meff_corr=False

json_name="/afs/cern.ch/user/c/crizzi/storage/susy_EW/macro_yields/json/17_06_14.json"

folder_in="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-4-1/"

name_infile_data=folder_in+"Data_tagEW.2.4.28-4-1_SUSY10.root"
name_infile_bkg=folder_in+"Bkg_tagEW.2.4.28-4-1_SUSY10_METfilt_nominal_3b.root"
name_infile_QCD=folder_in+""
name_infile_signal=folder_in+"Sig_GGM_tagEW.2.4.28-4-1_SUSY10_nominal.root"

outfolder="./2017_06_15/"

if __name__ == "__main__":

    os.system("mkdir -p "+outfolder)

    masses=["130","150","200","300","400","500","600","800"]
    weights=["weight_lumi","weight_mc"]
    name_infile = dict()
    for m in masses:
        name_infile[m] = name_infile_signal
    signals=["GGM_Zh_300","GGM_Zh_500","GGM_Zh_800"]
    #signals=["GGM_Zh_150","GGM_Zh_200","GGM_Zh_500","GGM_Zh_800"]
    name_infile = dict()
    for s in signals:
        name_infile[s] = name_infile_signal

    #backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar_light","ttbar_cc","ttbar_bb"]
    backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar"]
    #backgrounds=["Zjets","Wjets","SingleTop","ttbar"]
    #backgrounds=["ttbar"]

    for b in backgrounds:
        name_infile[b]= name_infile_bkg

    #labels_sig = ["m(#tilde{#chi}) = 150 GeV","m(#tilde{#chi}) = 200 GeV","m(#tilde{#chi}) = 500 GeV","m(#tilde{#chi}) = 800 GeV"]
    labels_sig = ["m(#tilde{#chi}) = 300 GeV","m(#tilde{#chi}) = 500 GeV","m(#tilde{#chi}) = 800 GeV"]
    #labels_bkg = ["diboson","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}+light", "t#bar{t}+cc", "t#bar{t}+bb"]
    labels_bkg = ["diboson","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}"]
    #labels_bkg = ["Z+jets","W+jets","single top","t#bar{t}"]
    #labels_bkg = ["t#bar{t}"]
    weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
    #weights = ["weight_mc","weight_lumi","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
    myweights = "*".join(weights)


    plot_pie (json_name, myweights, backgrounds, name_infile, labels_bkg, ["1"], outfolder, "pie", region="_", do_scale=False)



