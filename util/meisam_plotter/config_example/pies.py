import glob, os
from plot_utils import *

lumi = 36074.56 # Moriond 2017

# json file containing the definition of the regions for which you want to make the pie charts
json_name="json_example/sel_example.json"

# folder where to put the plots
outfolder="plots/example_pies/"
os.system("mkdir -p "+outfolder)

# dictionary that associated to each background you might want to use the corresponding root file name (in this case it's always the same file)
name_infile = dict()
name_infile_bkg = "/eos/atlas/user/c/crizzi/susy_EW/HF_inputs/tag.2.4.33-5-0_3b/Bkg_tag.2.4.33-5-0_3b.root"
backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar_light","ttbar_cc","ttbar_bb","ttbar"]
for b in backgrounds:
    name_infile[b]= name_infile_bkg

# weights needed for the MC
# these I want to be the same for all the pies
weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
myweights = "*".join(weights)

# In this case I want to plot "slices" of one single background, ttbar, divided by HF classification
myslice=["ttbar_class==0","ttbar_class<0","ttbar_class>0"]
backgrounds=["ttbar"]
labels_bkg = ["t#bar{t}+light","t#bar{t}+cc","t#bar{t}+bb"]
plot_pie (json_name, myweights, backgrounds, name_infile, labels_bkg, myslice, outfolder, "ttbar_class", region="sel", do_scale=False, print_err=False, print_raw=False)

# In this case I want to plot each background in its integrity, but divide different backgorunds
myslice=["1"]
backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar"]
labels_bkg = ["diboson","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}"]
plot_pie (json_name, myweights, backgrounds, name_infile, labels_bkg, myslice, outfolder, "pie_bkg", region="sel", do_scale=False, print_err=False, print_raw=False)

# ttbar leptonic classification: single-lepton vs dilepton
myslice = ["ttbar_decay_type>=6", "ttbar_decay_type<6"] # ttbar_decay_type >5 --> singke lep, ttbar_decay_type <= 5 --> dilepton
backgrounds=["ttbar"]
labels_bkg = ["sin. lep","dilep"]
plot_pie (json_name, myweights, backgrounds, name_infile, labels_bkg, myslice, outfolder, "pie_bkg", region="sel", do_scale=False, print_err=False, print_raw=False)

# ttbar dilepton classification
myslice = ["ttbar_decay_type==0", "ttbar_decay_type==1", "ttbar_decay_type==2", "ttbar_decay_type==3", "ttbar_decay_type==4", "ttbar_decay_type==5"]
labels_bkg = ["ee","e#mu", "e#tau", "#mu#mu", "#mu#tau","#tau#tau"]
backgrounds=["ttbar"]
plot_pie (json_name, myweights, backgrounds, name_infile, labels_bkg, myslice, outfolder, "pie_tt_dilep", region="sel", do_scale=False, print_err=False, print_raw=False)

# ttbar single-lepton classification
myslice = ["ttbar_decay_type>=6 && ttbar_decay_type<=9", "ttbar_decay_type>=10 && ttbar_decay_type<=13", "ttbar_decay_type>=14 && ttbar_decay_type<=17"]
labels_bkg = ["e+jets","#mu+jets","#tau+jets"]
backgrounds=["ttbar"]
plot_pie (json_name, myweights, backgrounds, name_infile, labels_bkg, myslice, outfolder, "pie_tt_sinlep", region="sel", do_scale=False, print_err=False, print_raw=False)

