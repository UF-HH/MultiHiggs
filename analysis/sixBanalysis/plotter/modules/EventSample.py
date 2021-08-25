""" class that encapsulates a RDataFrame to process a list of samples and build histograms from it """

## the class will contain the following attributes
## name       : the name of the sample
## treename   : the name of the tree to read
## chain      : the tchain accessing the files
## rdf        : the root data frame 
## histos     : a dictionary that has key -> internal histo name, value -> the smart RDF histogram
## histodesc  : a dictionary that has key -> histo description
## slices     : a dictionary that has key -> sliced dataframe
## selections_defs    : a fictionary that has key -> definition of the selection
## weightdef  : tuple of weights str to be multiplied -> name of the column in the rdf

import ROOT
import uuid
import collections
import copy

class EventSample:
    def __init__(self, name, treename):
        self.name       = name
        self.treename   = treename
        self.histos     = {}
        self.histodesc  = {}
        self.slices     = {}
        self.selections = collections.OrderedDict()
        
        # verbosity
        # 0: no printout at all
        # 1: only essential printouts (start/stop/etc)
        # 2: logging of actions (histos booked, etc)
        # 3: debug
        self.verb       = 1 

        # sampletype = sampletype.lower()
        # if not sampletype in ['data', 'mc']:
        #     raise RuntimeError("wrong sample type")
    
    def build_dataframe(self, files):
        """ build the dataframe from a list of file names """
        self.chain = ROOT.TChain(self.treename)
        if self.verb >= 1 : print("[INFO] building", self.name, "with", len(files), "files")
        for f in files:
            self.chain.Add(f)
        self.rdf = ROOT.RDataFrame(self.chain)

    def add_column(self, colname, colexpr):
        if self.verb >= 1:
            print('[INFO] adding column', colname, 'to', self.name, 'defined as', colexpr)
        self.rdf = self.rdf.Define(colname, colexpr)

    def build_dataframe_from_filelist(self, filelistname):
        """ parse a filelist and build the dataframe """
        if self.verb >= 1 : print("[INFO] building", self.name, "from filelist:", filelistname)
        filelist = []
        with open (filelistname) as fIn:
            for line in fIn:
                line = (line.split("#")[0]).strip()
                if line:
                    filelist.append(line)
        self.build_dataframe(filelist)

    def make_histo_title(self, histodata):
        if 'title' in histodata:
            return histodata
        s = '{}_{}_{}'.format(self.name, histodata['sel'], histodata['var'])
        return s

    def make_histo_uuid(self):
        
        """ generate a string used to identify the histogram in the TFile """
        # try:
        #     self.histocounter
        # except AttributeError:
        #     self.histocounter = 0
        # name = 'histo_{}'.format(self.histocounter)
        # self.histocounter += 1
        # return name

        return str(uuid.uuid4())

    def book_histo(self, histodata):
        
        """ Book the histogram creations with RDataFrames. Expect Histo to contain the following keys:
            var                      : the variable to plot
            binning                  : the binning to use (as a list). Alternatively the ones below
            bins (nbins, xmin, xmax) : for the standard ROOT constructor
            sel                      : the name of the selection
            weightlist               : a list of the weights to apply
            NOTE: booking is actually done in two separate steps. First we collect all the histogram descriptions,
            than we find unique selections to be applied. Finally, we build fitered dataframes and book histograms from there
        """

        uname = self.make_histo_uuid()
        self.histodesc[uname] = copy.deepcopy(histodata)
        if self.histodesc[uname]['weightlist'] :
            self.histodesc[uname]['weightlist'] = tuple(sorted(self.histodesc[uname]['weightlist']))


    def get_all_booked_sel(self):
        
        """ return a list with all the names of the selections booked """
        sels = list(set([x['sel'] for x in self.histodesc.values()]))
        return sels

    def get_all_booked_weights(self):

        """ return all the weight expressions that were needed """
        weights = list(set([x['weightlist'] for x in self.histodesc.values() if x['weightlist']]))
        return weights

    def make_histos(self):

        """ analyse the histograms required, filter as needed and book histos to rdf. Generates the slices and the weight definitiona """

        ## 1) define all the column weights
        weightlists = self.get_all_booked_weights()
        weigthnames = ['HISTOW_{}'.format(i) for i in range(len(weightlists))]
        self.weightdef = {x[0] : x[1] for x in zip(weightlists, weigthnames)} # maps a list of weights to the rdf column 

        for wname, wdef in zip(weigthnames, weightlists):
            if self.verb >= 3:
                print("[DEBUG]", self.name, "created weight", wname, '->', wdef)
            self.rdf = self.rdf.Define(wname, '*'.join(wdef))

        ## 2) define all the slices - key name is given by selection
        self.slices = {}
        for selname, seldef in self.selections_defs.items():
            self.slices[selname] = self.rdf.Filter(seldef)

        ## 3) book the histograms
        for uuid, hd in self.histodesc.items():
            
            htitle  = self.make_histo_title(hd)
            wlist   = hd['weightlist']

            if 'binning' in hd:
                hmodel = ROOT.RDF.TH1DModel(uuid, htitle, len(hd['binning'] -1), array('d', hd['binning']))
            else:
                hmodel = ROOT.RDF.TH1DModel(uuid, htitle, *hd['bins'])
            
            if wlist:
                wname = self.weightdef[wlist]
                self.histos[uuid] = self.slices[hd['sel']].Histo1D( hmodel, hd['var'], wname)
            else:
                self.histos[uuid] = self.slices[hd['sel']].Histo1D( hmodel, hd['var'])

    def fill_histos(self):
        """ just trigger the filling of histograms """

        if self.verb >= 1: print('[INFO]', self.name, 'Making histograms. This might take a while, please wait...')
        
        # FIXME: this exception could be suppressed if needed
        if len(self.histos) == 0:
            print('[ERROR] Sample', self.name, 'has 0 histograms. Did you call make_histos() after booking them?')
            raise RuntimeError('no histograms found to process')
        
        for idx, (uuid, h) in enumerate(self.histos.items()):
            # print('... doing', idx, '/', len(self.histos))
            # print(h.GetEntries())
            h.GetName()
    
    # def write_histos(self, fOut):
    #     if self.verb >= 1: print('[INFO] Saving histograms to file')        
    #     fOut.cd()
    #     for idx, (uuid, h) in enumerate(self.histos.items()):
    #         h.Write()

    # def print_summary(self):

        # # dump content
        # print('----- dataframe : existing')
        # for k in self.rdf.GetColumnNames():
        #     print(k)
        # print('----- dataframe : defined')
        # for k in self.rdf.GetDefinedColumnNames():
        #     print(k)
        # print('----- slices : existing')
        # for sname, sval in self.slices.items():
        #     print ('====', sname)
        #     for k in sval.GetColumnNames():
        #         print(k)
        # print('----- slices : defined')
        # for sname, sval in self.slices.items():
        #     print ('====', sname)
        #     for k in sval.GetDefinedColumnNames():
        #         print(k)
