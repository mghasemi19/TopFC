import plot_utils
from plot_utils import *



sel_0L = "(dphi_min>0.4) && (jets_n>=4) &&  (met>200) && (baseline_electrons_n+baseline_muons_n==0) && pass_MET && bjets_n>=2"
name_infile_bkg = "/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-6-2/Bkg_tagEW.2.4.28-6-2_SUSY10_METfilt_nominal_2b.root"
#name_infile_bkg = "/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-4-1/Bkg_tagEW.2.4.28-4-1_SUSY10_METfilt_nominal_2b.root"
name_infile_data="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-6-2/Data_tagEW.2.4.28-6-2_SUSY10.root"
name_infile_signal="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-4-1/Sig_GGM_tagEW.2.4.28-4-1_SUSY10_nominal.root"

#sel_2L = "jets_n>=2 &&  (met>200) && (signal_leptons_n>=2) && pass_MET && bjets_n_77>=2"
#name_infile_bkg = "/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-3-3/bkg_tagEW.2.4.28-3-3_nominal.root"
#name_infile_data="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-3-3/Data_tagEW.2.4.28-3-3.root"
#name_infile_signal="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-3-3/Sig_GGM_tagEW.2.4.28-3-3_nominal.root"

lumi = 36074.56
logY = True
do_scale = False


folder_out="17_07_25_disgnostic/"

name_infile=dict()
#backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar"]
backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar"]
labels = ["diboson","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}"]
#backgrounds=["diboson","Wjets","Zjets","TopEW","SingleTop","ttbar_light","ttbar_cc","ttbar_bb"]
#labels = ["diboson","W+jets","Z+jets","t#bar{t}+X","single top","t#bar{t}+light","t#bar{t}+cc","t#bar{t}+bb"]
for b in backgrounds:
    print b
    name_infile[b] = name_infile_bkg
    name_infile[b+"_NoSys"] = name_infile_bkg

signals=["GGM_hh_300","GGM_hh_500","GGM_hh_800"]
for s in signals:
    name_infile[s] = name_infile_signal
    

name_infile["Data"] = name_infile_data

var_def=[]
#var_def += [{'def':("meff_4bj",20,300,1300),'leg':"meff 4b [GeV]"}]
#var_def += [{'def':("n_vtx",51,-0.5,50.5),'leg':"n_vtx"}]
#var_def += [{'def':("average_int_per_crossing",51,-0.5,50.5),'leg':"mu"}]
var_def += [{'def':("met_phi",80,-3.5, 3.5),'leg':"#phi(E_{T}^{miss})"}]

sel=sel_0L
for var in var_def:
    if "can" in var.keys():
        name_can = var['can']
    else:
        name_can = var['def'][0]

    name_can=name_can+"_2b"
    if "bvar"  in var.keys():
        bvar=var["bvar"]
    else:
        bvar=""
    #weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2","weight_pu"]
    weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
    myweights = "*".join(weights)
    print myweights
    write=["#bf{#it{ATLAS}} Internal","0L, #geq2b, #geq4J, E_{T}^{miss}>200 GeV, D#phi>0.4","36.1 fb^{-1}"]
    data_mc (var['def'], sel, myweights, backgrounds, name_infile, labels, var['leg'], lumi, logY, write, folder_out, name_can, do_scale=False, add_signal = False)


