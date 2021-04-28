""" class that encapsulates a RDataFrame to process a the normalization tree of an EventSample """

import ROOT
import copy

class NormSample:
    def __init__(self, name, treename):
        self.name        = name
        self.treename    = treename
        self.verb        = 2 

    ## FIXME: move the two functions below (in common with EventSample) in a 
    def build_dataframe(self, files):
        """ build the dataframe from a list of file names """
        self.chain = ROOT.TChain(self.treename)
        if self.verb >= 1 : print("[INFO] NormSample", self.name, "building", self.name, "with", len(files), "files")
        for f in files:
            self.chain.Add(f)
        self.rdf = ROOT.RDataFrame(self.chain)

    def build_dataframe_from_filelist(self, filelistname):
        """ parse a filelist and build the dataframe """
        if self.verb >= 1 : print("[INFO] NormSample", self.name, "building", self.name, "from filelist:", filelistname)
        filelist = []
        with open (filelistname) as fIn:
            for line in fIn:
                line = (line.split("#")[0]).strip()
                if line:
                    filelist.append(line)
        self.build_dataframe(filelist)   

    def load_weights(self, weightdef, normweights):
        """ Construct the new columns as needed to compute normalizations.
        The definition of all the weights used to fill histograms is contained in weightdef.
        The list of weights that must be considered for normalisation is normweights.
        Sums are constructed only for those unique combinations of normweights (all other weights are excluded) """

        ## find the unique weights participating to the normalisation
        self.weightdef  = copy.deepcopy(weightdef) # a dict, with 'tuple of weights -> weight_name'
        self.normwdef   = {} # a dict, with 'tuple of norm weights -> weight_name'
        self.normwremap = {} # maps the weightdef (tuple of weights used in EventSample) to the (restricted set) name used here

        # define these weights as new columns in the rdf
        for wlist, wname in self.weightdef.items():
            normws = tuple(sorted([x for x in wlist if x in normweights])) # only norm weights
            if normws not in self.normwdef: # this is a new set of norm weight products
                normwname = 'NORMW_{}'.format(len(self.normwdef))
                if self.verb >= 2: print("[DEBUG] NormSample", self.name, "created new norm weight", normwname, '->', normws) 
                self.normwdef[normws] = normwname
            self.normwremap[wname] = self.normwdef[normws]

        # define these weights as new columns in the rdf
        for wlist, wname in self.normwdef.items():
            self.rdf = self.rdf.Define(wname, '*'.join(wlist))
            if self.verb >= 2: print("[DEBUG] NormSample", self.name, "created weight", wname, '->', wlist)

    def build_norms(self):
        if self.verb >= 1:  print("[INFO] NormSample", self.name, ": booking sum of weights.")
        self.bookednorms = {} # wname -> sum
        for wname in self.normwdef.values():
            self.bookednorms[wname] = self.rdf.Sum(wname)

        # norms were booked, now trigger their calculation
        if self.verb >= 1:  print("[INFO] NormSample", self.name, ": computing sum of weights. This may take a while, please wait...")
        self.norms = {}
        for wname in self.normwdef.values():
            self.norms[wname] = self.bookednorms[wname].GetValue()

    def get_norm(self, wname):
        """ get the norm corresponding to the EventSample original weight """
        thisname = self.normwremap[wname]
        return self.norms[thisname]