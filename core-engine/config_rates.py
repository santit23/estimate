# config_rates.py

MATERIAL_RATES = {
    '90mm': {
        'mount': {
            # === CONFIGURATION ===
            # Based on your rates (178.75), this looks like price per 20ft Bar.
            # 178.75 / 20 = ~8.9 per ft (Close to Rohit's 9)
            'config': {
                'profile_unit': '20ft',  # Profiles calculated as: Price / 20
                'linear_unit': 'ft',     # Gasket/Brush
                'area_unit': 'sqft',     # Glass/Labour
                'hardware_unit': 'nos',  # Rollers/Locks
                'consumable_unit': 'set' # Screw/Silicon (Lump sum)
            },
            
            # === RATES ===
            'rates': {
                'topfr': 178.75, 
                'bottomfr': 234, 
                'sidefr': 139.75, 
                'topsht': 117, 
                'bottomsht': 126.75, 
                'sidesht': 149.5, 
                'interlocksht': 146.25, 
                'jali': 60.25, # Note: Ensure formula calls this 'jali' or 'jali_track'
                '11b': 133.25,
                '13d': 74.75,
                '13': 81.25,
                '18': 190.25,
                'clip': 26.5,
                              
                'glass': 19, 
                'gasket': 13, 
                'red_brush': 8, 
                'brush': 8, 
                'guide': 8, 
                'jali_gasket': 8, 
                'jali_angle': 4, 
                'jali_handle': 1, 
                'jali_roller': 2, 
                'roller': 4, 
                'lock': 2, 
                'silicon': 1, 
                'labour': 10, 
                'screw': 100,
            }
        },
        'rohit': {
            # === CONFIGURATION ===
            # Your rates (7, 9) look like Per Running Foot prices.
            'config': {
                'profile_unit': 'ft',    # Profiles calculated as: Price * Length
                'linear_unit': 'ft',
                'area_unit': 'sqft',
                'hardware_unit': 'nos',
                'consumable_unit': 'set'
            },
            
            # === RATES ===
            'rates': {
                'topfr': 7, 
                'bottomfr': 7, 
                'sidefr': 9, 
                'topsht': 7, 
                'bottomsht': 7, 
                'sidesht': 9, 
                'interlocksht': 9, 
                'jali': 16, 
                
                'glass': 21, 
                'gasket': 15, 
                'red_brush': 9, 
                'brush': 9, 
                'guide': 9, 
                'jali_gasket': 9, 
                'jali_angle': 5, 
                'jali_handle': 1, 
                'jali_roller': 2, 
                'roller': 5, 
                'lock': 2, 
                'silicon': 1, 
                'labour': 12, 
                'screw': 110,
            }
        }
    },
    '78mm': {
        'mount': {
            # === CONFIGURATION ===
            # Rates (6, 7) look like Per Running Foot
            'config': {
                'profile_unit': 'ft', 
                'linear_unit': 'ft',
                'area_unit': 'sqft',
                'hardware_unit': 'nos',
                'consumable_unit': 'set'
            },
            'rates': {
                'topfr': 6, 'bottomfr': 6, 'sidefr': 7, 'topsht': 6, 'bottomsht': 6, 
                'sidesht': 7, 'interlocksht': 7, 'jali': 14, 'glass': 18, 'gasket': 12, 
                'red_brush': 7, 'brush': 7, 'guide': 7, 'jali_gasket': 7, 'jali_angle': 4, 
                'jali_handle': 1, 'jali_roller': 2, 'roller': 4, 'lock': 2, 'silicon': 1, 
                'labour': 10, 'screw': 100,
            }
        },
        'rohit': {
            # === CONFIGURATION ===
            # Rates (6.5, 8) look like Per Running Foot
            'config': {
                'profile_unit': 'ft', 
                'linear_unit': 'ft',
                'area_unit': 'sqft',
                'hardware_unit': 'nos',
                'consumable_unit': 'set'
            },
            'rates': {
                'topfr': 6.5, 'bottomfr': 6.5, 'sidefr': 8, 'topsht': 6.5, 'bottomsht': 6.5, 
                'sidesht': 8, 'interlocksht': 8, 'jali': 15, 'glass': 20, 'gasket': 14, 
                'red_brush': 8, 'brush': 8, 'guide': 8, 'jali_gasket': 8, 'jali_angle': 4, 
                'jali_handle': 1, 'jali_roller': 2, 'roller': 4.5, 'lock': 2, 'silicon': 1, 
                'labour': 11, 'screw': 105,
            }
        }
    }
}


# Misceleneous Rates