# Material rates vayr by series and quality
# per sq ft

MATERIAL_RATES = {
    '90mm': {

        'mount': {
            'topfr': 6,
            'bottomfr': 6,
            'sidefr': 8,
            'topsht': 6,
            'bottomsht': 6,
            'sidesht': 8,
            'interlocksht': 8,
            'jali': 14,
            'glass': 19,
            'gasket': 13,
            'red_brush': 8,
            'brush': 8,
            'guide': 8, # pc
            'jali_gasket': 8,
            'jali_angle': 4, # pcs
            'jali_handle': 1, # pcs
            'jali_roller': 2, # pcs
            'roller': 4, # pcs
            'lock': 2, # pcs
            'silicon': 1, # pcs
            'labour': 10, # per sq ft
            'screw': 100, # rs
            },
        'rohit': {
            'topfr': 7,          # Top Frame (₹/ft)
            'bottomfr': 7,       # Bottom Frame (₹/ft)
            'sidefr': 9,         # Side Frame (₹/ft)
            'topsht': 7,         # Top Shutter (₹/ft)
            'bottomsht': 7,      # Bottom Shutter (₹/ft)
            'sidesht': 9,        # Side Shutter (₹/ft)
            'interlocksht': 9,   # Interlock Shutter (₹/ft)
            'jali': 16,          # Jali Mesh (₹/ft)
            'glass': 21,         # Glass (₹/ft) - Assuming better quality
            'gasket': 15,        # Gasket (₹/ft) - Better sealing
            'red_brush': 9,      # Red Brush (₹/ft)
            'brush': 9,          # Standard Brush (₹/ft)
            'guide': 9,          # Guide (PC)
            'jali_gasket': 9,    # Jali Gasket (₹/ft)
            'jali_angle': 5,     # Jali Angle (PC)
            'jali_handle': 1,    # Jali Handle (PC)
            'jali_roller': 2,    # Jali Roller (PC)
            'roller': 5,         # Roller (PC) - Better quality
            'lock': 2,           # Lock (PC) - Enhanced security
            'silicon': 1,        # Silicon (PC) - Premium sealant
            'labour': 12,        # Labour (₹/sq.ft) - Skilled workmanship
            'screw': 110, 
        }




    },
    '78mm': {
        'mount': {
            'topfr': 6,          # Top Frame (₹/ft)  
            'bottomfr': 6,       # Bottom Frame (₹/ft)  
            'sidefr': 7,         # Side Frame (₹/ft)  
            'topsht': 6,         # Top Shutter (₹/ft)  
            'bottomsht': 6,      # Bottom Shutter (₹/ft)  
            'sidesht': 7,        # Side Shutter (₹/ft)  
            'interlocksht': 7,   # Interlock Shutter (₹/ft)  
            'jali': 14,          # Jali Mesh (₹/ft)  
            'glass': 18,         # Glass (₹/ft) - Standard float/toughened  
            'gasket': 12,        # Gasket (₹/ft) - Better sealing  
            'red_brush': 7,      # Red Brush (₹/ft)  
            'brush': 7,          # Standard Brush (₹/ft)  
            'guide': 7,          # Guide (PC)  
            'jali_gasket': 7,    # Jali Gasket (₹/ft)  
            'jali_angle': 4,     # Jali Angle (PC)  
            'jali_handle': 1,    # Jali Handle (PC)  
            'jali_roller': 2,    # Jali Roller (PC)  
            'roller': 4,         # Roller (PC) - Smoother sliding  
            'lock': 2,           # Lock (PC)  
            'silicon': 1,        # Silicon (PC)  
            'labour': 10,        # Labour (₹/sq.ft)  
            'screw': 100,        # Screws (₹)  
        },
        'rohit': {
                # Frame & Shutter Rates (₹ per foot)
            'topfr': 6.5,        # Top Frame (Premium extrusion)
            'bottomfr': 6.5,     # Bottom Frame
            'sidefr': 8,         # Side Frame (Reinforced)
            'topsht': 6.5,       # Top Shutter
            'bottomsht': 6.5,    # Bottom Shutter
            'sidesht': 8,        # Side Shutter
            'interlocksht': 8,   # Interlock Shutter (Better sealing)
            
            # Accessories & Components
            'jali': 15,          # Jali (Anti-rust mesh)
            'glass': 20,         # Standard Clear Glass (5mm)
            'gasket': 14,        # EPDM Rubber Gasket
            'red_brush': 8,      # Red Pile Brush
            'brush': 8,          # Nylon Brush
            'guide': 8,          # U-Guide (PC)
            
            # Jali Components
            'jali_gasket': 8,    # Jali Gasket
            'jali_angle': 4,     # Jali Corner Angle (PC)
            'jali_handle': 1,    # Jali Handle (PC)
            'jali_roller': 2,    # Jali Roller (PC)
            
            # Hardware
            'roller': 4.5,       # Premium Rollers (PC)
            'lock': 2,           # Sliding Lock (PC)
            'silicon': 1,        # Silicone Sealant (PC)
            
            # Labour & Misc
            'labour': 11,        # Installation (₹ per sq.ft)
            'screw': 105, 
        }
    }
}