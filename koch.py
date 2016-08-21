#!$HOME/anaconda/bin/python
# -*- coding: utf-8 -*-
'''
Ripped from template.py 
- makes a "zenagon"
'''

import inkex       # Required
import simplestyle # will be needed here for styles support
import os          # here for alternative debug method only - so not usually required.
import random


__version__ = '0.1'

inkex.localize()



### Your helper functions go here


def cplxs2pts(zs):
    tt = []
    for z in zs:
        tt.extend([z.real,z.imag])
    return tt


from math import sqrt



def cplx2pt(z):
    return (z.real,z.imag)


class KochCurve(object):

    def __init__(self,curve):
        #make a copy of the list
        self.curve = curve[:]
    
    def mapto(self, edge):
        a,b = edge
        tx = a - self.curve[0]
        sx = (b - a)/ (self.curve[-1] - self.curve[0])
    
        return [sx*w + tx for w in self.curve]


def child(edge):

    
    a,b = edge
    tx = a - z0
    sx = (b - a)/ (z1 - z0)
    
    return [sx*w + tx for w in side]

def mk_pts(scale=500,depth = 2,full=False,pk_scale=1.):
    
    z0, z1 = 0 + 0J, 1 + 0J
    t = 1./3
    curve = z0, (1-t)*z0 + t*z1, .5*(z1 + z0) + pk_scale*(sqrt(3) + 1)/8.*abs(z0- z1)*1J, (1-t)*z1 + t*z0, z1
    
    model = KochCurve(curve)
    pts = curve
    
    for k in range(depth):
        npts = []
        for edge in zip(pts, pts[1:]):
            npts.extend(model.mapto(edge))
        pts = npts
        
    if full:
        ww = .5*(sqrt(3) + 1J)
        cc = (z1 - z0)/ww/sqrt(3) + z0
        ww = ww**4
        npts  = pts[:]
        for k in range(2):
            npts.extend( [(z-cc)/ww + cc for z in pts])
            ww *= ww
        pts = npts
            
    
    npts =[cplx2pt( scale*z ) for z in pts ] 
    
    mv = 'M '
    pth = [ '%.2f, %.2f '%z for z in npts]
    return mv + ''.join(pth)




class Myextension(inkex.Effect): # choose a better name
    
    def __init__(self):
        " define how the options are mapped from the inx file "
        inkex.Effect.__init__(self) # initialize the super class
        
        # Two ways to get debug info:
        # OR just use inkex.debug(string) instead...
        try:
            self.tty = open("/dev/tty", 'w')
        except:
            self.tty = open(os.devnull, 'w')  # '/dev/null' for POSIX, 'nul' for Windows.
            # print >>self.tty, "gears-dev " + __version__
            
        # list of parameters defined in the .inx file
        self.OptionParser.add_option("-t", "--num_lines",
                                     action="store", type="int",
                                     dest="depth", default=3,
                                     help="command line help")
        
        self.OptionParser.add_option("", "--shrink_ratio",
                                     action="store", type="float",
                                     dest="pk_scale", default=3,
                                     help="command line help")

    
        
        #self.OptionParser.add_option("-r", "--mk_filled",
        #                             action="store", type="inkbool", 
        #                             dest="mk_filled", default=False,
        #                             help="command line help")
        #
                
        self.OptionParser.add_option("", "--mk_full",
                                     action="store", type="inkbool", 
                                     dest="mk_full", default=False,
                                     help="command line help")


        # here so we can have tabs - but we do not use it directly - else error
        self.OptionParser.add_option("", "--active-tab",
                                     action="store", type="string",
                                     dest="active_tab", default='title', # use a legitmate default
                                     help="Active tab.")
        
 
           
    def calc_unit_factor(self):
        """ return the scale factor for all dimension conversions.
            - The document units are always irrelevant as
              everything in inkscape is expected to be in 90dpi pixel units
        """
        # namedView = self.document.getroot().find(inkex.addNS('namedview', 'sodipodi'))
        # doc_units = self.getUnittouu(str(1.0) + namedView.get(inkex.addNS('document-units', 'inkscape')))
        unit_factor = self.getUnittouu(str(1.0) + self.options.units)
        return unit_factor


### -------------------------------------------------------------------
### Main function and is called when the extension is run.

    
    def effect(self):

        #set up path styles
        path_stroke = '#DD0000' # take color from tab3
        path_fill   = 'none'     # no fill - just a line
        path_stroke_width  = 1. # can also be in form '0.6mm'
        page_id = self.options.active_tab # sometimes wrong the very first time
        
  
        styles = [ { 'stroke':  path_stroke , 'fill': 'none', 'stroke-width': path_stroke_width },
                   { 'stroke': 'none',  'fill': '#FFFF00', 'stroke-width': 0 }]
        
        styles = [simplestyle.formatStyle(x) for x in styles]

        

        # This finds center of current view in inkscape
        t = 'translate(%s,%s)' % (self.view_center[0], self.view_center[1] )
        
        # Make a nice useful name
        g_attribs = { inkex.addNS('label','inkscape'): 'koch' ,
                      inkex.addNS('transform-center-x','inkscape'): str(0),
                      inkex.addNS('transform-center-y','inkscape'): str(0),
                      'transform': t,
                      'style' : styles[1],
                      'info':'N: '+str(self.options.depth) }
        # add the group to the document's current layer
        topgroup = inkex.etree.SubElement(self.current_layer, 'g', g_attribs )

        

        payload =  mk_pts(depth=self.options.depth,
                          full = self.options.mk_full,
                          pk_scale = self.options.pk_scale)
        curve_attribs = { 'style': styles[0],
                                  'd': payload}
        
        inkex.etree.SubElement(topgroup,
                                    inkex.addNS('path','svg'),
                                    curve_attribs )




if __name__ == '__main__':
    e = Myextension()
    e.affect()


