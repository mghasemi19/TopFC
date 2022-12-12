import plot_utils
from plot_utils import *



sel_0L = "(dphi_min>0.4) && (jets_n>=4) &&  (met>200) && (baseline_electrons_n+baseline_muons_n==0) && pass_MET && bjets_n>=2"
name_infile_bkg = "/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.2.4.33-2-0/Bkg_tag.2.4.33-2-0_2b_0L_met.root"
#name_infile_data="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.2.4.33-2-0/Data_tag.2.4.33-2-0_2b_0L_met.root"
name_infile_data="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.2.4.33-2-0/Data_tag.2.4.33-2-0.root"
name_infile_signal="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.2.4.33-2-0/Sig_GGM_tag.2.4.33-2-0_nominal_3b_0L_met_all.root"

#sel_2L = "jets_n>=2 &&  (met>200) && (signal_leptons_n>=2) && pass_MET && bjets_n_77>=2"
#name_infile_bkg = "/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-3-3/bkg_tagEW.2.4.28-3-3_nominal.root"
#name_infile_data="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-3-3/Data_tagEW.2.4.28-3-3.root"
#name_infile_signal="/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-3-3/Sig_GGM_tagEW.2.4.28-3-3_nominal.root"

lumi = 36074.56
logY = True
do_scale = False


folder_out="17_07_27_data_mc/"

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
var_def += [{'def':("meff_4bj",20,300,1300),'leg':"meff 4b [GeV]"}]
var_def += [{'def':("bjets_n",4, 1.5,5.5),'leg':"Number of b-jets"}]
var_def += [{'def':("mTb_min",20,0,500),'leg':"m_{T}^{b,min}  [GeV]", "bvar":"mTb_min_tt"}]
var_def += [{'def':("pt_bjet_1",20,0,1000),'leg':"p_{T} Leading b-jet [GeV]", "bvar":"pt_bjet_1_tt"}]
var_def += [{'def':("pt_bjet_2",20,0,1000),'leg':"p_{T} Sub-leading b-jet [GeV]", "bvar":"pt_bjet_2_tt"}]
var_def += [{'def':("met",18,200.,1000),'leg':"E_{T}^{miss} [GeV]"}]
var_def += [{'def':("meff_incl",60, 0,3000),'leg':"m_{eff} [GeV]"}]
var_def += [{'def':("jets_n",6, 3.5,9.5),'leg':"Number of jets"}]
var_def += [{'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
var_def += [{'def':("pt_jet_1",20,0,1000),'leg':"p_{T} Leading jet [GeV]"}]
var_def += [{'def':("pt_jet_2",20,0,1000),'leg':"p_{T} Sub-leading jet [GeV]"}]
var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_dR"}] 
var_def += [{'def':("mass_h1_dR",30,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_dR"}]
var_def += [{'def':("mass_h2_dR",30,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_min_dR"}]
var_def += [{'def':("met_sig",30,0,30),'leg':"MET/#sqrt{H_{T}}   [#sqrt{GeV}]"}]



"""

#var_def += [{'def':("pt_bjet_3",20,0,1000),'leg':"p_{T} 3rd b-jet [GeV]", "bvar":"pt_bjet_3_tt"}]
#var_def += [{'def':("pt_bjet_4",20,0,1000),'leg':"p_{T} 4th b-jet [GeV]", "bvar":"pt_bjet_4_tt"}]
"""
"""
var_def += [{'def':("mass_h1_dR",30,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_dR"}]
var_def += [{'def':("mass_h2_dR",30,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_min_dR"}]
var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_dR"}] 
var_def += [{'def':("mTb_min",20,0,500),'leg':"m_{T}^{b,min}  [GeV]", "bvar":"mTb_min_tt"}]
#var_def += [{'def':("pt_bjet_1",20,0,1000),'leg':"p_{T} Leading b-jet [GeV]", "bvar":"pt_bjet_1_tt"}]
#var_def += [{'def':("pt_bjet_2",20,0,1000),'leg':"p_{T} Sub-leading b-jet [GeV]", "bvar":"pt_bjet_2_tt"}]
var_def += [{'def':("met",18,200.,1000),'leg':"E_{T}^{miss} [GeV]"}]
var_def += [{'def':("bjets_n",4, 1.5,5.5),'leg':"Number of b-jets"}]
var_def += [{'def':("jets_n",6, 3.5,9.5),'leg':"Number of jets"}]
var_def += [{'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
"""
"""
var_def += [{'def':("m_rho300_1",20,50,250),'leg':"m(j1) #rho 300 [GeV]",'can':"mass_VRj1_rho300"}]
var_def += [{'def':("m_rho300_2",20,50,250),'leg':"m(j2) #rho 300 [GeV]",'can':"mass_VRj2_rho300"}]
var_def += [{'def':("m_rho400_1",20,50,250),'leg':"m(j1) #rho 400 [GeV]",'can':"mass_VRj1_rho400"}]
var_def += [{'def':("m_rho400_2",20,50,250),'leg':"m(j2) #rho 400 [GeV]",'can':"mass_VRj2_rho400"}]
var_def += [{'def':("m_rho500_1",20,50,250),'leg':"m(j1) #rho 500 [GeV]",'can':"mass_VRj1_rho500"}]
var_def += [{'def':("m_rho500_2",20,50,250),'leg':"m(j2) #rho 500 [GeV]",'can':"mass_VRj2_rho500"}]
#var_def += [{'def':("mass_h1_min_diff",40,50,250),'leg':"m(h1) [GeV]",'can':"mass_h1_min_diff"}]
#var_def += [{'def':("mass_h2_min_diff",40,50,250),'leg':"m(h2) [GeV]",'can':"mass_h2_min_diff"}]
"""

#var_def += [{'def':("DeltaR_bb",30,0,5), 'leg':'dR(b_{1}, b_{2})', 'can':"dR_bb"}] 
#var_def += [{'def':("mass_bb",20,50,250),'leg':"m(b,b) [GeV]",'can':"mass_bb"}]
#var_def += [{'def':("Z_mass",20,50,250),'leg':"m(l,l) [GeV]",'can':"mass_ll"}]


#var_def += [{'def':("MJSum_rc_r08pt10",50,0,500),'leg':"MJSum [GeV]"}]
#var_def += [{'def':("pt_bjet_1",20,0,1000),'leg':"p_{T} Leading b-jet [GeV]", "can":"pt_bjet_1_noTRF"}]

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
    weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
    #weights = ["weight_mc","weight_lumi","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
    #weights = ["weight_mc","weight_lumi"]
    myweights = "*".join(weights)
    print myweights
    write=["#bf{#it{ATLAS}} Internal","0L, #geq2b, #geq4J, E_{T}^{miss}>200 GeV, D#phi>0.4","36.1 fb^{-1}"]
    #write=["#bf{#it{ATLAS}} Internal","2L, #geq2J,  #geq2b, E_{T}^{miss}>200 GeV","36.1 fb^{-1}"]
    data_mc (var['def'], sel, myweights, backgrounds, name_infile, labels, var['leg'], lumi, logY, write, folder_out, name_can, do_scale=False, add_signal = False)


