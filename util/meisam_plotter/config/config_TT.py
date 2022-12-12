import plot_utils
from plot_utils import *



sel_0L = "(dphi_min>0.4) && (jets_n>=4) &&  (met>200) && (signal_leptons_n==0) && pass_MET"
name_infile = "/afs/cern.ch/user/c/crizzi/storage/susy_EW/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.EW.2.4.28-4-1/Bkg_tagEW.2.4.28-4-1_SUSY10_nominal.root"

ntags = 2
isIncl = True
lumi = 36000
logY = True
do_scale = False

folder="17_05_30_ttbar/"

var_def=[]
#var_def += [{'def':("mass_h1_dR",30,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_dR"}]
#var_def += [{'def':("mass_h2_dR",30,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_min_dR"}]
#var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_dR"}] 
#var_def += [{'def':("mTb_min",20,0,500),'leg':"m_{T}^{b,min}  [GeV]", "bvar":"mTb_min_tt"}]
#var_def += [{'def':("pt_bjet_1",20,0,1000),'leg':"p_{T} Leading b-jet [GeV]", "bvar":"pt_bjet_1_tt"}]
#var_def += [{'def':("pt_bjet_2",20,0,1000),'leg':"p_{T} Sub-leading b-jet [GeV]", "bvar":"pt_bjet_2_tt"}]
#var_def += [{'def':("pt_bjet_3",20,0,1000),'leg':"p_{T} 3rd b-jet [GeV]", "bvar":"pt_bjet_3_tt"}]
#var_def += [{'def':("pt_bjet_4",20,0,1000),'leg':"p_{T} 4th b-jet [GeV]", "bvar":"pt_bjet_4_tt"}]
#var_def += [{'def':("met",18,200.,1000),'leg':"E_{T}^{miss} [GeV]"}]
#var_def += [{'def':("bjets_n",4, 1.5,5.5),'leg':"Number of b-jets"}]
#var_def += [{'def':("meff_incl",60, 0,3000),'leg':"m_{eff} [GeV]"}]
#var_def += [{'def':("jets_n",6, 3.5,9.5),'leg':"Number of jets"}]
#var_def += [{'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
#var_def += [{'def':("MJSum_rc_r08pt10",50,0,500),'leg':"MJSum [GeV]"}]
var_def += [{'def':("pt_bjet_1",20,0,1000),'leg':"p_{T} Leading b-jet [GeV]", "can":"pt_bjet_1_noTRF"}]


for var in var_def:
    if "can" in var.keys():
        name_can = var['can']
    else:
        name_can = var['def'][0]
    if "bvar"  in var.keys():
        bvar=var["bvar"]
    else:
        bvar=""

    background =  "ttbar"    
    sel = sel_0L
    write=["#bf{#it{ATLAS}} Internal","t#bar{t}, 0L, >=4J, MET>200 GeV, dphi>0.4","36 fb^{-1}"]
    tt_dt (var['def'], sel, background, name_infile, var['leg'], 2, isIncl, lumi, logY, write+["2b Inclusive"], folder, name_can+"_tt_in2b_0L", do_scale, bvar)
    tt_dt (var['def'], sel, background, name_infile, var['leg'], 3, isIncl, lumi, logY, write+["3b Inclusive"], folder, name_can+"_tt_in3b_0L", do_scale, bvar)
    tt_dt (var['def'], sel, background, name_infile, var['leg'], 4, isIncl, lumi, logY, write+["4b Inclusive"], folder, name_can+"_tt_in4b_0L", do_scale, bvar)

    background =  "ttbar_light"    
    sel = sel_0L
    write=["#bf{#it{ATLAS}} Internal","t#bar{t}+light, 0L, >=4J, MET>200 GeV, dphi>0.4","36 fb^{-1}"]
    tt_dt (var['def'], sel, background, name_infile, var['leg'], 2, isIncl, lumi, logY, write+["2b Inclusive"], folder, name_can+"_ttlight_in2b_0L", do_scale, bvar)
    tt_dt (var['def'], sel, background, name_infile, var['leg'], 3, isIncl, lumi, logY, write+["3b Inclusive"], folder, name_can+"_ttlight_in3b_0L", do_scale, bvar)
    tt_dt (var['def'], sel, background, name_infile, var['leg'], 4, isIncl, lumi, logY, write+["4b Inclusive"], folder, name_can+"_ttlight_in4b_0L", do_scale, bvar)

    background =  "ttbar_bb"    
    sel = sel_0L
    write=["#bf{#it{ATLAS}} Internal","t#bar{t}+bb, 0L, >=4J, MET>200 GeV, dphi>0.4","36 fb^{-1}"]
    tt_dt (var['def'], sel, background, name_infile, var['leg'], 2, isIncl, lumi, logY, write+["2b Inclusive"], folder, name_can+"_ttbb_in2b_0L", do_scale, bvar)
    tt_dt (var['def'], sel, background, name_infile, var['leg'], 3, isIncl, lumi, logY, write+["3b Inclusive"], folder, name_can+"_ttbb_in3b_0L", do_scale, bvar)
    tt_dt (var['def'], sel, background, name_infile, var['leg'], 4, isIncl, lumi, logY, write+["4b Inclusive"], folder, name_can+"_ttbb_in4b_0L", do_scale, bvar)

    background =  "ttbar_cc"    
    sel = sel_0L
    write=["#bf{#it{ATLAS}} Internal","t#bar{t}+cc, 0L, >=4J, MET>200 GeV, dphi>0.4","36 fb^{-1}"]
    tt_dt (var['def'], sel, background, name_infile, var['leg'], 2, isIncl, lumi, logY, write+["2b Inclusive"], folder, name_can+"_ttcc_in2b_0L", do_scale, bvar)
    tt_dt (var['def'], sel, background, name_infile, var['leg'], 3, isIncl, lumi, logY, write+["3b Inclusive"], folder, name_can+"_ttcc_in3b_0L", do_scale, bvar)
    tt_dt (var['def'], sel, background, name_infile, var['leg'], 4, isIncl, lumi, logY, write+["4b Inclusive"], folder, name_can+"_ttcc_in4b_0L", do_scale, bvar)


