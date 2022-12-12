#!/usr/bin/env python

import argparse
import ROOT
import logging
import os

ROOT.gROOT.SetBatch(True)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Plot options:")
    parser.add_argument("configFile", nargs="+", help="configuration file to execute")
    PlotArgs = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    has_extra_arguments = False
    for config in PlotArgs.configFile:
        if "++" in config:
            has_extra_arguments = True

    if has_extra_arguments:
        command ='python '+ ' '.join(PlotArgs.configFile)
        print "Running:",command
        print command
        os.system(command)

    else:
        for config in PlotArgs.configFile:
            logger.info("Running on "+config)
            execfile(config)
