## JINAbase

A basic GUI to plot the abundances of EMP stars as part of JINA's EMP stars database project.
The GUI gives you several options to view the data.

## Paper and instructions
Please read the paper (to come) or cookbook for useful instructions and information. If you find this database and/or GUI useful for your plots and/ or work, please cite the paper.
There might be some bugs with the database or the GUI, feel free to send suggestions or add issues you encounter.
This is a community project, help us improve it and keep it up to date. If you think the GUI could be better, help us improve it.

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

- The X-axis and Y-axis limits enable you to select a specific range of values.

- The PLot button is available once the references, location, science key ,c-key and type are selected.

- The Reference tab gives you the option to choose which references to include in the sample.

- The value beside the Show upper limits tick box is to set the length of the upper limmits arrow.

- The marker size is to select the size of the scatter points.

- When plotting the isochrones, only the stars shown in the plot tab are used.
To plot all available stars for a sample, use Fe for the x and y axes.

- For the user defined criteria, to include all values leave the upper and lower limits unchanged.

## How to use the query tab

- This tab enables you to retrieve the information for a list of stars from the database.

- The list including the star names and references must be in this form "star_name_nospaces reference", one entry per line without qoutes.

- To retrive all information for a star, include only the stars name once with no reference.

