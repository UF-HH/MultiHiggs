'''
DESCRIPTION:

Cross-section (in pb) of all samples used in multi-b analyses as a function of the energy (TeV)

Sources:
 [1] https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
 [2] https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWG
'''
class CrossSection:
    def __init__(self, name, energyDict):
        self.name = name
        for key, value in energyDict.items():
            setattr(self, key, value)
        return
        
    def get(self, energy):
        '''
        Return the cross-section based on the energy (TeV)
        '''
        print("\n XSection of %s is %s" % (self.name, getattr(self, energy)))
        try:
            return getattr(self, energy)
        except AttributeError:
            print("No cross section for energy %s TeV." % (energy))

class CrossSectionList:
    def __init__(self, *args):
        self.crossSections = args[:]
        
    def get(self, name, energy):
        for obj in self.crossSections:
            if name == obj.name:
                return obj.get(energy)

bkgXSectionList = CrossSectionList(
    CrossSection("TTJets", {"13": 831.76,}),
    CrossSection("TT",     {"13": 831.76,}),
    CrossSection("TTToHadronic", {"13": 831.76*0.6741*0.6741,}),       # 377.96 pb
    CrossSection("TTTo2L2Nu",    {"13": 831.76*0.3259*0.3259,}),       # 88.34 pb
    CrossSection("TTToSemiLeptonic", {"13": 831.76*2*0.6741*0.3259,}), # 365.45 pb
    # QCD b-Enriched
    CrossSection("QCD_bEnriched_HT100to200",   {"13": 1127000.0, }),
    CrossSection("QCD_bEnriched_HT200to300",   {"13": 80430.0,   }),
    CrossSection("QCD_bEnriched_HT300to500",   {"13": 16620.0,   }),
    CrossSection("QCD_bEnriched_HT500to700",   {"13": 1487.0,    }),
    CrossSection("QCD_bEnriched_HT700to1000",  {"13": 296.5,     }),
    CrossSection("QCD_bEnriched_HT1000to1500", {"13": 46.61,     }),
    CrossSection("QCD_bEnriched_HT1500to2000", {"13": 3.72,      }),
    CrossSection("QCD_bEnriched_HT2000toInf",  {"13": 0.6462,    }),
    # QCD mu-Enriched
    CrossSection("QCD_Pt_15to20_MuEnrichedPt5",   {"13": 3.625e+06, }),
    CrossSection("QCD_Pt_20to30_MuEnrichedPt5",   {"13": 3.153e+06, }),
    CrossSection("QCD_Pt_30to50_MuEnrichedPt5",   {"13": 1.652e+06, }),
    CrossSection("QCD_Pt_50to80_MuEnrichedPt5",   {"13": 4.488e+05, }),
    CrossSection("QCD_Pt_80to120_MuEnrichedPt5",  {"13": 1.052e+05, }),
    CrossSection("QCD_Pt_120to170_MuEnrichedPt5", {"13": 2.549e+04, }),
    CrossSection("QCD_Pt_170to300_MuEnrichedPt5", {"13": 8.639e+03, }),
    CrossSection("QCD_Pt_300to470_MuEnrichedPt5", {"13": 7.961e+02, }),
    CrossSection("QCD_Pt_470to600_MuEnrichedPt5", {"13": 7.920e+01, }),
    CrossSection("QCD_Pt_600to800_MuEnrichedPt5", {"13": 2.525e+01, }),
    CrossSection("QCD_Pt_800to1000_MuEnrichedPt5", {"13": 4.724e+00, }),
    CrossSection("QCD_Pt_1000toInf_MuEnrichedPt5", {"13": 1.619e+00, }),
)
