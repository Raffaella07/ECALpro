from parameters import *

def printFillCfg1( outputfile ):
    outputfile.write("useHLTFilter = " + useHLTFilter + "\n")
    outputfile.write("correctHits = " + correctHits + "\n\n")
    outputfile.write('import FWCore.ParameterSet.Config as cms\n')
    outputfile.write('import RecoLocalCalo.EcalRecProducers.ecalRecalibRecHit_cfi\n')
    outputfile.write('process = cms.Process("analyzerFillEpsilon")\n')
    outputfile.write('process.load("FWCore.MessageService.MessageLogger_cfi")\n\n')
    if(is2012):
        outputfile.write('process.load("Configuration.Geometry.GeometryIdeal_cff")\n\n')
    else:
        outputfile.write('process.load("Configuration.StandardSequences.GeometryIdeal_cff")\n\n')
    outputfile.write('process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")\n')
    outputfile.write("process.GlobalTag.globaltag = '" + globaltag + "'\n")

    if (overWriteGlobalTag):
        if not( alphaTagRecord=='' and alphaTag=='' and alphaDB=='' ):        
           outputfile.write("process.GlobalTag.toGet = cms.VPSet(\n")
           if not(laserTag==''):
              outputfile.write("        cms.PSet(record = cms.string('" + laserTagRecord + "'),\n")
              outputfile.write("             tag = cms.string('" + laserTag + "'),\n")
              outputfile.write("             connect = cms.untracked.string('" + laserDB + "')\n")
              outputfile.write('     ),\n')
           outputfile.write("     cms.PSet(record = cms.string('" + alphaTagRecord + "'),\n")
           outputfile.write("             tag = cms.string('" + alphaTag + "'),\n")
           outputfile.write("             connect = cms.untracked.string('" + alphaDB + "')\n")
           if(GeVTagRecord=='' and alphaTag2==''):
              outputfile.write('     )\n')
           if not(GeVTagRecord==''):
              outputfile.write('     ),\n')
              outputfile.write("     cms.PSet(record = cms.string('" + GeVTagRecord + "'),\n")
              outputfile.write("             tag = cms.string('" + GeVTag + "'),\n")
              outputfile.write("             connect = cms.untracked.string('" + GeVDB + "')\n")
              if(alphaTag2==''):
                 outputfile.write('     )\n')
           if not(alphaTag2==''):
              outputfile.write('     ),\n')
              outputfile.write("     cms.PSet(record = cms.string('" + alphaTagRecord2 + "'),\n")
              outputfile.write("             tag = cms.string('" + alphaTag2 + "'),\n")
              outputfile.write("             connect = cms.untracked.string('" + alphaDB2 + "')\n")
              outputfile.write('     )\n')
           outputfile.write(')\n\n')

    outputfile.write('### Recalibration Module to apply laser corrections on the fly\n')
    outputfile.write('if correctHits:\n')
    outputfile.write('    process.ecalPi0ReCorrected =  RecoLocalCalo.EcalRecProducers.ecalRecalibRecHit_cfi.ecalRecHit.clone(\n')
    outputfile.write('        doEnergyScale = cms.bool(' + doEnenerScale + '),\n')
    outputfile.write('        doIntercalib = cms.bool(' + doIC + '),\n')
    outputfile.write('        doLaserCorrections = cms.bool(' + doLaserCorr + '),\n')
    outputfile.write("        EBRecHitCollection = cms." + ebInputTag +",\n")
    outputfile.write("        EERecHitCollection = cms." + eeInputTag +",\n")
    outputfile.write('        EBRecalibRecHitCollection = cms.string("pi0EcalRecHitsEB"),\n')
    outputfile.write('        EERecalibRecHitCollection = cms.string("pi0EcalRecHitsEE")\n')
    outputfile.write('    )\n\n')

    outputfile.write('### Running on AlcaRAW requires filtering AlcaPi0 events from AlcaEta events\n')
    outputfile.write('if useHLTFilter:\n')
    outputfile.write('    import copy\n')
    outputfile.write('    from HLTrigger.HLTfilters.hltHighLevel_cfi import *\n')
    outputfile.write('    process.AlcaP0Filter = copy.deepcopy(hltHighLevel)\n')
    outputfile.write('    process.AlcaP0Filter.throw = cms.bool(False)\n')
    outputfile.write('    process.AlcaP0Filter.HLTPaths = ["' + HLTPaths + '"]\n\n')

    outputfile.write("process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(" + nEventsPerJob +") )\n")
    outputfile.write("process.MessageLogger.cerr.FwkReport.reportEvery = 1000000\n")
    outputfile.write("process.MessageLogger.cerr = cms.untracked.PSet(\n")
    outputfile.write("        threshold  = cms.untracked.string('WARNING'),\n")
    outputfile.write("        ERROR      = cms.untracked.PSet (\n")
    outputfile.write("                                         limit = cms.untracked.int32(1)\n")
    outputfile.write("        )\n")
    outputfile.write(")\n")
    outputfile.write("process.options = cms.untracked.PSet(\n")
    outputfile.write("   wantSummary = cms.untracked.bool(True)\n")
    outputfile.write(")\n")
    outputfile.write("process.source = cms.Source('PoolSource',\n")
    outputfile.write("    fileNames = cms.untracked.vstring(\n")

def printFillCfg2( outputfile, pwd , iteration, outputDir, ijob ):
    outputfile.write("    )\n")
    outputfile.write(")\n")
    outputfile.write("\n")
    outputfile.write("import os, sys, imp, re\n")
    outputfile.write('CMSSW_VERSION=os.getenv("CMSSW_VERSION")\n')
    outputfile.write("if(len('" + json_file + "')>0):\n")
    outputfile.write('   if(re.match("CMSSW_5_.*_.*",CMSSW_VERSION)):\n')
    outputfile.write("      import FWCore.PythonUtilities.LumiList as LumiList\n")
    outputfile.write("      process.source.lumisToProcess = LumiList.LumiList(filename = '" + pwd + "/common/" + json_file + "').getVLuminosityBlockRange()\n")
    outputfile.write("   else:\n")
    outputfile.write("      import PhysicsTools.PythonAnalysis.LumiList as LumiList\n")
    outputfile.write("      myLumis = LumiList.LumiList(filename = '" + pwd + "/common/" + json_file + "').getCMSSWString().split(',')\n")
    outputfile.write("      process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange()\n")
    outputfile.write("      process.source.lumisToProcess.extend(myLumis)\n")
    outputfile.write("\n")
    outputfile.write("process.analyzerFillEpsilon = cms.EDAnalyzer('FillEpsilonPlot')\n")
    outputfile.write("process.analyzerFillEpsilon.OutputDir = cms.untracked.string('" +  outputDir + "')\n")
    outputfile.write("process.analyzerFillEpsilon.OutputFile = cms.untracked.string('/" + NameTag +  outputFile + "_" + str(ijob) + ".root')\n")
    outputfile.write("process.analyzerFillEpsilon.ExternalGeometry = cms.untracked.string('"         + pwd + "/common/" + ExternalGeometry + "')\n")
    outputfile.write("process.analyzerFillEpsilon.calibMapPath = cms.untracked.string('root://eoscms//eos/cms" + eosPath + "/" + dirname + "/iter_" + str(iteration-1) + "/" + NameTag + "calibMap.root')\n")
    outputfile.write("process.analyzerFillEpsilon.useEBContainmentCorrections = cms.untracked.bool(" + useEBContainmentCorrections + ")\n")
    outputfile.write("process.analyzerFillEpsilon.useEEContainmentCorrections = cms.untracked.bool(" + useEEContainmentCorrections + ")\n")
    outputfile.write("process.analyzerFillEpsilon.EBContainmentCorrections = cms.untracked.string('" + pwd + "/common/" + EBContainmentCorrections + "')\n")
    outputfile.write("process.analyzerFillEpsilon.MVAEBContainmentCorrections_01  = cms.untracked.string('" + pwd + "/common/" + MVAEBContainmentCorrections_01 + "')\n")
    outputfile.write("process.analyzerFillEpsilon.MVAEBContainmentCorrections_02  = cms.untracked.string('" + pwd + "/common/" + MVAEBContainmentCorrections_02 + "')\n")
    outputfile.write("process.analyzerFillEpsilon.MVAEEContainmentCorrections_01  = cms.untracked.string('" + pwd + "/common/" + MVAEEContainmentCorrections_01 + "')\n")
    outputfile.write("process.analyzerFillEpsilon.MVAEEContainmentCorrections_02  = cms.untracked.string('" + pwd + "/common/" + MVAEEContainmentCorrections_02 + "')\n")
    outputfile.write("process.analyzerFillEpsilon.MVAEBContainmentCorrections_eta01  = cms.untracked.string('" + pwd + "/common/" + MVAEBContainmentCorrections_eta01 + "')\n")
    outputfile.write("process.analyzerFillEpsilon.MVAEBContainmentCorrections_eta02  = cms.untracked.string('" + pwd + "/common/" + MVAEBContainmentCorrections_eta02 + "')\n")
    outputfile.write("process.analyzerFillEpsilon.Endc_x_y                        = cms.untracked.string('" + pwd + "/common/" + Endc_x_y + "')\n")
    outputfile.write("process.analyzerFillEpsilon.EBPHIContainmentCorrections = cms.untracked.string('" + pwd + "/common/" + EBPHIContainmentCorrections + "')\n")
    outputfile.write("process.analyzerFillEpsilon.EEContainmentCorrections = cms.untracked.string('" + pwd + "/common/" + EEContainmentCorrections + "')\n")
    outputfile.write("process.analyzerFillEpsilon.ContCorr_EB              = cms.untracked.string('" + pwd + "/common/" + EBContCorr + "')\n")
    outputfile.write("process.analyzerFillEpsilon.json_file               = cms.untracked.string('" + pwd + "/common/" + json_file + "')\n")
    outputfile.write("process.analyzerFillEpsilon.HLTResults              = cms.untracked.bool(" + HLTResults + ")\n")
    if(Are_pi0):
        outputfile.write("process.analyzerFillEpsilon.Are_pi0                 = cms.untracked.bool(True)\n")
    else:
        outputfile.write("process.analyzerFillEpsilon.Are_pi0                 = cms.untracked.bool(False)\n")
    if(is2012):
        outputfile.write("process.analyzerFillEpsilon.Is2012               = cms.untracked.bool(True)\n")
    else:
        outputfile.write("process.analyzerFillEpsilon.Is2012               = cms.untracked.bool(False)\n")

    outputfile.write("process.analyzerFillEpsilon.useOnlyEEClusterMatchedWithES = cms.untracked.bool(" + useOnlyEEClusterMatchedWithES + ")\n\n")

    outputfile.write("### choosing proper input tag (recalibration module changes the collection names)\n")
    outputfile.write("if correctHits:\n")
    outputfile.write("    process.analyzerFillEpsilon.EBRecHitCollectionTag = cms.untracked.InputTag('ecalPi0ReCorrected','pi0EcalRecHitsEB')\n")
    outputfile.write("    process.analyzerFillEpsilon.EERecHitCollectionTag = cms.untracked.InputTag('ecalPi0ReCorrected','pi0EcalRecHitsEE')\n")
    outputfile.write("else:\n")
    outputfile.write("    process.analyzerFillEpsilon.EBRecHitCollectionTag = cms.untracked." + ebInputTag + "\n")
    outputfile.write("    process.analyzerFillEpsilon.EERecHitCollectionTag = cms.untracked." + eeInputTag + "\n")
    outputfile.write("process.analyzerFillEpsilon.ESRecHitCollectionTag = cms.untracked." + esInputTag + "\n")

    outputfile.write("process.analyzerFillEpsilon.L1TriggerTag = cms.untracked.InputTag('hltGtDigis')\n")
    outputfile.write("process.analyzerFillEpsilon.CalibType = cms.untracked.string('" + CalibType + "')\n")
    outputfile.write("process.analyzerFillEpsilon.CurrentIteration = cms.untracked.int32(" + str(iteration) + ")\n")
    outputfile.write("process.analyzerFillEpsilon.Pi0PtCutEB = cms.untracked.double(" + Pi0PtCutEB + ")\n")
    outputfile.write("process.analyzerFillEpsilon.Pi0PtCutEE = cms.untracked.double(" + Pi0PtCutEE + ")\n")
    outputfile.write("process.analyzerFillEpsilon.gPtCutEB = cms.untracked.double(" + gPtCutEB + ")\n")
    outputfile.write("process.analyzerFillEpsilon.gPtCutEE = cms.untracked.double(" + gPtCutEE + ")\n")
    outputfile.write("process.analyzerFillEpsilon.Pi0IsoCutEB = cms.untracked.double(" + Pi0IsoCutEB + ")\n")
    outputfile.write("process.analyzerFillEpsilon.Pi0IsoCutEE = cms.untracked.double(" + Pi0IsoCutEE + ")\n")
    outputfile.write("process.analyzerFillEpsilon.nXtal_1_EB = cms.untracked.double(" +  nXtal_1_EB+ ")\n")
    outputfile.write("process.analyzerFillEpsilon.nXtal_2_EB = cms.untracked.double(" +  nXtal_2_EB+ ")\n")
    outputfile.write("process.analyzerFillEpsilon.nXtal_1_EE = cms.untracked.double(" +  nXtal_1_EE+ ")\n")
    outputfile.write("process.analyzerFillEpsilon.nXtal_2_EE = cms.untracked.double(" +  nXtal_2_EE+ ")\n")
    outputfile.write("process.analyzerFillEpsilon.S4S9_EB = cms.untracked.double(" + S4S9_EB + ")\n")
    outputfile.write("process.analyzerFillEpsilon.S4S9_EE = cms.untracked.double(" + S4S9_EE + ")\n")
    outputfile.write("process.analyzerFillEpsilon.Barrel_orEndcap = cms.untracked.string('" + Barrel_or_Endcap + "')\n")
    outputfile.write("process.analyzerFillEpsilon.AlcaL1TrigNames = cms.untracked.vstring('L1_SingleIsoEG5','L1_SingleIsoEG8','L1_SingleIsoEG10','L1_SingleIsoEG12','L1_SingleIsoEG15','L1_SingleEG2','L1_SingleEG5','L1_SingleEG8','L1_SingleEG10','L1_SingleEG12','L1_SingleEG15','L1_SingleEG20','L1_SingleJet6U','L1_SingleJet10U','L1_SingleJet20U','L1_SingleJet30U','L1_SingleJet40U','L1_SingleJet50U','L1_DoubleJet30U','L1_DoubleEG5','L1_DoubleEG2')\n\n")
    if isMC:
       outputfile.write("process.analyzerFillEpsilon.isMC = cms.untracked.bool(True)\n")
    outputfile.write("process.p = cms.Path()\n")
    outputfile.write("if useHLTFilter:\n")
    outputfile.write("    process.p *= process.AlcaP0Filter\n")
    outputfile.write("if correctHits:\n")
    outputfile.write("    print 'ADDING RECALIB RECHIT MODULE WITH PARAMETERS'\n")
    outputfile.write("    print 'ENERGY SCALE '+str(process.ecalPi0ReCorrected.doEnergyScale)\n")
    outputfile.write("    print 'INTERCALIBRATION '+str(process.ecalPi0ReCorrected.doIntercalib)\n")
    outputfile.write("    print 'LASER '+str(process.ecalPi0ReCorrected.doLaserCorrections)\n")
    outputfile.write("    process.p *= process.ecalPi0ReCorrected\n")
    outputfile.write("process.p *= process.analyzerFillEpsilon\n")




def printFitCfg( outputfile, iteration, outputDir, nIn, nFin, EBorEE, nFit ):
    outputfile.write("import FWCore.ParameterSet.Config as cms\n")
    outputfile.write("process = cms.Process('FitEpsilonPlot')\n")
    outputfile.write("process.load('FWCore.MessageService.MessageLogger_cfi')\n")
    outputfile.write("process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )\n")
    outputfile.write("process.source =   cms.Source('EmptySource')\n")
    outputfile.write("process.fitEpsilon = cms.EDAnalyzer('FitEpsilonPlot')\n")
    outputfile.write("process.fitEpsilon.OutputFile = cms.untracked.string('" + NameTag + EBorEE + "_" + str(nFit) + "_" + calibMapName + "')\n")
    outputfile.write("process.fitEpsilon.CalibType = cms.untracked.string('" + CalibType + "')\n")
    outputfile.write("process.fitEpsilon.OutputDir = cms.untracked.string('" +  outputDir + "')\n")
    outputfile.write("process.fitEpsilon.CurrentIteration = cms.untracked.int32(" + str(iteration) + ")\n")
    outputfile.write("process.fitEpsilon.NInFit = cms.untracked.int32(" + str(nIn) + ")\n")
    outputfile.write("process.fitEpsilon.NFinFit = cms.untracked.int32(" + str(nFin) + ")\n")
    outputfile.write("process.fitEpsilon.EEorEB = cms.untracked.string('" + EBorEE + "')\n")
    outputfile.write("process.fitEpsilon.is_2011 = cms.untracked.bool(" + is_2011 + ")\n")
    if(Are_pi0):
        outputfile.write("process.fitEpsilon.Are_pi0 = cms.untracked.bool( True )\n")
    else:
        outputfile.write("process.fitEpsilon.Are_pi0 = cms.untracked.bool( False )\n")
    outputfile.write("process.fitEpsilon.StoreForTest = cms.untracked.bool( False )\n")
    outputfile.write("process.fitEpsilon.Barrel_orEndcap = cms.untracked.string('" + Barrel_or_Endcap + "')\n")
    outputfile.write("process.fitEpsilon.EpsilonPlotFileName = cms.untracked.string('root://eoscms//eos/cms" + eosPath + "/" + dirname + "/iter_" + str(iteration) + "/" + NameTag + "epsilonPlots.root')\n")
    outputfile.write("process.fitEpsilon.calibMapPath = cms.untracked.string('root://eoscms//eos/cms" + eosPath + "/" + dirname + "/iter_" + str(iteration-1) + "/" + NameTag + "calibMap.root')\n")
    outputfile.write("process.p = cms.Path(process.fitEpsilon)\n")


def printSubmitFitSrc(outputfile, cfgName, source, destination, pwd, logpath):
    outputfile.write("#!/bin/bash\n")
    outputfile.write("cd " + pwd + "\n")
    if(is2012):
        outputfile.write("export SCRAM_ARCH=slc5_amd64_gcc462\n")
    else:       
        outputfile.write("export SCRAM_ARCH=slc5_amd64_gcc434\n")
    outputfile.write("eval `scramv1 runtime -sh`\n")
    outputfile.write("echo 'cmsRun " + cfgName + " 2>&1 | awk {quote}/FIT_EPSILON:/ || /WITHOUT CONVERGENCE/ || /HAS CONVERGED/{quote}' > " + logpath  + "\n")
    outputfile.write("cmsRun " + cfgName + " 2>&1 | awk '/FIT_EPSILON:/ || /WITHOUT CONVERGENCE/ || /HAS CONVERGED/' >> " + logpath  + "\n")
    outputfile.write("echo 'ls " + source + " >> " + logpath + " 2>&1' \n" )
    outputfile.write("ls " + source + " >> " + logpath + " 2>&1 \n" )
    outputfile.write("echo 'cmsStage -f " + source + " " + destination + "' >> " + logpath  + "\n")
    outputfile.write("cmsStage -f " + source + " " + destination + " >> " + logpath + " 2>&1 \n")
    outputfile.write("echo 'rm -f " + source + "' >> " + logpath + " \n")
    outputfile.write("rm -f " + source + " >> " + logpath + " 2>&1 \n")

def printSubmitSrc(outputfile, cfgName, source, destination, pwd, logpath):
    outputfile.write("#!/bin/bash\n")
    outputfile.write("cd " + pwd + "\n")
    if(is2012):
        outputfile.write("export SCRAM_ARCH=slc5_amd64_gcc462\n")
    else:       
        outputfile.write("export SCRAM_ARCH=slc5_amd64_gcc434\n")
    outputfile.write("eval `scramv1 runtime -sh`\n")
    if not(Silent):
        outputfile.write("echo 'cmsRun " + cfgName + "'\n")
        outputfile.write("cmsRun " + cfgName + "\n")
        outputfile.write("echo 'cmsStage -f " + source + " " + destination + "'\n")
        outputfile.write("cmsStage -f " + source + " " + destination + "\n")
        outputfile.write("echo 'rm -f " + source + "'\n")
        outputfile.write("rm -f " + source + "\n")
    else:
        outputfile.write("echo 'cmsRun " + cfgName + " 2>&1 | awk {quote}/FILL_COUT:/{quote}' > " + logpath  + "\n")
        outputfile.write("cmsRun " + cfgName + " 2>&1 | awk '/FILL_COUT:/' >> " + logpath  + "\n")
        outputfile.write("echo 'ls " + source + " >> " + logpath + " 2>&1' \n" )
        outputfile.write("ls " + source + " >> " + logpath + " 2>&1 \n" )
        outputfile.write("echo 'cmsStage -f " + source + " " + destination + "' >> " + logpath  + "\n")
        outputfile.write("cmsStage -f " + source + " " + destination + " >> " + logpath + " 2>&1 \n")
        outputfile.write("echo 'rm -f " + source + "' >> " + logpath + " \n")
        outputfile.write("rm -f " + source + " >> " + logpath + " 2>&1 \n")

def printParallelHadd(outputfile, outFile, list, destination, pwd):
    outputfile.write("#!/bin/bash\n")
    if(is2012):
         outputfile.write("cd /afs/cern.ch/work/l/lpernie/pi0/Calibration/CMSSW_4_2_4/src\n")
    else:
         outputfile.write("cd " + pwd + "\n")
    outputfile.write("export SCRAM_ARCH=slc5_amd64_gcc434\n")
    outputfile.write("eval `scramv1 runtime -sh`\n")
    outputfile.write("echo 'hadd -f /tmp/" + outFile + " @" + list + "'\n")
    outputfile.write("hadd -f /tmp/" + outFile + " @" + list  + "\n")
    outputfile.write("echo 'cmsStage -f /tmp/" + outFile + " " + destination + "'\n")
    outputfile.write("cmsStage -f /tmp/" + outFile + " " + destination + "\n")
    outputfile.write("rm -f /tmp/" + outFile + "\n")

def printFinalHadd(outputfile, list, destination, pwd):
    outputfile.write("#!/bin/bash\n")
    if(is2012):
         outputfile.write("cd /afs/cern.ch/work/l/lpernie/pi0/Calibration/CMSSW_4_2_4/src\n")
    else:
         outputfile.write("cd " + pwd + "\n")
    outputfile.write("export SCRAM_ARCH=slc5_amd64_gcc434\n")
    outputfile.write("eval `scramv1 runtime -sh`\n")
    outputfile.write("echo 'hadd -f /tmp/" + NameTag + "epsilonPlots.root @" + list + "'\n")
    outputfile.write("hadd -f /tmp/" + NameTag + "epsilonPlots.root @" + list  + "\n")
    outputfile.write("echo 'cmsStage -f /tmp//" + NameTag + "epsilonPlots.root " + destination + "'\n")
    outputfile.write("cmsStage -f /tmp/" + NameTag + "epsilonPlots.root " + destination + "\n")
    outputfile.write("rm -f /tmp/" + NameTag + "epsilonPlots.root\n")
