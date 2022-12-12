import glob, os
import plot_utils
from plot_utils import *

lumi = 36074.56 # Moriond 2017

remove_meff_corr=False

pickle_sel="../../cuts_pickle/sel_wei_dict_presel.pickle"
pickle_sel_no_wei="../../cuts_pickle/sel_dict_presel.pickle"

folder_in="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-3-3/"

name_infile_data=folder_in+"Data_2.4.28-0-0_skim_2b.root"
#name_infile_bkg=folder_in+"bkg_tagEW.2.4.28-1_nominal.root"
name_infile_bkg=folder_in+"bkg_tagEW.2.4.28-3-3_nominal_2b.root"
name_infile_QCD=folder_in+""
name_infile_signal=folder_in+"Sig_GGM_tagEW.2.4.28-3-3_nominal_all_types.root"

outfolder="./2017_06_27_sig_bkg_2L/"

if __name__ == "__main__":

    os.system("mkdir -p "+outfolder)

    masses=["130","150","200","300","400","500","600","800"]
    weights=["weight_lumi","weight_mc"]
    name_infile = dict()
    for m in masses:
        name_infile[m] = name_infile_signal

    num_sel=["jets_n>=4"]
    legend = [">= 4 jets"]
    den_sel = "hh_type==10"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, "./", "4j_efficiency_4b_hh4b.pdf")



    # +++++++++++++
    # Data/MC plots
    # +++++++++++++



                

    signals=["GGM_Zh_300_Zhllbb","GGM_Zh_500_Zhllbb","GGM_Zh_800_Zhllbb"]
    name_infile = dict()
    for s in signals:
        name_infile[s] = name_infile_signal

    backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar"]
        #backgrounds=["Zjets","Wjets","SingleTop","ttbar"]
    #backgrounds=["ttbar"]
    for b in backgrounds:
        name_infile[b]= name_infile_bkg

    labels_sig = ["m(#tilde{#chi}) = 150 GeV","m(#tilde{#chi}) = 200 GeV","m(#tilde{#chi}) = 500 GeV","m(#tilde{#chi}) = 800 GeV"]
    labels_bkg = ["diboson","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}"]
    #labels_bkg = ["Z+jets","W+jets","single top","t#bar{t}"]
    #labels_bkg = ["t#bar{t}"]


    for var in var_def:
        if "can" in var.keys():
            name_can = var['can']
        else:
            name_can = var['def'][0]

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","2L, #geq 2j, #geq 2b ","Zh #rightarrow llbb"]
        sel="(mass_bb>90 && mass_bb<140 && met>200 && Z_OSLeps && jets_n>=2 && bjets_n_77==2 && signal_leptons_n==2)*(weight_mc*weight_lumi*weight_elec*weight_muon*weight_jvt*weight_WZ_2_2)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_2j_2b_2l_mbb90140_Zh", signals, labels_sig)




