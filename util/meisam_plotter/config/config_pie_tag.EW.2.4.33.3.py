import glob, os
from plot_utils import *

lumi = 36074.56 # Moriond 2017


json_name="../../HistFitter/v54/analysis/HF_EW/json_sel/sel.json"

folder_in="/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.33-4-0/"
folder_in_data="/nfs/pic.es/user/c/crizzi/scratch2/susy_EW/HF_inputs/tag.2.4.33-4-0/"
name_infile_data=folder_in_data+"Data_tag.2.4.33-4-0.root"
name_infile_bkg=folder_in+"Bkg_tag.2.4.33-4-0_Vjets221_nominal.root"
name_infile_signal=folder_in+"Sig_GGM_tag.2.4.33-4-0_nominal_all.root"


outfolder="./2017_08_24/"

if __name__ == "__main__":

    os.system("mkdir -p "+outfolder)

    name_infile = dict()
    #backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar_light","ttbar_cc","ttbar_bb"]
    backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar"]
    #backgrounds=["ttbar_light","ttbar_cc","ttbar_bb"]
    #backgrounds=["ttbar"]
    #labels_bkg = ["t#bar{t}+light","t#bar{t}+cc","t#bar{t}+bb"]   
    labels_bkg = ["diboson","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}"]
    #labels_bkg = ["QCD","non-QCD"]

    name_infile["Data"]=name_infile_data

    for b in backgrounds:
        name_infile[b]= name_infile_bkg

    weights = ["weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_WZ_2_2"]
    myweights = "*".join(weights)
    #myslice=["weight_lumi>2.081e-08 && weight_lumi<2.082e-08","!(weight_lumi>2.081e-08 && weight_lumi<2.082e-08)"]
    #myslice=["(is_QCD)","(!is_QCD)"]
    myslice=["ttbar_class==0","ttbar_class<0","ttbar_class>0"]
    #myslice=["1"]

    #plot_pie (json_name, myweights, backgrounds, name_infile, labels_bkg, myslice, outfolder, "pie_bkg", region="SR", do_scale=False)

    myslice = ["ttbar_decay_type>=6", "ttbar_decay_type<6"] # ttbar_decay_type >5 --> singke lep, ttbar_decay_type <= 5 --> dilepton
    backgrounds=["ttbar"]
    labels_bkg = ["sin. lep","dilep"]
    #plot_pie (json_name, myweights, backgrounds, name_infile, labels_bkg, myslice, outfolder, "pie_tt_dec", region="_", do_scale=False)

    myslice = ["ttbar_decay_type==0", "ttbar_decay_type==1", "ttbar_decay_type==2", "ttbar_decay_type==3", "ttbar_decay_type==4", "ttbar_decay_type==5"]
    labels_bkg = ["ee","e#mu", "e#tau", "#mu#mu", "#mu#tau","#tau#tau"]
    backgrounds=["ttbar"]
    #plot_pie (json_name, myweights, backgrounds, name_infile, labels_bkg, myslice, outfolder, "pie_tt_dilep", region="_", do_scale=False)

    myslice = ["ttbar_decay_type>=6 && ttbar_decay_type<=9", "ttbar_decay_type>=10 && ttbar_decay_type<=13", "ttbar_decay_type>=14 && ttbar_decay_type<=17"]
    labels_bkg = ["e+jets","#mu+jets","#tau+jets"]
    backgrounds=["ttbar"]
    #plot_pie (json_name, myweights, backgrounds, name_infile, labels_bkg, myslice, outfolder, "pie_tt_sinlep", region="_", do_scale=False)


    backgrounds=["diboson","Zjets","Wjets","TopEW","SingleTop","ttbar"]
    labels_bkg = ["diboson","Z+jets","W+jets","t#bar{t}+X","single top","t#bar{t}"]
    var = {'def':("met",15,100.,400),'leg':"E_{T}^{miss} [GeV]"}
    num_sel="pass_MET"
    den_sel="(baseline_electrons_n+baseline_muons_n)==0 && jets_n>=4 && bjets_n>=2 && pass_HLT_xe70_mht"
    #num_sel="bjets_n>=3"
    #den_sel="(baseline_electrons_n+baseline_muons_n)==0 && jets_n>=4 && bjets_n>=2"
    write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, #geq 4j, #geq 2b","reference: HLT_xe70_mht"]
    turn_on (var['def'], num_sel, den_sel, weights, backgrounds, name_infile, labels_bkg, var['leg'], outfolder="./", name_can="turn_on_2b_v2.pdf", doLogY=False, write=write)
    triggers = ["HLT_xe70_mht", "HLT_xe90_mht_L1XE50", "HLT_xe100_mht_L1XE50", "HLT_xe110_mht_L1XE50"]
    rn_sel = ["run_number<290000","run_number >= 296939 && run_number <= 302872", "run_number >= 302919 && run_number <= 303892", "run_number >= 303943"]
    it =0
    for tr in triggers:
        write_tr=[]
        write_tr.append(tr+" tunr on")
        print write_tr
        name_can = tr+"turn_on_v2.pdf"
        name_can_data = tr+"turn_on_data.pdf"
        den_sel_tr = den_sel+" && "+rn_sel[it]
        #turn_on (var['def'], num_sel, den_sel_tr, weights, backgrounds, name_infile, labels_bkg, var['leg'], outfolder="./", name_can=name_can, doLogY=False, write=write+write_tr)
        #turn_on_data (var['def'], num_sel, den_sel_tr, weights, backgrounds, name_infile, labels_bkg, var['leg'], outfolder="./", name_can=name_can_data, doLogY=False, write=write+write_tr)
        it+=1


    var = {'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}
    #signals=["GGM_hh_250_hhall"]
    signals=["GGM_Zh_250_Zhall"]
    labels_sig = ["m(#tilde{#chi}) = 250 GeV"]

    for s in signals:
        name_infile[s] = name_infile_signal

    if "can" in var.keys():
        name_can = var['can']
    else:
        name_can = var['def'][0]

    write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","0L, #geq 4j, #geq 3b","hh #rightarrow 4b"]
    sel="(pass_MET && met>200 && jets_n>=4 && bjets_n>=2 && (baseline_electrons_n+baseline_muons_n)==0)*(weight_mc*weight_lumi*weight_btag*weight_elec*weight_muon*weight_jvt*weight_WZ_2_2)"
    
    #sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_test", signals, labels_sig)
    var_def=[]
    #var_def += [{'def':("baseline_leptons_5_n",5, -0.5,4.5),'leg':"Number of baseline leptons pT > 5 GeV"}]
    #var_def += [{'def':("baseline_leptons_10_n",5, -0.5,4.5),'leg':"Number of baseline leptons pT > 10 GeV"}]
    #var_def += [{'def':("baseline_leptons_15_n",5, -0.5,4.5),'leg':"Number of baseline leptons pT > 15 GeV"}]
    #var_def += [{'def':("baseline_leptons_n",5, -0.5,4.5),'leg':"Number of baseline leptons pT > 20 GeV"}]
    var_def += [{'def':("bjets_n",4, 1.5,5.5),'leg':"Number of b-jets"}]
    var_def += [{'def':("meff_4bj",20,300,1300),'leg':"meff 4b [GeV]"}]
    var_def += [{'def':("ZCR_meff_4bj",20,300,1300),'leg':"meff 4b [GeV]"}]
    var_def += [{'def':("bjets_n",4, 1.5,5.5),'leg':"Number of b-jets"}]
    var_def += [{'def':("mTb_min",20,0,500),'leg':"m_{T}^{b,min}  [GeV]", "bvar":"mTb_min_tt"}]
    var_def += [{'def':("pt_bjet_1",20,0,1000),'leg':"p_{T} Leading b-jet [GeV]", "bvar":"pt_bjet_1_tt"}]
    var_def += [{'def':("pt_bjet_2",20,0,1000),'leg':"p_{T} Sub-leading b-jet [GeV]", "bvar":"pt_bjet_2_tt"}]
    var_def += [{'def':("met",20,0.,1000),'leg':"E_{T}^{miss} [GeV]"}]
    var_def += [{'def':("ZCR_met",18,200.,1000),'leg':"E_{T}^{miss} [GeV]"}]
    var_def += [{'def':("meff_incl",60, 0,3000),'leg':"m_{eff} [GeV]"}]
    var_def += [{'def':("jets_n",6, 3.5,9.5),'leg':"Number of jets"}]
    var_def += [{'def':("dphi_min",20,0,4),'leg':"#Delta#phi^{min}_{4j}(j,MET)"}]
    var_def += [{'def':("pt_jet_1",20,0,1000),'leg':"p_{T} Leading jet [GeV]"}]
    var_def += [{'def':("pt_jet_2",20,0,1000),'leg':"p_{T} Sub-leading jet [GeV]"}]
    var_def += [{'def':("max(DeltaR_h1_dR,DeltaR_h2_dR)",30,0,5), 'leg':'max dR(b_{1}, b_{2})', 'can':"dRmax_dR"}] 
    var_def += [{'def':("mass_h1_dR",15,50,200),'leg':"m(h1) [GeV]",'can':"mass_h1_min_dR"}]
    var_def += [{'def':("mass_h2_dR",15,50,200),'leg':"m(h2) [GeV]",'can':"mass_h2_min_dR"}]
    var_def += [{'def':("met_sig",15,0,30),'leg':"MET/#sqrt{H_{T}}   [#sqrt{GeV}]"}]

    #write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}","#geq 4j, #geq 2b","hh #rightarrow all"]
    write=["#bf{#it{ATLAS}} Internal","Simulation, 36.1 fb^{-1}"]
    sel="(pass_MET && met>200 && jets_n>=4 && bjets_n>=2)*(weight_mc*weight_lumi*weight_btag*weight_elec*weight_muon*weight_jvt*weight_WZ_2_2)"

    for var in var_def:
        if "can" in var.keys():
            name_can = var['can']
        else:
            name_can = var['def'][0]
            #sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_hhall", signals, labels_sig)     

    #sel="(pass_MET && met>200 && jets_n>=4 && bjets_n>=2 && (baseline_electrons_n+baseline_muons_n)==0 && dphi_min>0.4)*(weight_mc*weight_lumi*weight_btag*weight_elec*weight_muon*weight_jvt*weight_WZ_2_2)"
    sel="(((signal_muon_trig_pass && signal_muons_n==2) || (signal_electron_trig_pass && signal_electrons_n==2)) && pt_lep_1>60 && jets_n>=4 && bjets_n>=2 && signal_leptons_n==2 && ZCR_met>200 && fabs(Z_mass-91.2)<5 && Z_OSLeps && ZCR_meff_4bj>700 && max(DeltaR_h1_dR,DeltaR_h2_dR)<3)"
    myweights="(weight_mc*weight_lumi*weight_btag*weight_elec*weight_muon*weight_jvt*weight_WZ_2_2*weight_elec_trigger*weight_muon_trigger)"

    for var in var_def:
        if "can" in var.keys():
            name_can = var['can']+"_Vjets221"
        else:
            name_can = var['def'][0]+"_Vjets221"        
        #data_mc (var['def'], sel, myweights, backgrounds, name_infile, labels_bkg, var['leg'], lumi, True, write, outfolder, name_can, do_scale=False, add_signal = False)
        #sig_bkg (var['def'], sel, backgrounds,name_infile, labels_bkg, var['leg'], lumi, True, write, False, outfolder, name_can+"_ZVR", signals, labels_sig)
