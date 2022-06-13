"""
Datacard dictionary.
For systematics append: _nosys / _jerUp / _jes_Down
"""
import numpy as np
from collections import OrderedDict
import ROOT as r

class datacardrefs:
    def __init__(self, year, chan, datadir, verbose=True):
        self.year = year
        self.chan = chan #ele, mu, had

        #treename for accessing events
        self.tn = 'Events'

        #variable you are using for histograms/templates:
        self.var = 'fj_msoftdrop'
        tageff = {
            'had':{'signal':'*0.4',
                   'QCD'   :'*0.01',
                   'wjets' :'*0.4',
                   'ttbar' :'*0.5',
                   'zjets' :'*0.4',
                   'other' :'*0.04',
                   'data'  :'*0.0'},
            'ele':{'signal':'*0.40',
                   'QCD'   :'*0.5',
                   'wjets' :'*0.01',
                   'ttbar' :'*0.01',
                   'zjets' :'*0.5',
                   'other' :'*0.04',
                   'data'  :'*0.0'},
            'mu':{'signal':'*0.40',
                  'QCD'   :'*0.5',
                  'wjets' :'*0.01',
                  'ttbar' :'*0.01',
                  'zjets' :'*0.5',
                  'other' :'*0.04',
                  'data'  :'*0.0'},
        }
        self.tageff = tageff[self.chan]
        print(self.tageff)

        self.verbose = verbose 

        #histogram settings
        self.nbins = 20
        self.selrange = [0.0, 350.0]

        lumi = {'2016':'35.92',
                '2017':'41.53',
                '2018':'59.74'}
        self.lumi = lumi[year]
        
        self.mcprocs = ['signal', 'QCD', 'wjets', 'ttbar', 'zjets']
        self.processes = ['signal', 'QCD', 'wjets', 'ttbar', 'zjets']
        
        self.datafile = '{}/{}/data_{}_merged.root'.format(datadir,year,chan)

        signalName = {
            'ele': 'GluGluHToWWToLNuQQ',
            'mu': 'GluGluHToWWToLNuQQ',
            'had': 'GluGluHToWWTo4q',
        }[chan]
        wjetsName = {
            'ele': 'WJetsLNu',
            'mu': 'WJetsLNu',
            'had': 'WQQ',
        }[chan]
        zjetsName = {
            'ele': 'DYJets',
            'mu': 'DYJets',
            'had': 'ZQQ',
        }[chan]
        
        self.procfiles={
            'signal' : '{}/{}/{}_{}_merged.root'.format(datadir,year,signalName,chan),
            'QCD': '{}/{}/QCD_{}_merged.root'.format(datadir,year,chan),
            'wjets': '{}/{}/{}_{}_merged.root'.format(datadir,year,wjetsName,chan),
            'ttbar': '{}/{}/TTbar_{}_merged.root'.format(datadir,year,chan),
            'zjets':  '{}/{}/{}_{}_merged.root'.format(datadir,year,zjetsName,chan),
        }
        
        metfilters   = ' && (goodverticesflag && haloflag && HBHEflag && HBHEisoflag && ecaldeadcellflag && badmuonflag)'
        if year=='2016':
            metfilters =  ' && (goodverticesflag && haloflag && HBHEflag && HBHEisoflag && ecaldeadcellflag && badmuonflag && eeBadScFilterflag)'
        self.metfilters = metfilters

        self.binsels =self.getbinsels()
        
    #leaving as example
    def getsels(self, proc, systyp='nosys', isMC=True):
        # wgtstr = '*tot_weight'
        wgtstr = '*tot_weight'+self.tageff[proc]
        #preselection:
        basesel = 'fj_pt>=300.0'
        binsels = self.getbinsels()
        if not isMC:
            # sel = '('+basesel+')'#trigcorr
            sel = basesel
            return sel
        elif isMC:
            sel = ''+basesel+')'+wgtstr
            return sel

    # leaving for now as example of how SR categories are set up
    def getbinsels(self):
        binsels = {'cat1':'fj_msoftdrop>=20.0'}
        return binsels    

    def getyield(self, hist):
        errorVal = r.Double(0)
        minbin=0
        maxbin=hist.GetNbinsX()+2
        hyield = hist.IntegralAndError(minbin, maxbin, errorVal)
        #if self.verbose:
        print 'yield:', round(hyield, 3), '+/-', round(errorVal, 3), '\n'
        return hyield,  errorVal
    
    def fixref(self, rootfile, hist):
        hist.SetDirectory(0)
        rootfile.Close()

    def makeroot(self, infile, treename, options="read"):
        rfile = r.TFile(infile, options)
        tree = rfile.Get(treename)
        return rfile, tree
