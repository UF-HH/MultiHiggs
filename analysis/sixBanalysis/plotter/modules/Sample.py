""" class that handles both EventSample and NormSample to automatically prepare and scale all histos """

from modules.EventSample import EventSample
from modules.NormSample import NormSample
import copy
import collections

class Sample:
    def __init__(self, name, sampletype, sampledesc=None, filelist=None, files=None, evt_treename='sixBtree', norm_treename='NormWeightTree'):
        self.name       = name
        self.sampletype = sampletype
        self.verb       = 3
        allowedtypes = ['data', 'mc']
        if self.sampletype not in allowedtypes:
            print('[ERROR] Sample', self.name, 'declared as', self.sampletype, '. Must be in', allowedtypes)
            raise RuntimeError('wrong sample type')

        ## create subclasses
        self.evt_sample  = EventSample(self.name, evt_treename)
        if self.sampletype == 'data':
            self.norm_sample = None
        elif self.sampletype == 'mc':
            self.norm_sample = NormSample(self.name, norm_treename)

        ## sampledesc contains information to understand how events must be processed
        if self.sampletype == 'mc':
            if not sampledesc:
                print('[ERROR]: sample', self.name, 'is marked as mc, please pass a sampledesc')
            self.lumi  = sampledesc['lumi']
            self.xs    = sampledesc['xs']
            self.scale = sampledesc['scale'] if 'scale' in sampledesc else 1.

            # default is xs in pb and lumi in pb-1. Can be changed with appropriate arguments
            self.lumi_units = sampledesc['lumi_units'] if 'lumi_units' in sampledesc else 'pbinv' 
            self.xs_units   = sampledesc['xs_units']   if 'xs_units'   in sampledesc else 'pb' 

            lumidict = {'fbinv' : 1000.,  'pbinv' : 1.}
            xsdict   = {'fb'    : 0.001,  'pb'    : 1.}

            self.lumiscale = lumidict[self.lumi_units]
            self.xsscale   = xsdict[self.xs_units]

        ## open samples
        if not filelist and not files:
            print('[ERROR] Sample', self.name, '. Please construct with a filelist (in a plain text file) or a list of filenames')
            raise RuntimeError('Sample initialization error')
        if files:
            self.evt_sample.build_dataframe(files)
            if self.sampletype == 'mc':
                self.norm_sample.build_dataframe(files)
                if self.verb >= 2: print('[INFO]', self.name, ' : NormSample does not (yet) implement weight caching for a construction from a python list of files, disabling caching')
                self.norm_sample.use_cache = False
        elif filelist:
            self.evt_sample.build_dataframe_from_filelist(filelist)
            if self.sampletype == 'mc':
                self.norm_sample.build_dataframe_from_filelist(filelist)

    # def make_selections(self, selecti):
    #     pass

    def do_histos(self, histos_descs, norm_weights):
        
        # first tell the event sample which histograms to make
        for h in histos_descs:
            desc = copy.deepcopy(h)
            if self.sampletype == 'data' and 'weightlist' in desc:
                desc['weightlist'] = None
            self.evt_sample.book_histo(desc)
        
        if self.verb >= 2: print('[INFO]', self.name, 'going to make histos of this EventSample')
        self.evt_sample.make_histos()

        # if it is a MC sample, also prepare the norms - these will have been 
        if self.sampletype == 'mc':
            self.norm_sample.load_weights(self.evt_sample.weightdef, norm_weights)

        # fill the histograms
        self.evt_sample.fill_histos()

        # apply the necessary scalings
        if self.sampletype == 'mc':
            self.norm_sample.build_norms()
            for uuid, h in self.evt_sample.histos.items():
                hd = self.evt_sample.histodesc[uuid]
                wname = self.evt_sample.weightdef[hd['weightlist']]
                
                if self.verb >= 3 :
                    print ('[DEBUG] Histo described as', hd, 'will be scaled by the following')
                    print ('        scale     :', self.scale)
                    print ('        lumi      :', self.lumi, self.lumi_units)
                    print ('        lumiscale :', self.lumiscale)
                    print ('        xs        :', self.xs, self.xs_units)
                    print ('        xsscale   :', self.xsscale)
                    print ('        Norm retrieved for weight', wname, '->', self.norm_sample.normwremap[wname], 'is', self.norm_sample.get_norm(wname))
                global_scale = self.scale * self.lumi * self.lumiscale * self.xs * self.xsscale
                norm_scale   = self.norm_sample.get_norm(wname)
                h.Scale(global_scale / norm_scale)

    def make_histo_dir_name(self, histodata):
        """ generate a name used to save the hsitogram in the TFile.
        Histodata is a dictionary that defines how the histogram was created.
        Return a tuple with (directory, histoname). Directory can be empty for base file directory """

        rdir = '{sample}/{sel}'.format(sample=self.name, sel=histodata['sel'])
        hname = '{var}'.format(var=histodata['var'])
        if 'nametag' in histodata:
            hname += '_{}'.format(histodata['nametag'])
        # FIXME: add systematics naming

        return (rdir, hname)

    def write_histos(self, fOut):
        
        if self.verb >= 1:  print('[INFO] sample', self.name, 'will save to file', len(self.evt_sample.histos), 'histos')

        onames = {}
        # check all save paths
        for uuid in self.evt_sample.histos.keys():
            hd = self.evt_sample.histodesc[uuid]
            dir_name = self.make_histo_dir_name(hd)
            onames[uuid] = dir_name

        # make all directories
        all_dirs = next(zip(*onames.values()))
        all_dirs = list(set(all_dirs))
        all_dirs = [x for x in all_dirs if x] # remove null directories

        for d in all_dirs:
            if self.verb >= 3: print('[DEBUG] sample', self.name, 'will create directory: ', d)
            fOut.mkdir(d)

        # now rename histograms and save them
        for uuid, h in self.evt_sample.histos.items():
            fOut.cd(onames[uuid][0])
            h.SetName(onames[uuid][1])
            h.Write()

    def print_end_summary(self):
        print('[END SUMMARY] : Sample', self.name, ', type', self.sampletype)
        print('              : EventSample did', self.evt_sample.rdf.GetNRuns(), 'event loops') 
        if self.norm_sample:
            print('              : NormWeight did', self.evt_sample.rdf.GetNRuns(), 'event loops') 
        else:
            print('              : NormWeight was not defined')