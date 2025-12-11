# Topfix, bottomfix window
sldht = 0.75
fixht = 0.25

sldtbmht = 0.6
fixtbmht = 0.4



# Base Formulas (Standard Window)
WINDOW_FORMULAS = {
    "2_panel_slide": {
        'topfr':        lambda l, h: l,
        'bottomfr':     lambda l, h: l,
        'sidefr':       lambda l, h: h * 2,
        
        'topsht':       lambda l, h: l,         # Logic: Top+Bottom
        'bottomsht':    lambda l, h: l,
        'sidesht':      lambda l, h: h * 2,     # Logic: 2 sides per panel? usually 4 vertical for 2 panel
        'interlocksht': lambda l, h: h * 2,
        
        'glass':        lambda l, h: l * h,
        'gasket':       lambda l, h: (l*4) + (h*8),
        'red_brush':    lambda l, h: l * 2,
        'brush':        lambda l, h: (l*2) + (h*4),
        
        'guide':        lambda l, h: 4*2,         # Example: 4 guides
        'roller':       lambda l, h: 4,         # 2 per panel
        'lock':         lambda l, h: 1,
        'silicon':      lambda l, h: 1,
        'screw':        lambda l, h: 1,         # Fixed cost multiplier
        'labour':       lambda l, h: l * h,
        # --- Jali Configuration ---
        'jali':       lambda l, h: (0.5*l) * h,  
        'jali_gasket':  lambda l, h: (0.5*l) + (h*2),
        'jali_angle':   lambda l, h: 4,
        'jali_handle':  lambda l, h: 1,
        'jali_roller':  lambda l, h: 2

    },
    
    "3_panel_slide": {
        'topfr':        lambda l, h: l,
        'bottomfr':     lambda l, h: l,
        'sidefr':       lambda l, h: h * 2,
        
        'topsht':       lambda l, h: l,
        'bottomsht':    lambda l, h: l,
        'sidesht':      lambda l, h: h * 3,     # 3 Panels
        'interlocksht': lambda l, h: h * 4,     # 2 meeting points
        
        'glass':        lambda l, h: l * h,
        'gasket':       lambda l, h: (l*6) + (h*12),
        'red_brush':    lambda l, h: l * 3,
        'brush':        lambda l, h: (l*2) + (h*7),
        
        'guide':        lambda l, h: 4*3,
        'roller':       lambda l, h: 6,
        'lock':         lambda l, h: 1,
        'silicon':      lambda l, h: 1.5,
        'screw':        lambda l, h: 1,
        # 'labour':       lambda l, h: l * h,
        #  --- Jali Configuration ---
        'jali':       lambda l, h: (1/3)*l * h,
        'jali_gasket':  lambda l, h: (1/3)*2*l + (h*2),
        'jali_angle':   lambda l, h: 4,
        'jali_handle':  lambda l, h: 1,
        'jali_roller':  lambda l, h: 2
    },
    
    "4_panel_slide": {
        'topfr':        lambda l, h: l,
        'bottomfr':     lambda l, h: l,
        'sidefr':       lambda l, h: h * 2,
        
        'topsht':       lambda l, h: l,
        'bottomsht':    lambda l, h: l,
        'sidesht':      lambda l, h: h * 4,     # 4 Panels
        'interlocksht': lambda l, h: h * 4,     
        'jointsht':     lambda l, h: h,         # 2 joints for 4 panels
        
        'glass':        lambda l, h: l * h,
        'gasket':       lambda l, h: (l*4) + (h*16),
        'red_brush':    lambda l, h: l * 4,
        'brush':        lambda l, h: (l*2) + (h*9),
        
        'guide':        lambda l, h: 16,
        'roller':       lambda l, h: 8,
        'lock':         lambda l, h: 1,
        'silicon':      lambda l, h: 2,
        'screw':        lambda l, h: 1,

        # --- Jali Configuration ---
        'jali':       lambda l, h: (1/3)*l * h,
        'jali_gasket':  lambda l, h: l+h*4,
        'jali_angle':   lambda l, h: 8,
        'jali_handle':  lambda l, h: 1,
        'jali_roller':  lambda l, h: 8
},
    "2_pnl_topfix": {


        'topfr':        lambda l, h: l,
        'bottomfr':     lambda l, h: l,
        'sidefr':       lambda l, h: h * 2,
        
        'topsht':       lambda l, h: l,
        'bottomsht':    lambda l, h: l,
        'sidesht':      lambda l, h: sldht * 2,
        'interlocksht': lambda l, h: sldht * 2,
        '11b':         lambda l, h: l,
        '13d':         lambda l, h: l,
        '13':          lambda l, h: fixht * 2,
        '18':          lambda l, h: fixht,
        'clip':         lambda l, h: l*2 + fixht*4,
        
        'glass':        lambda l, h: l * h,
        'gasket':       lambda l, h: (l*8) + (h*8),
        'red_brush':    lambda l, h: l * 4 * 3,
        'brush':        lambda l, h: (l*2) + (h*3),
        
        'guide':        lambda l, h: 8,
        'roller':       lambda l, h: 4,
        'lock':         lambda l, h: 2,
        'silicon':      lambda l, h: 1,
        'screw':        lambda l, h: 1,
        'labour':       lambda l, h: l * h,
        # --- Jali Configuration ---
        'jali':       lambda l, h: l * sldht * 0.5,  
        'jali_gasket':  lambda l, h: l + sldht*2,
        'jali_angle':   lambda l, h: 4,
        'jali_handle':  lambda l, h: 1,
        'jali_roller':  lambda l, h: 2,
          
    },
    "3_pnl_topfix": {


        'topfr':        lambda l, h: l,
        'bottomfr':     lambda l, h: l,
        'sidefr':       lambda l, h: h * 2,
        
        'topsht':       lambda l, h: l,
        'bottomsht':    lambda l, h: l,
        'sidesht':      lambda l, h: sldht * 2,
        'interlocksht': lambda l, h: sldht * 4,
        '11b':         lambda l, h: l,
        '13d':         lambda l, h: l,
        '13':          lambda l, h: fixht * 2,
        '18':          lambda l, h: fixht * 2,
        'clip':         lambda l, h: l*2 + fixht*6,
        
        'glass':        lambda l, h: l * h,
        'gasket':       lambda l, h: (l*8) + (h*12),
        'red_brush':    lambda l, h: l * 4 * 3,
        'brush':        lambda l, h: sldht*8,
        
        'guide':        lambda l, h: 12,
        'roller':       lambda l, h: 4,
        'lock':         lambda l, h: 2,
        'silicon':      lambda l, h: 1,
        'screw':        lambda l, h: 1,
        'labour':       lambda l, h: l * h,
        # --- Jali Configuration ---
        'jali':       lambda l, h: l*sldht*0.33,  
        'jali_gasket':  lambda l, h: l * 0.66 + sldht*2,
        'jali_angle':   lambda l, h: 4,
        'jali_handle':  lambda l, h: 1,
        'jali_roller':  lambda l, h: 2,
          
    },
    "4_pnl_topfix": {


        'topfr':        lambda l, h: l,
        'bottomfr':     lambda l, h: l,
        'sidefr':       lambda l, h: h * 2,
        
        'topsht':       lambda l, h: l,
        'bottomsht':    lambda l, h: l,
        'sidesht':      lambda l, h: sldht * 4,
        'interlocksht': lambda l, h: sldht * 4,
        '11b':         lambda l, h: l,
        '13d':         lambda l, h: l,
        '13':          lambda l, h: fixht * 2,
        '18':          lambda l, h: fixht * 3,
        'clip':         lambda l, h: l*2 + fixht*8,
        
        'glass':        lambda l, h: l * h,
        'gasket':       lambda l, h: (l*8) + (h*16),
        'red_brush':    lambda l, h: l * 4 * 3,
        'brush':        lambda l, h: sldht*10,
        
        'guide':        lambda l, h: 16,
        'roller':       lambda l, h: 8,
        'lock':         lambda l, h: 3,
        'silicon':      lambda l, h: 1,
        'screw':        lambda l, h: 1,
        'labour':       lambda l, h: l * h,
        # --- Jali Configuration ---
        'jali':       lambda l, h: l*sldht*0.5,  
        'jali_gasket':  lambda l, h: l  + sldht*4,
        'jali_angle':   lambda l, h: 4,
        'jali_handle':  lambda l, h: 1,
        'jali_roller':  lambda l, h: 4,
          
    },
    "2_pnl_topbtmfix": {


        'topfr':        lambda l, h: l,
        'bottomfr':     lambda l, h: l,
        'sidefr':       lambda l, h: h * 2,
        
        'topsht':       lambda l, h: l,
        'bottomsht':    lambda l, h: l,
        'sidesht':      lambda l, h: sldtbmht * 2,
        'interlocksht': lambda l, h: sldtbmht * 2,
        '11b':         lambda l, h: l * 2,
        '13d':         lambda l, h: l * 2,
        '13':          lambda l, h: fixtbmht * 2,
        '18':          lambda l, h: fixtbmht,
        'clip':         lambda l, h: l*4 + fixtbmht*4,
        
        'glass':        lambda l, h: l * h,
        'gasket':       lambda l, h: (l*12) + (h*8),
        'red_brush':    lambda l, h: l * 4 ,
        'brush':        lambda l, h: sldtbmht*6,
        
        'guide':        lambda l, h: 8,
        'roller':       lambda l, h: 4,
        'lock':         lambda l, h: 2,
        'silicon':      lambda l, h: 1,
        'screw':        lambda l, h: 1,
        'labour':       lambda l, h: l * h,
        # --- Jali Configuration ---
        'jali':       lambda l, h: l+4*sldtbmht,  
        'jali_gasket':  lambda l, h: l  + sldtbmht*2,
        'jali_angle':   lambda l, h: 4,
        'jali_handle':  lambda l, h: 1,
        'jali_roller':  lambda l, h: 2,
          
    },
    "3_pnl_topbtmfix": {


        'topfr':        lambda l, h: l,
        'bottomfr':     lambda l, h: l,
        'sidefr':       lambda l, h: h * 2,
        
        'topsht':       lambda l, h: l,
        'bottomsht':    lambda l, h: l,
        'sidesht':      lambda l, h: sldtbmht * 2,
        'interlocksht': lambda l, h: sldtbmht * 4,
        '11b':         lambda l, h: l * 2,
        '13d':         lambda l, h: l * 2,
        '13':          lambda l, h: fixtbmht * 2,
        '18':          lambda l, h: fixtbmht*2,
        'clip':         lambda l, h: l*4 + fixtbmht*6,
        
        'glass':        lambda l, h: l * h,
        'gasket':       lambda l, h: (l*12) + (h*12),
        'red_brush':    lambda l, h: l * 4 ,
        'brush':        lambda l, h: sldtbmht*8,
        
        'guide':        lambda l, h: 12,
        'roller':       lambda l, h: 4,
        'lock':         lambda l, h: 2,
        'silicon':      lambda l, h: 1,
        'screw':        lambda l, h: 1,
        'labour':       lambda l, h: l * h,
        # --- Jali Configuration ---
        'jali':       lambda l, h: l*0.67+2*sldtbmht,  
        'jali_gasket':  lambda l, h: l*0.66  + sldtbmht*2,
        'jali_angle':   lambda l, h: 4,
        'jali_handle':  lambda l, h: 1,
        'jali_roller':  lambda l, h: 2,
          
    },
    "4_pnl_topbtmfix": {


        'topfr':        lambda l, h: l,
        'bottomfr':     lambda l, h: l,
        'sidefr':       lambda l, h: h * 2,
        
        'topsht':       lambda l, h: l,
        'bottomsht':    lambda l, h: l,
        'sidesht':      lambda l, h: sldtbmht * 4,
        'interlocksht': lambda l, h: sldtbmht * 4,
        '11b':         lambda l, h: l * 2,
        '13d':         lambda l, h: l * 2,
        '13':          lambda l, h: fixtbmht * 2,
        '18':          lambda l, h: fixtbmht*3,
        'clip':         lambda l, h: l*4 + fixtbmht*8,
        
        'glass':        lambda l, h: l * h,
        'gasket':       lambda l, h: (l*12) + (h*16),
        'red_brush':    lambda l, h: l * 4 ,
        'brush':        lambda l, h: sldtbmht*10,
        
        'guide':        lambda l, h: 16,
        'roller':       lambda l, h: 8,
        'lock':         lambda l, h: 3,
        'silicon':      lambda l, h: 1,
        'screw':        lambda l, h: 1,
        'labour':       lambda l, h: l * h,
        # --- Jali Configuration ---
        'jali':       lambda l, h: l+4*sldtbmht,  
        'jali_gasket':  lambda l, h: l  + sldtbmht*4,
        'jali_angle':   lambda l, h: 8,
        'jali_handle':  lambda l, h: 1,
        'jali_roller':  lambda l, h: 4,
          
    }
}
# 2. Add-on Formulas (Only calculated if has_mesh=True)
# MESH_FORMULAS = {
#     'jali':         lambda l, h: l + (h*2),     # Profile length
#     'jali_gasket':  lambda l, h: l + (h*2),
#     'jali_angle':   lambda l, h: 4,             # 4 corners
#     'jali_handle':  lambda l, h: 1,
#     'jali_roller':  lambda l, h: 2,
# }