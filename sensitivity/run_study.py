import argparse
import os
from autodatacards import autodatacards
from plot_templates import postfit
import subprocess

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='python run_study.py')
    parser.add_argument("-o", "--outdir",   dest="outdir",   required=True, help="directory to put datacards in")
    parser.add_argument("-i", "--idir",     dest="idir",     required=True, help="input directory with merged files")
    parser.add_argument("--tag", dest="tag", required=True)
    args = parser.parse_args()

    args.notremakehists = False
    args.shapefile = "shapehists.root"
    tag = args.tag
    cpath = os.getcwd()
   
    significances = {}

    channels = ["ele","mu","had"]
    # years = ["2016","2016APV","2017","2018"]
    years = ["2017"]

    args.verbose = False

    for chan in channels:
        significances[chan] = {}
        for year in years:
            args.year = year
            args.chan = chan

            # make datacards
            args.tag = "%s_%s"%(tag,chan)
            cards = autodatacards(args)
            startbinnum=0
            lastbinnum = cards.cardsetup(startbinnum)

            # plot templates
            newdir = "%s/%s_%s"%(args.outdir,tag,chan)
            args.fitfile = "%s/hwwcard_%s_%s"%(newdir,year,args.shapefile)
            args.tag = "%s_%s"%(tag,chan)
            args.var = "fj0_msoftdrop"
            pf = postfit(args)
            pf.rungraphs()

            # run combine inside directory
            dirpath = "%s/%s"%(cpath,newdir)
            os.chdir(dirpath)
            datacard = "hwwcard_cat1_" +year + "_datacard0.txt"
            cmd_sig = "combine -M Significance -d %s -t -1 --expectSignal 1 "%datacard
            result = subprocess.check_output(cmd_sig,shell=True)
            significances[chan][year] = result.splitlines()[-2].split(' ')[-1]
            os.chdir(cpath)

    print(significances)
