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

    def load_weights(self, weightdef):
        self.weightdef = copy.deepcopy(weightdef) # a dict, with 'tuple of weights -> weight_name'

        # define these weights as new columns in the rdf
        for wlist, wname in self.weightdef.items():
            self.rdf = self.rdf.Define(wname, '*'.join(wlist))
            if self.verb >= 2: print("[DEBUG] NormSample", self.name, "created weight", wname, '->', wlist)

    def build_norms(self):
        if self.verb >= 1:  print("[INFO] NormSample", self.name, ": booking sum of weights.")
        self.bookednorms = {} # wname -> sum
        for wname in self.weightdef.values():
            self.bookednorms[wname] = self.rdf.Sum(wname)

        # norms were booked, now trigger their calculation
        if self.verb >= 1:  print("[INFO] NormSample", self.name, ": computing sum of weights. This may take a while, please wait...")
        self.norms = {}
        for wname in self.weightdef.values():
            self.norms[wname] = self.bookednorms[wname].GetValue()