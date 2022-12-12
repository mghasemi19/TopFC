import os
from plot_utils import *

mysel = {

#'1L_4j':{
#        'sel':"(jets_n==4) &&  (met>200) && (signal_electrons_n+signal_muons_n>=1) && bjets_n>=2",                                                                                       
#        'write':["#bf{#it{ATLAS}} Internal","1L, #geq2b, =4J, E_{T}^{miss}>200 GeV","79.9 fb^{-1} tag 21.2.18"],                                                                      
#        'folder':"plots/tag_21.2.18/2015-2016-2017/N_Jets_studies/1L_4j/"
#        },  
#'1L_5j':{
#        'sel':"(jets_n==5) &&  (met>200) && (signal_electrons_n+signal_muons_n>=1) && bjets_n>=2",
#        'write':["#bf{#it{ATLAS}} Internal","1L, #geq2b, =5J, E_{T}^{miss}>200 GeV","79.9 fb^{-1} tag 21.2.18"],
#        'folder':"plots/tag_21.2.18/2015-2016-2017/N_Jets_studies/1L_5j/"
#        },

#'1L_6j':{
#        'sel':"(jets_n==6) &&  (met>200) && (signal_electrons_n+signal_muons_n>=1) && bjets_n>=2",
#        'write':["#bf{#it{ATLAS}} Internal","1L, #geq2b, =6J, E_{T}^{miss}>200 GeV","79.9 fb^{-1} tag 21.2.18"],
#        'folder':"plots/tag_21.2.18/2015-2016-2017/N_Jets_studies/1L_6j/"
#        },
#'1L_7j':{
#        'sel':"(jets_n==7) &&  (met>200) && (signal_electrons_n+signal_muons_n>=1) && bjets_n>=2",
#        'write':["#bf{#it{ATLAS}} Internal","1L, #geq2b, 7J, E_{T}^{miss}>200 GeV","79.9 fb^{-1} tag 21.2.18"],
#        'folder':"plots/tag_21.2.18/2015-2016-2017/N_Jets_studies/1L_7j/"
#        },
#'1L_8jin':{
#        'sel':"(jets_n>=8) &&  (met>200) && (signal_electrons_n+signal_muons_n>=1) && bjets_n>=2",
#        'write':["#bf{#it{ATLAS}} Internal","1L, #geq2b, #geq8J, E_{T}^{miss}>200 GeV","79.9 fb^{-1} tag 21.2.18"],
#        'folder':"plots/tag_21.2.18/2015-2016-2017/N_Jets_studies/1L_8jin/"
#        },
'0L_4j':{
        'sel':"(jets_n==4) &&  (met>200) && (signal_electrons_n+signal_muons_n==0) && bjets_n>=2",
        'write':["#bf{#it{ATLAS}} Internal","1L, #geq2b, =4J, E_{T}^{miss}>200 GeV","79.9 fb^{-1} tag 21.2.18"],
        'folder':"plots/tag_21.2.18/2015-2016-2017/N_Jets_studies/0L_4j/"
        }
}
'''
'0L_5j':{
        'sel':"(jets_n==5) &&  (met>200) && (signal_electrons_n+signal_muons_n==0) && bjets_n>=2",
        'write':["#bf{#it{ATLAS}} Internal","1L, #geq2b, =5J, E_{T}^{miss}>200 GeV","79.9 fb^{-1} tag 21.2.18"],
        'folder':"plots/tag_21.2.18/2015-2016-2017/N_Jets_studies/0L_5j/"
        },

'0L_6j':{
        'sel':"(jets_n==6) &&  (met>200) && (signal_electrons_n+signal_muons_n==0) && bjets_n>=2",
        'write':["#bf{#it{ATLAS}} Internal","1L, #geq2b, =6J, E_{T}^{miss}>200 GeV","79.9 fb^{-1} tag 21.2.18"],
        'folder':"plots/tag_21.2.18/2015-2016-2017/N_Jets_studies/0L_6j/"
        },
'0L_7j':{
        'sel':"(jets_n==7) &&  (met>200) && (signal_electrons_n+signal_muons_n==0) && bjets_n>=2",
        'write':["#bf{#it{ATLAS}} Internal","1L, #geq2b, 7J, E_{T}^{miss}>200 GeV","79.9 fb^{-1} tag 21.2.18"],
        'folder':"plots/tag_21.2.18/2015-2016-2017/N_Jets_studies/0L_7j/"
        },
'0L_8jin':{
        'sel':"(jets_n>=8) &&  (met>200) && (signal_electrons_n+signal_muons_n==0) && bjets_n>=2",
        'write':["#bf{#it{ATLAS}} Internal","1L, #geq2b, #geq8J, E_{T}^{miss}>200 GeV","79.9 fb^{-1} tag 21.2.18"],
        'folder':"plots/tag_21.2.18/2015-2016-2017/N_Jets_studies/0L_8jin/"
        },
'''



# luminosity (to scale MC)
lumi = 79900.00
# produce plots with log scale on Y axis
logY = True
do_scale = False # doesn't do anything for now!


# backgrounds (names as in the input file, except removing "_NoSys")
backgrounds=["diboson","Z_jets","W_jets","topEW","singletop","ttbar"]
# backgrounds (as you want them in the legend)
labels = ["diboson","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}"]

# create the dictionaty that points to the correct input file for each background and for data
name_infile=dict()
#name_infile["diboson"]    =   "/eos/user/c/cmorenom/SUSY_files/Bkg_21.2.18_mc16a.diboson.root"
#name_infile["Z_jets"]     =   "/eos/user/c/cmorenom/SUSY_files/Bkg_21.2.18_mc16a.Z_jets.root"
#name_infile["W_jets"]     =   "/eos/user/c/cmorenom/SUSY_files/Bkg_21.2.18_mc16a.W_jets.root"
#name_infile["topEW"]      =   "/eos/user/c/cmorenom/SUSY_files/Bkg_21.2.18_mc16a.topEW.root"
#name_infile["singletop"]  =   "/eos/user/c/cmorenom/SUSY_files/Bkg_21.2.18_mc16a.singletop.root"
#name_infile["ttbar"]      =   "/eos/user/c/cmorenom/SUSY_files/Bkg_21.2.18_mc16a.ttbar.root"
#name_infile["data"]       =   "/eos/user/c/cmorenom/SUSY_files/Merged_Inputs/Data_21.2.18.root"

name_infile["diboson"] = "/eos/user/g/gstark/MBJ/Bkg_21.2.18_mc16a.diboson.root"
name_infile["Z_jets"] = "/eos/user/g/gstark/MBJ/Bkg_21.2.18_mc16a.Z_jets.root"
name_infile["W_jets"] = "/eos/user/g/gstark/MBJ/Bkg_21.2.18_mc16a.W_jets.root"
name_infile["topEW"] = "/eos/user/g/gstark/MBJ/Bkg_21.2.18_mc16a.topEW.root"
name_infile["singletop"] = "/eos/user/g/gstark/MBJ/Bkg_21.2.18_mc16a.singletop.root"
name_infile["ttbar"] = "/eos/user/g/gstark/MBJ/Bkg_21.2.18_mc16a.ttbar.root"
name_infile["Data"] = ["/eos/user/g/gstark/MBJ/Data_21.2.18_20152016.root","/eos/user/g/gstark/MBJ/Data_21.2.18_2017.root"]

# create myweights, a *single* string with the weights to be used sepatated by a *
weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
myweights = "*".join(weights)


# Here I organize the vatiables that I want to plot in a list that I can loop on. This is not strictly necessary but can be useful
# I've chosen to have a list of dictionaries, that put together different arguments of data_mc associated to the same variable. Also this is not mandatory
var_def=[]
#var_def += [{'def':("bjets_n",5, 1.5,6.5),'leg':"Number of b-jets"}]
#var_def += [{'def':("jets_n",10, 3.5,13.5),'leg':"Number of jets"}]
#var_def += [{'def':("met",16,200.,1000),'leg':"E_{T}^{miss} [GeV]"}]
#var_def += [{'def':("met_phi",17,0,3.4),'leg':"#phi_{p_{T}^{\text{miss}}}"}]
#var_def += [{'def':("mTb_min",24,0,1200),'leg':"m_{T}^{b,min}  [GeV]"}]
var_def += [{'def':("meff_incl",32, 0,3500),'leg':"m_{eff} [GeV]"}]
#var_def += [{'def':("dphi_min",17,0,3.4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
#var_def += [{'def':("dphi_1jet",17,0,3.4),'leg':"#Delta#phi^{min}(j-1,MET)"}]
#var_def += [{'def':("pt_jet_1",26,0,1300),'leg':"p_{T} jet 1 [GeV]"}]
#var_def += [{'def':("pt_jet_2",26,0,1300),'leg':"p_{T} jet 2 [GeV]"}]
#var_def += [{'def':("pt_jet_3",26,0,1300),'leg':"p_{T} jet 3 [GeV]"}]
#var_def += [{'def':("pt_jet_4",26,0,1300),'leg':"p_{T} jet 4 [GeV]"}]
#var_def += [{'def':("pt_bjet_1",40,0,2000),'leg':"p_{T} b-jet 1 [GeV]"}]
#var_def += [{'def':("pt_bjet_2",28,0,1400),'leg':"p_{T} b-jet 2 [GeV]"}]
#var_def += [{'def':("MJSum_rc_r08pt10",20,0,1000),'leg':"M_{J}^{#Sum} [GeV]"}]
#var_def += [{'def':("pt_lep_1",40,0,2000),'leg':"p_{T} lepton 1 [GeV]"}]
#var_def += [{'def':("mT",24,0,1200),'leg':"m_{T}  [GeV]"}]
#var_def += [{'def':("bweight_1",20,0,1.1),'leg':"MV2c10 output jet 1 [GeV]"}]
#var_def += [{'def':("bweight_2",20,0,1.1),'leg':"MV2c10 output jet 2 [GeV]"}]
#var_def += [{'def':("bweight_3",20,0,1.1),'leg':"MV2c10 output jet 3 [GeV]"}]
#var_def += [{'def':("bweight_4",20,0,1.1),'leg':"MV2c10 output jet 4 [GeV]"}]
#var_def += [{'def':("asymmetry",20,0,1.1),'leg':"Asymmetry"}]
#var_def += [{'def':("average_int_per_crossing",40,0,50),'leg':"Average interactions per crossing"}]
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
        data_mc (var['def'], sel['sel'], myweights, backgrounds, name_infile, labels, var['leg'], lumi, logY, sel['write'], sel['folder'], name_can, do_scale=False, add_signal = False)
