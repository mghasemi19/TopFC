# Top Flavor Changing
In this analysis, we will look for Flavor-Changing Neutral Currents of top quark such as $t \to u$ or $t \to c$ which is absent at tree-level in the Standard model. The signal of FCNC effects in the top sector may be an indicator of new flavor physics beyond the Standard Model. We will consider the di-lepton and tri-lepton signals with a pair of opposite-sign same-flavor (OSSF) leptons, where a selection of a single $b$-tagged jet is used with the last equation and, in general $l=e,\mu$ or $\tau$, and $l^{'}=l$ and/or $l^{'} \neq l$ can be considered in the tri-lepton channels.

<p align="center">
<img width="700" alt="Signal_diagram" src="https://user-images.githubusercontent.com/59040860/192085302-c5a889d0-43d8-442a-82c0-c3dc902f7815.png">
</p>

The main backgrounds in the SM for this analysis are: 
- single-top production in association with a gauge-boson such as Z or W boson (in W boson case there should be ca fake lepton)
- ttV where V represents weak bosons like Z and W (V bosons should decay leptonically to pass the preselection) 
- top quark pair production with fake lepton can occur through quark-antiquark annihilation or through gluon-gluon fusion. Then top-pair can decay to different channels such as **di-lepton** (10.5%), **single-lepton** (43.8%), and **all-hadronic** with (45.7%) decay branching ratios.
- single-top production via s-channel, t-channel, and Wt-channel with fake leptons

**Table of Contents** for this repositry
- [to-do list](#to-do-list)
- [Feynman Diagrams](#feynman-diagrams)
- [Signal and background ntuple generation](#signal-and-background-ntuple-generation)
- [BDT implementation](#bdt-implementation)
- [Event selection](#event-selection)


## to-do list
- [x] Read the [paper](https://arxiv.org/pdf/2101.05286.pdf) and review QFT for the related phenomology parts
- [X] Determine the signal and dominant/sub-dominant backgrounds (make all the Feynman diagrams)
- [X] Generate signal and background ntuples using MadGraph+Delphes (useful [link](http://feynrules.irmp.ucl.ac.be/wiki/FourFermionFCNCtqll))
- [ ] Event selection: signal vs. background
- [ ] Implement BDT algorithm to gain ML weights
- [ ] Perform cut-and-count analysis using BDT weights to define signal regions



## Feynman Diagrams
## Signal and background ntuple generation
## BDT implementation
## Event selection
