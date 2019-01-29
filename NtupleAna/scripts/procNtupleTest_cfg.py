import FWCore.ParameterSet.Config as cms

process = cms.PSet()

#fileNames = ["root://cmsxrootd-site.fnal.gov//store/mc/RunIISummer16NanoAOD/ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/90000/8E9245DE-0616-E811-A45D-141877638F39.root",
#             "root://cmsxrootd-site.fnal.gov//store/mc/RunIISummer16NanoAOD/ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/90000/46052100-4316-E811-898E-44A84224053C.root"]
fileNames = ["/uscms/home/bryantp/nobackup/ZZ4b/ZH_HToBB_ZToLL_M125_13TeV_powheg_herwigpp/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/00000/380F111E-F342-E811-B579-0025905D1E02.root"]
fileNames = cms.vstring(fileNames)

#Setup framework lite input file object
process.fwliteInput = cms.PSet(
    fileNames   = fileNames,
    maxEvents   = cms.int32(-1),                             ## optional, -1 for no max
    )

#Setup framwork lite output file object
process.fwliteOutput = cms.PSet(
    fileName  = cms.string('test.root'),  ## mandatory
    )

#
# Setup picoAOD. For some reason this function gets evaluated twice...
#
import os
def mkpath(path):
    print "mkpath",path
    dirs = path.split("/")
    thisDir = ""
    for d in dirs:
        thisDir = thisDir+d+"/"
        if not os.path.exists(thisDir):
            os.mkdir(thisDir)

picoAOD = fileNames[0].replace("NANO","pico")
exists  = os.path.isfile(picoAOD) # file exists
if not exists: 
    path = '/'.join(picoAOD.split("/")[:-1])+"/"
    #print path
    mkpath(path)


use    = exists  # if picoAOD already existed, let's use it
#use    = False
create = not use # if not, let's create it
process.picoAOD = cms.PSet(
    fileName = cms.string(picoAOD),
    create   = cms.bool(create),
    use      = cms.bool(use),
    )

#Setup event loop object
process.procNtupleTest = cms.PSet(
    ## input specific for this analyzer
    debug = cms.bool(False),
    isMC  = cms.bool(True),
    lumi  = cms.double(150e3),
    )

