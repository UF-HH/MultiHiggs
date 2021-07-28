import ROOT
import argparse
import os

parser = argparse.ArgumentParser('cmd line options')
parser.add_argument('--input', required=True)
parser.add_argument('--Nevthreshold', type=int, default = 499, help = "file valid if Nevents > Nevthreshold")

args = parser.parse_args()

print '... running on:', args.input

fin = open(args.input)

allfiles  = []
goodfiles = []
badfiles  = []

for l in fin:
    fname = l.strip()
    if not fname:
        continue
    allfiles.append(fname)
fin.close()

for i, f in enumerate(allfiles):
    # print '... ... checking file', fname
    if i%10 == 0:
        print '... ... checking %i/%i' % (i, len(allfiles))
    fIn = ROOT.TFile.Open(f)
    # FIXME: check for zombies etc here
    tIn = fIn.Get('Events')
    
    # print  '>> ', tIn.GetEntries()
    # print  '>> ', tIn.GetEntries()
    if tIn.GetEntries() <= args.Nevthreshold:
        badfiles.append(f)
    else:
        goodfiles.append(f)
    
    fIn.Close()

print "... ", len (allfiles), 'have been analysed. Good: ', len(goodfiles), 'bad :', len(badfiles)

print '----- bad files:'
for f in badfiles:
    print f

if len(badfiles) > 0:
    ## make a new flist
    os.system('cp %s %s.original' % (args.input, args.input))

    fout = open(args.input, 'w')
    for f in goodfiles:
        fout.write(f + '\n')
    fout.close()