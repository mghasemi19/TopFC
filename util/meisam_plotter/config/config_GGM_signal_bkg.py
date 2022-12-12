import glob, os
import plot_utils
from plot_utils import *

lumi = 36074.56 # Moriond 2017

remove_meff_corr=False

pickle_sel="../../cuts_pickle/sel_wei_dict_presel.pickle"
pickle_sel_no_wei="../../cuts_pickle/sel_dict_presel.pickle"

folder_in="/afs/cern.ch/user/c/crizzi/storage/susy_EW/merge_HF_inputs/"

name_infile_data=folder_in+"Data_2.4.28-0-0_skim_2b.root"
#name_infile_bkg=folder_in+"bkg_tagEW.2.4.28-1_nominal.root"
name_infile_bkg="../eos/atlas/user/c/crizzi/susy_EW/bkg_tagEW.2.4.28-1_v3_nominal_aliases.root"
name_infile_QCD=folder_in+""
name_infile_signal=folder_in+"Sig_GGM_17_03_22_tagEW.2.4.28-1_nominal_aliases.root"

outfolder="./2017_03_22/"

if __name__ == "__main__":

    os.system("mkdir -p "+outfolder)

    masses=["130","150","200","300","400","500","600","800"]
    weights=["weight_lumi","weight_mc"]
    name_infile = dict()
    for m in masses:
        name_infile[m] = name_infile_signal

    num_sel=["is_hh_4b"]
    legend = ["hh #rightarrow 4b"]
    den_sel = "1"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "is_hh_4b.pdf")

    num_sel=["is_hh_4b","hh_type==1","hh_type==2","hh_type==3","hh_type!=1 &&hh_type!=2 && hh_type!=3"]
    legend = ["hh #rightarrow 4b","hh #rightarrow 4b test","hh #rightarrow max 2b","hh #rightarrow 0b","no hh"]
    den_sel = "(signal_leptons_n)==0"
    #signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder, "is_hh_4b_test.pdf")


    # +++++++++++++
    # Data/MC plots
    # +++++++++++++
    var_def=[]

    var_def += [{'def':("max(DeltaR_h1_min_diff,DeltaR_h2_min_diff)",15,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_min_diff"}] 
    #var_def += [{'def':("(mass_h1_min_diff+mass_h2_min_diff)/2",15,50,200),'leg':"<m> [GeV]",'can':"mass_average_min_diff"}]
    #var_def += [{'def':("met",20,0.,1000),'leg':"E_{T}^{miss} [GeV]"}]
    #var_def += [{'def':("mTb_min",15,0,300),'leg':"m_{T}^{min}(b,MET) [GeV]"}]

    #var_def += [{'def':("mass_h1_min_diff",15,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_diff"}]
    # 'def': variable to plot: (name, nbins, x-low, x-max)
    # 'leg': legend of the x-axis

    #var_def += [{'def':("fabs(mass_h1_min_diff-mass_h2_min_diff)",20,0,100),'leg':"|m1-m2| [GeV]",'can':"mass_diff_min_diff"}]
    #var_def += [{'def':("fabs(mass_h1_115-mass_h2_115)",20,0,100),'leg':"|m1-m2| [GeV]",'can':"mass_diff_115"}]
    #var_def += [{'def':("fabs(mass_h1_dR-mass_h2_dR)",20,0,100),'leg':"|m1-m2| [GeV]",'can':"mass_diff_min_dR"}]

    #var_def += [{'def':("met_sig",30,0,30),'leg':"MET/#sqrt{H_{T}}   [#sqrt{GeV}]"}]
    #var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_dR"}] 
    #var_def += [{'def':("max(DeltaR_h1_115,DeltaR_h2_115)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_115"}] 



    """
    var_def += [{'def':("mass_h1_115",30,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_115"}]
    var_def += [{'def':("mass_h2_115",30,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_115"}]
    var_def += [{'def':("(mass_h1_115+mass_h2_115)/2",30,50,200),'leg':"<m> [GeV]",'can':"mass_average_115"}]
    var_def += [{'def':("DeltaR_h1_115",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{1}'}]
    var_def += [{'def':("DeltaR_h2_115",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{2}'}]

    var_def += [{'def':("(mass_h1_min_diff+mass_h2_min_diff)/2",30,50,200),'leg':"<m> [GeV]",'can':"mass_average_min_diff"}]
    var_def += [{'def':("mass_h1_min_diff",30,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_diff"}]
    var_def += [{'def':("mass_h2_min_diff",30,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_min_diff"}]
    var_def += [{'def':("DeltaR_h1_min_diff",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{1}'}]
    var_def += [{'def':("DeltaR_h2_min_diff",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{2}'}]

    var_def += [{'def':("(mass_h1_dR+mass_h2_dR)/2",30,50,200),'leg':"<m> [GeV]",'can':"mass_average_min_dR"}]
    var_def += [{'def':("mass_h1_dR",30,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_dR"}]
    """

    #var_def += [{'def':("(mass_h1_min_diff>100 && mass_h1_min_diff<140) + (mass_h2_min_diff>100 && mass_h2_min_diff<140)",3,-0.5,2.5),'leg':"Number of higgs candidates",'can':"h_cand_n_min_diff"}]
    #var_def += [{'def':("(mass_h1_115>100 && mass_h1_115<140) + (mass_h2_115>100 && mass_h2_115<140)",3,-0.5,2.5),'leg':"Number of higgs candidates",'can':"h_cand_n_115"}]
    #var_def += [{'def':("(mass_h1_max_pt>100 && mass_h1_max_pt<140) + (mass_h2_max_pt>100 && mass_h2_max_pt<140)",3,-0.5,2.5),'leg':"Number of higgs candidates",'can':"h_cand_n_max_pt"}]
    #var_def += [{'def':("(mass_h1_dR>100 && mass_h1_dR<140) + (mass_h2_dR>100 && mass_h2_dR<140)",3,-0.5,2.5),'leg':"Number of higgs candidates",'can':"h_cand_n_min_dR"}]

    """
    var_def += [{'def':("mass_h2_dR",30,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_min_dR"}]
    var_def += [{'def':("DeltaR_h1_dR",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{1}'}]
    var_def += [{'def':("DeltaR_h2_dR",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{2}'}]
    """
    #var_def += [{'def':("fabs(m_h1_max_pt-mass_h2_max_pt)",20,0,50),'leg':"|m1-m2| [GeV]",'can':"mass_diff_max_pt"}]
    #var_def += [{'def':("(m_h1_max_pt+mass_h2_max_pt)/2",30,50,200),'leg':"<m> [GeV]",'can':"mass_average_max_pt"}]



    #var_def += [{'def':("mass_h1_max_pt",30,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_max_pt"}]
    #var_def += [{'def':("mass_h2_max_pt",30,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_max_pt"}]
    #var_def += [{'def':("DeltaR_h1_max_pt",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{1}'}]
    #var_def += [{'def':("DeltaR_h2_max_pt",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{2}'}]

    #var_def += [{'def':("fabs(mass_h1_true_match-mass_h2_true_match)",50,0,50),'leg':"|m1-m2| [GeV]",'can':"mass_diff_true_match"}]
    #var_def += [{'def':("(mass_h1_true_match+mass_h2_true_match)/2",30,50,200),'leg':"<m> [GeV]",'can':"mass_average_true_match"}]
    #var_def += [{'def':("mass_h1_true_match",30,50,200),'leg':"<m> [GeV]",'can':"mass_h1_true_match"}]
    #var_def += [{'def':("mass_h2_true_match",30,50,200),'leg':"<m> [GeV]",'can':"mass_h2_true_match"}]
    #var_def += [{'def':("DeltaR_h1_true_match",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{1}'}]
    #var_def += [{'def':("DeltaR_h2_true_match",30,0,5), 'leg':'dR(b_{1}, b_{2}) h_{2}'}]

    #var_def += [{'def':("pt_trueb1_h1",16, 0,800),'leg':"true-b_{1} from h_{1} p_{T} [GeV]"}]
    #var_def += [{'def':("pt_trueb2_h1",16, 0,800),'leg':"true-b_{2} from h_{1} p_{T} [GeV]"}]
    #var_def += [{'def':("pt_trueb1_h2",16, 0,800),'leg':"true-b_{1} from h_{2} p_{T} [GeV]"}]
    #var_def += [{'def':("pt_trueb2_h2",16, 0,800),'leg':"true-b_{2} from h_{2} p_{T} [GeV]"}]

    #var_def += [{'def':("eta_trueb1_h1",40,-4,4),'leg':"true-b_{1} from h_{1} #eta"}]
    #var_def += [{'def':("eta_trueb2_h1",40,-4,4),'leg':"true-b_{2} from h_{1} #eta"}]
    #var_def += [{'def':("eta_trueb1_h2",40,-4,4),'leg':"true-b_{1} from h_{2} #eta"}]
    #var_def += [{'def':("eta_trueb2_h2",40,-4,4),'leg':"true-b_{2} from h_{2} #eta"}]
    
    """

    var_def += [{'def':("jets_n",11, -0.5,10.5),'leg':"Number of jets"}]
    var_def += [{'def':("signal_leptons_n",5, -0.5,4.5),'leg':"Number of signal leptons"}]
    var_def += [{'def':("asymmetry",20, 0.,1.),'leg':"Asymmetry"}]
    var_def += [{'def':("bjets_n_85",6, -0.5,5.5),'leg':"Number of b-jets 85%"}]
    var_def += [{'def':("bjets_n_70",6, -0.5,5.5),'leg':"Number of b-jets 70%"}]
    var_def += [{'def':("bjets_n_77",6, -0.5,5.5),'leg':"Number of b-jets 77%"}]
    var_def += [{'def':("bjets_n_60",6, -0.5,5.5),'leg':"Number of b-jets 60%"}]
    var_def += [{'def':("pt_jet_1",16, 0,800),'leg':"1st jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_2",16, 0,800),'leg':"2nd jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_3",16, 0,800),'leg':"3rd jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_4",16, 0,800),'leg':"4th jet p_{T} [GeV]"}]
    var_def += [{'def':("pt_jet_5",16, 0,800),'leg':"5th jet p_{T} [GeV]"}]
    var_def += [{'def':("ht",20,0.,1000),'leg':"HT [GeV]"}]
    var_def += [{'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
    var_def += [{'def':("dphi_1jet",20,0,4),'leg':"#Delta#phi(j^{1},MET)"}]
    var_def += [{'def':("MJSum_rc_r08pt10",25,0,500),'leg':"MJSum [GeV]"}]
    """
    #var_def += [{'def':("dphi_mettrack_met",20,0,4),'leg':"#Delta#phi(MET^{track},MET)"}]

                

    #signals=["GGM_hh_130","GGM_hh_150","GGM_hh_200","GGM_hh_300","GGM_hh_400","GGM_hh_500","GGM_hh_600","GGM_hh_800"]
    signals=["GGM_hh_150","GGM_hh_200","GGM_hh_500","GGM_hh_800"]
    name_infile = dict()
    for s in signals:
        name_infile[s] = name_infile_signal

    backgrounds=["dijet","Zjets","Wjets","TopEW","SingleTop","ttbar"]
    #backgrounds=["ttbar"]
    for b in backgrounds:
        name_infile[b]= name_infile_bkg

    labels_sig = ["m(#tilde{#chi}) = 150 GeV","m(#tilde{#chi}) = 200 GeV","m(#tilde{#chi}) = 500 GeV","m(#tilde{#chi}) = 800 GeV"]
    labels_bkg = ["dijet","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}"]
    #labels_bkg = ["t#bar{t}"]

    for var in var_def:
        if "can" in var.keys():
            name_can = var['can']
        else:
            name_can = var['def'][0]

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j30, 2b77, met>200"]
        sel="(pt_jet_4>30 && is_hh_4b && jets_n>=4 && bjets_n_77>=2 && pt_bjet_2>30 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>200)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j30_2b77_met200", signals, labels_sig)
        """

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j30, 3b77, met>200"]
        sel="(pt_jet_4>30 && is_hh_4b && jets_n>=4 && bjets_n_77>=3 && pt_bjet_3>30  && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>200)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j30_3b77_met200", signals, labels_sig)

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j30, 4b77, met>200"]
        sel="(pt_jet_4>30 && is_hh_4b && jets_n>=4 && bjets_n_77>=4 && pt_bjet_4>30 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>200)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j30_4b77_met200", signals, labels_sig)

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j20, 2b77, met>200"]
        sel="(is_hh_4b && jets_n>=4 && bjets_n_77>=2 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>200)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j20_2b77_met200", signals, labels_sig)

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j20, 3b77, met>200"]
        sel="(is_hh_4b && jets_n>=4 && bjets_n_77>=3 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>200)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j20_3b77_met200", signals, labels_sig)

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j20, 4b77, met>200"]
        sel="(is_hh_4b && jets_n>=4 && bjets_n_77>=4 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>200)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j20_4b77_met200", signals, labels_sig)

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j20, 2b77, met>180"]
        sel="(is_hh_4b && jets_n>=4 && bjets_n_77>=2 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>180)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j20_2b77_met180", signals, labels_sig)

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j20, 3b77, met>180"]
        sel="(is_hh_4b && jets_n>=4 && bjets_n_77>=3 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>180)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j20_3b77_met180", signals, labels_sig)

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j20, 4b77, met>180"]
        sel="(is_hh_4b && jets_n>=4 && bjets_n_77>=4 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>180)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j20_4b77_met180", signals, labels_sig)

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j20, 2b70, met>180"]
        sel="(is_hh_4b && jets_n>=4 && bjets_n_70>=2 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>180)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j20_2b70_met180", signals, labels_sig)

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j20, 3b70, met>180"]
        sel="(is_hh_4b && jets_n>=4 && bjets_n_70>=3 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>180)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j20_3b70_met180", signals, labels_sig)

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j20, 4b70, met>180"]
        sel="(is_hh_4b && jets_n>=4 && bjets_n_70>=4 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>180)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j20_4b70_met180", signals, labels_sig)

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j20, 2b85, met>180"]
        sel="(is_hh_4b && jets_n>=4 && bjets_n_85>=2 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>180)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j20_2b85_met180", signals, labels_sig)

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j20, 3b85, met>180"]
        sel="(is_hh_4b && jets_n>=4 && bjets_n_85>=3 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>180)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j20_3b85_met180", signals, labels_sig)

        write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, 4j20, 4b85, met>180"]
        sel="(is_hh_4b && jets_n>=4 && bjets_n_85>=4 && signal_leptons_n==0 && pass_MET && dphi_min>0.4 && met>180)*(weight_mc*weight_lumi)"
        sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_4j20_4b85_met180", signals, labels_sig)
        """

    for var in var_def:
        # list of things to write on the plot
        #print var['def']
        if "can" in var.keys():
            name_can = var['can']
        else:
            name_can = var['def'][0]

        if "true_match" in var['def'][0]:
            sel="(is_hh_4b && match_possible)*(weight_mc*weight_lumi)"
            write=["#bf{#it{ATLAS}} Internal","hh #rightarrow 4b, true match"]
            #plot_var(var['def'], sel, signals, name_infile, name_infile, labels,var['leg'], myslice, outfolder, name_can+"_true_match", lumi, do_scale=False, doLogY=True, write=write)
            #plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_true_match", do_scale=True, doLogY=False, write=write)

        sel="(is_hh_4b)*(weight_mc*weight_lumi)"
        write=["#bf{#it{ATLAS}} Internal","hh #rightarrow 4b"]
        #plot_var(var['def'], sel, signals, name_infile, labels,var['leg'], myslice, outfolder,name_can, do_scale=False, doLogY=True, write=write)
        #plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can, do_scale=True, doLogY=False, write=write)

        sel="(is_hh_4b && jets_n>=4)*(weight_mc*weight_lumi)"
        write=["#bf{#it{ATLAS}} Internal","hh #rightarrow 4b, #geq 4 jets"]
        #plot_var(var['def'], sel, signals, name_infile, labels,var['leg'], myslice, outfolder,name_can+"_4j", do_scale=False, doLogY=True, write=write)
        #plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_4j", do_scale=True, doLogY=False, write=write)

        sel="(is_hh_4b && pass_MET && met>180 && jets_n>=4 && bjets_85_n>=2 && dphi_min>0.4)*(weight_mc*weight_lumi)"
        write=["#bf{#it{ATLAS}} Internal","hh #rightarrow 4b, Preselection"]
        #plot_var(var['def'], sel, signals, name_infile, labels,var['leg'], myslice, outfolder,name_can+"_presel", do_scale=False, doLogY=True, write=write)
        #plot_var(var['def'], sel, signals, name_infile, labels, var['leg'], myslice, outfolder,name_can+"_presel", do_scale=True, doLogY=False, write=write)

