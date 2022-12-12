# Making Plots (chiara_plotter)

This package provides the tools to produce basic plots starting from ROOT ntuples that contain variables and proper event weights. In order to produce plots, the user has to write a configuration file containing the calls to the existing plotting functions.

Please put the configuration files that you want to keep track of in the [config](config) folder.

Changes are ongoing to reduce the hard-coded parts and make the code easier to use, so please check often for updates.

## Get the code

```
git clone ssh://git@gitlab.cern.ch:7999/MultiBJets/chiara_plotter.git
```

## Basic usage

Write one (or more) configuration file containing calls to the existing plotting funtions, and run it with:

```
./make_plots.py name_of_config_file_1 name_of_config_file_2 etc
```

For example:

```
./make_plots.py config_example/data_mc.py 
```

## Use cases

Here some simple examples are described

### Data-MC plots

The main funciton that produces data-MC plots is

```
data_mc (var, selection, myweights, backgrounds, name_infile, labels, title_x_axis, lumi, logY=False, write=[], outfolder="./plots/", name_can="", do_scale=False, add_signal = False, signals=[], do_blind=False)
```

Where the meaning of the arguments is:
* var : tuple of the format (var_name, n_bins, x_low, x_high), for example ("bjets_n",4, 1.5,5.5). Note: this can also be a fucntion of other variablse in the TTree
* selection : string with the selection to be applied for the plot
* myweights : string with the weights to be applied to MC, separated by a *
* backgrounds : list of strings containing the name of the backgrounds exactly as they are in the input file, except the suffix "_NoSys"
* name_infile : python dictionary associating to each of the backgrouns and to data the correct TFile (in the form of a string)
* labels : list of background names (strings) for the legend, in the same order as in the "backgrounds" argument
* title_x_axis : string, title for the X-axis
* lumi : float, luminosity to which scale the backgrounds
* logY : bool, sets if the Y-axis has log scale
* write : list of strings that will be written on the top-left corner of the canvas
* outfolder : name of the folder where the plots will be stored
* name_can : name of the final plot file
* do_scale : bool, does not have any effect now, in the future will allow to scale MC to data
* add_signal : bool, if True it adds signal distribution overlaid to data-MC comparison
* signals : list of strings containing the signal names as in the input file
* do_blind : if True, sum of MC is used instead of data

#### Configuration file
An example configuration file is [data_mc.py](config_example/data_mc.py), or [data_mc_blinded.py](config_example/data_mc_blinded.py) for the version with blinded data.
They both use input files from eos, so From lxplus you can run them out of the box with:

```
./make_plots.py config_example/data_mc.py config_example/data_mc_blinded.py
```

You can refer to this configuration file for a practical example of how to make data-MC plots with loop on many different variables.

#### ATTENTION: Caveats
* data_mc : "_NoSys" expected in the end of the name
* do_scale : does not do anything
* At the moment unfortunately all the style options, including the colors of the backgrounds, are hard-coded in [plot_functions.py](plot_utils/plot_functions.py). This will soon be changed, but for now all the backgroud colors are the ones used in ATLAS-SUSY-2016-10-002  


### 2D Data-MC plots

The data_mc function can also produce 2D plots data-MC comparison. In this case the X and Y axes show the two variables, and the Z axis the data/MC ratio. The 2D function is activated by a difference in the way the data_mc arguments are structured. In particular, the first argument should be a longet tuple with the format: ("bjets_n",4, 1.5,5.5, "jets_n",6, 3.5,9.5)

#### Configuration file

An example configuration file for 2D data-MC comparison is [data_mc_2D.py](config_example/data_mc_2D.py).
It uses input files from eos, so From lxplus you can run it out of the box with:

```
./make_plots.py config_example/data_mc_2D.py
```


#### ATTENTION: Caveats
* "_NoSys" expected in the end of the name
* do_scale : does not do anything
* Signal overlay is not active in this mode
* Not possible to personalize axis titles, they are just the name of the variable
* Text overlaps with plot (since all the canvas is filled by the plot)

### Signal vs background plots

The main funciton that produces signal vs background plots is

```
sig_bkg (var, sel, backgrounds,name_infile, labels, title_x_axis, lumi, logY=False, write=[], do_scale=False, outfolder="./plots/", name_can="", signals=[], lables_sig=[],signal_sel="1", signal_scale=1.0)
```

Where the meaning of the arguments is:
* var : tuple of the format (var_name, n_bins, x_low, x_high), for example ("bjets_n",4, 1.5,5.5). Note: this can also be a fucntion of other variablse in the TTree
* sel : string with the selection to be applied for the plot. ATTENTION: unlike in data_mc, this string also has to contain the event weights, just like you would do in a TTree.Draw()
* backgrounds : list of strings containing the name of the backgrounds exactly as they are in the input file, except the suffix "_NoSys"
* name_infile : python dictionary associating to each of the backgrouns and to data the correct TFile (in the form of a string)
* labels : list of background names (strings) for the legend, in the same order as in the "backgrounds" argument
* title_x_axis : string, title for the X-axis
* lumi : float, luminosity to which scale the backgrounds
* logY : bool, sets if the Y-axis has log scale
* write : list of strings that will be written on the top-left corner of the canvas
* outfolder : name of the folder where the plots will be stored
* name_can : name of the final plot file
* do_scale : bool, does not have any effect now, in the future will allow to scale signal to MC
* add_signal : bool, if True it adds signal distribution overlaid to data-MC comparison
* signals : list of strings containing the signal names as in the input file
* lables_sig : signal names as in the leged
* signal_sel : if you want only a sub-selection of your signal to be consider, you can put the selection string here (e.g. a flag to select only a specific decay channel)
* signal_scale : scale the signal by this factor with respect to the nominal cross section

#### Configuration file

An example for a configuration file with instrucions that produces signal vs background plots can be found in [sig_vs_bkg](config_example/sig_vs_bkg.py).

It uses input files from eos, so From lxplus you can run it out of the box with:

```
./make_plots.py config_example/sig_vs_bkg.py
```

#### ATTENTION: Caveats
* "_NoSys" expected in the end of the name
* do_scale : does not do anything
* Not possible to personalize style
* Because of this, the colors for new signals need to be hard coded into [plot_functions.py](plot_utils/plot_functions.py)

### Composition pie-charts

The main function that produces pie-charts is:
```
plot_pie (myjson_sel, weights, backgrounds, name_infile, labels, slices, outfolder="./", name_can="pie", region="_", do_scale=False, mypickle_fit="", print_err=True, print_raw=True)
```

Where the meaning of the arguments is:

* myjson_sel : json file contaning the definition of the regions where you want the pie-charts (one plot for each region)
* backgrounds : list of strings containing the name of the backgrounds to be used
* name_infile : python dictionary associating to each of the backgrouns and to data the correct TFile (in the form of a string)
* labels : label for each slice of the pie
* slices : list of strings containing the definition of the different slices of the pie. If this list is ["1"], no selection will be applied and the background will be considered in it's integrity - this is useful when you just want to look at the fraction of different backgrounds
* outfolder : name of the folder where the plots will be stored
* name_can : name of the pdf file - the final name will be this + name of the region as in the json file
* region : request this pattern in the name of the regions in the json file (e.g. if you have a json file with all the regions and you just want the plots in the SRs)
* do_scale : function not yet active
* mypickle_fit : function not yet active
* print_err : bool, print the statistical uncertainty on the fraction
* print_raw : bool, print the raw number of events in each slice

Since the main purpose of the `plot_pie` function is to study the background composition in mny different regions, you will need a json file with the region definition. If you want one single region, you just need to have only that region defined in your json file. You can find an example of json file in [sel_example.json](json_example/sel_example.json).

There are mainly two ways in which you can obtain a pie:
* Relative fraction of each background. In this case, you will have slices=["1"], backgrounds=[list of backgrounds] and labels=[list of background labels]
* For one single background, relative fraction of different selections. In this calse you will have slices=[list of selections], backgrounds=[your chosen background], labels=[list of labels for each slice]

If you have lists with more than one entry for both slices and backrounds, the final division will be based on the slices and the different backgrounds will be added.

#### Configuration file

An example for a configuration file with instrucions that produces pie-charts can be found in [pies.py](config_example/pies.py).

It uses input files from eos, so From lxplus you can run it out of the box with:

```
./make_plots.py config_example/pies.py
```



### Shape comparison (different backgorunds or signals)


### Truth-tagging vs direct tagging


### Trigger efficiency


### Diagnostic plots: pu dependence

