bkgs = ['ttbar', 'tbarW', 'ttbarZ', 'tttt', 'tZ', 'WZ', 'ZZ']
xsec_bkg = [5.691, 0.0001, 0.0026, 1.378e-05, 0.0025, 0.0905, 0.4475]

sig = ['signal_charm', 'signal_up']
xsec_sig = [0.01376, 0.01376]

def xsec_computer(cross, bkg):
    weight = {}
    for i in range(len(cross)):
        #bkg_name = bkgs[i]
        weight[bkg[i]] = cross[i] * 10**-12 * 3000 * 10**15 / (2 * 10**6)
    return weight

weight_bkg = xsec_computer(xsec_bkg, bkgs)        
print(weight_bkg)
weight_sig = xsec_computer(xsec_sig, sig)        
print(weight_sig)

