#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# macro to produce plots starting form HF input files and pickle file with the dictionary for the selections
# to be used to produce:
# - pie charts for composition studies
# - data/MC plots pre-fit
# - shape-comparison of variables in MC
# - signal vs bkg plots
# - diagnostic plots like pile-up dependence
# authors: chiara rizzi chiara.rizzi@cern.ch
#          meisam ghasemi mghasemi@ipm.ir
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import pickle, sys
import glob, os
import re
import ROOT
from array import array
import time
import json
import math
import types

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

# Make legend 
def make_leg(n, labels, x1=0.7, y1=0.6, x2=0.876, y2=0.87, hdata=None, textSize=0):
    leg=ROOT.TLegend(x1,y1,x2,y2)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.SetLineWidth(0)
    if textSize>0:
        leg.SetTextFont(43)
        leg.SetTextSize(textSize)
    i=len(n)
    if not hdata is None:
        leg.AddEntry(hdata, "Data")
    for h in reversed(n):
        i-=1
        if "hh" in labels[i]:
            continue
        if h.GetFillColor() or "ulti" in labels[i] :
            leg.AddEntry(h,labels[i],"f")
        else:
            leg.AddEntry(h,labels[i].replace("GGM_","").replace("_"," "),"l")
    i=len(n)
    for h in reversed(n):
        i-=1
        if not "hh" in labels[i]:
            continue
        if h.GetFillColor() :
            leg.AddEntry(h,labels[i],"f")
        else:
            leg.AddEntry(h,labels[i].replace("GGM_","").replace("_"," "),"l")

    return leg

# Get sample color for backgrounds and signals
def getSampleColor(sample):
    if "_NoSys" in sample:
        sample = sample.replace("_NoSys","")
    if "_nominal" in sample:
        sample = sample.replace("_nominal","")
    # sample colors for SUSY analyses
    if sample == "ttbar_bb":         return ROOT.kBlue-6
    if sample == "ttbar_cc":         return ROOT.kBlue-10
    if sample == "ttbar_light":         return ROOT.kWhite
    if sample == "ttbar":         return ROOT.kAzure+8
    if sample == "Wjets":       return ROOT.kOrange-3
    if sample == "W":       return ROOT.kOrange-3
    if sample == "multijet":       return ROOT.kWhite
    if sample == "Zjets":     return ROOT.kYellow-4
    if sample == "Z":     return ROOT.kYellow-4
    if sample == "Wjets_220":       return ROOT.kOrange-3
    if sample == "W_jets":       return ROOT.kOrange-3
    if sample == "Zjets_220":     return ROOT.kYellow-4
    if sample == "Z_jets":     return ROOT.kYellow-4
    if sample == "singletop":     return ROOT.kGreen-9
    if sample == "SingleTop":     return ROOT.kGreen-9
    if sample == "SingleTop_DS":     return ROOT.kGreen-9
    if sample == "TopEW":     return ROOT.kGreen+2
    if sample == "topEW":     return ROOT.kGreen+2
    if sample == "diboson":     return ROOT.kRed+1
    if sample == "other":     return ROOT.kRed+1
    if sample == "Dijets":     return ROOT.kOrange-4
    if sample == "Dijet":     return ROOT.kOrange-4
    if sample == "dijet":     return ROOT.kOrange-4
    
    if sample == "Dibosons": return ROOT.kRed+1
    if sample == "Fourtops": return ROOT.kRed+3
    if sample == "ttbarlight": return ROOT.kWhite
    if sample == "ttbarcc": return ROOT.kViolet-3
    if sample == "ttbarbb": return ROOT.kPink+1

    # sample colors for TopFC analysis
    if sample == "ttbarW": return ROOT.kOrange-3
    if sample == "ttbarZ": return ROOT.kYellow-4
    if sample == "tttt": return ROOT.kGreen-9
    if sample == "tZ": return ROOT.kGreen+2
    if sample == "WZ": return ROOT.kRed+1
    if sample == "ZZ": return ROOT.kOrange-4
    
    if sample == "signalcharm": return ROOT.kPink+1
    if sample == "signalup": return ROOT.kAzure+1
    
    #colors = [609, 856, 410, 801, 629, 879, 602, 921, 622]

    if "300_hh4b" in sample: return ROOT.kPink+1
    if "500_hh4b" in sample: return ROOT.kGreen+1
    if "400_hh4b" in sample: return ROOT.kGreen+1
    if "800_hh4b" in sample: return ROOT.kRed+1
    if "600_hh4b" in sample: return ROOT.kAzure+1

    if "250_hhall" in sample: return ROOT.kPink+1
    if "300_hhall" in sample: return ROOT.kPink+1
    if "500_hhall" in sample: return ROOT.kGreen+1
    if "400_hhall" in sample: return ROOT.kGreen+1
    if "800_hhall" in sample: return ROOT.kRed+1
    if "600_hhall" in sample: return ROOT.kAzure+1
    if "700_hhall" in sample: return ROOT.kAzure+1

    if "300_Zh4b" in sample: return ROOT.kPink+2
    if "500_Zh4b" in sample: return ROOT.kGreen+2
    if "800_Zh4b" in sample: return ROOT.kRed+2
    if "600_Zh4b" in sample: return ROOT.kAzure+2

    if "300_ZZ4b" in sample: return ROOT.kPink+3
    if "500_ZZ4b" in sample: return ROOT.kGreen+3
    if "800_ZZ4b" in sample: return ROOT.kRed+3
    if "600_ZZ4b" in sample: return ROOT.kAzure+3

    if "150_Zhllbb" in sample: return ROOT.kBlue
    if "200_Zhllbb" in sample: return ROOT.kOrange
    if "300_Zhllbb" in sample: return ROOT.kPink+1
    if "500_Zhllbb" in sample: return ROOT.kTeal
    if "400_Zhllbb" in sample: return ROOT.kGreen+1
    if "800_Zhllbb" in sample: return ROOT.kRed+1
    if "600_Zhllbb" in sample: return ROOT.kAzure+1

    if "200_ZZllbb" in sample: return ROOT.kOrange
    if "300_ZZllbb" in sample: return ROOT.kPink+1
    if "500_ZZllbb" in sample: return ROOT.kGreen+1
    if "400_ZZllbb" in sample: return ROOT.kGreen+1
    if "800_ZZllbb" in sample: return ROOT.kRed+1
    if "600_ZZllbb" in sample: return ROOT.kAzure+1

    if "_130" in sample: return 609
    if "_150" in sample: return 856
    if "_200" in sample: return 410
    if "_300" in sample: return 801
    if "_400" in sample: return 629
    if "_500" in sample: return 879
    if "_600" in sample: return 602
    if "_800" in sample: return 921

    else:
        print "cannot find color for sample (",sample,")"
    return 1

   
def skip_sel(key, region):
    if "weights" in key:
        return True
    if "_L_" in key:
        return True
    if not region in key: return True
    else: return False

def signal_bkg (var, selection, myweights, backgrounds, signals, name_infile, labels, title_x_axis, lumi, logY=False, write=[], outfolder="./plots/", name_can="", do_overflow=True, is_2D=False):
    is_2D = False    
    if len(var)>4:
        is_2D = True

    # Get all the necessary files
    infile = dict()
    for b in backgrounds:
        infile[b]= ROOT.TFile.Open(name_infile[b],"READ")

    for m in signals:
        infile[m]=ROOT.TFile.Open(name_infile[m],"READ")

    # First draw signal histograms    
    h_signals = []
    for m in signals:
        t_signal = infile[m].Get(m)
        name_h_sig = name_can+m
        hsignal = ROOT.TH1D(name_h_sig, name_h_sig, var[1], var[2], var[3])
        hsignal.GetXaxis().SetTitle(title_x_axis)
        hsignal.Sumw2()
        string_draw=var[0]+">>"+name_can+m
        #print string_draw
        sel_signal = ""
        #sel_signal="("+sel+")*("+signal_sel+")"
        t_signal.Draw(string_draw,sel_signal,"goff")
            
        if not do_overflow:
           hsignal_of = ROOT.TH1D(name_h_sig+"_of", name_h_sig+"_of", var[1], var[2], var[3])
           hsignal_of.Sumw2()
           string_draw_of = str(var[3]) + " - (0.5*("+ str(var[3])+"-"+str(var[2])+")/"+str(var[1]) +") >>"+name_h_sig+"_of"
           #12 - (0.5*(12-0)/12) >>jetNo_signal_charm_of
           #print (string_draw_of)
           t_signal.Draw(string_draw_of, sel_signal+"*("+ var[0]+">"+str(var[3])  +")")
           hsignal.Add(hsignal_of)                    

        if do_overflow:
           hsignal_of = ROOT.TH1D(name_h_sig+"_of", name_h_sig+"_of", var[1], var[2], var[3])
           hsignal_of.Sumw2()
	   string_draw_of = var[0]+">>"+name_h_sig+"_of"
           t_signal.Draw(string_draw_of,sel_signal,"goff")
           hsignal_of.GetXaxis().SetRangeUser(var[2], var[3]+1)

        hsignal_of.Scale(lumi)
        h_signals.append(hsignal_of)


    sel = "("+selection+")*"+myweights
    print sel
    n=[]
    n_allbkg=[]
    colors=[]
    for b in backgrounds:
        """
        if do_scale:
        with open(mypickle_fit, 'rb') as handle2:
        fit_res = pickle.load(handle2)
        prefit = fit_res["MC_exp_events_"+b][0]
        postfit = fit_res["Fitted_events_"+b][0]
        SF=postfit/prefit
        """
        n_thisbkg=[]
        color=getSampleColor(b)
        colors.append(color)

        t = infile[b].Get(b)
        if (not t):
           print b,"not found"
           continue
        sel_slice=sel
        if is_2D:
            htmp=ROOT.TH2D(name_can+"_"+b, name_can+"_"+b, var[1], var[2], var[3], var[5], var[6], var[7])
            string_draw=var[4]+":"+var[0]+" >>"+name_can+"_"+b
            htmp.GetXaxis().SetTitle(name_can)
            htmp.Sumw2()
            t.Draw(string_draw,sel_slice,"goff")
            htmp.Scale(lumi)
            n_thisbkg.append(htmp.Clone())
            htmp.Clear()
        else:                        
            htmp_name = name_can+"_"+b
            htmp=ROOT.TH1D(htmp_name, htmp_name, var[1], var[2], var[3])
            htmp.GetXaxis().SetTitle(title_x_axis)
            htmp.Sumw2()
            string_draw=var[0]+">>"+name_can+"_"+b
            print string_draw
            t.Draw(string_draw,sel,"goff")

            if not do_overflow:
               htmp_of = ROOT.TH1D(htmp_name+"_of", htmp_name+"_of", var[1], var[2], var[3])
               htmp_of.Sumw2()
               string_draw_of = str(var[3]) + " - (0.5*("+ str(var[3])+"-"+str(var[2])+")/"+str(var[1]) +") >>"+name_can+"_"+str(i)+"_"+b+"_of"
               t.Draw(string_draw_of, sel_slice+"*("+ var[0]+">"+str(var[3])  +")")
               htmp.Add(htmp_of)                    

            if do_overflow:
               htmp_of = ROOT.TH1D(htmp_name+"_of", htmp_name+"_of", var[1], var[2], var[3])
               htmp_of.Sumw2()
               string_draw_of = var[0]+">>"+htmp_name+"_of"
               print (string_draw_of)
               t_signal.Draw(string_draw_of,sel,"goff")
               htmp_of.GetXaxis().SetRangeUser(var[2], var[3]+1)	       

            htmp_of.Scale(lumi)
            n_thisbkg.append(htmp_of.Clone())
            htmp.Clear()
            htmp_of.Clear()

        n_allbkg.append(n_thisbkg)

    print (n_allbkg)
    quit()


    if len(slices)>1: # look at the composizion of one background
        isel=0
        for s in slices: # loop sulle slice
            n_sel=ROOT.TH1D(name_can, name_can, var[1], var[2], var[3])
            for n_allbkg_i in n_allbkg:
                n_sel.Add(n_allbkg_i[isel])
            isel+=1
            n.append(n_sel)
    else: # look at bkg composition
        for n_allbkg_i in n_allbkg:
            n.append(n_allbkg_i[0])

    histo_max=0
    i=0
    stack = ROOT.THStack("stack","stack")
    for h in n:
                #print h.Integral()
        h.SetLineColor(colors[i])
        h.SetFillColor(colors[i])
        h.SetLineColor(1)
        h.GetXaxis().SetTitle(var[0])
        if h.GetMaximum() > histo_max:
            histo_max=h.GetMaximum()
        stack.Add(h)
        if i==0:
            htot=h.Clone("htot")
        else:
            htot.Add(h)
        i+=1

    c = ROOT.TCanvas("can"+name_can,"can"+name_can,600,600)
    if is_2D:
        pad2 = ROOT.TPad("pad2", "pad2",0.0,0.0,1.0,1.0,22)
    elif not do_fraction:
        pad1 = ROOT.TPad("pad1", "pad1",0.0,0.35,1.0,1.0,21)
        pad2 = ROOT.TPad("pad2", "pad2",0.0,0.0,1.0,0.35,22)
        pad2.SetGridy()
        pad1.SetFillColor(0)
        pad1.Draw()
    else:
        pad1 = ROOT.TPad("pad1", "pad1",0.0,0.47,1.0,1.0,21)
        pad3 = ROOT.TPad("pad3", "pad3",0.0,0.24,1.0,0.50,22)
        pad2 = ROOT.TPad("pad2", "pad2",0.0,0.0,1.0,0.26,22)
        pad2.SetGridy()
        pad1.SetFillColor(0)
        pad3.SetGridy()
        pad1.SetFillColor(0)
        pad1.SetFillStyle(0)
        pad2.SetFillColor(0)
        pad2.SetFillStyle(0)
        pad3.SetFillColor(0)
        pad3.SetFillStyle(0)
        pad1.SetTickx()
        pad2.SetTickx()
        pad3.SetTickx()
        pad1.SetTicky()
        pad2.SetTicky()
        pad3.SetTicky()
        pad1.Draw()
        pad3.Draw()

    pad2.SetFillColor(0)
    pad2.Draw()

    # chiara: here
    if do_fraction:
        n_frac=[]
        for h in n:
            n_frac.append(h.Clone())
        stack_fraction = ROOT.THStack("stack_fraction","stack_fraction")
        for i in range(0,htot.GetNbinsX()+2):
            for h in n_frac:
                if htot.GetBinContent(i)>0:
                    frac = 100*h.GetBinContent(i)/htot.GetBinContent(i)
                    h.SetBinContent(i,frac)
                else:
                    h.SetBinContent(i,0)
        for h in n_frac:
            stack_fraction.Add(h)

        pad3.cd()
        stack_fraction.Draw("histo")
        #pad3.SetTopMargin(0.01)
        #pad3.SetBottomMargin(0.01)

        hone = htot.Clone("hone")
        for ibin in range(1, hone.GetNbinsX()+1):
            hone.SetBinContent(ibin, 100)
        hone.SetMaximum(100/2.)
        hone.GetYaxis().SetTitle("Composition [%]")

        hone.SetFillStyle(0)
        hone.GetXaxis().SetTitleSize(0)
        hone.GetXaxis().SetLabelSize(0)
        hone.GetYaxis().SetTitleFont(43)
        hone.GetYaxis().SetTitleSize(19)
        hone.GetYaxis().SetLabelFont(43)
        hone.GetYaxis().SetLabelSize(15)
        hone.GetYaxis().SetTitleOffset(1.3)        
        hone.Draw('histo')

        stack_fraction.Draw("histo same")        
        pad3.SetGridy()
        pad3.SetTicky()
        pad3.SetTickx()
        pad3.RedrawAxis("g")
        pad3.Update()


    if do_blind:
        hdata = htot.Clone("h_tot_pseudo_data")

    if not is_2D:
        pad1.cd()
        if logY:
            histo_max *= 150
            pad1.SetLogy()

        hdata.SetMarkerStyle(20)
        histo_max=max(histo_max,hdata.GetMaximum())

        stack.Draw("hist")

        stack.GetYaxis().SetTitleFont(43)
        stack.GetYaxis().SetTitle("Events")
        stack.GetYaxis().SetTitleSize(19)
        stack.GetYaxis().SetLabelFont(43)
        stack.GetYaxis().SetLabelSize(15)
        stack.GetYaxis().SetTitleOffset(1.3)        

        stack.GetXaxis().SetTitle(title_x_axis)
        stack.GetXaxis().SetTitleFont(43)
        stack.GetXaxis().SetTitleSize(19)
        stack.GetXaxis().SetLabelFont(43)
        stack.GetXaxis().SetLabelSize(15)
        stack.GetXaxis().SetTitleOffset(1.5)        

        pad1.SetBottomMargin(0.14)
        pad1.SetTickx()
        pad1.SetTicky()

        stack.SetMaximum(1.4 * histo_max)
        stack.SetMinimum(0.1)

        stack.Draw("hist")
        hdata.Draw("E0 same")

        pad1.RedrawAxis()

        leg = make_leg(n, labels, hdata=hdata)
        leg.Draw()

        text =  ROOT.TLatex()
        text.SetNDC()
        text.SetTextAlign( 11 )
        text.SetTextFont( 42 )
        text.SetTextSize( 0.05 )
        text.SetTextColor( 1 )
        y = 0.82
        #write.append(region.replace("_","-"))
        for t in write:
            text.DrawLatex(0.15,y, t)
            y = y-0.06
            #text.DrawLatex(0.15,y, var[0].replace("_","-"))
        pad1.Update()

    pad2.cd()
    pad2.SetTicky()
    hratio = hdata.Clone("h_ratio")

    hratio.GetYaxis().SetTitleFont(43)
    hratio.GetYaxis().SetTitleSize(19)

    hratio.GetYaxis().SetLabelFont(43)
    hratio.GetYaxis().SetLabelSize(15)
    hratio.GetYaxis().SetTitleOffset(1.3)        
    hratio.GetYaxis().SetTitle("Data/MC")
    hratio.Divide(htot)
    hratio.SetLineColor(1)
    hratio.SetMinimum(0)
    hratio.SetMaximum(2)
    hratio.Draw()

    if is_2D:
        hratio.GetXaxis().SetTitle(var[0])
        hratio.GetXaxis().SetTitleFont(43)
        hratio.GetXaxis().SetTitleSize(19)
        hratio.GetXaxis().SetLabelFont(43)
        hratio.GetXaxis().SetLabelSize(15)
        hratio.GetXaxis().SetTitleOffset(1.3)
        hratio.GetXaxis().SetTitle(var[4])
        hratio.Draw("COLZ")
        hratio.Draw("TEXTE same")
        text =  ROOT.TLatex()
        text.SetNDC()
        text.SetTextAlign( 11 )
        text.SetTextFont( 42 )
        text.SetTextSize( 0.05 )
        text.SetTextColor( 1 )
        y = 0.82
        for t in write:
            text.DrawLatex(0.15,y, t)
            y = y-0.06
            #text.DrawLatex(0.15,y, var[0].replace("_","-"))
        pad2.Update()


    if not is_2D:
        hratio.GetXaxis().SetLabelSize(0)
        hratio.GetXaxis().SetTitleSize(0)
        hline=ROOT.TH1D("hline", "hline", 1, var[2], var[3])
        hline.SetLineColor(ROOT.kRed)
        hline.SetBinContent(1,1)
        hline.GetYaxis().SetTitle("Data/MC")
        hline.Draw("same")
        #pad2.SetTopMargin(0.01)
        #pad2.SetBottomMargin(0.3)


    name_can = "data_mc_"+name_can
    if add_signal:
        name_can=name_can+"_sig"
    if do_scale:
        name_pdf=name_can+"_scale.pdf"
    else:
        name_pdf=name_can
    c.SaveAs(outfolder+name_pdf+".pdf")
    c.SaveAs(outfolder+name_pdf+".png")
    print outfolder+name_pdf
    c.Clear()
    stack.Clear()

def data_mc_all (var, mypickle_sel, backgrounds, name_infile, labels, title_x_axis, lumi, region="_", logY=False, write=[], outfolder="./", name_can="", do_scale=False, add_signal = False):
    print "ciao"

    with open(mypickle_sel, 'rb') as handle:
        x = pickle.load(handle)
        weights=x["weights"]
        myweights = "("
        for mywei in weights:
            mywei=mywei.replace("weight_muon_trigger","(weight_muon_trigger==0 + weight_muon_trigger)")
            myweights += mywei
            myweights += "*"            
        myweights = myweights[0:-1]
        myweights+=')'      

        for key in x.keys():
            if skip_sel(key, region): continue
            selection = x[key]
            # ifae top
            data_mc (var, selection, myweights, backgrounds, name_infile, labels, title_x_axis, lumi, logY, write, outfolder, name_can, do_scale, add_signal)


def region_composition(json_dict,  backgrounds, myweights, name_infile, labels, region="", slices=["1"], write=[], outfolder="./", name_can=""):
    print "ciao"
    with open(json_dict, 'rb') as handle:
        x = json.load(handle)
    x_sel = dict()

    if ',' in region:
        region_list = region.split(',') 
        for key in region_list:
            x_sel[key] = x[key]
    else:
        for key in x:
            if len(region)>0:
                if region not in key: continue
            x_sel[key] = x[key]
        region_list = sorted(x_sel)

    infile = dict()
    for b in backgrounds:
        infile[b]= ROOT.TFile.Open(name_infile[b],"READ")

    n=[]
    n_allbkg=[]
    colors=[]
    if len(slices)>1:
        colors = [410, 856, 607, 801, 629, 879, 602, 921, 622]
    for b in backgrounds:
        n_thisbkg=[]

        if not len(slices)>1:
            color=getSampleColor(b)                #print b,color
            colors.append(color)

        print b
        t = infile[b].Get(b)
        if (not t):
            b=b+"_nominal"  
            t = infile[b].Get(b)                  
            if (not t):
                print b,"not found"
                continue

        i=0
        for s in slices:
            htmp_name = name_can+"_"+str(i)+"_"+b
            # temporary histogram, one for each background, with one bin for each region
            htmp=ROOT.TH1D(htmp_name, htmp_name, len(x_sel), 0, len(x_sel))
            htmp.Sumw2()
            
            # loop on the selections to fill the histogram
            ibin=1
            for key in region_list:
                selection = x_sel[key]
                sel = "("+selection+")*"+myweights
                print sel
                sel_slice=sel+"*("+s+")"
                htmp_name_reg = name_can+"_"+str(i)+"_"+b+"_"+key
                htmp_reg = ROOT.TH1D(htmp_name_reg,htmp_name_reg, 1, -1, 2)
                t.Draw("1>>"+htmp_name_reg,sel_slice,"goff")
                yields = htmp_reg.Integral()
                htmp.SetBinContent(ibin, yields)
                ibin+=1

            n_thisbkg.append(htmp.Clone())
            htmp.Clear()
            i+=1

        n_allbkg.append(n_thisbkg)

    if len(slices)>1: # look at the composizion of one background
        isel=0
        for s in slices: # loop sulle slice
            n_sel=ROOT.TH1D(name_can, name_can, len(x_sel), 0, len(x_sel))
            for n_allbkg_i in n_allbkg:
                n_sel.Add(n_allbkg_i[isel])
            isel+=1
            n.append(n_sel)
    else: # look at bkg composition
        for n_allbkg_i in n_allbkg:
            n.append(n_allbkg_i[0])

    histo_max=0
    i=0
    stack = ROOT.THStack("stack","stack")
    for h in n:
                #print h.Integral()
        h.SetLineColor(colors[i])
        h.SetFillColor(colors[i])
        h.SetLineColor(1)
        #h.GetXaxis().SetTitle(var[0])
        if h.GetMaximum() > histo_max:
            histo_max=h.GetMaximum()
        stack.Add(h)
        if i==0:
            htot=h.Clone("htot")
        else:
            htot.Add(h)
        i+=1


    n_frac=[]
    for h in n:
        n_frac.append(h.Clone())
    stack_fraction = ROOT.THStack("stack_fraction","stack_fraction")
    for i in range(0,htot.GetNbinsX()+2):
        for h in n_frac:
            if htot.GetBinContent(i)>0:
                frac = 100*h.GetBinContent(i)/htot.GetBinContent(i)
                h.SetBinContent(i,frac)
            else:
                h.SetBinContent(i,0)
    for h in n_frac:
        stack_fraction.Add(h)
    stack_fraction.SetMaximum(100)

    hone = htot.Clone("hone")

    def rename_regions(name):
        name= name.replace("VR1L", "VR-1L")
        name= name.replace("VR0L", "VR-0L")
        name= name.replace("SR1L", "SR-1L")
        name= name.replace("SR0L", "SR-0L")
        name= name.replace("IStR", "ISR")
        name= name.replace("VR1-Gtt-1L","VR-m_{T}-Gtt-1L")
        name= name.replace("VR2-Gtt-1L","VR-m_{T,min}^{b-jets}-Gtt-1L")
        return name

    for ibin in range(1, hone.GetNbinsX()+1):
        hone.SetBinContent(ibin, 1)
        hone.GetXaxis().SetBinLabel(ibin, rename_regions(region_list[ibin-1].replace('_','-')))
    hone.SetMaximum(100)

    honezero = htot.Clone("hone")
    for ibin in range(1, hone.GetNbinsX()+1):
        if ibin%2 == 0:
            honezero.SetBinContent(ibin, 100)
        else:
            honezero.SetBinContent(ibin, 0)
    honezero.SetFillStyle(0)
    honezero.SetLineColor(1)
        
    c = ROOT.TCanvas("can"+name_can,"can"+name_can,1500,600)
    pad1 = ROOT.TPad("pad1", "pad1",0.0,0.0,0.85,1.0,22)
    pad1.SetGridy()
    pad1.SetFillColor(0)
    pad1.Draw()

    pad2 = ROOT.TPad("pad2", "pad2",0.8,0.0,1.0,1.0,22)
    pad2.SetFillColor(0)
    pad2.SetFillStyle(0)
    pad2.Draw()

    pad2.cd()
    pad2.SetLeftMargin(0)
    pad2.SetRightMargin(0.000001)
    leg = make_leg(n, labels, 0., 0.2,0.99,0.92)
    ROOT.gStyle.SetLegendTextSize(0.09)
    leg.Draw()

    pad1.cd()
    hone.GetXaxis().SetLabelSize(0.06)
    hone.GetXaxis().SetLabelOffset(0.01)
    hone.Draw()    
    hone.GetYaxis().SetTitle("Composition [%]")
    hone.GetYaxis().SetLabelSize(0.045)
    hone.GetYaxis().SetTitleSize(0.055)
    hone.GetYaxis().SetTitleOffset(0.8)
    stack_fraction.Draw("histo same")
    honezero.Draw("same")
    pad1.SetGridx()
    #hone.GetXaxis().SetAxisColor(6)
    pad1.RedrawAxis()
    pad1.SetGridy()
    pad1.SetTicky()
    pad1.SetTopMargin(0.09)
    pad1.SetBottomMargin(0.16)
    text =  ROOT.TLatex()
    text.SetNDC()
    text.SetTextAlign( 11 )
    text.SetTextFont( 42 )
    text.SetTextSize( 0.05 )
    text.SetTextColor( 1 )
    y = 0.93
    for t in write:
        text.DrawLatex(0.15,y, t)
        y = y-0.046


        #stack_fraction.GetXaxis().SetLabelSize(stack_fraction.GetXaxis().GetLabelSize()*300)
        #stack_fraction.GetXaxis().SetLabelOffset(0.02)
        #stack_fraction.GetYaxis().SetLabelSize(stack_fraction.GetYaxis().GetLabelSize()*1.6)
        #stack_fraction.GetYaxis().SetLabelOffset(0.0001)
        #stack_fraction.GetYaxis().SetTitleSize(stack_fraction.GetYaxis().GetTitleSize()*3)
        #stack_fraction.GetYaxis().SetTitleOffset(0.25)
        #stack_fraction.GetXaxis().SetTitleSize(stack_fraction.GetXaxis().GetTitleSize()*3)
        #stack_fraction.GetXaxis().SetTitleOffset(1.05)
    pad1.RedrawAxis("g")
    pad1.Update()
    pad1.Draw()

    c.SaveAs(outfolder+"/"+name_can+".pdf")



    #h20 = r.TH1F("h20","h20", len(x_sel), 0, len(x_sel))
        

def var_corr(variables, labels, samples, name_infile, name_can = "correlation.pdf"):

    infile = dict()
    print name_infile
    for s in samples:
        infile[s] = ROOT.TFile.Open(name_infile[s],"READ")

    h_ov = ROOT.TH2F("h_correlation","h_correlation", len(variables), 0, 1, len(variables), 0, 1)  

    ix =0
    for key in sorted(variables):
        iy =0
        ix+=1
        h_ov.GetXaxis().SetBinLabel(ix, labels[ix-1])
        for key2 in sorted(variables):
            totbkg=0
            nttbar=0
            totbkg2=0
            nttbar2=0
            iy+=1
            if ix ==1:
                h_ov.GetYaxis().SetBinLabel(iy, labels[iy-1])

            wei="(weight_mc*weight_lumi*weight_WZ_2_2)*(signal_leptons_n==0 && met>180 && dphi_min>0.4 && bjets_n_85>=2)"
            print ix, iy
            hname="hcorr_"+key+"_"+key2
            hname=hname.replace("/","_over_").replace("(","").replace(")","")
            print hname
            for b in samples:
                b = b+"_nominal"
                t = infile[b.replace("_nominal","")].Get(b)
                if (not t):
                    print b,"not found"
                    continue
                print b
                # here I need to fill the histograms and compute the correlation
                t.Draw(key+":"+key2+">>+"+hname, wei, "goff")
            h2 = ROOT.gDirectory.Get(hname)
            print h2.Integral()
            corr = h2.GetCorrelationFactor()
            print "corelation",key,key2,corr
            h_ov.SetBinContent(ix, iy, corr)
    h_ov.GetXaxis().LabelsOption("v")
    h_ov.GetXaxis().SetNdivisions(len(variables))
    h_ov.GetYaxis().SetNdivisions(len(variables))
    #print "divisions ",len(variables)
    c = ROOT.TCanvas("mycan")
    c.SetLeftMargin(0.25)
    c.SetBottomMargin(0.25)
    c.cd()
    h_ov.Draw("COLZ")
    #h_ov.Draw("TEXTE same")
    h_ov.Draw("TEXT same")
    c.SaveAs(name_can)
    return True


def sig_bkg_all (var, mypickle_sel, backgrounds,name_infile, labels, title_x_axis, lumi, region="_", logY=False, write=[], do_scale=False, outfolder="./", name_can="", masses=[], labels_sig=[], signal_sel="1"):
    with open(mypickle_sel, 'rb') as handle:
        x = pickle.load(handle)
    for key in x.keys():
        if skip_sel(key, region): continue
        selection = x[key]
        print key
        sel=selection
        name_can = name_can+"_"+key
        write_key = write
        write_key.append(key.replace("_","-"))
        sig_bkg (var, sel, backgrounds,name_infile, labels, title_x_axis, lumi, logY, write_key, do_scale, outfolder, name_can, masses, labels_sig,signal_sel)

def sig_bkg (var, sel, backgrounds,name_infile, labels, title_x_axis, lumi, logY=False, write=[], do_scale=False, outfolder="./plots/", name_can="", signals=[], lables_sig=[],signal_sel="1", signal_scale=1.0):

    infile = dict()
    for b in backgrounds:
        infile[b] = ROOT.TFile.Open(name_infile[b],"READ")
    for m in signals:
        infile[m] = ROOT.TFile.Open(name_infile[m],"READ")
    name_can=name_can.replace("/","_over_")
    h_signals = []
    for m in signals:
        t_signal = infile[m].Get(m+"_nominal")
        name_h_sig = name_can+"_signal_"+m
        hsignal = ROOT.TH1D(name_h_sig, name_can+"_signal_"+m, var[1], var[2], var[3])
        hsignal.GetXaxis().SetTitle(title_x_axis)
        hsignal.Sumw2()
        string_draw=var[0]+">>"+name_can+"_signal_"+m
        #print string_draw
        sel_signal="("+sel+")*("+signal_sel+")"
        t_signal.Draw(string_draw,sel_signal,"goff")
        hsignal.Scale(lumi)
        # chiara: scale to hh 
        if "ZZ4b" in m:
            hsignal.Scale(4.)
        elif "Zh4b" in m:
            hsignal.Scale(2.)
        h_signals.append(hsignal)

    n=[]
    n_allbkg=[]
    colors=[]
    
    for b in backgrounds:
        """
        if do_scale:
        with open(mypickle_fit, 'rb') as handle2:
        fit_res = pickle.load(handle2)
        prefit = fit_res["MC_exp_events_"+b][0]
        postfit = fit_res["Fitted_events_"+b][0]
        SF=postfit/prefit
        """
        n_thisbkg=[]
        color=getSampleColor(b)
        colors.append(color)
        b=b+"_nominal"
        t = infile[b.replace("_nominal","")].Get(b)
        if (not t):
            print b,"not found"
            continue
        htmp=ROOT.TH1D(name_can+"_"+b, name_can+"_"+b, var[1], var[2], var[3])
        htmp.GetXaxis().SetTitle(name_can)
        htmp.Sumw2()
        string_draw=var[0]+">>"+name_can+"_"+b
        t.Draw(string_draw,sel,"goff")
        htmp.Scale(lumi)
        """
        if do_scale:
        htmp.Scale(1./htmp.Integral())
        """
        print b,htmp.Integral()
        n_thisbkg.append(htmp.Clone())
        htmp.Clear()
        
        n_allbkg.append(n_thisbkg)

    for n_allbkg_i in n_allbkg:
        n.append(n_allbkg_i[0])

    histo_max=0
    histo_min=9999999999
    i=0
    stack = ROOT.THStack("stack","stack")
    for h in n:
        h.SetLineColor(colors[i])
        h.SetFillColor(colors[i])
        h.SetLineColor(1)
        h.GetXaxis().SetTitle(name_can)
        if h.GetMaximum() > histo_max:
            histo_max=h.GetMaximum()
        if h.GetMinimum() < histo_min:
            histo_min=h.GetMinimum()        
        stack.Add(h)
        if i==0:
            htot=h.Clone("htot")
        else:
            htot.Add(h)
        i+=1

    c = ROOT.TCanvas("can"+name_can,"can"+name_can,600,600)
    pad1 = ROOT.TPad("pad1", "pad1",0.0,0.35,1.0,1.0,21)
    pad2 = ROOT.TPad("pad2", "pad2",0.0,0.0,1.0,0.35,22)
    pad1.SetFillColor(0)
    pad1.Draw()    
    pad2.SetFillColor(0)
    pad2.Draw()

    pad1.cd()
    if logY:
        histo_max *= 300
        pad1.SetLogy()

    max_h_signal =0
    min_h_signal = 9999999999
    max_lowest_signal = 99999
    for hsignal in h_signals:
        if hsignal.GetMaximum() > max_h_signal:
            max_h_signal = hsignal.GetMaximum()
        if hsignal.GetMinimum() < min_h_signal:
            min_h_signal = hsignal.GetMinimum()
        if hsignal.GetMaximum() <  max_lowest_signal:
            max_lowest_signal = hsignal.GetMaximum()

    histo_max=max(histo_max,max_h_signal)            
    histo_min=min(histo_min,min_h_signal)            

    h_signals[0].GetYaxis().SetTitle("Events")
            #h_signals[0].SetMarkerStyle(20)
    h_signals[0].SetMaximum(1.4*histo_max)
    if histo_min>0.1:
        h_signals[0].SetMinimum(min(histo_min,max_lowest_signal/10.))
    else:
        h_signals[0].SetMinimum(min(0.1,max_lowest_signal/10.))
            #h_signals[0].GetXaxis().SetLabelSize(h_signals[0].GetXaxis().GetLabelSize()*0.01)
    h_signals[0].GetYaxis().SetLabelSize(h_signals[0].GetYaxis().GetLabelSize()*1.4)
    h_signals[0].GetYaxis().SetTitleSize(h_signals[0].GetYaxis().GetTitleSize()*1.3)
            #h_signals[0].GetXaxis().SetLabelOffset(1)
    pad1.SetTickx()
    pad1.SetTicky()
    h_signals[0].Draw("hist")
    stack.Draw("hist same")
    h_white=dict()
    for hsignal in h_signals:
        hsignal.SetLineWidth(3)
        h_white[hsignal.GetName()] = hsignal.Clone("appo_white_"+hsignal.GetName())
        h_white[hsignal.GetName()].SetLineColor(ROOT.kWhite)
        hsignal.SetLineColor(getSampleColor(hsignal.GetName()))
        #print "name histo"
        #print hsignal.GetName()
        #print "color"
        #print getSampleColor(hsignal.GetName()),"\n"
        hsignal.SetLineStyle(4)
        #print hsignal.GetName(),"color",getSampleColor(hsignal.GetName())
        h_white[hsignal.GetName()].Draw("hist same")
        hsignal.Draw("hist same")
        n.append(hsignal)
        pad1.RedrawAxis() # pad1
    for m in signals:
        labels.append(m)
    leg = make_leg(n, labels)
    leg.Draw()
    text =  ROOT.TLatex()
    text.SetNDC()
    text.SetTextAlign( 11 )
    text.SetTextFont( 42 )
    text.SetTextSize( 0.036 )
    text.SetTextColor( 1 )
    y = 0.82
    for t in write:
        text.DrawLatex(0.15,y, t)
        y = y-0.046
    pad1.Update()
    
    
    pad2.cd()

    pad2.SetTickx()
    pad2.SetTicky()

    max_ratio=0
    h_ratio=dict()
    for hsignal in h_signals:
        #hsignal.SetLineColor(getSampleColor(hsignal.GetName()))
        hsignal.SetLineWidth(3)        
        h_ratio[hsignal.GetName()] = hsignal.Clone(hsignal.GetName()+"_ratio")
        h_ratio[hsignal.GetName()].SetLineStyle(1)
        h_ratio[hsignal.GetName()].Divide(htot)
        #h_ratio[hsignal.GetName()].SetLineColor(getSampleColor(hsignal.GetName()))
        h_ratio[hsignal.GetName()].SetLineWidth(3)
        for i in range( h_ratio[hsignal.GetName()].GetNbinsX() +1):
            if h_ratio[hsignal.GetName()].GetBinContent(i) > max_ratio:
                max_ratio = h_ratio[hsignal.GetName()].GetBinContent(i)

    max_ratio_plot = 1
    if max_ratio < 0.025:
        max_ratio_plot = 0.025
    elif max_ratio < 0.05:
        max_ratio_plot = 0.05
    elif max_ratio < 0.1:
        max_ratio_plot = 0.1
    elif max_ratio < 0.2:
        max_ratio_plot = 0.2
    elif max_ratio < 0.5:
        max_ratio_plot = 0.5

    print "max_ratio_plot", max_ratio_plot

    #if "4b" in name_can:
    #    max_ratio_plot = 1
    #elif "3b" in name_can:
    #    max_ratio_plot = 0.2
    #elif "2b" in name_can:
    #    max_ratio_plot = 0.05

    print max_ratio, max_ratio_plot
    i=0    
    for h_r_key in sorted(h_ratio):
        h_r = h_ratio[h_r_key]
        h_r.SetMinimum(0.0000001)
        #h_r.SetMaximum(max_ratio_plot)
        h_r.SetMaximum(0.04)
        if i==0:
            h_r.GetXaxis().SetTitle("")
            h_r.GetYaxis().SetTitle("S/B")
            h_r.GetYaxis().SetTitleSize(0.1)
            h_r.GetYaxis().SetTitleOffset(0.45)
            h_r.GetYaxis().SetLabelSize(0.07)
            h_r.Draw("hist")
        else:
            h_r.Draw("hist same")
        #pad2.RedrawAxis() # pad1    
        i+=1

    pad2.SetTopMargin(0.01)
    pad2.SetBottomMargin(0.3)
    
    if do_scale:
        name_pdf=name_can+"_scale.pdf"
    else:
        name_pdf=name_can+".pdf"
    c.SaveAs(outfolder+"hh_"+name_pdf)
    c.Clear()
    stack.Clear()

def plot_all_var (var, mypickle_sel, backgrounds, name_infile, labels,title_x_axis, slices, outfolder="./", name_can="", lumi=1, region="_", do_scale=False, doLogY=False):
    print "ciao"
    with open(mypickle_sel, 'rb') as handle:
        x = pickle.load(handle)
        infile = ROOT.TFile.Open(name_infile,"READ")
        for key in x.keys():
            print key, region
            if skip_sel(key, region): continue
            selection = x[key]
            print key
            sel=selection
            name_can=name_can+"_"+key
            plot_var (var, sel, backgrounds, name_infile, labels, slices, outfolder, name_can, lumi, do_scale, doLogY)

# only one panel, plot shapes
def plot_var (var, sel, backgrounds, name_infile, labels,title_x_axis, slices, outfolder="./", name_can="", lumi=1, do_scale=False, doLogY=False, write=[]):
    #print "ciao"
    infile = dict()
    for b in backgrounds:
        infile[b] = ROOT.TFile.Open(name_infile[b],"READ") 
    n=[]
    n_allbkg=[]
    for b in backgrounds:
        n_thisbkg=[]
        #b=b+"_nominal"
        t = infile[b].Get(b+"_nominal")
        if (not t):
            t = infile[b].Get(b)
            if (not t):
                print b,"not found"
                continue
        i=0
        for s in slices:
            htmp_name = name_can+"_"+str(i)+"_"+b
            htmp=ROOT.TH1D(htmp_name, htmp_name, var[1], var[2], var[3])
            htmp.GetXaxis().SetTitle(title_x_axis)
            htmp.Sumw2()
            sel_slice=sel+"*("+s+")"
            string_draw=var[0]+">>"+name_can+"_"+str(i)+"_"+b
            #print string_draw
            t.Draw(string_draw,sel_slice,"goff")
            htmp.Scale(lumi)
            if do_scale and htmp.Integral():
                htmp.Scale(1./htmp.Integral())
            #print b,htmp.Integral()
            n_thisbkg.append(htmp.Clone())
            htmp.Clear()
        n_allbkg.append(n_thisbkg)

    if len(slices)>1: # look at the composizion of one background
        isel=0
        for s in slices: # loop sulle slice
            n_sel=ROOT.TH1D(name_can, name_can, var[1], var[2], var[3])
            for n_allbkg_i in n_allbkg:
                n_sel.Add(n_allbkg_i[isel])
                isel+=1
            n.append(n_sel)
    else: # look at bkg composition
        for n_allbkg_i in n_allbkg:
            n.append(n_allbkg_i[0])

    #colors = [3,6,2,4,5,7,8,9,46,38,30,40]
    colors = [609, 856, 410, 801, 629, 879, 602, 921, 622]
    histo_max=0
    i=0

    for h in n:
        #h.SetLineColor(getSampleColor(backgrounds[i]))
        h.SetLineWidth(3)
        #h.SetLineStyle(4)
        h.SetLineColor(colors[i])
        h.GetXaxis().SetTitle(title_x_axis)
        if h.GetMaximum() > histo_max:
            histo_max=h.GetMaximum()
        i+=1

    c = ROOT.TCanvas("can"+name_can,"can"+name_can,600,500)
    if doLogY:
        c.SetLogy()
    i=0
    for h in n:
        h.SetLineWidth(3)
        h.SetMaximum(1.4*histo_max)
        #h_appo_white = h.Clone("h_appo_white"+h.GetName())
        #h_appo_white.SetLineColor(ROOT.kWhite)
        #h_appo_white.SetLineStyle(1)
        if i==0:
            #h_appo_white.Draw("histo")
            h.Draw("histo same")
        else:
            #h_appo_white.Draw("histo same")
            h.Draw("histo same")
        i+=1

    leg=make_leg(n, labels)
    leg.Draw()

    text =  ROOT.TLatex()
    text.SetNDC()
    text.SetTextAlign( 11 )
    text.SetTextFont( 42 )
    text.SetTextSize( 0.05 )
    text.SetTextColor( 1 )
    y = 0.82
    for t in write:
        text.DrawLatex(0.15,y, t)
        y = y-0.06
    #text.DrawLatex(0.15,y, key.replace("_","-"))
    c.Update()


    if do_scale:
        name_pdf=name_can+"_scale.pdf"
    else:
        name_pdf=name_can+".pdf"
    c.SaveAs(outfolder+name_pdf)
    c.Clear()


def plot_pie (myjson_sel, weights, backgrounds, name_infile, labels, slices, outfolder="./", name_can="pie", region="_", do_scale=False, mypickle_fit="", print_err=True, print_raw=True):
    with open(myjson_sel, 'rb') as handle:
        x =json.load(handle)
        #x = pickle.load(handle)
        infile = dict()
        #for name_f in name_infile:
        for b in backgrounds:
            infile[b] = ROOT.TFile.Open(name_infile[b],"READ")
        #weights=x["weights"]
        #myweights = "("
        #for mywei in weights:
        #    myweights += mywei
        #    myweights += "*"
        #myweights = myweights[0:-1]
        #myweights+=')'
        #sel = "("+selection+")*"+myweights
        for key in x.keys():
            #if skip_sel(key, region): continue
            if not region in key: continue
            selection = x[key]
            print key
            #sel = "("+selection+")*"+myweights
            sel=selection
            # chiara: remove!!
            #sel=sel.replace("*weight_WZ_2_2","")
            #sel=sel.replace("&& (razor_PP_mDeltaR>-1)","")
            #sel=sel.replace("","")
            n=[]
            n_err=[]
            n_raw=[]
            n_allbkg=[]
            n_allbkg_err=[]
            n_allbkg_raw=[]
            for b in backgrounds:
                if do_scale:
                     with open(mypickle_fit, 'rb') as handle2:
                         fit_res = pickle.load(handle2)
                         prefit = fit_res["MC_exp_events_"+b][0]
                         postfit = fit_res["Fitted_events_"+b][0]
                         SF=postfit/prefit
                n_thisbkg=[]
                n_thisbkg_err=[]
                n_thisbkg_raw=[]

                #b=b+"_nominal"
                #for infile_appo in infile:
                t = infile[b].Get(b+"_nominal")
                #    if t:
                #        continue
                if (not t):
                    print b,"not found"
                    continue
                for s in slices:
                    htmp=ROOT.TH1D("htmp","htmp",1,0,2)
                    htmp.Sumw2()
                    sel_slice=sel+"&&("+s+")"
                    sel_slice = "("+weights+")*("+sel_slice+")"
                    t.Draw("1>>htmp",sel_slice,"goff")
                    if do_scale:
                        htmp.Scale(SF)
                    err_tmp = ROOT.Double(0)
                    n_slice = htmp.IntegralAndError(0, htmp.GetNbinsX()+1, err_tmp)
                    #print n_slice, err_tmp
                    n_thisbkg.append(n_slice)
                    n_thisbkg_err.append(err_tmp)
                    n_thisbkg_raw.append(htmp.GetEntries())
                    htmp.Clear()
                n_allbkg.append(n_thisbkg)
                n_allbkg_err.append(n_thisbkg_err)
                n_allbkg_raw.append(n_thisbkg_raw)

            #print n_allbkg_err

            if len(slices)>1: # look at the composizion of one background
                isel=0
                for s in slices: # loop sulle slice
                    #print ""
                    #print s
                    n_sel=0
                    n_sel_err=0
                    n_sel_raw=0
                    j=0
                    for n_allbkg_i in n_allbkg:
                        #print "  ",isel,n_allbkg_i[isel]
                        n_sel+=n_allbkg_i[isel]
                        n_sel_err+=(n_allbkg_err[j][isel]*n_allbkg_err[j][isel])
                        n_sel_raw+=n_allbkg_raw[j][isel]
                        j+=1
                    n_sel_err=math.sqrt(n_sel_err)
                    isel+=1
                    n.append(n_sel)
                    n_err.append(n_sel_err)
                    n_raw.append(n_sel_raw)
                    #print "tot", n_sel
            else: # look at bkg composition
                j=0
                for n_allbkg_i in n_allbkg:
                    n.append(n_allbkg_i[0])
                    n_err.append(n_allbkg_err[j][0])
                    n_raw.append(n_allbkg_raw[j][0])
                    j+=1

            j=0
            tot=0
            err_tot=0
            for val in n:
                tot+= val
                err_tot+=(n_err[j]*n_err[j])
            err_tot = math.sqrt(err_tot)
            
            perc = []
            err_perc = []
            j=0
            for val in n:
                if tot>0:                    
                    perc.append(100.*val/tot)
                else:
                    perc.append(0)
                if val>0:
                    #print "rel err A:", n_err[j]/val
                    #print "rel err B:",err_tot/tot
                    #print "rel err A/B:", math.sqrt( (n_err[j]/val)*(n_err[j]/val) + (err_tot/tot)*(err_tot/tot) )
                    #print "err tot:",(100.*val/tot)*math.sqrt( (n_err[j]/val)*(n_err[j]/val) + (err_tot/tot)*(err_tot/tot) )
                    #print "tot:",(100.*val/tot)
                    #print ""
                    err_appo = (100.*val/tot)*math.sqrt( (n_err[j]/val)*(n_err[j]/val) + (err_tot/tot)*(err_tot/tot) )
                else:
                    err_appo=0
                if tot>0:
                    err_perc.append(min(100.*val/tot,err_appo))
                else:
                    err_perc.append(100)
                j+=1
            #print "perc"
            #print perc
            #print err_perc
                
            colors = [3,6,2,4,5,7,8,9,46,38,30,40]
            pie=ROOT.TPie(key,         key,       len(n), array('f', n), array('i',colors))
            #print n
            pie.SetRadius(.2)
            pie.SetLabelsOffset(.01)
            pie.SetLabelFormat("%txt");
            print pie
            print "entries",pie.GetEntries()
            en=0
            tot_cont=0            
            for l in labels:
                if print_err:
                    l_err = str(round(perc[en],1))+" #pm "+str(round(err_perc[en],1))+" %"
                else:
                    l_err = str(round(perc[en],1))+" %"
                l = "#splitline{"+l+"}"+"{"+l_err+"}"
                if print_raw:
                    l_raw="raw:"+str(n_raw[en])
                    l = "#splitline{"+l+"}"+"{"+l_raw+"}"
                pie.SetEntryLabel(en,l)
                print " label",pie.GetEntryLabel(en)
                print " content",pie.GetEntryVal(en)
                tot_cont+=pie.GetEntryVal(en)
                en+=1
            if not tot_cont>0:
                continue
            c = ROOT.TCanvas("can"+key,"can"+key,200,230)
            pie.Draw("rs")
            if do_scale:
                name_pdf=name_can+"_"+key+"_postfit.pdf"
            else:
                name_pdf=name_can+"_"+key+".pdf"
            c.SaveAs(outfolder+name_pdf)
            pie.Clear()
            c.Clear()


def signal_eff(masses, name_infile, num_sel, den_sel, weights, legend, outfolder="./", name_can="eff"):
    infile = dict()
    for m in masses:
        infile[m] = ROOT.TFile.Open(name_infile[m],"READ")  
    h = ROOT.TH1F("h","h",len(masses),0,len(masses))
    h.GetXaxis().SetTitle("m(#tilde{#chi})   [GeV]")
    h.GetYaxis().SetTitle("Efficiency")
    #h.GetXaxis().SetTitleSize(0.5)    
    for i in range(len(masses)):
        h.GetXaxis().SetBinLabel(i+1, masses[i])
    #h.SetMaximum(1)
    wei = "*".join(weights)
    sel_common = "("+den_sel+")*("+wei+")"
    hs = list()
    for i in range(len(num_sel)):
        hs.append(ROOT.TH1F("h_eff_"+str(i),"h",len(masses),0,len(masses)))
    im=0
    for m in masses:
        im+=1
        #t = infile[m].Get("GGM_hh_"+m+"_nominal")
        t = infile[m].Get("GGM_hh_"+m+"_NoSys")
        h_den = ROOT.TH1F("h_den_"+m,"h_den_"+m, 1, 0, 2)
        t.Draw("1 >> "+"h_den_"+m, sel_common, "goff")
        denominator = h_den.Integral()
        isel=0
        for sel in num_sel:
            sel = "("+sel+" && "+den_sel+")*("+wei+")"
            h_num = ROOT.TH1F("h_"+str(isel)+m,"h_"+sel+m, 1, 0, 2)
            t.Draw("1 >> "+"h_"+str(isel)+m, sel, "goff")
            numerator = h_num.Integral()
            if denominator >0:
                hs[isel].SetBinContent(im, numerator/denominator)
            else:
                hs[isel].SetBinContent(im, 0)
            isel+=1

    leg=ROOT.TLegend(0.13,0.68,0.31,0.89)            
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    ih =0
    for myh in hs:
        leg.AddEntry(myh, legend[ih], "l")
        ih+=1
    c = ROOT.TCanvas(name_can)
    c.SetTicky()
    c.cd()
    h.Draw()
    leg.Draw()
    colors = [609, 856, 410, 801, 629, 879, 602, 921, 622]
    ih=0
    for myh in hs:        
        myh.SetLineColor(colors[ih])
        myh.SetLineWidth(3)
        myh.Draw("histo same")
        ih+=1
    c.Print(outfolder+name_can)
    
    return



def tt_dt (var, sel, background, name_infile, title_x_axis, ntags, isIncl, lumi, logY=False, write=[], outfolder="./", name_can="", do_scale=False, b_dep_var=""):
    print "ciao"
    infile = ROOT.TFile.Open(name_infile,"READ")
    
    myweights="(weight_mc*weight_lumi*weight_jvt*weight_btag)"

    selection=sel
    h_tt=ROOT.TH1D(name_can+"_"+"_tt", name_can+"_"+"_tt", var[1], var[2], var[3])
    h_dt=ROOT.TH1D(name_can+"_"+"_dt", name_can+"_"+"_dt", var[1], var[2], var[3])

    h_dt.GetXaxis().SetTitle(title_x_axis)
    h_dt.Sumw2()
    h_tt.Sumw2()
    symbol="=="
    tt_wei="truthTagWei_ex_Nominal"
    if isIncl:
        symbol = ">="
        tt_wei = "truthTagWei_in_Nominal"
        if b_dep_var != "":
            b_dep_var+="_in"
    else:
        if b_dep_var != "":
            b_dep_var+="_ex"

    sel_dt = "("+selection+" && bjets_n"+symbol+str(ntags)+")*"+myweights
    sel_tt = "("+selection+")*"+myweights+"*("+tt_wei+"["+str(ntags)+"])"
    sel_tt = sel_tt.replace("*weight_btag","")


    print "sel_dt"
    print sel_dt
    print "sel_tt"
    print sel_tt
        
    string_draw_dt=var[0]+">>"+name_can+"_"+"_dt"
    if b_dep_var == "":        
        string_draw_tt=var[0]+">>"+name_can+"_"+"_tt"
    else:
        string_draw_tt=b_dep_var+"["+str(ntags)+"]"+">>"+name_can+"_"+"_tt"

    t = infile.Get(background+"_nominal")
    t.Draw(string_draw_dt,sel_dt,"goff")            
    t.Draw(string_draw_tt,sel_tt,"goff")            
    h_dt.SetLineColor(4)
    h_tt.SetLineColor(6)
    h_dt.SetMarkerColor(4)
    h_tt.SetMarkerColor(6)
    h_dt.Scale(lumi)
    h_tt.Scale(lumi)

    print "h_dt.Integral()",h_dt.Integral()
    print "h_tt.Integral()",h_tt.Integral()
    print "h_dt.GetEntries()",h_dt.GetEntries()
    print "h_tt.GetEntries()",h_tt.GetEntries()

    if do_scale:
        h_tt.Scale(h_dt.Integral()/h_tt.Integral())

    err_tt = ROOT.Double(0)
    int_tt = h_tt.IntegralAndError(0, h_tt.GetNbinsX()+1, err_tt)

    err_dt = ROOT.Double(0)
    int_dt = h_dt.IntegralAndError(0, h_dt.GetNbinsX()+1, err_dt)
    
    print "int_tt",int_tt
    print "int_dt",int_dt

    c = ROOT.TCanvas("can","can",600,600)
    
    pad1 = ROOT.TPad("pad1", "pad1",0.0,0.35,1.0,1.0,21)
    pad2 = ROOT.TPad("pad2", "pad2",0.0,0.0,1.0,0.35,22)
    pad1.SetFillColor(0)
    pad1.Draw()
    pad2.SetFillColor(0)
    pad2.Draw()

    histo_max=max(h_dt.GetMaximum(), h_tt.GetMaximum())
    pad1.cd()
    if logY:
        histo_max *= 100
        pad1.SetLogy()
    h_dt.GetYaxis().SetTitle("Yields")
        #hdata.SetMarkerStyle(20)
    h_dt.SetMaximum(1.4 * histo_max)
    #h_dt.GetXaxis().SetLabelSize(h_dt.GetXaxis().GetLabelSize()*0.01)
    #h_dt.GetYaxis().SetLabelSize(h_dt.GetYaxis().GetLabelSize()*1.4)
    #h_dt.GetYaxis().SetTitleSize(h_dt.GetYaxis().GetTitleSize()*1.3)
    #h_dt.GetXaxis().SetLabelOffset(1)
    pad1.SetBottomMargin(0.12)
    pad1.SetTickx()
    pad1.SetTicky()
    h_dt.Draw("")
    h_tt.Draw("same")
    pad1.RedrawAxis()

    leg=ROOT.TLegend(0.6,0.55,0.88,0.87)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.AddEntry(h_tt, "TT: "+str(round(int_tt,2))+" #pm "+str(round(err_tt,2)), "l")
    leg.AddEntry(h_dt, "DT: "+str(round(int_dt,2))+" #pm "+str(round(err_dt,2)), "l")
    leg.Draw()

    text =  ROOT.TLatex()
    text.SetNDC()
    text.SetTextAlign( 11 )
    text.SetTextFont( 42 )
    text.SetTextSize( 0.048 )
    text.SetTextColor( 1 )
    y = 0.82
            #write.append(region.replace("_","-"))
    for t in write:
        text.DrawLatex(0.15,y, t)
        y = y-0.055
        #text.DrawLatex(0.15,y, key.replace("_","-"))
    pad1.Update()

    pad2.cd()
    pad2.SetTickx()
    pad2.SetTicky()
    hratio = h_tt.Clone("h_ratio")
    hratio.Divide(h_dt)
    hratio.SetLineColor(1)
    hratio.SetMinimum(0)
    hratio.SetMaximum(2)
    hratio.Draw()
    
    hline=ROOT.TH1D("hline", "hline", 1, var[2], var[3])
    hline.SetLineColor(ROOT.kRed)
    hline.SetBinContent(1,1)
    hline.Draw("same")

    hratio.GetYaxis().SetTitle("TT/DT")
    pad2.SetTopMargin(0.01)
    pad2.SetBottomMargin(0.3)
    hratio.GetXaxis().SetLabelSize(hratio.GetXaxis().GetLabelSize()*300)
    hratio.GetXaxis().SetLabelOffset(0.02)
    hratio.GetYaxis().SetLabelSize(hratio.GetYaxis().GetLabelSize()*1.6)
    hratio.GetYaxis().SetLabelOffset(0.01)
    hratio.GetYaxis().SetTitleSize(hratio.GetYaxis().GetTitleSize()*2)
    hratio.GetYaxis().SetTitleOffset(0.5)
    hratio.GetXaxis().SetTitleSize(hratio.GetXaxis().GetTitleSize()*3)
    hratio.GetXaxis().SetTitleOffset(1.05)

    if do_scale:
        name_pdf=name_can+"_scale"
    else:
        name_pdf=name_can
    c.SaveAs(outfolder+name_pdf+".pdf")
    c.SaveAs(outfolder+name_pdf+".png")
    print outfolder+name_pdf
    c.Clear()




def turn_on (var, num_sel, den_sel, weights, backgrounds, name_infile, labels, title_x_axis, outfolder="./", name_can="", doLogY=False, write=[]):
    #print "ciao"
    infile = dict()
    for b in backgrounds:
        infile[b] = ROOT.TFile.Open(name_infile[b],"READ") 
    n=[]
    for b in backgrounds:
        n_thisbkg=[]
        #b=b+"_nominal"
        t = infile[b].Get(b+"_nominal")
        if (not t):
            t = infile[b].Get(b)
            if (not t):
                print b,"not found"
                continue
        i=0

        htmp_num_name = name_can+"_"+str(i)+"_"+b
        htmp_den_name = name_can+"_"+str(i)+"_"+b+"_den"
        htmp_num=ROOT.TH1D(htmp_num_name, htmp_num_name, var[1], var[2], var[3])
        htmp_den=ROOT.TH1D(htmp_den_name, htmp_den_name, var[1], var[2], var[3])

        htmp_num.GetXaxis().SetTitle(title_x_axis)
        htmp_num.Sumw2()

        wei = "*".join(weights)
        sel_num = "("+num_sel+" && "+den_sel+")*("+wei+")"
        sel_den = "("+den_sel+")*("+wei+")"


        string_draw_num=var[0]+">>"+htmp_num_name
        string_draw_den=var[0]+">>"+htmp_den_name
            #print string_draw
        t.Draw(string_draw_num,sel_num,"goff")
        t.Draw(string_draw_den,sel_den,"goff")
        
        htmp_num.Divide(htmp_den)
        
        n.append(htmp_num.Clone())
        htmp_num.Clear()
        htmp_den.Clear()


    #colors = [3,6,2,4,5,7,8,9,46,38,30,40]
    colors = [609, 856, 410, 801, 629, 879, 602, 921, 622]
    histo_max=0
    i=0

    for h in n:
        h.SetLineColor(getSampleColor(backgrounds[i]))
        h.SetLineWidth(3)
        #h.SetLineStyle(4)
        #h.SetLineColor(colors[i])
        h.GetXaxis().SetTitle(title_x_axis)
        if h.GetMaximum() > histo_max:
            histo_max=h.GetMaximum()
        i+=1

    c = ROOT.TCanvas("can"+name_can,"can"+name_can,600,500)
    if doLogY:
        c.SetLogy()
    i=0
    for h in n:
        h.SetLineWidth(3)
        h.SetMaximum(1.2*histo_max)
        h.SetMinimum(0.7)
        #h_appo_white = h.Clone("h_appo_white"+h.GetName())
        #h_appo_white.SetLineColor(ROOT.kWhite)
        #h_appo_white.SetLineStyle(1)
        if i==0:
            #h_appo_white.Draw("histo")
            h.Draw("histo")
        else:
            #h_appo_white.Draw("histo same")
            h.Draw("histo same")
        i+=1

    leg=make_leg(n, labels)
    leg.Draw()

    text =  ROOT.TLatex()
    text.SetNDC()
    text.SetTextAlign( 11 )
    text.SetTextFont( 42 )
    text.SetTextSize( 0.04 )
    text.SetTextColor( 1 )
    y = 0.82
    for t in write:
        text.DrawLatex(0.15,y, t)
        y = y-0.05
    #text.DrawLatex(0.15,y, key.replace("_","-"))
    c.Update()


    name_pdf=name_can.replace(".pdf","")+".pdf"
    c.SaveAs(outfolder+name_pdf)
    c.Clear()



def turn_on_data (var, num_sel, den_sel, weights, backgrounds, name_infile, labels, title_x_axis, outfolder="./", name_can="", doLogY=False, write=[]):
    #print "ciao"
    infile = dict()
    for b in backgrounds:
        infile[b] = ROOT.TFile.Open(name_infile[b],"READ") 
    infile["data"] = ROOT.TFile.Open(name_infile["data"],"READ")
    n=[]
    for b in ["data"]+backgrounds:
        print b
        n_thisbkg=[]
        #b=b+"_nominal"
        t = infile[b].Get(b+"_nominal")
        if (not t):
            t = infile[b].Get(b)
            if (not t):
                print b,"not found"
                continue
        i=0

        htmp_num_name = name_can+"_"+str(i)+"_"+b
        htmp_den_name = name_can+"_"+str(i)+"_"+b+"_den"
        htmp_num=ROOT.TH1D(htmp_num_name, htmp_num_name, var[1], var[2], var[3])
        htmp_den=ROOT.TH1D(htmp_den_name, htmp_den_name, var[1], var[2], var[3])

        htmp_num.GetXaxis().SetTitle(title_x_axis)
        htmp_num.Sumw2()

        wei = "*".join(weights)
        if "data" in b:
            wei = "1"
        sel_num = "("+num_sel+" && "+den_sel+")*("+wei+")"
        sel_den = "("+den_sel+")*("+wei+")"

        print "sel_num"
        print sel_num
        print "sel_den"
        print sel_den

        string_draw_num=var[0]+">>"+htmp_num_name
        string_draw_den=var[0]+">>"+htmp_den_name
            #print string_draw
        t.Draw(string_draw_num,sel_num,"goff")
        t.Draw(string_draw_den,sel_den,"goff")
        
        print "Integral Num"
        print htmp_num.Integral()
        print "Integral Den"
        print htmp_den.Integral()
        print ""

        htmp_num.Divide(htmp_den)
        if not "data" in b:
            n.append(htmp_num.Clone())
        else:
            h_data = htmp_num.Clone()            
        htmp_num.Clear()
        htmp_den.Clear()


    #colors = [3,6,2,4,5,7,8,9,46,38,30,40]
    colors = [609, 856, 410, 801, 629, 879, 602, 921, 622]
    histo_max=0
    i=0

    for h in n:
        h.SetLineColor(getSampleColor(backgrounds[i]))
        h.SetLineWidth(3)
        #h.SetLineStyle(4)
        #h.SetLineColor(colors[i])
        h.GetXaxis().SetTitle(title_x_axis)
        if h.GetMaximum() > histo_max:
            histo_max=h.GetMaximum()
        i+=1

    h_data.SetLineColor(1)
    h_data.SetLineWidth(3)
    h_data.GetXaxis().SetTitle(title_x_axis)
    if h_data.GetMaximum() > histo_max:
        histo_max=h_data.GetMaximum()


    c = ROOT.TCanvas("can"+name_can,"can"+name_can,600,600)
    pad1 = ROOT.TPad("pad1", "pad1",0.0,0.35,1.0,1.0,21)
    pad2 = ROOT.TPad("pad2", "pad2",0.0,0.0,1.0,0.35,22)
    pad1.SetFillColor(0)
    pad1.Draw()
    pad2.SetFillColor(0)
    pad2.Draw()

    if doLogY:
        pad1.SetLogy()
    pad1.cd()
    pad1.SetBottomMargin(0.01)
    pad1.SetTickx()
    pad1.SetTicky()

    i=0
    for h in [h_data]+n:
        h.SetLineWidth(3)
        h.SetMaximum(1.2*histo_max)
        h.SetMinimum(0.7)
        if i==0:
            h.Draw("histo")
        else:
            h.Draw("histo same")
        i+=1

    leg=make_leg([h_data]+n, ["data"]+labels)
    leg.Draw()

    text =  ROOT.TLatex()
    text.SetNDC()
    text.SetTextAlign( 11 )
    text.SetTextFont( 42 )
    text.SetTextSize( 0.04 )
    text.SetTextColor( 1 )
    y = 0.82
    for t in write:
        text.DrawLatex(0.15,y, t)
        y = y-0.05
    #text.DrawLatex(0.15,y, key.replace("_","-"))
    pad1.Update()


    pad2.cd()
    pad2.SetTopMargin(0.01)
    pad2.SetBottomMargin(0.3)

    hline=ROOT.TH1D("hline", "hline", 1, var[2], var[3])
    hline.SetLineColor(ROOT.kRed)
    hline.SetBinContent(1,1)
    hline.GetYaxis().SetTitle("Data/MC")
    hline.SetMinimum(0)
    hline.SetMaximum(2)
    hline.GetXaxis().SetLabelSize(hline.GetXaxis().GetLabelSize()*300)
    hline.GetXaxis().SetLabelOffset(0.02)
    hline.GetYaxis().SetLabelSize(hline.GetYaxis().GetLabelSize()*1.6)
    hline.GetYaxis().SetLabelOffset(0.01)
    hline.GetYaxis().SetTitleSize(hline.GetYaxis().GetTitleSize()*3)
    hline.GetYaxis().SetTitleOffset(1.05)
    hline.GetXaxis().SetTitleSize(hline.GetXaxis().GetTitleSize()*3)
    hline.GetXaxis().SetTitleOffset(1.05)

    hline.Draw()


    i=0
    hratio=[]
    for h in n:
        hratio.append(h_data.Clone("h_ratio_"+str(i)))
        hratio[i].Divide(h)
        hratio[i].SetLineColor(getSampleColor(backgrounds[i]))
        hratio[i].SetLineWidth(3)
        hratio[i].Draw("same")
        i+=1    

    name_pdf=name_can.replace(".pdf","")+".pdf"
    c.SaveAs(outfolder+name_pdf)
    c.Clear()




def pu_dependence(var, selections, weights, mc_chan, bkg, name_infile, pu_file, labels, title_x_axis, outfolder="./", name_can="", doLogY=False, write=[]):
    print "ciao chiara"
    
    infile = ROOT.TFile.Open(name_infile,"READ")
    t = infile.Get(bkg+"_nominal")
    if (not t):
        t = infile[b].Get(bkg)
        if (not t):
            print b,"not found"

    file_pu = ROOT.TFile.Open(pu_file,"READ")
    h_orig= file_pu.Get("PileupReweighting/pileup_chan"+mc_chan+"_run284500")
    print h_orig.Integral()
    h_orig.Sumw2()

    h_new=list()
    isel=0
    colors = [609, 856, 410, 801, 629, 879, 602, 921, 622]
    for sel in selections:
        h_new_appo=h_orig.Clone("h_new_"+str(isel))
        h_new_appo.Sumw2()
        wei = "*".join(weights)    
        sel = "("+sel+" && channel_number=="+mc_chan+")*("+wei+")"
        string_draw= var+">>h_new_"+str(isel)
        t.Draw(string_draw, sel, "goff")
        print h_new_appo.Integral()
        h_new_appo.Scale(1./h_new_appo.Integral())
        h_new_appo.SetLineColor(colors[isel])
        h_new.append(h_new_appo)
        isel+=1

    h_orig.Scale(1./h_orig.Integral())
    h_orig.SetLineColor(ROOT.kBlue)
    
    c = ROOT.TCanvas("can"+name_can,"can"+name_can,600,600)
    pad1 = ROOT.TPad("pad1", "pad1",0.0,0.35,1.0,1.0,21)
    pad2 = ROOT.TPad("pad2", "pad2",0.0,0.0,1.0,0.35,22)
    pad1.SetFillColor(0)
    pad1.Draw()
    pad2.SetFillColor(0)
    pad2.Draw()

    pad1.cd()
    h_orig.SetMaximum(1.4*h_orig.GetMaximum())
    h_orig.GetXaxis().SetTitle("<#mu>")
    h_orig.Draw()
    for h in h_new:
        h.Draw("same")

    #leg=ROOT.TLegend(0.65,0.68,0.85,0.89)
    #leg.SetFillStyle(0)
    #leg.SetLineColor(0)
    #leg.AddEntry(h_orig,"original","l")
    #leg.AddEntry(h_new,"after sel","l")
    leg = make_leg(h_new+[h_orig], labels+["original"],0.5)
    leg.Draw()

    text =  ROOT.TLatex()
    text.SetNDC()
    text.SetTextAlign( 11 )
    text.SetTextFont( 42 )
    text.SetTextSize( 0.04 )
    text.SetTextColor( 1 )
    y = 0.82
    for t in write:
        text.DrawLatex(0.15,y, t)
        y = y-0.05
    #text.DrawLatex(0.15,y, key.replace("_","-"))
    pad1.Update()


    pad2.cd()
    pad2.SetTopMargin(0.01)
    pad2.SetBottomMargin(0.3)

    hline=ROOT.TH1D("hline", "hline", 1, 0, 100)
    hline.SetLineColor(ROOT.kBlue)
    hline.SetBinContent(1,1)
    hline.GetYaxis().SetTitle("New/Old")
    hline.SetLineStyle(1)
    hline.SetMinimum(0.6)
    hline.SetMaximum(1.4)
    hline.GetXaxis().SetLabelSize(hline.GetXaxis().GetLabelSize()*300)
    hline.GetXaxis().SetLabelOffset(0.02)
    hline.GetYaxis().SetLabelSize(hline.GetYaxis().GetLabelSize()*1.6)
    hline.GetYaxis().SetLabelOffset(0.01)
    hline.GetYaxis().SetTitleSize(hline.GetYaxis().GetTitleSize()*3)
    hline.GetYaxis().SetTitleOffset(1.05)
    hline.GetXaxis().SetTitleSize(hline.GetXaxis().GetTitleSize()*3)
    hline.GetXaxis().SetTitleOffset(1.05)
    hline.Draw("same")

    h_ratio=list()
    isel=0
    for sel in selections:
        h_ratio_appo=h_new[isel].Clone("h_ratio_"+str(isel))
        h_ratio_appo.Divide(h_orig)
        h_ratio.append(h_ratio_appo)
        isel+=1

    for h_r in h_ratio:
        h_r.Draw("same")


    name_pdf=name_can.replace(".pdf","")+".pdf"
    c.SaveAs(outfolder+name_pdf)
    c.Clear()



################################

# top panel: show shapes or distributions for individual backgrounds or sum of backgrounds
# botton panel: ratio to reference
def compare (var, selection, wei_list, to_compare, name_infile_list, labels, title_x_axis, lumi, logY=False, write=[], outfolder="./plots/", name_can="", do_scale=False, is_first_data=False, do_overflow=True, x1leg=0.7, y1leg=0.6, leg_size=24, do_ratio=True, scale_max=1, text_size=24):

    if not len(wei_list)>0:
        print "check len lists"
        return
    if not len(wei_list)==len(to_compare) or not len(wei_list)==len(name_infile_list) or not len(wei_list)==len(labels):
        print "check len lists"
        return

    colors = [609, 856, 410, 801, 629, 879, 602, 921, 622]
    hists=[]
    for i in range(len(to_compare)):
        sel_slice = "("+selection+")*"+wei_list[i]
        #n=[]
        hists.append(ROOT.TH1D(name_can+"_tot_"+str(i), name_can+"_tot_"+str(i), var[1], var[2], var[3]))
        hists[i].Sumw2()
        #print "hists[",str(i),"]", hists[i]
        infile = dict()
        for b in to_compare[i]:
            infile[b]= ROOT.TFile.Open(name_infile_list[i][b],"READ")
            t = infile[b].Get(b)
            if (not t):
                t = infile[b].Get(b)
                if (not t):
                    t = infile[b].Get(b+"_nominal")
                    if (not t):
                        print b,"not found"
                        continue            
            htmp_name = name_can+"_"+b+"_"+str(i)
            htmp=ROOT.TH1D(htmp_name, htmp_name, var[1], var[2], var[3])
            htmp.Sumw2()
            string_draw=var[0]+">>"+htmp_name
            t.Draw(string_draw,sel_slice,"goff")
            if do_overflow:
                htmp_of = ROOT.TH1D(htmp_name+"_of", htmp_name+"_of", var[1], var[2], var[3])
                htmp_of.Sumw2()
                string_draw_of = str(var[3]) + " - (0.5*("+ str(var[3])+"-"+str(var[2])+")/"+str(var[1]) +") >>"+htmp_name+"_of"
                t.Draw(string_draw_of, sel_slice+"*("+ var[0]+">"+str(var[3])  +")")
                htmp.Add(htmp_of)                    

            #print "i",i
            #print "hists[",str(i),"]", hists[i]
            hists[i].Add(htmp.Clone())
            infile[b].Close()
        print b,"tot",hists[i].Integral()
        if is_first_data:
            if i>0:
                hists[i].Scale(lumi)
        else:
            hists[i].Scale(lumi)
        hists[i].SetLineColor(colors[i])
        hists[i].SetLineWidth(3)
        if i ==0 and is_first_data:
             hists[i].SetLineColor(1)
             hists[i].SetMarkerColor(1)
        #print "hists[i] integral", hists[i].Integral()
        #print "print hists"
        #print hists
        


    if do_ratio:
        c = ROOT.TCanvas("can"+name_can,"can"+name_can,600,600)
        pad1 = ROOT.TPad("pad1", "pad1",0.0,0.37,1.0,1.0,21)
        pad1.SetBottomMargin(0.02)
        pad2 = ROOT.TPad("pad2", "pad2",0.0,0.0,1.0,0.37,22)
        pad2.SetFillColor(0)
        pad2.SetFillStyle(0)
        pad2.SetGridy()
        pad2.SetTickx()
    # new things
        pad2.SetTopMargin(0.02)
        pad2.SetBottomMargin(0.28)
        pad2.Draw()

    else:
        c = ROOT.TCanvas("can"+name_can,"can"+name_can,750,600)
        pad1 = ROOT.TPad("pad1", "pad1",0.0,0.0,1.0,1.0,21)

    pad1.SetFillStyle(0)
    pad1.SetFillColor(0)
    pad1.SetTopMargin(0.08)
    pad1.SetBottomMargin(0.13)
    pad1.SetTickx()
    pad1.SetTicky()

    pad1.Draw()


    if do_scale:
        for h in hists:
            h.Scale(1./h.Integral())

    histo_max=0
    for h in hists:
        if h.GetMaximum()>histo_max:
            histo_max=h.GetMaximum()
    
    pad1.cd()
    if logY:
        if do_scale:
            histo_max = histo_max*30.
        else:
            histo_max = histo_max*900.
        pad1.SetLogy()
    histo_max = histo_max * scale_max
    # HERE

    hists[0].GetYaxis().SetTitleFont(43)
    hists[0].GetYaxis().SetTitle("Events")
    if do_scale:
        hists[0].GetYaxis().SetTitle("Events scaled to unit area")
    hists[0].GetYaxis().SetTitleSize(30)
    hists[0].GetYaxis().SetTitleOffset(1)
    hists[0].GetYaxis().SetLabelFont(43)
    hists[0].GetYaxis().SetLabelSize(15)
    hists[0].GetXaxis().SetTitle(" ") 
    #hists[0].GetXaxis().SetTitle(title_x_axis)
    #hists[0].GetXaxis().SetTitleFont(43)
    #hists[0].GetXaxis().SetTitleOffset(1.3)
    #hists[0].GetXaxis().SetTitleSize(20)
    #hists[0].GetXaxis().SetLabelFont(43)
    #hists[0].GetXaxis().SetLabelSize(15)
    #hists[0].GetXaxis().SetTitleSize(0)
    #hists[0].GetXaxis().SetLabelSize(0)

    hists[0].SetMaximum(1.5 * histo_max)
    print "max",histo_max

    #hists[0].GetYaxis().SetTitleSize(hists[0].GetYaxis().GetTitleSize()*1.3)
    #hists[0].GetXaxis().SetLabelOffset(0.01)
    hists[0].SetMaximum(1.5 * histo_max)
    hists[0].SetMinimum(0.01)
    hists[0].GetXaxis().SetTitle(title_x_axis)
    hists[0].GetXaxis().SetTitleFont(43)
    hists[0].GetXaxis().SetTitleSize(30)
    hists[0].GetXaxis().SetLabelFont(43)
    hists[0].GetXaxis().SetLabelSize(20)
    hists[0].GetYaxis().SetLabelFont(43)
    hists[0].GetYaxis().SetLabelSize(20)
    #hists[0].GetXaxis().SetTitleOffset(2.5)

    if do_scale:
        hists[0].SetMinimum(0.001)
    if is_first_data:
        hists[0].SetMarkerStyle(20)
        hists[0].Draw()
    else:
        hists[0].Draw("hist")
    for i in range(1,len(hists)):
        hists[i].Draw("hist same")
    pad1.RedrawAxis()
    leg = make_leg(hists, labels, x1 = x1leg, y1=y1leg, textSize=leg_size)
    leg.Draw()
    text =  ROOT.TLatex()
    text.SetNDC()
    text.SetTextAlign( 11 )
    text.SetTextFont( 43 )
    text.SetTextSize( text_size )
    text.SetTextColor( 1 )
    y = 0.86
        #write.append(region.replace("_","-"))
    for t in write:
        text.DrawLatex(0.13,y, t)
        y = y-0.06
            #text.DrawLatex(0.15,y, var[0].replace("_","-"))
    pad1.Update()

    if do_ratio:
        pad2.cd()
        hratio =[]
        i=0
        for h in hists:
            hratio.append( hists[i].Clone("h_ratio"))
            hratio[i].Divide(hists[0])
            i+=1

        hline=ROOT.TH1D("hline", "hline", 1, var[2], var[3])
    #hline.SetLineColor(ROOT.kBlack)
        hline.SetLineColor(hists[0].GetLineColor())
        hline.SetLineWidth(3)
        hline.SetBinContent(1,1)
        
        hline.GetYaxis().SetTitleFont(43)
        hline.GetYaxis().SetTitle("Events")
        hline.GetYaxis().SetTitleSize(20)
        hline.GetYaxis().SetTitleOffset(1)
        hline.GetYaxis().SetLabelFont(43)
        hline.GetYaxis().SetLabelSize(15)
        hline.GetYaxis().SetTitle("Ratio to "+labels[0])
        
        hline.GetXaxis().SetTitle(title_x_axis)
        hline.GetXaxis().SetTitleFont(43)
        hline.GetXaxis().SetTitleSize(20)
        hline.GetXaxis().SetLabelFont(43)
        hline.GetXaxis().SetLabelSize(15)
        hline.GetXaxis().SetTitleOffset(1)
        
    #hline.GetXaxis().SetTitleSize(0)
    #hline.GetXaxis().SetLabelSize(0)
        hline.SetMinimum(0)
        hline.SetMaximum(2)
        """
        hline.GetXaxis().SetLabelOffset(0.02)
        hline.GetYaxis().SetLabelSize(hline.GetYaxis().GetLabelSize()*1.6)
        hline.GetYaxis().SetLabelOffset(0.01)
        hline.GetYaxis().SetTitleSize(hline.GetYaxis().GetTitleSize()*3)
        hline.GetYaxis().SetTitleOffset(1.05)
        hline.GetXaxis().SetTitleSize(hline.GetXaxis().GetTitleSize()*3)
        hline.GetXaxis().SetTitleOffset(1.05)
        """
        hline.Draw("hist")

        hratio[0].SetMinimum(0.5)
        hratio[0].SetMaximum(1.5)
        i=0
        for hr in hratio:
            if i>0:
                hr.Draw("hist same")
            i+=1     

    #pad2.SetTopMargin(0.01)
    #pad2.SetBottomMargin(0.3)
    #pad1.RedrawAxis()

    name_can = name_can
    if do_scale:
        name_pdf=name_can+"_scale.pdf"
    else:
        name_pdf=name_can+".pdf"
    c.SaveAs(outfolder+name_pdf)
    print outfolder+name_pdf
    c.Clear()


def mc_stack (var, selection, myweights, backgrounds, name_infile, labels, title_x_axis, lumi, logY=False, write=[], outfolder="./plots/", name_can="", do_scale=False, add_signal = False, signals=[], do_fraction=True, slices=["1"], do_overflow=True):

    ROOT.gStyle.SetTitleFontSize(43)

    is_2D = False
    if len(var)>4:
        is_2D = True
    infile = dict()
    for b in backgrounds:
        infile[b]= ROOT.TFile.Open(name_infile[b],"READ")

    for m in signals:
        infile[m]=ROOT.TFile.Open(name_infile[m],"READ")

    if not is_2D and add_signal:
        for m in signals:
            t_signal = infile[m].Get(m)
            name_h_sig = name_can+"_signal_"+m
            hsignal = ROOT.TH1D(name_h_sig, name_can+"_signal_"+m, var[1], var[2], var[3])
            hsignal.GetXaxis().SetTitle(title_x_axis)
            hsignal.Sumw2()
            string_draw=var[0]+">>"+name_can+"_signal_"+m
        #print string_draw
            sel_signal="("+sel+")*("+signal_sel+")"
            t_signal.Draw(string_draw,sel_signal,"goff")
            if do_overflow:
                hsignal_of = ROOT.TH1D(name_h_sig+"_of", name_h_sig+"_of", var[1], var[2], var[3])
                hsignal_of.Sumw2()
                string_draw_of = str(var[3]) + " - (0.5*("+ str(var[3])+"-"+str(var[2])+")/"+str(var[1]) +") >>"+name_h_sig+"_of"
                t_signal.Draw(string_draw_of, sel_signal+"*("+ var[0]+">"+str(var[3])  +")")
                hsignal.Add(hsignal_of)                    
            hsignal.Scale(lumi)
            h_signals.append(hsignal)


    sel = "("+selection+")*"+myweights
    print sel
            #sel=selection
    n=[]
    n_allbkg=[]
    colors=[]
    if len(slices)>1:
        colors = [410, 856, 607, 801, 629, 879, 602, 921, 622, 588]
    for b in backgrounds:
        """
        if do_scale:
        with open(mypickle_fit, 'rb') as handle2:
        fit_res = pickle.load(handle2)
        prefit = fit_res["MC_exp_events_"+b][0]
        postfit = fit_res["Fitted_events_"+b][0]
        SF=postfit/prefit
        """
        n_thisbkg=[]

        if not len(slices)>1:
            color=getSampleColor(b)                #print b,color
            colors.append(color)
        t = infile[b].Get(b)
        if (not t):
            t = infile[b].Get(b+"nominal")
            if (not t):
                print b,"not found"
                continue
        sel_slice=sel
        if is_2D:
            htmp=ROOT.TH2D(name_can+"_"+b, name_can+"_"+b, var[1], var[2], var[3], var[5], var[6], var[7])
            string_draw=var[4]+":"+var[0]+" >>"+name_can+"_"+b
            htmp.GetXaxis().SetTitle(name_can)
            htmp.Sumw2()
            t.Draw(string_draw,sel_slice,"goff")
            htmp.Scale(lumi)
            n_thisbkg.append(htmp.Clone())
            htmp.Clear()
        else:            
            i=0
            for s in slices:
                htmp_name = name_can+"_"+str(i)+"_"+b
                htmp=ROOT.TH1D(htmp_name, htmp_name, var[1], var[2], var[3])
                htmp.GetXaxis().SetTitle(title_x_axis)
                htmp.Sumw2()
                sel_slice=sel+"*("+s+")"
                string_draw=var[0]+">>"+name_can+"_"+str(i)+"_"+b
            #print string_draw
                t.Draw(string_draw,sel_slice,"goff")
                if do_overflow:
                    htmp_of = ROOT.TH1D(htmp_name+"_of", htmp_name+"_of", var[1], var[2], var[3])
                    htmp_of.Sumw2()
                    string_draw_of = str(var[3]) + " - (0.5*("+ str(var[3])+"-"+str(var[2])+")/"+str(var[1]) +") >>"+name_can+"_"+str(i)+"_"+b+"_of"
                    t.Draw(string_draw_of, sel_slice+"*("+ var[0]+">"+str(var[3])  +")")
                    htmp.Add(htmp_of)                    

                htmp.Scale(lumi)
                n_thisbkg.append(htmp.Clone())
                htmp.Clear()
                i+=1

        n_allbkg.append(n_thisbkg)


    if len(slices)>1: # look at the composizion of one background
        isel=0
        for s in slices: # loop sulle slice
            n_sel=ROOT.TH1D(name_can, name_can, var[1], var[2], var[3])
            for n_allbkg_i in n_allbkg:
                n_sel.Add(n_allbkg_i[isel])
            isel+=1
            n.append(n_sel)
    else: # look at bkg composition
        for n_allbkg_i in n_allbkg:
            n.append(n_allbkg_i[0])

    histo_max=0
    i=0
    stack = ROOT.THStack("stack","stack")
    for h in n:
                #print h.Integral()
        h.SetLineColor(colors[i])
        h.SetFillColor(colors[i])
        h.SetLineColor(1)
        h.GetXaxis().SetTitle(var[0])
        if h.GetMaximum() > histo_max:
            histo_max=h.GetMaximum()
        stack.Add(h)
        if i==0:
            htot=h.Clone("htot")
        else:
            htot.Add(h)
        i+=1

    c = ROOT.TCanvas("can"+name_can,"can"+name_can,600,600)
    if is_2D:
        pad2 = ROOT.TPad("pad2", "pad2",0.0,0.0,1.0,1.0,22)
    else:
        pad1 = ROOT.TPad("pad1", "pad1",0.0,0.33,1.0,1.0,21)
        pad2 = ROOT.TPad("pad2", "pad2",0.0,0.0,1.0,0.35,22)
        pad2.SetGridy()
        pad1.SetFillStyle(0)
        pad1.SetFillColor(0)
        pad1.Draw()

    pad2.SetFillColor(0)
    pad2.SetFillStyle(0)
    pad2.Draw()

    # chiara: here
    if do_fraction:
        n_frac=[]
        for h in n:
            n_frac.append(h.Clone())
        stack_fraction = ROOT.THStack("stack_fraction","stack_fraction")
        for i in range(0,htot.GetNbinsX()+2):
            for h in n_frac:
                if htot.GetBinContent(i)>0:
                    frac = 100*h.GetBinContent(i)/htot.GetBinContent(i)
                    h.SetBinContent(i,frac)
                else:
                    h.SetBinContent(i,0)
        for h in n_frac:
            stack_fraction.Add(h)

        pad2.cd()        
        pad2.SetGridy()
        pad2.SetTicky()
        pad2.SetTickx()
        hone = htot.Clone("hone")
        for ibin in range(1, hone.GetNbinsX()+1):
            hone.SetBinContent(ibin, 100)
        hone.SetMaximum(100/2.)
        hone.GetYaxis().SetTitle("Composition [%]")
        hone.GetXaxis().SetLabelSize(hone.GetXaxis().GetLabelSize()*300)
        hone.GetXaxis().SetLabelOffset(0.02)
        hone.GetXaxis().SetTitleSize(hone.GetXaxis().GetTitleSize()*3)
        hone.GetXaxis().SetTitleOffset(1.05)
        hone.GetYaxis().SetTitleFont(43)
        hone.GetYaxis().SetTitleSize(20)
        hone.GetYaxis().SetLabelFont(43)
        hone.GetYaxis().SetLabelSize(15)
        hone.GetYaxis().SetTitleOffset(1.3)        
        hone.Draw('histo')
        stack_fraction.Draw("histo same")        
        #pad2.SetTopMargin(0.01)
        #pad2.SetBottomMargin(0.01)
        pad2.RedrawAxis("g")
        pad2.Update()

    if not is_2D:
        pad1.cd()
        if logY:
            histo_max *= 150
            pad1.SetLogy()
        #htot.SetMaximum(1.4 * histo_max)
        #htot.GetXaxis().SetLabelSize(htot.GetXaxis().GetLabelSize()*0.01)
        #htot.GetYaxis().SetLabelSize(htot.GetYaxis().GetLabelSize()*1.4)
        #htot.GetYaxis().SetTitleSize(htot.GetYaxis().GetTitleSize()*1.3)
        #htot.GetXaxis().SetLabelOffset(1)
        stack.Draw("hist")
        stack.GetYaxis().SetTitleFont(43)
        stack.GetYaxis().SetTitle("Events")
        stack.GetYaxis().SetTitleSize(20)
        stack.GetYaxis().SetTitleOffset(1.3)
        stack.GetYaxis().SetLabelFont(43)
        stack.GetYaxis().SetLabelSize(15)
        stack.GetXaxis().SetTitle(title_x_axis)
        stack.GetXaxis().SetTitleFont(43)
        stack.GetXaxis().SetTitleOffset(1.3)
        stack.GetXaxis().SetTitleSize(20)
        stack.GetXaxis().SetLabelFont(43)
        stack.GetXaxis().SetLabelSize(15)


        pad1.SetBottomMargin(0.11)
        pad1.SetTickx()
        pad1.SetTicky()
        stack.SetMaximum(1.4 * histo_max)
        stack.SetMinimum(0.1)
        stack.Draw("hist")
        pad1.RedrawAxis()
        leg = make_leg(n, labels, 0.69)
        leg.Draw()
        text =  ROOT.TLatex()
        text.SetNDC()
        text.SetTextAlign( 11 )
        text.SetTextFont( 42 )
        text.SetTextSize( 0.05 )
        text.SetTextColor( 1 )
        y = 0.82
        #write.append(region.replace("_","-"))
        for t in write:
            text.DrawLatex(0.13,y, t)
            y = y-0.06
            #text.DrawLatex(0.15,y, var[0].replace("_","-"))
        pad1.Update()

    if is_2D:
        pad2.cd()
        pad2.SetTicky()
        hratio = htot.Clone("h_mc_tot")
        hratio.GetYaxis().SetTitle("Events")
        hratio.GetYaxis().SetTitleOffset(0.25)
        hratio.SetLineColor(1)
        hratio.GetXaxis().SetTitle(var[0])
        hratio.GetYaxis().SetTitle(var[4])
        hratio.Draw("COLZ")
        hratio.Draw("TEXTE same")
        text =  ROOT.TLatex()
        text.SetNDC()
        text.SetTextAlign( 11 )
        text.SetTextFont( 42 )
        text.SetTextSize( 0.05 )
        text.SetTextColor( 1 )
        y = 0.82
        for t in write:
            text.DrawLatex(0.15,y, t)
            y = y-0.06
            #text.DrawLatex(0.15,y, var[0].replace("_","-"))
        pad2.Update()

    """
    if not is_2D:
        hline=ROOT.TH1D("hline", "hline", 1, var[2], var[3])
        hline.SetLineColor(ROOT.kRed)
        hline.SetBinContent(1,1)
        hline.GetYaxis().SetTitle("Data/MC")
        hline.Draw("same")
        
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.3)
        hratio.GetXaxis().SetLabelSize(hdata.GetXaxis().GetLabelSize()*300)
        hratio.GetXaxis().SetLabelOffset(0.02)
        hratio.GetYaxis().SetLabelSize(hdata.GetYaxis().GetLabelSize()*1.6)
        hratio.GetYaxis().SetLabelOffset(0.01)
        hratio.GetYaxis().SetTitleSize(hdata.GetYaxis().GetTitleSize()*3)
        #hratio.GetYaxis().SetTitleOffset(1.05)
        hratio.GetXaxis().SetTitleSize(hdata.GetXaxis().GetTitleSize()*3)
        hratio.GetXaxis().SetTitleOffset(1.05)
        """

    name_can = "mc_stack_"+name_can
    if add_signal:
        name_can=name_can+"_sig"
    if do_scale:
        name_pdf=name_can+"_scale.pdf"
    else:
        name_pdf=name_can
    c.SaveAs(outfolder+name_pdf+".pdf")
    c.SaveAs(outfolder+name_pdf+".png")
    print outfolder+name_pdf
    c.Clear()
    stack.Clear()
