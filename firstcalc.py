from Common import *

#list of tuples with references and 3-letter+year abrevation
ref= list(map(tuple,[line[1:] for line in references[2:]]))

# list of elements from all_data defined in common.py
elements = list(all_data.columns.values[24:])

#metallicity list used for relative abundance calculation
Z = [str(item) for item in all_data['Fe'].values.tolist()]

#lists with location,science key nad type options
loc = [('*', 'MW Halo'), ('BU', 'Bulge'), ('DW', 'Classical Dwarfs'), ('UF','Ultra-faint Dwarfs')]
sci = [('R1','r-I rich'), ('R2','r-II rich'), ('S','s-rich'),\
       ('RS','r/s stars'), ('*', 'Unclasified')]
crich = [ ('CR','CEMP'), ('NO','CEMP-no'), ('*', 'Unclasified')]
types = [('RG', 'Giants'), ('SG', 'Subgiants'), ('MS', 'Dwarfs'), ('HB', 'Horizontal branch')]

class FirstCalc(HasTraits):

    # Add Traits objects
    xoptions       = Enum('Fe', elements) #x-axis X option for [X/Y] realtive abundance
    yoptions       = Enum('Ba', elements) #y-axis X option for [X/Y] realtive abundance
    zxoptions      = Enum('Fe', elements) #x-axis Y option for [X/Y] realtive abundance
    zyoptions      = Enum('Fe', elements) #y-axis Y option for [X/Y] realtive abundance
    xuplim         = Float() #upper limit for x-axis values
    xlolim         = Float() #upper limit for y-axis values
    yuplim         = Float() #lower limit for x-axis values
    ylolim         = Float() #lower limit for y-axis values
    xreset_button  = Button('Reset axis values') #button to reset x-axis limits
    yreset_button  = Button('Reset axis values') #button to reset y-axis limits
    sample_xup     = Bool(False) #boolen to get x-axis upper limit from data
    sample_xlo     = Bool(False) #boolen to get y-axis upper limit from data
    sample_yup     = Bool(False) #boolen to get x-axis lower limit from data
    sample_ylo     = Bool(False) #boolen to get y-axis lower limit from data
    loc_list       = List(editor=CheckListEditor(values=loc, cols=4),value=['*']) #locations
    sci_list       = List(editor=CheckListEditor(values=sci, cols=5)) #science keys
    crich_list     = List(editor=CheckListEditor(values=crich, cols=3)) #cemp keys
    loc_sel_all    = Button('All') #button to select all locations
    sci_sel_all    = Button('All') #button to select all science keys
    crich_sel_all  = Button('All') #button to select all cemp keys

    
    normoptions    = Enum('Asplund09', ('Asplund09', 'Asplund05', 'Grevesse&Sauval98', 'Anders&Grevesse89')) #solar normalization options
    norm_button    = Button('Normalize Abundances') #normalization button, activated with the plot button
    plot_button    = Button('Plot Abundances!') #button to plot data
    isochrone      = Button('Plot data on isochrones') #button to plot data with isochrones
    xhorfe         = Enum('[X/H]', ('[X/H]','[X/Fe]','[X/Y]', 'No')) #x-axis relative abundance options
    yhorfe         = Enum('[X/Fe]', ('[X/H]','[X/Fe]','[X/Y]', 'No')) #y-axis relative abundance options
    xlimits        = Bool(False) #boolen to show upper or lower limits for x-axis data
    ylimits        = Bool(False) #boolen to show upper or lower limits for y-axis data
    star_type      = List(editor=CheckListEditor(values=types, cols=4)) #types of stars
    star_type_sel_all    = Button('All') #button to select all types

    ref_sel_all    = Button('Select all') #button to select all references
    ref_desel_all  = Button('Deselect all') #button to deselect all references
    ref_list       = List(editor=CheckListEditor(values=ref, cols=3), value=[item[0] for item in ref]) #list with all references
    ref            = Bool(False) #boolen to only available references in references tab
    x              = List #x-axis data
    y              = List #y-axis data
    zx             = List #x-axis relative abundance denominator data
    zy             = List #y-axis relative abundance denominator data
    errx           = Float(0.3) #length of x-axis upper or lower limit arrow
    erry           = Float(0.15) ##length of y-axis upper or lower limit arrow
    var_ref        = List #list with references for data selected
    background     = Bool(False) #boolen to show halo stars behind small samples
    legend         = Bool(False) #boolen to show legend
    num_stars      = Bool(True) #boolen to show number of stars
    num_limits     = Bool(False) #boolen to show number of upper limits
    xback          = List #x-axis data for halo stars in background
    yback          = List #y-axis data for halo stars in background
    markersize     = Range(0,100,30) #size of markers

    file_name        = File #filename for query tab
    openbutton       = Button('Open...') #button to open folder tree to read in user's list
    retrieve_button  = Button('Retrieve data for selected list') #button to retrieve data for user's list
    not_found        = List() #list with unrecognized entries from user's list
    output_list      = List(List) #list with all information for plotted data
    save_button      = Button('Save output file') #button to save a list with plotted data 
    criteria_element = Enum('C', elements) #user defined criteria
    criteria_Y       = Enum('Fe', elements) #normalization option for [X/Y] realtive abundance
    criteria_norm    = Enum('[X/Fe]', ('[X/H]','[X/Fe]','[X/Y]', 'Log(e)')) #x-axis relative abundance options
    criteria_bool    = Bool(False) # boolen to enable user criteria
    criteria_upper   = Float(5) #upper limit for criteria
    criteria_lower   = Float(0.7) #lower limit for criteria
    criteria         = List #list to save criteria values
    criteria_up_bool = Bool(True) #boolen to reset upper limit
    criteria_lo_bool = Bool(True) #boolen to reset lower limit
    criteria_abund   = List()
    xabund           = List()
    yabund           = List()
    completeness_bool = Bool(False)
    priority          = Bool(False)

    star_name        = Str()
    star_plot        = Button('Plot abundances for star')
    star_horfe       = Enum('[X/H]', ('[X/H]','[X/Fe]', 'Log(e)'))


    #Construct the view
    pan0 = Group(HGroup(Item(name='xlolim', label='From',style='simple'),
    					Item(name='xuplim', label='To', style='simple'),
    					'10',Item(name='xreset_button', show_label=False), label='X-axis'),
                 HGroup(Item(name='ylolim', label='From',style='simple'),
                        Item(name='yuplim', label='To', style='simple'),
                        '10',Item(name='yreset_button', show_label=False), label= 'Y-axis'),
                 '1','_',
                 Group(HGroup(Group(Item(name='loc_list',style='custom',label='Location'),springy=True),
                              VGroup(Item(name='loc_sel_all',show_label=False),)),
             		   '1','_',
             		   HGroup(Group(Item(name='star_type',style='custom',label='Type'),springy=True),
                 		      VGroup(Item(name='star_type_sel_all',show_label=False),)),
                 	   '1','_',
                       VGroup(HGroup(Item(name='sci_list',style='custom',show_label=False),
                 	                 Item(name='sci_sel_all',show_label=False),label='n-capture keys'),
                              HGroup(Item('crich_list', style='custom',show_label=False),
                                     Item('crich_sel_all', show_label=False),label='c-rich keys'),label='Science keys',show_border=True)
                       ), show_border=True, label='Sample selection',padding=5)
    
    pan1 = VGroup(HGroup(Item(name='num_stars',label='No. of stars'),
                  Item(name='num_limits',label='No. of limits'),
                  Item(name='legend',label='Show Legend'),
			      Item(name='background',label='Halo stars in background', enabled_when='legend'),
                  Item(name='completeness_bool',label='Completeness limit')),
                  Item('priority', label='Multiple entries'),
			      label='Options to show on the plot',show_border=True)
                     
    pan2 = Group(HGroup(Item(name='xoptions',label='X-axis'),
                        Item(name='xhorfe', label='select relative abundance'),
                        Item(name='zxoptions',show_label=False,enabled_when="xhorfe == '[X/Y]'"),
                        Item(name='xlimits',label= 'Show upper limits data'),
                        Item(name='errx', show_label=False,enabled_when='xlimits == True'),springy=True),
                  HGroup(Item(name='yoptions',label='Y-axis'),
                        Item(name='yhorfe', label='select relative abundance'),
                        Item(name='zyoptions',show_label=False,enabled_when="yhorfe == '[X/Y]'"),
                        Item(name='ylimits',label= 'Show upper limits data'),
                        Item(name='erry', show_label=False,enabled_when='ylimits == True'),springy=True),
                  HGroup(Item('criteria_bool',show_label=False),
                         HGroup(Item('criteria_element',label='Element'),
                                Item('criteria_norm',label='Noramlization'),
                                Item('criteria_Y',show_label= False, enabled_when="criteria_norm == '[X/Y]'"),
                                Item('criteria_lower',label='From'),
                                Item('criteria_upper',label='To'),enabled_when='criteria_bool'),
                                label='User criteria',show_border=True),
                  Item(name='markersize',label='Marker Size',springy=True),
                  HGroup(Item(name='normoptions',label='Solar Normalization'),
                         Item(name='plot_button',show_label=False,springy=True,
                              enabled_when='loc_list != [] and sci_list !=[] and star_type != [] and ref_list != []')),
                  HGroup(Item('save_button',show_label=False,enabled_when='x != []',springy=True),
                         Item('isochrone',show_label=False,enabled_when='x != []',springy=True)),
                         show_border=True, label = 'Plot Options',padding=10)
     
                       
    tab1 = Group(pan0, '1', pan1, '1', pan2, '1', label='Sample selection')
                        
    tab2 = Group(HGroup(Item(name='ref_sel_all', show_label=False),
    					Item(name='ref_desel_all', show_label=False)),
			Group(Item(name='ref_list', style='custom', show_label= False),scrollable=True),label='References',padding=5)

    tab3 = Group(HGroup(Item('file_name',style='readonly', springy=True),
                        Item('openbutton',show_label=False,springy=True)),
                 '_',
                 Group(Item('not_found', label='Entries not found or recognized', style='readonly'),scrollable=True),
                 Group(Item('retrieve_button',show_label=False)),label='Query')

    tab4 = Group(Item('star_name',label="Enter star's name"),
                 Item('star_horfe',label='Relative abundance to plot'),
                 Item('star_plot',show_label=False),label="Star's statistics")
                        
                        
    view = View(tab1, tab2, tab3, tab4)
    

    def _normoptions_changed(self):
        self.norm_button = True
    
    def _xuplim_changed(self):
        self.sample_xup = True
        
    def _xlolim_changed(self):
        self.sample_xlo = True
        
    def _yuplim_changed(self):
        self.sample_yup = True
        
    def _ylolim_changed(self):
        self.sample_ylo = True
    
    def _xreset_button_fired(self):
        #reset x-axis limits if reset button pressed
        self.sample_xup = False
        self.sample_xlo = False
        self.xuplim = max(float(val) for val in self.x if val !='*')
        self.xlolim = min(float(val) for val in self.x if val !='*')
    
    def _yreset_button_fired(self):
        #reset y-axis limits if reset button pressed
        self.sample_yup = False
        self.sample_ylo = False
        self.yuplim = max(float(val) for val in self.y if val !='*')
        self.ylolim = min(float(val) for val in self.y if val !='*')
        
    	
    def _xoptions_changed(self):
        #reset x-axis limits if element plotted changed
        self.sample_xup = False
        self.sample_xlo = False
        self.sample_yup = False
        self.sample_ylo = False
        self.ref = True
        

    def _yoptions_changed(self):
        #reset y-axis limits if element plotted changed
        self.sample_xup = False
        self.sample_xlo = False
        self.sample_yup = False
        self.sample_ylo = False
        self.ref = True

    def _xhorfe_changed(self):
        self.sample_xup = False
        self.sample_xlo = False

    def _yhorfe_changed(self):
        self.sample_yup = False
        self.sample_ylo = False
        
    def _loc_sel_all_fired(self):
        self.loc_list = [item[0] for item in loc]
        
    def _sci_sel_all_fired(self):
        self.sci_list = [item[0] for item in sci]
    	
    def _crich_sel_all_fired(self):
        self.crich_list = [item[0] for item in crich]
    
    def _star_type_sel_all_fired(self):
        self.star_type = [item[0] for item in types]
    	        
    def _loc_list_changed(self):
        self.sample_xup = False
        self.sample_xlo = False
        self.sample_yup = False
        self.sample_ylo = False
        self.ref = True

    def _sci_list_changed(self):
        self.sample_xup = False
        self.sample_xlo = False
        self.sample_yup = False
        self.sample_ylo = False
        self.ref = True

    def _star_type_changed(self):
        self.sample_xup = False
        self.sample_xlo = False
        self.sample_yup = False
        self.sample_ylo = False
        self.ref = True

    def _crich_list_changed(self):
        self.sample_xup = False
        self.sample_xlo = False
        self.sample_yup = False
        self.sample_ylo = False
        self.ref = True
    	
    def _ref_sel_all_fired(self):
        self.ref_list = [item[0] for item in ref]
        
    def _ref_desel_all_fired(self):
        self.ref_list = []

    def _ref_list_changed(self):
        self.ref = False

    def _criteria_upper_changed(self):
        self.criteria_up_bool = True
        
    def _criteria_lower_changed(self):
        self.criteria_lo_bool = True

    def _criteria_element_changed(self):
        self.criteria_up_bool = False
        self.criteria_lo_bool = False
        
    def _norm_button_fired(self):
        if self.priority:
            priority_key = ['1','2']
        else:
            priority_key = ['1']

        if self.ref:
            #select all references when some options are changed
            self.ref_list = [item[0] for item in ref]
        self.x = [str(item) for item in all_data[self.xoptions].values.tolist()]
        self.y = [str(item) for item in all_data[self.yoptions].values.tolist()]
        self.zx = [str(item) for item in all_data[self.zxoptions].values.tolist()] #list for x-axis element Y in [X/Y]
        self.zy = [str(item) for item in all_data[self.zyoptions].values.tolist()] #list for y-axis element Y in [X/Y]
        solar = readfile('files/'+self.normoptions+'.txt') #read in solar abundances
        self.var_ref, self.xback, self.yback = [], [], []

        for m in range(len(self.x)):
            if self.xhorfe == '[X/H]':
                if (self.x[m] != '*') and self.background and (all_data['key'].values[m] in priority_key):
                    self.xback.append(round(float(self.x[m]) - float(solar[self.xoptions].values[-1]),2))
                elif (self.x[m] == '*') and self.background and (all_data['key'].values[m] in priority_key):
                    self.xback.append('*')

                if (self.x[m] != '*') and (all_data['key'].values[m] in priority_key):
                    self.x[m] = round(float(self.x[m]) - float(solar[self.xoptions].values[-1]),2)
                else:
                    self.x[m] = '*'

            elif self.xhorfe == '[X/Fe]':
                if (self.x[m] != '*') and self.background and (all_data['key'].values[m] in priority_key):
                    self.xback.append(round(float(self.x[m]) - float(solar[self.xoptions].values[-1])\
                       					 - (float(Z[m]) - float(solar['Fe'].values[-1])),2))
                elif (self.x[m] == '*'):# and self.background and (all_data['key'].values[m] in priority_key):
                    self.xback.append('*')

                if (self.x[m] != '*') and (all_data['key'].values[m] in priority_key):
                    self.x[m] = round(float(self.x[m]) - float(solar[self.xoptions].values[-1])\
                           					 - (float(Z[m]) - float(solar['Fe'].values[-1])),2)
                else:
                    self.x[m] = '*'

            elif self.xhorfe == '[X/Y]':
                if (self.x[m] != '*') and (self.zx[m] != '*') and self.background and (all_data['key'].values[m] in priority_key):
                    self.xback.append(round((float(self.x[m]) - float(solar[self.xoptions].values[-1]) -\
                                             float(self.zx[m]) + float(solar[self.zxoptions].values[-1])),2))
                elif ((self.x[m] == '*') or (self.zx[m] == '*')) and self.background and (all_data['key'].values[m] in priority_key):
                    self.xback.append('*')

                if (self.x[m] != '*') and (self.zx[m] != '*') and (all_data['key'].values[m] in priority_key):
                    self.x[m] = round((float(self.x[m]) - float(solar[self.xoptions].values[-1]) -\
                                       float(self.zx[m]) + float(solar[self.zxoptions].values[-1])),2)
                else:
                    self.x[m] = '*'

            else:
                if (self.x[m] != '*') and self.background and (all_data['key'].values[m] in priority_key):
                    self.xback.append(round((float(self.x[m])),2))
                elif (self.x[m] == '*') and self.background and (all_data['key'].values[m] in priority_key):
                    self.xback.append('*')

                if (self.x[m] != '*') and (all_data['key'].values[m] in priority_key):
                    self.x[m] = round(float(self.x[m]),2)
                else:
                    self.x[m] = '*'

        for m in range(len(self.y)):
            if self.yhorfe == '[X/H]':
                if (self.y[m] != '*') and self.background and (all_data['key'].values[m] in priority_key):
                    self.yback.append(round(float(self.y[m]) - float(solar[self.yoptions].values[-1]),2))
                elif (self.y[m] == '*') and self.background and (all_data['key'].values[m] in priority_key):
                    self.yback.append('*')

                if (self.y[m] != '*') and (all_data['key'].values[m] in priority_key):
                    self.y[m] = round(float(self.y[m]) - float(solar[self.yoptions].values[-1]),2)
                else:
                    self.y[m] = '*'

            elif self.yhorfe == '[X/Fe]':
                if (self.y[m] != '*') and self.background and (all_data['key'].values[m] in priority_key):
                    self.yback.append(round(float(self.y[m]) - float(solar[self.yoptions].values[-1])\
                       					 - (float(Z[m]) - float(solar['Fe'].values[-1])),2))
                elif (self.y[m] == '*') and self.background and (all_data['key'].values[m] in priority_key):
                    self.yback.append('*')

                if (self.y[m] != '*') and (all_data['key'].values[m] in priority_key):
                    self.y[m] = round(float(self.y[m]) - float(solar[self.yoptions].values[-1]) - (float(Z[m]) - float(solar['Fe'].values[-1])),2)
                else:
                    self.y[m] = '*'

            elif self.yhorfe == '[X/Y]':
                if (self.y[m] != '*') and (self.zy[m] != '*') and self.background and (all_data['key'].values[m] in priority_key):
                    self.yback.append(round((float(self.y[m]) - float(solar[self.yoptions].values[-1]) -\
                                             float(self.zy[m]) + float(solar[self.zyoptions].values[-1])),2))
                elif ((self.y[m] == '*') or (self.zy[m] == '*')) and self.background and (all_data['key'].values[m] in priority_key):
                    self.yback.append('*')

                if (self.y[m] != '*') and (self.zy[m] != '*') and (all_data['key'].values[m] in priority_key):
                    self.y[m] = round((float(self.y[m]) - float(solar[self.yoptions].values[-1]) -\
                                       float(self.zy[m]) + float(solar[self.zyoptions].values[-1])),2)
                else:
                    self.y[m] = '*'

            else:
                if (self.y[m] != '*') and self.background and (all_data['key'].values[m] in priority_key):
                    self.yback.append(round((float(self.y[m])),2))
                elif (self.y[m] == '*') and self.background and (all_data['key'].values[m] in priority_key):
                    self.yback.append('*')

                if (self.y[m] != '*') and (all_data['key'].values[m] in priority_key):
                    self.y[m] = round(float(self.y[m]),2)
                else:
                    self.y[m] = '*'

        for m in range(len(self.x)):
            if (all_data['C_key'].values[m] in self.crich_list) and (all_data['Sci_key'].values[m] in self.sci_list) and \
            (all_data['Reference'].values[m] in self.ref_list) and (all_data['type'].values[m] in self.star_type) \
            and (all_data['Loc'].values[m] in self.loc_list):
                if self.x[m] =='*' or self.y[m] =='*':
                    self.x[m] = '*'
                    self.y[m] = '*'
                else:
                    self.var_ref.append(all_data['Reference'].values[m])
            else:
                self.x[m] = '*'
                self.y[m] = '*'

        if not self.sample_xup:
            self.xuplim = max(float(val) for val in self.x if val !='*')
        if not self.sample_xlo:
            self.xlolim = min(float(val) for val in self.x if val !='*')
            
        if not self.sample_yup:
            self.yuplim = max(float(val) for val in self.y if val !='*')
        if not self.sample_ylo:
            self.ylolim = min(float(val) for val in self.y if val !='*')


        if self.criteria_bool:
            self.criteria = [str(item) for item in all_data[self.criteria_element].values.tolist()]
            criteria_z    = [str(item) for item in all_data[self.criteria_Y].values.tolist()]

            for m in range(len(self.criteria)):
                if self.criteria[m] != '*' and (all_data['Loc'].values[m] in self.loc_list) \
                and (all_data['Reference'].values[m] in self.ref_list) and (all_data['type'].values[m] in self.star_type) \
                and (all_data['C_key'].values[m] in self.crich_list) and (all_data['Sci_key'].values[m] in self.sci_list):
                    if self.criteria_norm == '[X/H]':
                        self.criteria[m] = round(float(self.criteria[m]) - float(solar[self.criteria_element].values[-1]),2)
                        
                    elif self.criteria_norm == '[X/Fe]':
                        self.criteria[m] = round(float(self.criteria[m]) - float(solar[self.criteria_element].values[-1])\
                               					 - (float(Z[m]) - float(solar['Fe'].values[-1])),2)
                    
                    elif self.criteria_norm == '[X/Y]':
                        self.criteria[m] = round((float(self.criteria[m]) - float(solar[self.criteria_element].values[-1]) -\
                                                  float(criteria_z[m]) + float(solar[self.criteria_Y].values[-1])),2)
                        
                    else:
                        self.criteria[m] = round(float(self.criteria[m]),2)
                else:
                    self.criteria[m] = '*'

            if not self.criteria_up_bool:
                self.criteria_upper = max(float(val) for val in self.criteria if val !='*')
            if not self.criteria_lo_bool:
                self.criteria_lower = min(float(val) for val in self.criteria if val !='*')
        
        self.var_ref = list(set(self.var_ref))
        self.var_ref.sort()
        self.ref_list = self.var_ref
        self.ref = False
        

    def _plot_button_fired(self):
        self.norm_button = True
        varx, vary, varx_yup, vary_yup, varx_xup, vary_xup = [], [], [], [], [], []
        varx_ylo, vary_ylo = [], []
        abundances = elements[4:]
        if self.xoptions in abundances:
            upperx = [str(item) for item in abund_limits['ul'+self.xoptions].values.tolist()]
        if self.yoptions in abundances:
            uppery = [str(item) for item in abund_limits['ul'+self.yoptions].values.tolist()]
        self.xabund, self.yabund, self.output_list, self.criteria_abund = [], [], [], []
        figure = self.main.display_plot
        figure.clear()
        ax = figure.add_axes([0.14, 0.1, 0.6, 0.8])
        
        if self.legend:
            col=['r', 'g', 'b', 'orange','y', 'k', 'lightgreen', 'c', 'm', 'crimson', 'fuchsia']*len(self.var_ref)
            shape = ['s', '*', '8', 'd', 'o']*len(self.var_ref)
            c, d = 0, 0
            for m in range(len(self.var_ref)):
                varx, vary, varx_yup, vary_yup, varx_xup, vary_xup = [], [], [], [], [], []
                varx_ylo, vary_ylo, varx_ref = [], [], []
                for i in range(len(self.y)):
                    if self.criteria_bool and self.xoptions in abundances and self.yoptions in abundances:
                        if (self.criteria[i] !='*') and (float(self.criteria[i]) <= self.criteria_upper) and\
                        (float(self.criteria[i]) >= self.criteria_lower):
                            if (self.y[i] != '*') and (self.x[i] != '*') and (all_data['Reference'].values[i] == self.var_ref[m]):
                                if (float(self.x[i]) <= self.xuplim) and (float(self.x[i]) >= self.xlolim) and\
                                (float(self.y[i]) <= self.yuplim) and (float(self.y[i]) >=self.ylolim):
                                    self.output_list.append(all_data.values[i].tolist())
                                    self.xabund.append(self.x[i])
                                    self.yabund.append(self.y[i])
                                    self.criteria_abund.append(self.criteria[i])
                                    if (uppery[i] == '1'):
                                        varx_yup.append(float(self.x[i]))
                                        vary_yup.append(float(self.y[i]))
                                        if self.ylimits:
                                            d+=1
                                    elif (uppery[i] == '-1'):    
                                        varx_ylo.append(float(self.x[i]))
                                        vary_ylo.append(float(self.y[i]))
                                        if self.ylimits:
                                            d+=1
                                    elif (upperx[i] != '1'):
                                        varx.append(float(self.x[i]))
                                        vary.append(float(self.y[i]))
                                        varx_ref.append(self.var_ref[m])
                                        c+=1
                                    if (upperx[i] == '1'):
                                    	varx_xup.append(float(self.x[i]))
                                    	vary_xup.append(float(self.y[i]))
                                    	if self.xlimits and (upperx[i] != uppery[i]):
                                    	    d+=1

                    elif self.xoptions in abundances and self.yoptions in abundances:
                        if (self.y[i] != '*') and (self.x[i] != '*') and (all_data['Reference'].values[i] == self.var_ref[m]):
                            if (float(self.x[i]) <= self.xuplim) and (float(self.x[i]) >= self.xlolim) and\
                            (float(self.y[i]) <= self.yuplim) and (float(self.y[i]) >=self.ylolim):
                                self.output_list.append(all_data.values[i].tolist())
                                self.xabund.append(self.x[i])
                                self.yabund.append(self.y[i])

                                if (uppery[i] == '1'):
                                    varx_yup.append(float(self.x[i]))
                                    vary_yup.append(float(self.y[i]))
                                    if self.ylimits:
                                        d+=1
                                elif (uppery[i] == '-1'):
                                    varx_ylo.append(float(self.x[i]))
                                    vary_ylo.append(float(self.y[i]))
                                    if self.ylimits:
                                        d+=1
                                elif (upperx[i] != '1'):
                                    varx.append(float(self.x[i]))
                                    vary.append(float(self.y[i]))
                                    varx_ref.append(self.var_ref[m])
                                    c+=1
                                if (upperx[i] == '1'):
                                	varx_xup.append(float(self.x[i]))
                                	vary_xup.append(float(self.y[i]))
                                	if self.xlimits and (upperx[i] != uppery[i]):
                                	    d+=1
                    else:
                        if (self.y[i] != '*') and (self.x[i] != '*') and (all_data['Reference'].values[i] == self.var_ref[m]):
                            if (float(self.x[i]) <= self.xuplim) and (float(self.x[i]) >= self.xlolim) and\
                            (float(self.y[i]) <= self.yuplim) and (float(self.y[i]) >=self.ylolim):
                                self.output_list.append(all_data.values[i].tolist())
                                self.xabund.append(self.x[i])
                                self.yabund.append(self.y[i])

                                if (uppery[i] == '1'):
                                    varx_yup.append(float(self.x[i]))
                                    vary_yup.append(float(self.y[i]))
                                    if self.ylimits:
                                        d+=1
                                elif (uppery[i] == '-1'):
                                    varx_ylo.append(float(self.x[i]))
                                    vary_ylo.append(float(self.y[i]))
                                    if self.ylimits:
                                        d+=1
                                else:
                                    varx.append(float(self.x[i]))
                                    vary.append(float(self.y[i]))
                                    varx_ref.append(self.var_ref[m])
                                    c+=1
                                
                        
                if varx !=[] and vary != []:                
                    ax.scatter(varx, vary,marker=shape[m],color=col[m],s=self.markersize, lw=0 ,zorder=-30,label=self.var_ref[m])

                if self.ylimits and varx_yup !=[] and vary_yup != [] and (self.var_ref[m] not in varx_ref):
                    ax.scatter(varx_yup, vary_yup,marker=shape[m],color=col[m],s=self.markersize, lw=0, label=self.var_ref[m])
                    ax.errorbar(varx_yup, vary_yup, color=col[m], yerr=self.erry,\
                        fmt=shape[m], uplims=True, capsize=0,markersize=0, elinewidth=0, mew=0)
                elif self.ylimits and varx_yup !=[] and vary_yup != [] and (self.var_ref[m] in varx_ref):
                    ax.scatter(varx_yup, vary_yup,marker=shape[m],color=col[m],s=self.markersize, lw=0)
                    ax.errorbar(varx_yup, vary_yup, color=col[m], yerr=self.erry,\
                        fmt=shape[m], uplims=True, capsize=0,markersize=0, elinewidth=0, mew=0)

                if self.ylimits and varx_ylo !=[] and vary_ylo != []:
                    ax.scatter(varx_ylo, vary_ylo,marker=shape[m],color=col[m],s=self.markersize, lw=0)#,label=self.var_ref[m])
                    ax.errorbar(varx_ylo, vary_ylo, color=col[m], yerr=self.erry,\
                        fmt=shape[m], lolims=True, capsize=0,markersize=0, elinewidth=0, mew=0)

                if self.xlimits and varx_xup !=[] and vary_xup != []:
                    ax.scatter(varx_xup, vary_xup,marker=shape[m],color=col[m],s=self.markersize, lw=0)#,label=self.var_ref[m])
                    ax.errorbar(varx_xup, vary_xup, color=col[m], xerr=self.errx,\
                        fmt=shape[m], xuplims=True, capsize=0,markersize=0, elinewidth=0, mew=0)
        else:
            varx, vary, varx_yup, vary_yup, varx_xup, vary_xup = [], [], [], [], [], []
            varx_ylo, vary_ylo = [], []
            c, d = 0, 0
            for i in range(len(self.y)):
                if self.criteria_bool and self.xoptions in abundances and self.yoptions in abundances:
                    if (self.criteria[i] !='*') and (float(self.criteria[i]) <= self.criteria_upper) and\
                    (float(self.criteria[i]) >= self.criteria_lower):
                        if (self.y[i] != '*') and (self.x[i] != '*'):
                            if (float(self.x[i]) <= self.xuplim) and (float(self.x[i]) >= self.xlolim)\
                            and (float(self.y[i]) <= self.yuplim) and (float(self.y[i]) >=self.ylolim):
                                self.output_list.append(all_data.values[i].tolist())
                                self.xabund.append(self.x[i])
                                self.yabund.append(self.y[i])
                                self.criteria_abund.append(self.criteria[i])

                                if (uppery[i] == '1'):
                                    varx_yup.append(float(self.x[i]))
                                    vary_yup.append(float(self.y[i]))
                                    if self.ylimits:
                                        d+=1
                                elif (uppery[i] == '-1'):
                                    varx_ylo.append(float(self.x[i]))
                                    vary_ylo.append(float(self.y[i]))
                                    if self.ylimits:
                                        d+=1
                                elif (upperx[i] != '1'):
                                    varx.append(float(self.x[i]))
                                    vary.append(float(self.y[i]))
                                    c+=1
                                if (upperx[i] == '1'):
                                    varx_xup.append(float(self.x[i]))
                                    vary_xup.append(float(self.y[i]))
                                    if self.xlimits and (upperx[i] != uppery[i]):
                                        d+=1

                elif self.xoptions in abundances and self.yoptions in abundances:
                    if (self.y[i] != '*') and (self.x[i] != '*'):
                        if (float(self.x[i]) <= self.xuplim) and (float(self.x[i]) >= self.xlolim)\
                        and (float(self.y[i]) <= self.yuplim) and (float(self.y[i]) >=self.ylolim):
                            self.output_list.append(all_data.values[i].tolist())
                            self.xabund.append(self.x[i])
                            self.yabund.append(self.y[i])

                            if (uppery[i] == '1'):
                                varx_yup.append(float(self.x[i]))
                                vary_yup.append(float(self.y[i]))
                                if self.ylimits:
                                    d+=1
                            elif (uppery[i] == '-1'):
                                varx_ylo.append(float(self.x[i]))
                                vary_ylo.append(float(self.y[i]))
                                if self.ylimits:
                                    d+=1
                            elif (upperx[i] != '1'):
                                varx.append(float(self.x[i]))
                                vary.append(float(self.y[i]))
                                c+=1
                            if (upperx[i] == '1'):
                                varx_xup.append(float(self.x[i]))
                                vary_xup.append(float(self.y[i]))
                                if self.xlimits and (upperx[i] != uppery[i]):
                                    d+=1
                elif self.xoptions in abundances or self.yoptions in abundances:
                    if (self.y[i] != '*') and (self.x[i] != '*'):
                        if (float(self.x[i]) <= self.xuplim) and (float(self.x[i]) >= self.xlolim) and\
                        (float(self.y[i]) <= self.yuplim) and (float(self.y[i]) >=self.ylolim):
                            self.output_list.append(all_data.values[i].tolist())
                            self.xabund.append(self.x[i])
                            self.yabund.append(self.y[i])
                            if (uppery[i] == '1'):
                                varx_yup.append(float(self.x[i]))
                                vary_yup.append(float(self.y[i]))
                                if self.ylimits:
                                    d+=1
                            elif (uppery[i] == '-1'):
                                varx_ylo.append(float(self.x[i]))
                                vary_ylo.append(float(self.y[i]))
                                if self.ylimits:
                                    d+=1
                            else:
                                varx.append(float(self.x[i]))
                                vary.append(float(self.y[i]))
                                c+=1
                else:
                    if (self.y[i] != '*') and (self.x[i] != '*'):
                        if (float(self.x[i]) <= self.xuplim) and (float(self.x[i]) >= self.xlolim) and\
                        (float(self.y[i]) <= self.yuplim) and (float(self.y[i]) >=self.ylolim):
                            self.output_list.append(all_data.values[i].tolist())
                            self.xabund.append(self.x[i])
                            self.yabund.append(self.y[i])
                            varx.append(float(self.x[i]))
                            vary.append(float(self.y[i]))
                            c+=1
                        
            if varx !=[] and vary != []:                
                ax.scatter(varx, vary,marker='o',color='darkgray',s=self.markersize, lw=0 ,zorder=-30)
            if self.ylimits and varx_yup !=[] and vary_yup != []:
                ax.scatter(varx_yup, vary_yup,marker='o',color='k',s=self.markersize, lw=0)#,label=self.var_ref[m])
                ax.errorbar(varx_yup, vary_yup, color='k', yerr=self.erry,\
                        fmt='o', uplims=True, capsize=0,markersize=0, elinewidth=0, mew=0)

            if self.ylimits and varx_ylo !=[] and vary_ylo != []:
                ax.scatter(varx_ylo, vary_ylo,marker='o',color='k',s=self.markersize, lw=0)#,label=self.var_ref[m])
                ax.errorbar(varx_ylo, vary_ylo, color='k', yerr=self.erry,\
                        fmt='o', lolims=True, capsize=0,markersize=0, elinewidth=0, mew=0)

            if self.xlimits and varx_xup !=[] and vary_xup != []:
                ax.scatter(varx_xup, vary_xup,marker='o',color='k',s=self.markersize, lw=0)#,label=self.var_ref[m])
                ax.errorbar(varx_xup, vary_xup, color='k', xerr=self.errx,\
                        fmt='o', xuplims=True, capsize=0,markersize=0, elinewidth=0, mew=0)
                
        if self.background:
            var_xback, var_yback = [], []
            var_xback_yup, var_yback_yup = [], []
            for m in range(len(self.xback)):
                if (self.xback[m] != '*') and (self.yback[m] != '*'): 
                    if uppery[m] =='1':
                        var_xback_yup.append(self.xback[m])
                        var_yback_yup.append(self.yback[m])
                    else:
                        var_xback.append(self.xback[m])
                        var_yback.append(self.yback[m])

            ax.scatter(var_xback, var_yback,marker='o',color='lightgray',s=30, lw=0 ,zorder=-40,label='MW Halo')
            if self.ylimits:
                ax.errorbar(var_xback_yup, var_yback_yup, color='lightgray', yerr=self.erry,\
                    fmt='o', uplims=True, capsize=0,markersize=5, elinewidth=0, mew=0,zorder=-40)

        #ax = figure.add_subplot(111)
        #ax = self.main.display.axes[0]

        if self.xhorfe == '[X/H]':
            ax.set_xlabel('[%s/H]' %self.xoptions, fontsize=16)
        elif self.xhorfe == '[X/Fe]':
            ax.set_xlabel('[%s/Fe]' %self.xoptions, fontsize=16)
        elif self.xhorfe == '[X/Y]':
            ax.set_xlabel('[%s/%s]' %(self.xoptions,self.zxoptions), fontsize=16)
        else:
            ax.set_xlabel('%s' %self.xoptions, fontsize=16)

        if self.yhorfe == '[X/H]':
	        ax.set_ylabel('[%s/H]' %self.yoptions, fontsize=16)
        elif self.yhorfe == '[X/Fe]':
	        ax.set_ylabel('[%s/Fe]' %self.yoptions, fontsize=16)
        elif self.yhorfe == '[X/Y]':
	        ax.set_ylabel('[%s/%s]' %(self.yoptions,self.zyoptions), fontsize=16)
        else:
            ax.set_ylabel('%s' %self.yoptions, fontsize=16)

        if self.legend:
            if len(self.var_ref) > 27:
                n = round(float(len(self.var_ref))/27.,0)
            else:
                n=1

            ax.legend(bbox_to_anchor=(1., 1.01),loc='upper left', ncol = int(n), fontsize=11)
        	
        if self.yoptions in abundances:
            ax.axhline(0, color='darkgray',linestyle='dashed')
        if self.xoptions in abundances:
            ax.axvline(0, color='darkgray',linestyle='dashed')
        #ax.grid(which='major', color='w', linewidth=0.5)
        #ax.grid(which='minor', color='w', linewidth=0.5)

        if self.completeness_bool and self.xoptions == 'Fe' and self.xhorfe == '[X/H]':
            ax.axvline(-2, color='crimson',linestyle='-.')

        txt1 = 'No. of stars: %d' %c
        txt2 = 'Upper limits: %d' %d
        if self.num_stars:
            ax.annotate(txt1, xy=(0.01, 1.01), xycoords='axes fraction', fontsize=15)
        if self.num_limits:
            ax.annotate(txt2, xy=(0.5, 1.01), xycoords='axes fraction', fontsize=15)
            
        wx.CallAfter(self.main.display_plot.canvas.draw)

    def _save_button_fired(self):
        plotted_data = []
        self.output_list.insert(0,all_data.columns.values.tolist())
        plotted_data = [line[:23] for line in self.output_list]
        for line in plotted_data:
             del line[7:19]
        for i in range(len(plotted_data)):
            if i == 0:
                if self.xhorfe == '[X/H]':
                    plotted_data[0].append('['+self.xoptions+'/H]')
                elif self.xhorfe == '[X/Fe]':
                    plotted_data[0].append('['+self.xoptions+'/Fe]')
                elif self.xhorfe == '[X/Y]':
                    plotted_data[0].append('['+self.xoptions+'/'+self.zxoptions+']')
                else:
                    plotted_data[0].append(self.xoptions)
                
                if self.yhorfe == '[X/H]':
                    plotted_data[0].append('['+self.yoptions+'/H]')
                elif self.yhorfe == '[X/Fe]':
                    plotted_data[0].append('['+self.yoptions+'/Fe]')
                elif self.yhorfe == '[X/Y]':
                    plotted_data[0].append('['+self.yoptions+'/'+self.zyoptions+']')
                else:
                    plotted_data[0].append(self.yoptions)
                
                if self.criteria_bool:
                    if self.criteria_norm == '[X/H]':
                        plotted_data[0].append('['+self.criteria_element+'/H]')
                    elif self.criteria_norm == '[X/Fe]':
                        plotted_data[0].append('['+self.criteria_element+'/Fe]')
                    elif self.criteria_norm == '[X/Y]':
                        plotted_data[0].append('['+self.criteria_element+'/'+self.criteria_Y+']')
                    else:
                        plotted_data[0].append(self.criteria_element)
                
            else:
                plotted_data[i].append(str(self.xabund[i-1]))
                plotted_data[i].append(str(self.yabund[i-1]))
                if self.criteria_bool:
                    plotted_data[i].append(str(self.criteria_abund[i-1]))
            

            
        write(self.output_list,'data.txt')
        write(plotted_data,'plotted_data.txt')

        all_bibtex = readbib('files/all_bibtex.bib')
        bibtex = []
        for r in self.ref_list:
            for bib in all_bibtex:
                if r in bib[0]:
                    bibtex.append(bib)

        with open('bibtex.bib','w') as f:
            for bib in bibtex:
                for line in bib:
                    f.write('%s' %line)


    def _openbutton_changed(self):
        read_file_name = open_file()
        if read_file_name != '':
            self.file_name = read_file_name

    def _retrieve_button_fired(self):
        query_list = readtxt(self.file_name)
        for line in query_list:
            if len(line) < 2:
                line.append('')
        full_list = [[str(x) for x in y] for y in all_data.values.tolist()]
        new_list, names=[], []
        for item in query_list:
            for line in full_list:
                if (item[0] in line[2] or item[0] in line[3]) and item[1] in line[1]:
                    new_list.append(line)
                    names.append(item)
        
        self.not_found = [x for x in query_list if x not in names]
        new_list.insert(0,all_data.columns.values)
        write(new_list,'retrieved_data.txt')

    def _isochrone_fired(self):
        self.output_list = []
        for i in range(len(self.y)):
            if (self.y[i] != '*') and (self.x[i] != '*') and (all_data['Reference'].values[i] in self.ref_list):
               if (float(self.x[i]) <= self.xuplim) and (float(self.x[i]) >= self.xlolim) and\
               (float(self.y[i]) <= self.yuplim) and (float(self.y[i]) >=self.ylolim):
                   self.output_list.append(all_data.values[i].tolist())

        # Stellar isochrones, age = 12 Gyr, [Fe/H] = -1.5, -2, -2.5, -3
        datafile1 = 'files/isochrones/afe030feh150set1_12gyr.txt'
        datafile2 = 'files/isochrones/afe040feh200set1_12gyr.txt'
        datafile3 = 'files/isochrones/afe040feh250set1_12gyr.txt'
        datafile4 = 'files/isochrones/afe040feh300set1_12gyr.txt'


        lgT150, g150 = np.loadtxt(datafile1, skiprows=3, usecols = (1, 3),unpack = True)
        lgT200, g200 = np.loadtxt(datafile2, skiprows=3, usecols = (1, 3),unpack = True)
        lgT250, g250 = np.loadtxt(datafile3, usecols = (1, 3),unpack = True)
        lgT300, g300 = np.loadtxt(datafile4, skiprows=3, usecols = (1, 3), unpack = True)

        # Convert to isochrone lgT's to T's
        T150 = 10**lgT150
        T200 = 10**lgT200
        T250 = 10**lgT250
        T300 = 10**lgT300

        stars = read_params(self.output_list)
        ref = []
        for star in stars:
            ref.append(star['ref'])
        ref = list(set(ref))
        
        col = ['r', 'g', 'b', 'orange','y', 'k', 'lightgreen', 'c', 'm', 'crimson', 'fuchsia']*len(ref)
        shape = ['s','*','8','D']*len(ref)
        figure = self.main.display_isochrone
        figure.clear()
        ax = figure.add_axes([0.14, 0.1, 0.6, 0.8])
        #ax.set_axis_bgcolor('lightgray')

        ax.plot(T150, g150, c = 'black', linestyle = '-', label = '[Fe/H] = -1.5')
        ax.plot(T200, g200, c = 'black', linestyle = '-.', label = '[Fe/H] = -2.0')
        ax.plot(T250, g250, c = 'black', linestyle = '--', label = '[Fe/H] = -2.5')
        ax.plot(T300, g300, c = 'black', linestyle = ':', label = '[Fe/H] = -3.0')
        if self.legend:
            c = 0
            for i in range(len(ref)):
                x, y, d =[], [], 0
                for star in stars:
                    if star['ref'] == ref[i]:
                        x.append(star['teff'])
                        y.append(star['logg'])
                        d+=1
                c +=d
                ax.scatter(x, y, c=col[i],marker=shape[i], s = 25, label = ref[i], lw=0)
        else:
            x, y, c =[], [], 0
            for star in stars:
                x.append(star['teff'])
                y.append(star['logg'])
                c += 1
            ax.scatter(x, y, color='gray', s = 25, lw=0)

        
        ax.set_xlim(7500, 3500)
        ax.set_ylim(5.5, -0.5)
        ax.set_xlabel('Teff (K)')
        ax.set_ylabel('log g')
        ax.legend(bbox_to_anchor=(1.44, 1.01),ncol=1,fontsize =11)

        txt1 = 'No. of stars: %d' %c
        if self.num_stars:
            ax.annotate(txt1, xy=(0.01, 1.01), xycoords='axes fraction', fontsize=15)

        #ax.grid(which='major', color='w', linewidth=0.5)
        #ax.grid(which='minor', color='w', linewidth=0.5)

        wx.CallAfter(self.main.display_isochrone.canvas.draw)

    def _star_plot_fired(self):
        solar = readfile('files/'+self.normoptions+'.txt') #read in solar abundances
        figure = self.main.display_star
        figure.clear()
        ax = figure.add_axes([0.1, 0.1, 0.7, 0.8]) # set axes for plot
        # the median and values per reference
        x_med, y_med, x_all, y_all = [], [], [], []
        var_ref, txt = [],[]
        data =pd.DataFrame()
        for i,line in enumerate(all_data.values.tolist()):
            if self.star_name in line:
                var_ref.append(line[1]) 
                data = data.append(all_data.iloc[i], ignore_index=True)
        var_ref = list(set(var_ref))
        col=['r','b','g','y','m','c','orange','lightgreen','crimson','fuchsia','darkgray']*len(var_ref)
        shape = ['s','o','H','p']*len(var_ref)
        for k,r in enumerate(var_ref):
            x, y, upperx, uppery = [], [], [], []
            for m in range(len(elements[:-6])):
                element = data[elements[m]].values.tolist()
                x_elm, y_elm, upperx_elm, uppery_elm = [], [], [], []
                for i in range(len(element)):
                    if ((self.star_name in data['Simbad_Identifier'].values[i]) or (self.star_name in data['Name'].values[i])) \
                    and r in data['Reference'].values[i] and element[i] !='*':
                        x_elm.append(float(solar[elements[m]].values[0]))
                        if self.star_horfe == '[X/H]':
                            y_elm.append(float(element[i])- float(solar[elements[m]].values[1]))
                        elif self.star_horfe == '[X/Fe]':
                            y_elm.append(float(element[i])- float(solar[elements[m]].values[1]) - (float(data['Fe'].values[i]) - float(solar['Fe'].values[-1])))
                        else:
                            y_elm.append(float(element[i]))
                if y_elm != []:
                    for item in x_elm:
                        x.append(item)
                    for item in y_elm:
                        y.append(item)
                    txt.append([elements[m], float(solar[elements[m]].values[0])])
            if y !=[] or uppery != []:
                ax.scatter(x, y, marker=shape[k], s =20, edgecolors= col[k], lw =1,facecolors='none',label=r)
                for item in x:
                    x_all.append(item)
                for item in y:
                    y_all.append(item)
        ly, uy = ax.get_ylim()
        txt.sort(key=lambda x: x[1])
        txt = list(txt for txt,_ in itertools.groupby(txt))
        for j in range(len(txt)):
            x_med.append(txt[j][1])
            if j % 2 == 0:
                ax.annotate(txt[j][0], (txt[j][1]-0.5, uy-0.4), fontsize=9)
            else:
                ax.annotate(txt[j][0], (txt[j][1]-0.5, uy-0.7), fontsize=9)
        x_med.sort()
        num_star, y_std, y_mean = [], [], []
        for item in x_med:
            y_x= []
            num = 0
            for line in range(len(x_all)):
                if item == x_all[line]:
                    y_x.append(y_all[line])
                    num+=1
            y_med.append(round(np.median(y_x),2))
            if len(y_x) > 1:
                y_std.append(round(np.std(y_x),2))
                y_mean.append(round(np.mean(y_x),2))
            elif len(y_x) <= 1:
                y_std.append(0)
                y_mean.append(round(np.mean(y_x),2))
            num_star.append(num)
        ax.plot(x_med, y_med,'k+:',label='median') #plotting the median
        ax.minorticks_on() # minor grid on
        ax.grid(which='both', axis='x',linewidth=0.3, color='darkgray', linestyle='--') # minor grid forma
        ax.legend(bbox_to_anchor=(1, 1.01), loc ='upper left', fontsize=9)
        ax.set_xlim(0,txt[-1][-1]+5)
        if self.star_horfe == '[X/H]':
            ax.set_ylabel('[X/H]', fontsize=14)
        elif self.star_horfe == '[X/Fe]':
            ax.set_ylabel('[X/Fe]', fontsize=14)
        else:
            ax.set_ylabel('Log(e)', fontsize=14)
        ax.set_xlabel('Z', fontsize=14)
        wx.CallAfter(self.main.display_star.canvas.draw)
           		

    def __init__(self, main, **kwargs):
        HasTraits.__init__(self)
        self.main = main
        
