import pickle

def find_key(trgs, trg_name):
    found = []
    for t in trgs.keys():
        tnamev = trg_name + '_v'
        if t.startswith(tnamev):
            found.append(t)
    if len(found) == 0:
        return None
    if len(found) > 1:
        print "*** WARNING : multiple keys match", trg_name
        for t in found:
            print ' --> ', t
        print '... returning last:', found[-1] 
    return found[-1]

f_prescales = open('trg_prescales_run_323725.pkl', 'rb')
trg_prescales = pickle.load(f_prescales)['trgs']

print '... I have loaded the prescales of', len(trg_prescales), 'triggers'

col_threshold = 1
print "... trigger labelled as UNPRESCALED if prescale = 1 for all columns >=", col_threshold

trgs_to_check = [
    'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5',
    'HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59',
    'HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94',
    'HLT_PFHT400_SixPFJet32',
    'HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59',
    'HLT_PFHT450_SixPFJet36',
]

for tc in trgs_to_check:
    key = find_key(trg_prescales, tc)
    if not key:
        print "{:<80} : NO INFO FOUND".format(tc)
    else:
        presc = trg_prescales[key][1]
        vals  = presc[col_threshold:]
        uvals = list(set(vals))
        if len(uvals) > 1 or uvals[0] != 1:
            print "{:<80} : PRESCALED".format(tc), presc
        else:
            print "{:<80} : UNPRESCALED".format(tc)