## JINAbase

A basic GUI to plot the abundances of EMP stars as part of JINA's EMP stars database project.
The GUI gives you several options to view the data.

## Requirements

To get the GUI to work on your device you'll need the following python packages,
It's recommended to have anaconda installed, in that case use 'conda install package'.

    wxpython
    traits
    pandas

The following package needs to be installed as follow for the latest version available,

    pip install traitsui

## Running the GUI

In a terminal cd into the directory of the GUI, then run:
`python main.py` 

If this gives an error on Mac os, something about main display permission,
try the following:
`ipython` then `run main.py` 

## Information for using the GUI

- IMPORTANT:: Only use 'Show Legend when 'MW Halo' stars not in the main selection,
or have less than 20 references chosen to plot.

- The PLot button is available once the references, location, science key and type are selected.

- The Reference tab gives you the option to choose which references to plot.

- The X-axis and Y-axis limits enable you to select a specific range of values, they can be specified at any time.

- The value beside the Show upper limits tick box is the length of the upper limmits arrow.

- The marker size is to select the size of the scatter points.

- When plotting the isochrones, only the stars shown in the plot tab are used.
To plot all available stars for a sample, use Fe for the x and y axes.

- For the user defined criteria, to include all values leave the upper and lower limits empty.

## How to use the query tab

- This tab enables you to retrieve the information for a list of stars from the database.

- The list including the star names and references must be in this form "star_name_nospaces reference", one entry per line without qoutes.

- To retrive all information for a star, include only the stars name once with no reference.

