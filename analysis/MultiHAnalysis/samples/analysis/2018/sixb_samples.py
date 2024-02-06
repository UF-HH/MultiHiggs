merged_samples = {}

# ---- Run2_UL/RunIISummer20UL18NanoAODv9/JetHT.py

from metis.Sample import DirectorySample, DBSSample

samples = {
"JetHT_Run2018A-UL2018_MiniAODv2_NanoAODv9-v2_NANOAOD" : DBSample(dataset="/JetHT/Run2018A-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD"),
"JetHT_Run2018B-UL2018_MiniAODv2_NanoAODv9-v1_NANOAOD" : DBSample(dataset="/JetHT/Run2018B-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD"),
"JetHT_Run2018C-UL2018_MiniAODv2_NanoAODv9-v1_NANOAOD" : DBSample(dataset="/JetHT/Run2018C-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD"),
"JetHT_Run2018D-UL2018_MiniAODv2_NanoAODv9-v2_NANOAOD" : DBSample(dataset="/JetHT/Run2018D-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD"),
}
merged_samples.update(samples)

# ---- Run2_UL/RunIISummer20UL18NanoAODv9/QCD_bEnriched.py

from metis.Sample import DirectorySample, DBSSample

samples = {
"QCD_bEnriched_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8_RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1_NANOAODSIM" : DBSample(dataset="/QCD_bEnriched_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM"),
"QCD_bEnriched_HT100to200_TuneCP5_13TeV-madgraph-pythia8_RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1_NANOAODSIM" : DBSample(dataset="/QCD_bEnriched_HT100to200_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM"),
"QCD_bEnriched_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8_RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1_NANOAODSIM" : DBSample(dataset="/QCD_bEnriched_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM"),
"QCD_bEnriched_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8_RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1_NANOAODSIM" : DBSample(dataset="/QCD_bEnriched_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM"),
"QCD_bEnriched_HT200to300_TuneCP5_13TeV-madgraph-pythia8_RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1_NANOAODSIM" : DBSample(dataset="/QCD_bEnriched_HT200to300_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM"),
"QCD_bEnriched_HT300to500_TuneCP5_13TeV-madgraph-pythia8_RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1_NANOAODSIM" : DBSample(dataset="/QCD_bEnriched_HT300to500_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM"),
"QCD_bEnriched_HT500to700_TuneCP5_13TeV-madgraph-pythia8_RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1_NANOAODSIM" : DBSample(dataset="/QCD_bEnriched_HT500to700_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM"),
"QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8_RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1_NANOAODSIM" : DBSample(dataset="/QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM"),
}
merged_samples.update(samples)

# ---- Run2_UL/RunIISummer20UL18NanoAODv9/TTJets_FXFX.py

from metis.Sample import DirectorySample, DBSSample

samples = {
"TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1_NANOAODSIM" : DBSample(dataset="/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM"),
}
merged_samples.update(samples)

samples = dict(merged_samples)
