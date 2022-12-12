import glob, os
import plot_utils
from plot_utils import *

lumi = 36074.56 # Moriond 2017


json_name="../HistFitter/v54/analysis/HF_EW/json_sel/sel.json"

folder_in="/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.33-4-0/"
folder_in_data="/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.33-4-0/"
name_infile_data=folder_in_data+"Data_tag.2.4.33-4-0.root"
name_infile_bkg=folder_in+"Bkg_tag.2.4.33-4-0_Vjets221_nominal.root"
name_infile_signal=folder_in+"Sig_GGM_tag.2.4.33-4-0_nominal_all.root"


outfolder="./2017_08_24/"

if __name__ == "__main__":

    os.system("mkdir -p "+outfolder)

    name_infile = dict()
    #backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar_light","ttbar_cc","ttbar_bb"]
    backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar"]
    #backgrounds=["ttbar_light","ttbar_cc","ttbar_bb"]
    #backgrounds=["ttbar"]
    #labels_bkg = ["t#bar{t}+light","t#bar{t}+cc","t#bar{t}+bb"]   
    labels_bkg = ["diboson","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}"]
    #labels_bkg = ["QCD","non-QCD"]

    name_infile["Data"]=name_infile_data

    for b in backgrounds:
        name_infile[b]= name_infile_bkg

    weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
    #myweights = "*".join(weights)


    var="average_int_per_crossing"
    sel = ["pass_MET && met>200 && (baseline_electrons_n+baseline_muons_n)==0 && jets_n>=4 && jets_n<=5 && meff_4bj>900","pass_MET && met>200 && (baseline_electrons_n+baseline_muons_n)==0 && jets_n>=4 && jets_n<=5","pass_MET && met>200 && (baseline_electrons_n+baseline_muons_n)==0 && jets_n>=4"]
    label=["MET>200, 0L, 4-5 j, meff4b>900","MET>200, 0L, 4-5 j","MET>200, 0L, #geq 4j"]
    mc_chan="407012"
    bkg="ttbar"
    name_infile=name_infile_bkg
    pu_file="purw/merged_prw_mc15c_latest.root"
    variableLegend="pile up"    
    name_can="test"
    outfolder="./"
    write=["ATLAS Internal",mc_chan]
    doLogY=False

    pu_dependence(var, sel, weights, mc_chan, bkg, name_infile, pu_file, label, variableLegend, outfolder, name_can, doLogY, write)

    
    
