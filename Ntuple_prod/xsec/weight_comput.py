bkgs = ['ttbar', 'tbarW', 'ttbarZ', 'tttt', 'tZ', 'WZ', 'ZZ']
xsec = [5.691, 0.0001, 0.0026, 1.378e-05, 0.0025, 0.0905, 0.4475]
weight = {}

def xsec_computer(cross, bkg):
    for i in range(len(cross)):
        #bkg_name = bkgs[i]
        weight[bkgs[i]] = cross[i] * 10**-12 * 3000 * 10**15 / (2 * 10**6)

xsec_computer(xsec, bkgs)        
print(weight)
