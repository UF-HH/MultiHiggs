""" class that encapsulates a RDataFrame to process a the normalization tree of an EventSample 
NOTE: since computing norms can be expensive, the calculation of these results can be cached.
The code checks whether the cache is updated (compared to the last modification date of filelists)
and if it contains the norm weight needed.
To keep the cache assocaited to the file, the cache name is determined from an has of the absolute path to the filelist
(so needs to be recalculated on any system)
"""

import ROOT
import copy
import os
import pickle
import hashlib

class NormSample:
    def __init__(self, name, treename):
        self.name        = name
        self.treename    = treename
        self.use_cache   = True 
        self.cache_dir   = 'norm_cache' 

        # verbosity
        # 0: no printout at all
        # 1: only essential printouts (start/stop/etc)
        # 2: logging of actions (histos booked, etc)
        # 3: debug
        self.verb        = 1

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
        self.filelistname = os.path.abspath(filelistname) # for cache name
        if self.use_cache:
            self.filelist_mtime = os.path.getmtime(filelistname)

    def load_weights(self, weightdef, normweights):
        """ Construct the new columns as needed to compute normalizations.
        The definition of all the weights used to fill histograms is contained in weightdef.
        The list of weights that must be considered for normalisation is normweights.
        Sums are constructed only for those unique combinations of normweights (all other weights are excluded) """

        ## find the unique weights participating to the normalisation
        self.weightdef   = copy.deepcopy(weightdef) # a dict, with 'tuple of weights -> weight_name'
        self.normwdef    = {} # a dict, with 'tuple of norm weights -> weight_name'
        self.normwremap  = {} # maps the weightdef (tuple of weights used in EventSample) to the (restricted set) name used here

        # define these weights as new columns in the rdf
        for wlist, wname in self.weightdef.items():
            normws = tuple(sorted([x for x in wlist if x in normweights])) # only norm weights
            if normws not in self.normwdef: # this is a new set of norm weight products
                normwname = 'NORMW_{}'.format(len(self.normwdef))
                if self.verb >= 3: print("[DEBUG] NormSample", self.name, "created new norm weight", normwname, '->', normws) 
                self.normwdef[normws] = normwname
            self.normwremap[wname] = self.normwdef[normws]

        # define these weights as new columns in the rdf
        for wlist, wname in self.normwdef.items():
            self.rdf = self.rdf.Define(wname, '*'.join(wlist))
            if self.verb >= 3: print("[DEBUG] NormSample", self.name, "created weight", wname, '->', wlist)

    def build_norms(self):
        if self.verb >= 1:  print("[INFO] NormSample", self.name, ": booking sum of weights.")
        self.bookednorms = {} # wname -> sum

        cached = []
        if self.use_cache and self.cache_exists() and self.cache_is_recent():
            if self.verb >= 1:  print("[INFO] NormSample", self.name, ": will use cached values if available")
            self.cache = self.get_cache()
            cached = self.cache.keys()
            if self.verb >= 1:  print("[INFO] NormSample", self.name, ": found", len(cached), 'cached weights')
            if self.verb >= 3:  print("[DEBUG] NormSample", self.name, ": cached weights", cached)

        for wlist, wname in self.normwdef.items():
            if wlist not in cached:
                self.bookednorms[wname] = self.rdf.Sum(wname)

        # norms were booked, now trigger their calculation
        if self.verb >= 1:  print("[INFO] NormSample", self.name, ": computing sum of weights. This may take a while, please wait...")
        self.norms = {}
        for wlist, wname in self.normwdef.items():
            if wlist in cached:
                if self.verb >= 3:  print("[DEBUG] NormSample", self.name, 'weight', wname, '-->', wlist, 'read from cache')
                self.norms[wname] = self.cache[wlist]
            else:
                if self.verb >= 3:  print("[DEBUG] NormSample", self.name, 'weight', wname, '-->', wlist, 'computed')
                self.norms[wname] = self.bookednorms[wname].GetValue()

    def get_norm(self, wname):
        """ get the norm corresponding to the EventSample original weight """
        thisname = self.normwremap[wname]
        return self.norms[thisname]

    def cache_file_name(self):
        if self.verb >= 3 : print('[DEBUG] NormSample:', self.name, 'file list abs path:', self.filelistname)
        cachename = hashlib.md5(self.filelistname.encode('utf-8')).hexdigest() + '.pkl'
        if self.verb >= 3 : print('[DEBUG] NormSample:', self.name, 'cache name:', cachename)
        return cachename

    def cache_full_name(self):
        return self.cache_dir + '/' + self.cache_file_name()

    def get_cache(self):

        """ get the cache dictionary, None if could not open """
        cachename = self.cache_full_name()
        if self.verb >= 3 : print('[DEBUG] NormSample:', self.name, 'cache is in:', cachename)
        try:
            f = open(cachename, 'rb')
        except IOError:
            if self.verb >= 3 : print('[DEBUG] NormSample:', self.name, 'could not open cache (IOError)')
            return None

        data = pickle.load(f)
        f.close()

        # cross check the filelist name
        if data['filelistname'] != self.filelistname:
            print('[ERROR] NormSample:', self.name, 'cache name differs from the filelist one:', data['filelistname'], self.filelistname)
            raise RuntimeError("norm cache mismatch")

        # retrieve cache
        return data['norms']

    def cache_exists(self):
        cn = self.cache_full_name()
        exists = os.path.isfile(cn)
        if self.verb >= 3 : print('[DEBUG] NormSample:', self.name, 'cache exists?', exists)
        return exists

    def cache_is_recent(self):
        
        """ compare cache last mod time with fileliast last mod time. True: cache older than filelist """
        cn = self.cache_full_name()
        cmtime = os.path.getmtime(cn)

        if cmtime > self.filelist_mtime: # cache older than filelist
            is_recent = True
        else:
            is_recent = False
        if self.verb >= 3 : print('[DEBUG] NormSample:', self.name, 'cache is recent?', is_recent)
        return is_recent

    def merge_caches(self, cache1, cache2):
        """ merge the caches. for common keys, verify compatibility """
        if self.verb >= 3 : print('[DEBUG] NormSample:', self.name, 'merging caches')

        cout = {}

        k1_not_in_2 = [x for x in cache1.keys() if x not in cache2.keys()]
        k2_not_in_1 = [x for x in cache2.keys() if x not in cache1.keys()]
        common = [x for x in cache1.keys() if x in cache2.keys()]

        if len(k1_not_in_2) + len(common) != len(cache1):
            raise RuntimeError("cache size mismatch")
        if len(k2_not_in_1) + len(common) != len(cache2):
            raise RuntimeError("cache size mismatch")

        for k in k1_not_in_2:
            cout[k] = cache1[k]
        for k in k2_not_in_1:
            cout[k] = cache2[k]
        for k in common:
            v1 = cache1[k]
            v2 = cache2[k]
            if v1 != v2:
                print('[ERROR] NormSample:', self.name, 'cache for key', k, 'differs between caches')
                raise RuntimeError("cache merge values differ")
            cout[k] = v1

        return cout

    def write_cache(self):
        
        if not self.use_cache:
           if self.verb >= 1 : print('[INFO] NormSample:', self.name, 'cannot save cache since use_cache =', self.use_cache)
           return

        cn = self.cache_full_name()
        
        # reindex self.norms (idx = NORMW_i) with the wlist
        inverse_def = {value : key for key,value in self.normwdef.items()}
        reidx_norms = {inverse_def[key] : value for key, value in self.norms.items()}

        try:
            self.cache
            if self.verb >= 1 : print('[INFO] NormSample:', self.name, 'will update existing cache')
            out_cache = self.merge_caches(self.cache, reidx_norms)
        except AttributeError:
            if self.verb >= 1 : print('[INFO] NormSample:', self.name, 'will create a new cache file')
            out_cache = reidx_norms

        odata = {}
        odata['filelistname'] = self.filelistname
        odata['norms'] = out_cache

        fout = open(cn, 'wb')
        pickle.dump(odata, fout)
        fout.close()