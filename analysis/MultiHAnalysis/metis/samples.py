from metis.Sample import DirectorySample, DBSSample

# Master list of all samples
# Specify a dataset name and a short name for the output root file on nfs

samples = {

    # Signal
    # USER DEFINED PRIVATE SAMPLES THAT RESIDES IN SOME CEPH AREA IN UCSD T2 STORAGE SPACE
    # DirectorySample(location="/ceph/cms/store/user/phchang/my/private/sample/location/dir/in/ceph/area/", dataset="/MySignalSampleNameOfMyOwnChoosingInCMSStyleConvention/RunIISummer20UL18NanoAODv9/NANOAODSIM"),

    # Data
    "QCD_bEnriched_HT1000to1500_UL18" : DBSSample(dataset="/QCD_bEnriched_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM"),
}
