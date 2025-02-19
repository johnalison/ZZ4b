#/usr/local/Cellar/python/3.7.1/bin/python3
#have to use python 3 with ROOT 6. ROOT 6 is required for ExRootAnalysis which is the madgraph package for converting .lhe files to .root files.
import ROOT

#Load the classes for LHE objects in ROOT
EXROOTANALYSIS_PATH='/Applications/MG5_aMC_v2_6_4/ExRootAnalysis/libExRootAnalysis.so'
ROOT.gSystem.Load(EXROOTANALYSIS_PATH)

from particle import *
from diJet import *
from eventView import *
from eventHists import *
from eventData import *
from cutflowHists import *
from toyTree import *
import selection as sel

class analysis:
    def __init__(self, tree, outFileName, debug=False):
        self.debug = debug
        self.nEvents = 0
        self.tree  = tree
        #self.tree.Print()
        #self.tree.SetBranchStatus("*",0)
        self.tree.GetEntry(0)
        if self.debug:
            self.tree.Show()

        self.outFileName = outFileName
        self.outFile = ROOT.TFile(self.outFileName,"RECREATE")

        self.lumi = 1
        self.kFactor = 1

        #cutflow
        self.cutflow = cutflowHists(self.outFile, "cutflow")

        #hists
        self.allEvents   = truthHists(self.outFile, "allEvents")
        self.passPreSel  = eventHists(self.outFile, "passPreSel",  True)
        self.passMDRs    = eventHists(self.outFile, "passMDRs",    True)
        self.passMDCs    = eventHists(self.outFile, "passMDCs",    True)
        self.passHCdEta  = eventHists(self.outFile, "passHCdEta",  True)
        self.passTopVeto = eventHists(self.outFile, "passTopVeto", True)

        #event
        self.thisEvent = eventData(self.tree, self.debug)

        #toyTree for Tudor's studies
        self.toy = toyTree(outFileName.replace(".root",""), self.debug)
            
    #Event Loop
    def eventLoop(self,events=None):
        #events is a list of events to process
        if events:
            self.nEvents=len(events)
        else:
            self.nEvents=self.tree.GetEntries()
            events = range(self.nEvents)

        print( "Processing",self.nEvents,"Events" )
        i=0
        for e in events:
            self.processEvent(e)
            i+=1
            if i%1000 == 0: print( "Processed",str(i).rjust(len(str(self.nEvents))),"of",str(self.nEvents),"Events" )
            
    def processEvent(self, entry):
        #initialize event and do truth level stuff before moving to reco (actual data analysis) stuff
        self.thisEvent.update(entry)
        self.thisEvent.weight *= self.lumi/self.nEvents * self.kFactor

        self.allEvents.Fill(self.thisEvent, self.thisEvent.weight)
        self.cutflow.Fill("all", self.thisEvent.weight)

        #
        #basic cuts
        #
        passJetMultiplicity = len(self.thisEvent.recoJets) >= 4
        if not passJetMultiplicity:
            if self.debug: print( "Fail Jet Multiplicity" )
            return
        self.cutflow.Fill("jetMultiplicity", self.thisEvent.weight)

        #Jet pt cut
        nPassJetPt = 0
        for jet in self.thisEvent.recoJets:
            if jet.pt > sel.minPt:
                nPassJetPt += 1
        passJetPt = nPassJetPt >= 4
        if not passJetPt:
            if self.debug: print( "Fail Jet Pt" )
            return
        self.cutflow.Fill("jetPt", self.thisEvent.weight)

        #Jet eta cut
        nPassJetEta = 0
        for jet in self.thisEvent.recoJets:
            if jet.eta < sel.maxEta:
                nPassJetEta += 1
        passJetEta = nPassJetEta >= 4
        if not passJetEta:
            if self.debug: print( "Fail Jet Eta" )
            return
        self.cutflow.Fill("jetEta", self.thisEvent.weight)

        #b-tagging
        self.thisEvent.applyTagSF(self.thisEvent.recoJets)
        self.cutflow.Fill("btags", self.thisEvent.weight)

        #
        #if event passes basic cuts start doing higher level constructions
        #
        self.thisEvent.buildViews(self.thisEvent.recoJets)
        self.thisEvent.buildTops(self.thisEvent.recoJets, [])
        self.passPreSel.Fill(self.thisEvent, self.thisEvent.weight)

        self.thisEvent.applyMDRs()
        if not self.thisEvent.views:
            if self.debug: print( "No Views Pass MDRs" )
            return
        self.cutflow.Fill("MDRs", self.thisEvent.weight)
        self.passMDRs.Fill(self.thisEvent, self.thisEvent.weight)

        if not self.thisEvent.views[0].passMDCs:
            if self.debug: print( "Fail MDCs" )
            return
        self.cutflow.Fill("MDCs", self.thisEvent.weight)
        self.passMDCs.Fill(self.thisEvent, self.thisEvent.weight)
        
        if not self.thisEvent.views[0].passHCdEta:
            if self.debug: print( "Fail HC dEta" )
            return
        self.cutflow.Fill("HCdEta", self.thisEvent.weight)
        self.passHCdEta.Fill(self.thisEvent, self.thisEvent.weight)

        #write this event to toyTree
        if self.thisEvent.views[0].ZZSB or self.thisEvent.views[0].ZZCR or self.thisEvent.views[0].ZZSR:
            self.toy.Fill(self.thisEvent)
        
        if not self.thisEvent.passTopVeto:
            if self.debug: print( "Fail top veto" )
            return
        self.cutflow.Fill("topVeto", self.thisEvent.weight)
        self.passTopVeto.Fill(self.thisEvent, self.thisEvent.weight)
        
        if not self.thisEvent.views[0].ZZSR:
            if self.debug: print( "Fail xZZSR =",self.thisEvent.views[0].xZZ )
            return
        self.cutflow.Fill("xZZSR", self.thisEvent.weight)

        
                
    def Write(self):
        self.cutflow.Write()
        
        self.allEvents  .Write()
        self.passPreSel .Write()
        self.passMDRs   .Write()
        self.passMDCs   .Write()
        self.passHCdEta .Write()
        self.passTopVeto.Write()

        self.outFile.Close()

        self.toy.Write()



