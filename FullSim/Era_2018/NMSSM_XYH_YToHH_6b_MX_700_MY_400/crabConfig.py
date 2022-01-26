from CRABClient.UserUtilities import config
config = config()

config.General.requestName     = 'srosenzw_NMSSM_XYH_YToHH_6b_MX_700_MY_400_sl7_nano_5M_v1'
config.General.workArea        = 'srosenzw_NMSSM_XYH_YToHH_6b_MX_700_MY_400_sl7_nano_5M_v1'
config.General.transferOutputs = True
config.General.transferLogs    = False

config.JobType.pluginName  = 'PrivateMC'
config.JobType.psetName    = 'nanoAOD_step_fake.py'
config.JobType.maxMemoryMB = 3500
config.JobType.inputFiles  = ['scriptExe.sh', 'genSim_step.py','digiRaw_step.py','recoAOD_step.py','miniAOD_step.py','nanoAOD_step.py','pileup.py','NMSSM_XYH_YToHH_6b_MX_700_MY_400_slc7_amd64_gcc700_CMSSW_10_6_0_tarball2.tar.xz']
config.JobType.scriptExe   ='scriptExe.sh'
config.JobType.numCores    = 2

config.Data.splitting   = 'EventBased'
config.Data.unitsPerJob = 500
config.Data.totalUnits  = 5000000
# config.Data.outLFNDirBase = '/store/user/srosenzw/XYH_test_privateMC/'
config.Data.outLFNDirBase = '/store/group/lpchbb/srosenzw/XYH_YToHH/'
config.Data.publication = False
# config.Data.outputPrimaryDataset = 'ggZH_HToMuMu_ZToLL_M125_13TeV_powheg_pythia8'
config.Data.outputDatasetTag     = 'srosenzw_NMSSM_XYH_YToHH_6b_MX_700_MY_400_sl7_nano_5M_v1'

config.Site.storageSite = 'T3_US_FNALLPC'
