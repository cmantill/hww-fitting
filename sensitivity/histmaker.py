import os
import sys
import math
import numpy as np
import argparse
from ROOT import gROOT,TFile,TTree,TH1D
import ROOT as r
from refs import datacardrefs
gROOT.SetBatch(True)
import numpy as np
from array import array

"""
Create shape histograms for combine
"""
 
class histmaker:
    def __init__(self, year, chan, outfilename, df, verbose=True):
        self.df = df # datacard refs
        # self.systs = self.df.systs #dictionary of cut+bin ids and selections
        self.outroot = outfilename #name of shape rootfile
        self.year       = year
        self.chan = chan
        self.yields= {}
        data = self.df.datafile
        self.datafile = data
        self.verbose = verbose
        self.blind = True
        if data=='none' or '.root' not in data:
            if self.verbose:
                print('blind run. will add empty data_obs histograms')
            self.blind = True

    def datahist(self, channel, binsel):
        histname = channel+'_'+self.year+'_data_obs'
        datahist = r.TH1F(histname, histname, self.df.nbins, self.df.selrange[0], self.df.selrange[1])

        #actually fill the histogram if it isn't a blind analysis
        if not self.blind:
            if self.verbose:
                print(self.df.datafile)
            pfile = r.TFile(self.df.datafile)
            ptree = pfile.Get(self.df.tn)
            gROOT.cd()
            ptree.Draw(self.df.var+'>>'+histname, binsel)#apply bin selection
            yld, unc = self.df.getyield(datahist)
            self.yields[histname] = [yld, unc]
            if self.verbose:
                print('filled data hist ', histname, 'with selection', binsel, 'for process data_obs and bin', channel)
                print('data yield', yld)
        else:
            if self.verbose:
                print('created empty data_obs hist', histname)
                
        #open rootfile for writing histograms
        histfile = r.TFile(self.outroot, "UPDATE")
        datahist.Write()
        histfile.Close()
        del histfile

    #makes a histogram for each process and bin. channel is the binname
    def getmchists(self, histname, processname, selection):
        shapevar=self.df.var
        # get, modify and return histogram:
        pfile = r.TFile(self.df.procfiles[processname])
        ptree = pfile.Get(self.df.tn)
        dischist = r.TH1F(histname, histname, self.df.nbins, self.df.selrange[0], self.df.selrange[1])

        if self.verbose:
            print(pfile)
        ptree.Draw(shapevar+'>>'+histname, selection)#apply bin selection
        if self.verbose:
            print('filled hist ', histname, 'with selection', selection, 'for process', processname)

        print 'Process ',processname
        yld, unc = self.df.getyield(dischist)
        if self.verbose:
            print(yld, unc)
        
        self.yields[histname] = [yld, unc]

        histfile = r.TFile(self.outroot, "UPDATE")
        dischist.Write()
        histfile.Close()
        del histfile
                      
    def makehists(self):        
        #first get the nominal histograms
        for chanid, chansel in self.df.binsels.iteritems():
            #data hist
            dsel = '('+self.df.binsels[chanid]+' && '+self.df.getsels('data','nosys',False)+')'
            self.datahist(chanid, dsel)
            #mc hists
            for processname in self.df.mcprocs:
                histname = chanid+'_'+self.year+'_'+processname
                binsel = '('+chansel+' && '+self.df.getsels(processname,'nosys',True)
                self.getmchists(histname, processname, binsel)
        # can include systematic variations here too

        return self.yields



