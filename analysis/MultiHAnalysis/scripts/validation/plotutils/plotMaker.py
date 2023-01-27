import ROOT
import collections
import copy
import random

ROOT.gStyle.SetOptStat(0)
# ROOT.gStyle.SetOptStat('neuo')
random.seed(1)

class cut:
    def __init__(self, val):
        self.cut = val
    
    def concat(self, one, two):
        """ concatenate two strings """
        proto = '({one}) && ({two})'
        return proto.format(one=one, two=two)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.concat(self.cut, other.cut)
        elif isinstance(other, basestring):
            return self.concat(self.cut, other)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__, type(other)))

    def __iadd__(self, other):
        self.cut = self.cut + other
        return self

    def __str__(self):
        rep = 'CUT: ' + self.cut
        return rep

class histo:
    def __init__(self, name, title, expr, cut, nbins, range_binning):
        """ if nbins < 0, range_binning defines the user binning with boundaries
        if nbins >= 0, range_binning is the usual xmin / xmax """
        self.name  = name
        self.title = title
        self.expr  = expr
        self.cut   = cut
        self.nbins = nbins
        if self.nbins < 0:
            self.userBinning = True
            self.nbins       = len(range_binning) - 1
            self.binning     = array('d',range_binning)
        else:
            self.userBinning = False
            if len(range_binning) != 2:
                raise RuntimeError('histo : range_binning malformed: expect exactly two values')
            self.xmin = float(range_binning[0])
            self.xmax = float(range_binning[1])

        if self.userBinning:
            self.histo = ROOT.TH1D(self.name, self.title, self.nbins, self.binning)
        else:
            self.histo = ROOT.TH1D(self.name, self.title, self.nbins, self.xmin, self.xmax)
        
        self.histo.SetDirectory(0)

    def set_properties(self, properties):
        self.properties = copy.deepcopy(properties)

    def build_histo(self, tIn):
        self.histo.SetDirectory(ROOT.gDirectory) ## needed to make the ttree aware of this histo
        tIn.Draw('{expr} >> {hname}'.format(expr=self.expr, hname=self.name), self.cut)
        if 'norm' in self.properties:
            self.histo.Scale(self.properties['norm']/self.histo.Integral())
        self.histo.SetDirectory(0) 

#############################################################################################

class plotMaker:
    
    def __init__(self):
        self.verb = 2
        self.tag  = None # prepended automatically to all histos names
        self.msg_head = '... '
        self.histos = collections.OrderedDict()
        self.plot_alone_if_in_overlay = False
        self.plot_name_proto = '{hname}.pdf'
        self.def_col_palette = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+1, ROOT.kBlack, ROOT.kMagenta, ROOT.kCyan, ROOT.kOrange]
        self.frames = {} ## ROOT e veramente un programma di merda!
        self.bottom_frames = {} ## ROOT e veramente un programma di merda!
        self.bottom_diffs = {}

    def load_histos(self, histo_defs):
        if self.verb >= 1: print '%sloading histos' % self.msg_head
        for hd in histo_defs:
            properties = histo_defs[hd]
            name  = properties['name']  if not self.tag else self.tag + '_' + properties['name']
            title = properties['title'] if 'title' in properties else name
            expr  = properties['expr']
            cut   = properties['cut']   if 'cut' in properties else ''
            if 'nbins' in properties:
                nbins = properties['nbins']
                xmin  = properties['xmin']
                xmax  = properties['xmax']
                range_binning = (xmin, xmax)
            else:
                nbins = -1
                range_binning = properties['binning']
            this_h = histo(name, title, expr, cut, nbins, range_binning)
            this_h.set_properties(properties) ## will copy also some unneeded properties

            this_key = hd if not self.tag else self.tag + '_' + hd
            self.histos[this_key] = this_h
        if self.verb >= 1: print '%sloaded'% self.msg_head, len(self.histos), 'histos'

    def build_histos(self, tIn):
        if self.verb >= 1:  print "%sbuilding"% self.msg_head, len(self.histos), 'histos'
        for idx, hname in enumerate(self.histos):
            h = self.histos[hname]
            if idx%10 == 0:
                if self.verb >= 2: print ' >>> bulding {} / {}'.format(idx, len(self.histos))
            h.build_histo(tIn)

    def set_overlays(self, overlays):
        self.overlays = copy.deepcopy(overlays)
        self.all_to_overlay = []
        for ovr in self.overlays.values():
            self.all_to_overlay.extend(ovr['parts'])
        self.all_to_overlay = list(set(self.all_to_overlay))

    def set_axis_style(self, frame, removeXaxis=False):
            
        frame.GetXaxis().SetTitleFont(43) # so that size is in pixels
        frame.GetYaxis().SetTitleFont(43) # so that size is in pixels
        frame.GetXaxis().SetLabelFont(43) # so that size is in pixels
        frame.GetYaxis().SetLabelFont(43) # so that size is in pixels
        frame.GetYaxis().SetNdivisions(505)

        frame.GetXaxis().SetTitleOffset(2.8)
        frame.GetYaxis().SetTitleOffset(1.2)

        frame.GetXaxis().SetTitleSize(30 if not removeXaxis else 0);
        frame.GetXaxis().SetLabelSize(22 if not removeXaxis else 0);
        frame.GetYaxis().SetTitleSize(30);
        frame.GetYaxis().SetLabelSize(22);

        frame.GetXaxis().SetTickSize(0.10)
        frame.GetYaxis().SetTickSize(0.05)

    def plot_all(self, do_pdf=True, do_png=False):

        try: self.c1
        except AttributeError:
            if self.verb >= 1: print '%sbuilding internally a canvas'% self.msg_head
            self.c1 = ROOT.TCanvas('c1', 'c1', 600, 600)

        ## first plot all plots intended to be done alone
        if self.verb >= 1: print "%splotting individual plots"% self.msg_head
        for hname in self.histos:
            h = self.histos[hname]
            if not self.plot_alone_if_in_overlay and hname in self.all_to_overlay:
                continue
            plotname = self.plot_name_proto.format(hname=hname)
            h.histo.Draw()
            if do_pdf: self.c1.Print(plotname, 'pdf')
            if do_png: self.c1.Print(plotname.replace('.pdf', '.png'), 'png')

        ## now plot the overlays

        if self.verb >= 1: print "%splotting overlays"% self.msg_head
        for ovr, vals in self.overlays.items():
            
            if 'compare' in vals: ## will make a ratio
                self.c1.cd()
                self.pad1.Draw()
                self.pad1.cd()
            else:
                self.c1.cd()

            # print '///// ', ovr, vals
            frame = self.histos[vals['parts'][0]].histo.Clone(ovr)
            self.frames[ovr] = frame
            self.set_axis_style(frame, removeXaxis = True if 'compare' in vals else False)
            # frame = ROOT.TH1D(frame)
            # frame.SetDirectory(0)
            frame.Reset("ICESM")
            if 'title' in vals: frame.SetTitle(vals['title'])
            nelems = len(vals['parts'])
            if nelems > len(self.def_col_palette): ## expand the palette
                rndmcol = lambda: random.randint(0,255)
                for i in range(nelems - len(self.def_col_palette)):
                    col = ROOT.TColor.GetColor('#%02X%02X%02X' % (rndmcol(), rndmcol(), rndmcol()))
                    self.def_col_palette.append(col)

            mmaxs = [self.histos[h].histo.GetMaximum() for h in vals['parts']]
            mmax  = max(mmaxs)

            frame.SetMaximum(1.15*mmax)
            if ROOT.gPad.GetLogy(): frame.SetMinimum(0.5)
            else: frame.SetMinimum(0)

            frame.Draw()

            ## build the legend
            leg = ROOT.TLegend(0.6, 0.6, 0.88, 0.88)
            leg.SetFillStyle(0)
            leg.SetBorderSize(0)

            # plot the frame
            for idx, el in enumerate(vals['parts']):
                the_h = self.histos[el].histo
                the_h.SetLineColor(self.def_col_palette[idx])
                the_h.SetMarkerColor(self.def_col_palette[idx])
                the_h.SetLineWidth(2)
                the_h.SetMarkerStyle(8)
                the_h.SetMarkerSize(0.5)
                
                draw_style = 'hist'
                leg_style = 'l'
                if 'styles' in vals:
                    draw_style = vals['styles'][el]
                    if draw_style == 'line': draw_style = 'hist'
                    if draw_style == 'dots': draw_style = 'pe'
                the_h.Draw('%s same' % draw_style)

                leg_name = vals['leg'][el] if 'leg' in vals and el in vals['leg'] else el
                leg.AddEntry(the_h, leg_name, leg_style)
            leg.Draw()
            plotname = self.plot_name_proto.format(hname=ovr)
            
            c1statechange = False
            if 'logy' in vals:
                self.c1.SetLogy(vals['logy'])    
                c1statechange = True

            ## reset the canvas defaults
            if c1statechange:
                self.c1.SetLogy(False)

            if 'compare' in vals: ## make the ratio/diff plots
                self.c1.cd()
                self.pad2.Draw()
                self.pad2.cd()
                # if not self.pad2drawn:
                #     self.pad2.Draw()
                #     self.pad2drawn = True
                #     self.pad2.cd()

                bottom_frame = frame.Clone('bottom_' + ovr)
                self.set_axis_style(bottom_frame, removeXaxis=False)
                # bottom_frame.SetDirectory(0)
                self.bottom_frames[ovr] = bottom_frame
                self.bottom_diffs[ovr] = []
                if vals['compare'] == 'ratio':
                    bottom_frame.GetYaxis().SetTitle('Ratio')
                    bottom_frame.SetMinimum(0)
                    bottom_frame.SetMaximum(3)
                elif vals['compare'] == 'diff':
                    bottom_frame.GetYaxis().SetTitle('Difference')
                    bottom_frame.SetMinimum(-10)
                    bottom_frame.SetMaximum(10)
                elif vals['compare'] == 'norm':
                    bottom_frame.GetYaxis().SetTitle('#DeltaN/N')
                    bottom_frame.SetMinimum(-2)
                    bottom_frame.SetMaximum(2)
        
                bottom_frame.Draw()
                target = vals['target']
                h_target = self.histos[target]
                # print h_target.histo.GetName(), h_target.histo.GetEntries(), h_target.histo.GetNbinsX(), h_target.histo.GetBinLowEdge(1), h_target.histo.GetBinLowEdge( h_target.histo.GetNbinsX()+1)
                for idx, el in enumerate(vals['parts']):
                    if el == target: continue
                    
                    h_new  = self.histos[el].histo.Clone('bpanel_' + h_target.histo.GetName())
                    h_diff = self.histos[el].histo.Clone('hdiff_' + h_target.histo.GetName()) ## used to check differences
                    if vals['compare'] == 'ratio':
                        h_new.Divide(h_target.histo)
                    elif vals['compare'] == 'diff':
                        h_new.Add(h_target.histo, -1)
                    elif vals['compare'] == 'norm':
                        h_new.Add(h_target.histo, -1)
                        h_new.Divide(h_target.histo)
                    else:
                        raise RuntimeError ('cannot recognize compare option',vals['compare'] )
                    h_diff.Add(h_target.histo, -1)
                    self.bottom_diffs[ovr].append(h_diff)

                    draw_style = 'hist'
                    if 'styles' in vals:
                        draw_style = vals['styles'][el]
                        if draw_style == 'line': draw_style = 'hist'
                        if draw_style == 'dots': draw_style = 'pe'
                    h_new.Draw('%s same' % draw_style)
                    # print the_h.GetName(), the_h.GetEntries(), the_h.GetNbinsX(), the_h.GetBinLowEdge(1), the_h.GetBinLowEdge( the_h.GetNbinsX()+1)
 
            if do_pdf: self.c1.Print(plotname, 'pdf')
            if do_png: self.c1.Print(plotname.replace('.pdf', '.png'), 'png')

    def merge(self, other):
        for hname in other.histos:
            if hname in self.histos:
                print ' ** plotMaker : merge error : histo', hname, 'is in both, skipping'
                continue
            self.histos[hname] = other.histos[hname]

        if hasattr(other, 'overlays'):
            if not hasattr(self, 'overlays'):
                self.overlays = copy.deepcopy(other.overlays)
            else:
                for ovrl in other.overlays:
                    if ovrl in self.overlays:
                        print ' ** plotMaker : merge error : overlay', ovrl, 'is in both, skipping'
                        continue
                    self.overlays[ovrl] = copy.deepcopy(other.overlays[ovrl])