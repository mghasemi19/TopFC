bkgs = ['ttbar', 'ttbarW', 'ttbarZ', 'tttt', 'tZ', 'WZ', 'ZZ']
xsec_bkg = [5.691, 0.0001, 0.0026, 1.378e-05, 0.0025, 0.0905, 0.4475]
bkg_event = [15 * 10**6, 2 * 10**6, 1785616, 1478961, 2 * 10**6, 2 * 10**6, 2 * 10**6]

sig = ['signal_charm', 'signal_up']
xsec_sig = [0.01376, 0.01376]
sig_event = [3*10**6, 3*10**6]

def bkg_xsec_computer(cross, bkg, event):
    weight = {}
    for i in range(len(cross)):
        weight[bkg[i]] = cross[i] * 10**-12 * 3000 * 10**15 / (event[i])
    return weight

def sig_xsec_computer(cross, bkg, event):
    weight = {}
    for i in range(len(cross)):
        weight[bkg[i]] = cross[i] * 10**-12 * 3000 * 10**15 / (event[i])
    return weight

weight_bkg = bkg_xsec_computer(xsec_bkg, bkgs, bkg_event)        
print(weight_bkg)
weight_sig = sig_xsec_computer(xsec_sig, sig, sig_event) 
print(weight_sig)

