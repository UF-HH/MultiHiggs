### columns names
### taken from run 323725

# Index 0 Emergency   
# Index 1 2.2e34  
# Index 2 2.0e34+ZB+HLTPhysics    
# Index 3 1.7e34  
# Index 4 1.5e34  
# Index 5 1.3e34  
# Index 6 1.1e34  
# Index 7 9.0e33  
# Index 8 6.0e33  
# Index 9 1.7 to 0.6 e34 No Parking   
# Index 10 2.0e34 
# Index 11 900b   
# Index 12 600b   
# Index 13 3b 
# Index 14 3b_2coll


import collections
import pickle

fIn = open('triggers_copy_OMS_run323725.txt')

trgs = collections.OrderedDict()

all_lines = []
for l in fIn:
    l = l.strip()
    if not l:
        continue
    all_lines.append(l)

## every record takes 17 lines (15 prescales + 1 name + idx)
if len(all_lines) % 17 != 0:
    raise runtime_error("record number does not match : %i" % len(all_lines))

# read by blocks
while len(all_lines) > 0:
    block     = all_lines[:17]
    all_lines = all_lines[17:]
    idx  = int(block[0])
    name = block[1]
    prlist = block[2:]
    prescales = tuple([int(x) for x in prlist])
    trgs[name] = (idx, prescales)

for key, value in trgs.items():
    print key, value

print "... I have read", len(trgs), 'triggers'

fout = open('trg_prescales_run_323725.pkl', 'wb')
data_out = {'trgs' : trgs}
pickle.dump(data_out, fout)
