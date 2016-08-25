from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'wx'

from matplotlib.pyplot import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx

from traits.api import *
from traitsui.api import View, Item, Group, Heading, Label, \
                         HSplit, CheckListEditor, EnumEditor, \
                         ListEditor, Tabbed, VGroup, HGroup
from traits.api import Array, Any, Instance
from traitsui.wx.editor import Editor
from traitsui.wx.basic_editor_factory import BasicEditorFactory
from matplotlib import *
from traitsui.file_dialog import open_file

import numpy as np
import pandas as pd
import itertools
import os
import sys
import wx
import platform
import socket
import random
import subprocess


#import modules.readsnapshots.readsnapHDF5 as rsHD
#import modules.readsnapshots.readsnap as rs
#import modules.readsnapshots.readids as readids
#import modules.readhalos.readsubf as readsubf
#import modules.readhalos.RSDataReaderv2 as RSDataReader
#from modules.brendanlib.grifflib import *

from random import randint


class _MPLFigureEditor(Editor):

    scrollable  = True

    def init(self, parent):
        self.control = self._create_canvas(parent)
        self.set_tooltip()

    def update_editor(self):
        pass

    def _create_canvas(self, parent):
        """ Create the MPL canvas. """
        # The panel lets us add additional controls.
        
        panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        
        # matplotlib commands to create a canvas
        mpl_control = FigureCanvas(panel, -1, self.value)
        sizer.Add(mpl_control, 1, wx.LEFT | wx.TOP | wx.GROW)
        toolbar = NavigationToolbar2Wx(mpl_control)
        sizer.Add(toolbar, 0, wx.EXPAND)
        self.value.canvas.SetMinSize((10,10))
        
        return panel

class MPLFigureEditor(BasicEditorFactory):

    klass = _MPLFigureEditor
    x = Float(10.0)
    
def readfile(filename):
    #to read in the text files as pandas dataframes
    df = pd.read_csv(filename, header=0, delim_whitespace=True, index_col= 0)
    return df
	
def readtxt(filename):
    # to read in text files
    with open(filename,'r') as f:
        l = f.readlines()
        l = [x.strip() for x in l]
        l = [x.split(' ') for x in l]
        l = [[x for x in y if x !='']for y in l]        	
	return l

all_data = readfile('files/all_info.txt') #the main dataframe
abund_limits = readfile('files/limits_key.txt') #dataframe with upper limits keys

separator = all_data.values[0].tolist() #save the header separator line for writing output
all_data = all_data.drop(all_data.index[0]) #drop out the header separator line
abund_limits = abund_limits.drop(abund_limits.index[0]) #drop out the header separator line

references = readtxt('files/ref.txt') #list of references with abrevations

def read_params(list_name):
    #to get list with Teff and Logg from a list for isochrones
    lines = list_name
    stars = []
    for line in lines:
        stars.append({'name' : line[3],
                      'teff' : float(line[19]),
                      'logg' : float(line[20]),
                      'z'    : float(line[21]),
                      'ref' : line[1]})

    return stars

def readbib(filename):
    #read in bibtex file
    full, l =[], []
    with open(filename,'r') as f:
        for line in f:
            if line !='\n':
                l.append(line)
            else:
                if l !=[]:
                    full.append(l)
                l =[]
    return full

def write(data,filename):
    #write out aligned columns
    if len(data[0]) == len(separator):
        data.insert(1,separator)
    else:
        sep = separator
        del sep[7:19]
        data.insert(1,sep)
    cols = zip(*data)
    # Compute column widths by taking maximum length of values per column
    col_widths = [ max(len(value) for value in col) for col in cols ]
    # Create a suitable format string
    fmt = ' '.join(['{{:<{}}}'.format(width) for width in col_widths])

    # Print each row using the computed format
    with open(filename,'w') as f:
        for row in data:
            print>>f, fmt.format(*tuple(row))

