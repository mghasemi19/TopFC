import os
from plot_utils import *

# No selections to be applied 
#sel = "(dphi_min>0.4) && (jets_n>=4) &&  (met>200) && (baseline_electrons_n+baseline_muons_n==0) && pass_MET && bjets_n>=2"
sel = "1==1"
# luminosity (to scale MC)
#lumi = 3*(10**6)
lumi = 1
# produce plots with log scale on Y axis
logY = True
do_scale = False # doesn't do anything for now!

# define the output folder (and create it if it doesn't exist)
folder_out="plots/data_mc_couplings/"
os.system("mkdir -p "+folder_out)

# backgrounds (names as in the input file, except removing "_NoSys")
#backgrounds=['ttbar', 'ttbarW', 'ttbarZ', 'tttt', 'tZ', 'WZ', 'ZZ']
backgrounds=['ttbarW', 'ttbarZ', 'tttt', 'tZ', 'WZ', 'ZZ', 'ttbar']
signals = ['signal_up_SRR', 'signal_up_VRR', 'signal_up_TRR']
# backgrounds (as you want them in the legend)
#labels = ["t#bar{t}","t#bar{t}+W","t#bar{t}+Z","t#bar{t}t#bar{t}","tZ","WZ","ZZ"]
labels = ["t#bar{t}+W","t#bar{t}+Z","t#bar{t}t#bar{t}","tZ","WZ","ZZ","t#bar{t}"]

# create the dictionaty that points to the correct input file for each background and for data
name_infile=dict()
'''
name_infile = {'ttbar':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ttbar.root',
 'ttbarW':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ttbarW.root',
 'ttbarZ':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ttbarZ.root', 
 'tttt':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/tttt.root',
 'tZ':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/tZ.root',
 'WZ':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/WZ.root',
 'ZZ':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ZZ.root',
 'signal_up_SRR':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/signal_up_SRR.root',
 'signal_up_VRR':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/signal_up_VRR.root'}
 

name_infile = {'ttbar':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ttbar_trees/ttbar.root',
 'ttbarW':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ttbar_trees/ttbarW.root',
 'ttbarZ':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ttbar_trees/ttbarZ.root', 
 'tttt':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ttbar_trees/tttt.root',
 'tZ':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ttbar_trees/tZ.root',
 'WZ':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ttbar_trees/WZ.root',
 'ZZ':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ttbar_trees/ZZ.root',
 'signal_up_SRR':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ttbar_trees/signal_up_SRR.root',
 'signal_up_VRR':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ttbar_trees/signal_up_VRR.root'}
 '''

name_infile = {'ttbar':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ttbar.root',
 'ttbarW':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ttbarW.root',
 'ttbarZ':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ttbarZ.root', 
 'tttt':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/tttt.root',
 'tZ':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/tZ.root',
 'WZ':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/WZ.root',
 'ZZ':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ZZ.root',
 'signal_up_SRR':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ttbar_trees/signal_up_SRR.root',
 'signal_up_VRR':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ttbar_trees/signal_up_VRR.root',
 'signal_up_TRR':'/Users/mghasemi/Desktop/IPM/plotter/newtrees/ttbar_trees/signal_up_TRR.root'}


# create myweights, a *single* string with the weights to be used sepatated by a *
myweights = "weight"

# lsit of things to write on the plot
write=["#sqrt{s} = 13 TeV, L = 3000 fb^{-1}"]

# Here I organize the vatiables that I want to plot in a list that I can loop on. This is not strictly necessary but can be useful
# I've chosen to have a list of dictionaries, that put together different arguments of data_mc associated to the same variable. Also this is not mandatory
var_def=[]

#var_def += [{'def':("jetNo",10,0,10),'leg':"Number of jets"}]

var_def += [{'def':("jetPT",20,0,400),'leg':"jet p_{T}"}]
var_def += [{'def':("jetNo",10,0,10),'leg':"Number of jets"}]
var_def += [{'def':("jetPTLeading",20, 0,400),'leg':"Leading jet p_{T}"}]
var_def += [{'def':("jetETA",24,-6,6),'leg':"jet #eta"}]
var_def += [{'def':("jetPHI",16,-4,4),'leg':"jet #phi"}]

var_def += [{'def':("bjetPT",20, 0,400),'leg':"b-tagged jet p_{T}"}]
var_def += [{'def':("bjetETA",20,-5,5),'leg':"b-tagged jet #eta"}]

var_def += [{'def':("elecPT",20,0,400),'leg':"electron p_{T}"}]
var_def += [{'def':("elecPTLeading",20,0,400),'leg':"Leading electron p_{T}"}]
var_def += [{'def':("elecETA",24,-6,6),'leg':"electron #eta"}]
var_def += [{'def':("elecPHI",16,-4,4),'leg':"electron #phi"}]

var_def += [{'def':("dielecETA",50, -5.0, 5.0),'leg':"di-electron #eta"}]
var_def += [{'def':("dielecCOS",20, -1.5, 1.5),'leg':"di-electron Cos"}]
var_def += [{'def':("dielecMass",20, 0.0, 1000.0),'leg':"di-electron Mass"}]
var_def += [{'def':("dielecR",16, 0.0, 8.0),'leg':"di-electron R"}]

var_def += [{'def':("met",20,0,400),'leg':"Missing E_{T}"}]
var_def += [{'def':("WMass",50, 0, 500),'leg':"M_{W}"}]
var_def += [{'def':("TopMass",50, 0, 500),'leg':"SM M_{top}"}]

var_def += [{'def':("newWMass",50, 0, 500),'leg':"new-algorithm M_{W}"}]
var_def += [{'def':("newTopMass",50, 0, 500),'leg':"new-algorithm SM M_{top}"}]

var_def += [{'def':("nonTopMass",50, 0, 500),'leg':"#Delta#eta-algorithm non-SM M_{top}"}]
var_def += [{'def':("newnonTopMass",50, 0, 500),'leg':"min #Deltam leading jet non-SM M_{top}"}]
var_def += [{'def':("testnonTopMass",50, 0, 500),'leg':"min #Deltam all jet non-SM M_{top}"}]

#var_def += [{'def':("nonTopMass",20, 0, 500),'leg':"#Delta#eta-algorithm non-SM M_{top}"}]
#var_def += [{'def':("newnonTopMass",20, 0, 500),'leg':"min #Deltam leading jet non-SM M_{top}"}]
#var_def += [{'def':("testnonTopMass",20, 0, 500),'leg':"min #Deltam all jet non-SM M_{top}"}]

#var_def += [{'def':("newnonTopMass",20, 0, 1000),'leg':"new-algorithm non-SM M_{top}"}]


# loop on all the variables that you want to plot
for var in var_def:
    # this is just to define the name of the pdf file: if the key 'can' is in the dictionaly that will be the name, otherwise the name of the variable is used
    name_can = var['def'][0]
    # fianlly, the data_mc function is called
    signal_bkg_couplings (var['def'], sel, myweights, backgrounds, signals, name_infile, labels, var['leg'], lumi, logY, write, folder_out, name_can)


