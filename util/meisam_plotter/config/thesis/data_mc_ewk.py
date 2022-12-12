import os
from plot_utils import *

mysel = {
'0L_3bin':{
        'sel':"(jets_n>=4) &&  (met>200) && (signal_electrons_n+signal_muons_n==0) && bjets_n>=3 && dphi_min>0.4",
        'write':["C. Rizzi PhD Thesis","0L, #geq3b, #geq4J, E_{T}^{miss}>200 GeV","36.1 fb^{-1}"],
        'folder':"plots/ewk_prod/0L_3bin/"  
        }}
"""
,

'0L_2bin':{
        'sel':"(dphi_min>0.4) && (jets_n>=4) &&  (met>200) && (signal_electrons_n+signal_muons_n==0) && bjets_n>=2",
        'write':["C. Rizzi PhD Thesis","0L, #geq2b, #geq4J, E_{T}^{miss}>200 GeV","36.1 fb^{-1}"],
        'folder':"plots/ewk_prod/0L_2bin/"
        }
}
"""
# luminosity (to scale MC)
lumi = 36100.00 # 
# produce plots with log scale on Y axis
logY = True
do_scale = False # doesn't do anything for now!

# backgrounds (names as in the input file, except removing "_NoSys")
backgrounds=["multijet_NoSys","diboson_NoSys","Zjets_NoSys","Wjets_NoSys","TopEW_NoSys","SingleTop_NoSys","ttbar_NoSys"]
# backgrounds (as you want them in the legend)
labels = ["multijet","diboson","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}"]

# create the dictionaty that points to the correct input file for each background and for data
name_infile_bkg = "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.37-0-X_skim/Bkg_tag.2.4.37-0-X_useMET300400_3b_0L_met_br_wei.root"
name_infile_qcd = "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/qcd_trisha_from_calum/qcd_br_wei.root"
name_infile_data= "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.37-0-X_tmp/Data_tag.2.4.37-0-X.root"
name_infile_sig = "/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.37-0-X/Sig_GGM_tag.2.4.37-0-X.root"

name_infile=dict()
for b in backgrounds:
    name_infile[b] =  name_infile_bkg
name_infile["Data"] = name_infile_data
name_infile["multijet_NoSys"] = name_infile_qcd

# create myweights, a *single* string with the weights to be used sepatated by a *
weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
myweights = "*".join(weights)


# Here I organize the vatiables that I want to plot in a list that I can loop on. This is not strictly necessary but can be useful
# I've chosen to have a list of dictionaries, that put together different arguments of data_mc associated to the same variable. Also this is not mandatory
var_def=[]

var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",15,0,5), 'leg':'#DeltaR^{bb}_{max}', 'can':"dRmax_dR"}]
var_def += [{'def':("DeltaR_h1_dR",15,0,5), 'leg':'#DeltaR(h_{1})', 'can':"DeltaR_h1_dR"}]
var_def += [{'def':("DeltaR_h2_dR",15,0,5), 'leg':'#DeltaR(h_{2})', 'can':"DeltaR_h2_dR"}]
var_def += [{'def':("mass_h1_dR",15,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_dR"}]
var_def += [{'def':("mass_h2_dR",15,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_min_dR"}]
var_def += [{'def':("max(DeltaR_h1_min_diff,DeltaR_h2_min_diff)",15,0,5), 'leg':'#DeltaR^{bb}_{max}', 'can':"dRmax_min_diff"}]
var_def += [{'def':("DeltaR_h1_min_diff",15,0,5), 'leg':'#DeltaR(h_{1})', 'can':"DeltaR_h1_min_diff"}]
var_def += [{'def':("DeltaR_h2_min_diff",15,0,5), 'leg':'#DeltaR(h_{2})', 'can':"DeltaR_h2_min_diff"}]
var_def += [{'def':("mass_h1_min_diff",15,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_min_diff"}]
var_def += [{'def':("mass_h2_min_diff",15,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_min_min_diff"}]
var_def += [{'def':("max(DeltaR_h1_115,DeltaR_h2_115)",15,0,5), 'leg':'#DeltaR^{bb}_{max}', 'can':"dRmax_115"}]
var_def += [{'def':("DeltaR_h1_115",15,0,5), 'leg':'#DeltaR(h_{1})', 'can':"DeltaR_h1_115"}]
var_def += [{'def':("DeltaR_h2_115",15,0,5), 'leg':'#DeltaR(h_{2})', 'can':"DeltaR_h2_115"}]
var_def += [{'def':("mass_h1_115",15,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_115"}]
var_def += [{'def':("mass_h2_115",15,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_min_115"}]
var_def += [{'def':("meff_4bj",20,300,1300),'leg':"m^{4bj}_{eff} [GeV]"}]

var_def += [{'def':("bjets_n",3, 2.5,5.5),'leg':"Number of b-jets"}]
var_def += [{'def':("bjets_n",4, 1.5,5.5),'leg':"Number of b-jets",'can':"bjets_n_2b"}]
var_def += [{'def':("jets_n",10, 3.5,13.5),'leg':"Number of jets"}]
var_def += [{'def':("met",8,200.,1000),'leg':"E_{T}^{miss} [GeV]"}]
var_def += [{'def':("met_phi",17,0,3.4),'leg':"#phi_{p_{T}^{\text{miss}}}"}]
var_def += [{'def':("mTb_min",12,0,1200),'leg':"m_{T}^{b,min}  [GeV]"}]
var_def += [{'def':("meff_incl",16, 0,3500),'leg':"m_{eff} [GeV]"}]
var_def += [{'def':("dphi_min",10,0,3.4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
var_def += [{'def':("dphi_1jet",17,0,3.4),'leg':"#Delta#phi^{min}(j-1,MET)"}]
var_def += [{'def':("pt_jet_1",13,0,1300),'leg':"p_{T} jet 1 [GeV]"}]
var_def += [{'def':("pt_jet_2",13,0,1300),'leg':"p_{T} jet 2 [GeV]"}]
var_def += [{'def':("pt_jet_3",13,0,1300),'leg':"p_{T} jet 3 [GeV]"}]
var_def += [{'def':("pt_jet_4",26,0,1300),'leg':"p_{T} jet 4 [GeV]"}]
var_def += [{'def':("pt_bjet_1",40,0,2000),'leg':"p_{T} b-jet 1 [GeV]"}]
var_def += [{'def':("pt_bjet_2",28,0,1400),'leg':"p_{T} b-jet 2 [GeV]"}]
var_def += [{'def':("MJSum_rc_r08pt10",20,0,1000),'leg':"M_{J}^{#Sum} [GeV]"}]
var_def += [{'def':("pt_lep_1",40,0,2000),'leg':"p_{T} lepton 1 [GeV]"}]
var_def += [{'def':("mT",24,0,1200),'leg':"m_{T}  [GeV]"}]

#var_def += [{'def':("bweight_1",20,0,1.1),'leg':"MV2c10 output jet 1 [GeV]"}]
#var_def += [{'def':("bweight_2",20,0,1.1),'leg':"MV2c10 output jet 2 [GeV]"}]
#var_def += [{'def':("bweight_3",20,0,1.1),'leg':"MV2c10 output jet 3 [GeV]"}]
#var_def += [{'def':("bweight_4",20,0,1.1),'leg':"MV2c10 output jet 4 [GeV]"}]
#var_def += [{'def':("asymmetry",20,0,1.1),'leg':"Asymmetry"}]
#var_def += [{'def':("average_int_per_crossing",50,10,70),'leg':"Average interactions per crossing"}]
#var_def += [{'def':("n_vtx",40,0,50),'leg':"Number of vertices"}]
#var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_dR"}]


for key in mysel:

    sel = mysel[key]
    os.system("mkdir -p "+sel['folder'])
    print(sel)
# loop on all the variables that you want to plot
    for var in var_def:
    # this is just to define the name of the pdf file: if the key 'can' is in the dictionaly that will be the name, otherwise the name of the variable is used
        if "can" in var.keys():
            name_can = var['can']
        else:
            name_can = var['def'][0]
    # fianlly, the data_mc finction is called
        data_mc (var['def'], sel['sel'], myweights, backgrounds, name_infile, labels, var['leg'], lumi, logY, sel['write'], sel['folder'], name_can, do_scale=False, add_signal = False, isR20=True)
