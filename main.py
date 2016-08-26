#!/usr/bin/env python

from firstcalc import FirstCalc

from Common import *

class ApplicationMain(HasTraits):

    #scene = Instance(MlabSceneModel, ())

    firstcalc         = Instance(FirstCalc)
    display_plot      = Instance(Figure)
    display_isochrone = Instance(Figure)
    display_star = Instance(Figure)
    

    left_panel  = Tabbed(Group(Item('display_plot', editor=MPLFigureEditor(),
    					       show_label=False, resizable=True),scrollable=True,label='Plot'),
                         Group(Item('display_isochrone', editor=MPLFigureEditor(),
    					       show_label=False, resizable=True),scrollable=True,label='Isochrone'),
                         Group(Item('display_star', editor=MPLFigureEditor(),
    					       show_label=False, resizable=True),scrollable=True,label='Star'))
                               
    right_panel = Tabbed(Item('firstcalc', style='custom', label='PLotting',show_label=False))
                         #Item('secondcalc', style='custom', label='Table view',show_label=False))

    view = View(HSplit(left_panel,
                 right_panel),
                width = 1280,
                height = 750,
                resizable = True,
                title="JINAbase GUI"
            )

    def _display_plot_default(self):
        """Initialises the display."""
        figure = Figure(figsize=(8,4))
        #ax = figure.add_subplot(111)
        ax = figure.add_axes([0.15, 0.1, 0.6, 0.8])
        #ax = figure.axes[0]
        #ax.set_xlabel('Z')
        #ax.set_ylabel('[X/Fe]')
        #ax.set_xlim(0,1)
        #ax.set_ylim(0,1)

        # Set matplotlib canvas colour to be white
        rect = figure.patch
        rect.set_facecolor('w')
        return figure

    def _display_isochrone_default(self):
        """Initialises the display."""
        figure = Figure(figsize=(8,4))
        #ax = figure.add_subplot(111)
        ax = figure.add_axes([0.15, 0.1, 0.6, 0.8])
        #ax = figure.axes[0]
        #ax.set_xlabel('Z')
        #ax.set_ylabel('[X/Fe]')
        #ax.set_xlim(0,1)
        #ax.set_ylim(0,1)

        # Set matplotlib canvas colour to be white
        rect = figure.patch
        rect.set_facecolor('w')
        return figure

    def _display_star_default(self):
        """Initialises the display."""
        figure = Figure(figsize=(10,5))
        #ax = figure.add_subplot(111)
        ax = figure.add_axes([0.15, 0.1, 0.6, 0.8])
        #ax = figure.axes[0]
        #ax.set_xlabel('Z')
        #ax.set_ylabel('[X/Fe]')
        #ax.set_xlim(0,1)
        #ax.set_ylim(0,1)

        # Set matplotlib canvas colour to be white
        rect = figure.patch
        rect.set_facecolor('w')
        return figure

    def _firstcalc_default(self):
        # Initialize halos the way we want to.
        # Pass a reference of main (e.g. self) downwards
        return FirstCalc(self)
        

if __name__ == '__main__':
    app = ApplicationMain()
    app.configure_traits()

