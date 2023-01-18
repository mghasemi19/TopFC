import os
from plot_utils import *

# No selections to be applied 
#sel = "(dphi_min>0.4) && (jets_n>=4) &&  (met>200) && (baseline_electrons_n+baseline_muons_n==0) && pass_MET && bjets_n>=2"
sel = "1==1"
# luminosity (to scale MC)
lumi = 3*10**6
# produce plots with log scale on Y axis
logY = True
do_scale = False # doesn't do anything for now!

# define the output folder (and create it if it doesn't exist)
folder_out="plots/example_data_mc/"
os.system("mkdir -p "+folder_out)

# backgrounds (names as in the input file, except removing "_NoSys")
backgrounds=['ttbar', 'ttbarW', 'ttbarZ', 'tttt', 'tZ', 'WZ', 'ZZ']
signals = ['signal_charm', 'signal_up']
# backgrounds (as you want them in the legend)
labels = ["t#bar{t}","t#bar{t}+W","t#bar{t}+Z","t#bar{t}t#bar{t}","tZ","WZ","ZZ"]

# create the dictionaty that points to the correct input file for each background and for data
name_infile=dict()
name_infile = {'ttbar':'/home/mghasemi/project/TopFC/Ntuple_prod/MG5/MG5_aMC_v3_4_1/Delphes/trees/ttbar.root', 'ttbarW':'/home/mghasemi/project/TopFC/Ntuple_prod/MG5/MG5_aMC_v3_4_1/Delphes/trees/ttbarW.root', 'ttbarZ':'/home/mghasemi/project/TopFC/Ntuple_prod/MG5/MG5_aMC_v3_4_1/Delphes/trees/ttbarZ.root', 'tttt':'/home/mghasemi/project/TopFC/Ntuple_prod/MG5/MG5_aMC_v3_4_1/Delphes/trees/tttt.root', 'tZ':'/home/mghasemi/project/TopFC/Ntuple_prod/MG5/MG5_aMC_v3_4_1/Delphes/trees/tZ.root', 'WZ':'/home/mghasemi/project/TopFC/Ntuple_prod/MG5/MG5_aMC_v3_4_1/Delphes/trees/WZ.root', 'ZZ':'/home/mghasemi/project/TopFC/Ntuple_prod/MG5/MG5_aMC_v3_4_1/Delphes/trees/ZZ.root', 'signal_up':'/home/mghasemi/project/TopFC/Ntuple_prod/MG5/MG5_aMC_v3_4_1/Delphes/trees/signal_up.root', 'signal_charm':'/home/mghasemi/project/TopFC/Ntuple_prod/MG5/MG5_aMC_v3_4_1/Delphes/trees/signal_charm.root'}

# create myweights, a *single* string with the weights to be used sepatated by a *
myweights = "weight"

# lsit of things to write on the plot
write=["#sqrt 13 TeV, L = 3000 fb^{-1}"]

# Here I organize the vatiables that I want to plot in a list that I can loop on. This is not strictly necessary but can be useful
# I've chosen to have a list of dictionaries, that put together different arguments of data_mc associated to the same variable. Also this is not mandatory
var_def=[]
var_def += [{'def':("jetPT",20,0,1000),'leg':"jet p_{T}"}]
'''
var_def += [{'def':("jetNo",12,0,12),'leg':"Number of jets"}]
var_def += [{'def':("jetPTLeading",50, 0,500),'leg':"Leading jet p_{T}"}]
var_def += [{'def':("jetPT",50,0,500),'leg':"jet p_{T}"}]
var_def += [{'def':("jetETA",50,-5,5),'leg':"jet #eta"}]
var_def += [{'def':("jetPHI",16,-4,4),'leg':"jet #phi"}]

var_def += [{'def':("elecPT",50,0,500),'leg':"electron p_{T}"}]
var_def += [{'def':("elecPTLeading",50,0,500),'leg':"Leading electron p_{T}"}]
var_def += [{'def':("elecETA",50,-5,5),'leg':"electron #eta"}]
var_def += [{'def':("elecPHI",16,-4,4),'leg':"electron #phi"}]

var_def += [{'def':("dielecETA",50, -5.0, 5.0),'leg':"di-electron #eta"}]
var_def += [{'def':("dielecCOS",20, -1.5, 1.5),'leg':"di-electron Cos"}]
var_def += [{'def':("dielecMass",30, 0.0, 300.0),'leg':"di-electron Mass"}]
var_def += [{'def':("dielecR",16, 0.0, 8.0),'leg':"di-electron R"}]

#var_def += [{'def':("",100, 0, 300),'leg':"Missing E_{T}"}]
var_def += [{'def':("WMass",20, 50, 150),'leg':"M_{W}"}]
var_def += [{'def':("TopMass",30, 0, 300),'leg':"SM M_{top}"}]
var_def += [{'def':("nonTopMass",30, 0, 300),'leg':"non-SM M_{SM}"}]
var_def += [{'def':("newnonTopMass",30, 0, 300),'leg':"new non-SM M_{top}"}]
'''

# loop on all the variables that you want to plot
for var in var_def:
    # this is just to define the name of the pdf file: if the key 'can' is in the dictionaly that will be the name, otherwise the name of the variable is used
    name_can = var['def'][0]
    # fianlly, the data_mc function is called
    signal_bkg (var['def'], sel, myweights, backgrounds, signals, name_infile, labels, var['leg'], lumi, logY, write, folder_out, name_can)


