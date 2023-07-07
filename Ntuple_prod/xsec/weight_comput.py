# Background info
bkgs = ['ttbar', 'ttbarW', 'ttbarZ', 'tttt', 'tZ', 'WZ', 'ZZ']
# cross-sections (pb)
xsec_bkg = [5.691, 0.0001, 0.0026, 1.378e-05, 0.0025, 0.0905, 0.4475]
# number of events generated
bkg_event = [23 * 10**6, 2 * 10**6, 1785616, 1478961, 2 * 10**6, 10 * 10**6, 2 * 10**6]

# ttbar channel info
sig = ['signal_charm', 'signal_up']
# cross-sections (pb)
xsec_sig = [0.01376, 0.01376]
# number of events generated
sig_event = [3*10**6, 3*10**6]

# tW channel info
sig_tW = ['signal_tW_charm', 'signal_tW_up']
# cross-sections (pb)
xsec_sig_tW = [0.0007, 0.0007]
# number of events generated
sig_event_tW = [3*10**6, 3*10**6]


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
weight_sig_tW = sig_xsec_computer(xsec_sig_tW, sig_tW, sig_event_tW)
print(weight_sig_tW)

