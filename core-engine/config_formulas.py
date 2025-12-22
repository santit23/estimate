# Enhanced Formula Configuration with JSON Metadata
# Each formula now includes expression, description, unit, and constraints

# Constants for top/bottom fix windows
sldht = 0.75  # Sliding section height ratio
fixht = 0.25  # Fixed section height ratio

sldtbmht = 0.6  # Sliding section height ratio (top+bottom fix)
fixtbmht = 0.4  # Fixed section height ratio (top+bottom fix)


WINDOW_FORMULAS = {
    "2_panel_slide": {
        'topfr': {
            'expression': 'l',
            'description': 'Top frame runs the full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'bottomfr': {
            'expression': 'l',
            'description': 'Bottom frame runs the full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'sidefr': {
            'expression': 'h * 2',
            'description': 'Side frames on both left and right',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'topsht': {
            'expression': 'l',
            'description': 'Top shutter length (both panels combined)',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'bottomsht': {
            'expression': 'l',
            'description': 'Bottom shutter length (both panels combined)',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'sidesht': {
            'expression': 'h * 2',
            'description': 'Side shutters for both panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'interlocksht': {
            'expression': 'h * 2',
            'description': 'Interlock shutter between panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'glass': {
            'expression': 'l * h',
            'description': 'Total glass area',
            'unit': 'sqft',
            'constraints': {'min': 0}
        },
        'gasket': {
            'expression': '(l * 4) + (h * 8)',
            'description': 'Gasket perimeter for all panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'red_brush': {
            'expression': 'l * 2',
            'description': 'Red brush for top and bottom tracks',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'brush': {
            'expression': '(l * 2) + (h * 4)',
            'description': 'Brush seal for tracks and sides',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'guide': {
            'expression': '4 * 2',
            'description': 'Guide blocks (4 per panel)',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'roller': {
            'expression': '4',
            'description': 'Rollers (2 per panel)',
            'unit': 'nos',
            'constraints': {'min': 2, 'max': 20}
        },
        'lock': {
            'expression': '1',
            'description': 'Lock mechanism',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'silicon': {
            'expression': '1',
            'description': 'Silicon sealant',
            'unit': 'set',
            'constraints': {'min': 0}
        },
        'screw': {
            'expression': 'l * h',
            'description': 'Screws based on area',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'labour': {
            'expression': 'l * h',
            'description': 'Labour cost based on area',
            'unit': 'sqft',
            'constraints': {'min': 0}
        },
        # Jali/Mesh Configuration
        'jali': {
            'expression': 'l + (h * 2)',
            'description': 'Jali frame perimeter',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jali_gasket': {
            'expression': 'l + (h * 2)',
            'description': 'Jali gasket length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jali_angle': {
            'expression': '4',
            'description': 'Jali corner angles',
            'unit': 'nos',
            'constraints': {'min': 4}
        },
        'jali_handle': {
            'expression': '1',
            'description': 'Jali handle',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'jali_roller': {
            'expression': '2',
            'description': 'Jali rollers',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
    },
    
    "3_panel_slide": {
        'topfr': {
            'expression': 'l',
            'description': 'Top frame full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'bottomfr': {
            'expression': 'l',
            'description': 'Bottom frame full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'sidefr': {
            'expression': 'h * 2',
            'description': 'Side frames both sides',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'topsht': {
            'expression': 'l',
            'description': 'Top shutter for 3 panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'bottomsht': {
            'expression': 'l',
            'description': 'Bottom shutter for 3 panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'sidesht': {
            'expression': 'h * 2',
            'description': 'Side shutters (3 panels)',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'interlocksht': {
            'expression': 'h * 4',
            'description': 'Interlocks at 2 meeting points',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'glass': {
            'expression': 'l * h',
            'description': 'Total glass area',
            'unit': 'sqft',
            'constraints': {'min': 0}
        },
        'gasket': {
            'expression': '(l * 4) + (h * 12)',
            'description': 'Gasket for 3 panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'red_brush': {
            'expression': 'l * 2',
            'description': 'Red brush for tracks',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'brush': {
            'expression': '(l * 2) + (h * 4)',
            'description': 'Brush seal',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'guide': {
            'expression': '4 * 3',
            'description': '4 guides per panel',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'roller': {
            'expression': '4',
            'description': 'Rollers for sliding panels',
            'unit': 'nos',
            'constraints': {'min': 2, 'max': 20}
        },
        'lock': {
            'expression': '1',
            'description': 'Lock mechanism',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'silicon': {
            'expression': '1.5',
            'description': 'Silicon for 3 panels',
            'unit': 'set',
            'constraints': {'min': 0}
        },
        'screw': {
            'expression': 'l * h',
            'description': 'Screws based on area',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'labour': {
            'expression': 'l * h',
            'description': 'Labour cost based on area',
            'unit': 'sqft',
            'constraints': {'min': 0}
        },
        'jali': {
            'expression': '(l / 3) * h',
            'description': 'Jali for one panel (1/3 width)',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jali_gasket': {
            'expression': '(l * 2 / 3) + (h * 2)',
            'description': 'Jali gasket length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jali_angle': {
            'expression': '4',
            'description': 'Jali corner angles',
            'unit': 'nos',
            'constraints': {'min': 4}
        },
        'jali_handle': {
            'expression': '1',
            'description': 'Jali handle',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'jali_roller': {
            'expression': '2',
            'description': 'Jali rollers',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
    },
    
    "4_panel_slide": {
        'topfr': {
            'expression': 'l',
            'description': 'Top frame full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'bottomfr': {
            'expression': 'l',
            'description': 'Bottom frame full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'sidefr': {
            'expression': 'h * 2',
            'description': 'Side frames both sides',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'topsht': {
            'expression': 'l',
            'description': 'Top shutter for 4 panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'bottomsht': {
            'expression': 'l',
            'description': 'Bottom shutter for 4 panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'sidesht': {
            'expression': 'h * 4',
            'description': 'Side shutters (4 panels)',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'interlocksht': {
            'expression': 'h * 4',
            'description': 'Interlocks between panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jointsht': {
            'expression': 'h',
            'description': 'Joint shutter for center',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'glass': {
            'expression': 'l * h',
            'description': 'Total glass area',
            'unit': 'sqft',
            'constraints': {'min': 0}
        },
        'gasket': {
            'expression': '(l * 4) + (h * 16)',
            'description': 'Gasket for 4 panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'red_brush': {
            'expression': 'l * 2',
            'description': 'Red brush for tracks',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'brush': {
            'expression': '(l * 2) + (h * 6)',
            'description': 'Brush seal',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'guide': {
            'expression': '16',
            'description': '4 guides per panel',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'roller': {
            'expression': '8',
            'description': '2 rollers per panel',
            'unit': 'nos',
            'constraints': {'min': 4, 'max': 20}
        },
        'lock': {
            'expression': '2',
            'description': 'Lock mechanisms',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'silicon': {
            'expression': '2',
            'description': 'Silicon for 4 panels',
            'unit': 'set',
            'constraints': {'min': 0}
        },
        'screw': {
            'expression': 'l * h',
            'description': 'Screws based on area',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'jali': {
            'expression': '(l / 3) * h',
            'description': 'Jali for one panel',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jali_gasket': {
            'expression': 'l + (h * 4)',
            'description': 'Jali gasket length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jali_angle': {
            'expression': '8',
            'description': 'Jali corner angles (double)',
            'unit': 'nos',
            'constraints': {'min': 4}
        },
        'jali_handle': {
            'expression': '2',
            'description': 'Jali handles',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'jali_roller': {
            'expression': '4',
            'description': 'Jali rollers',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
    },
    
    "2_pnl_topfix": {
        'topfr': {
            'expression': 'l',
            'description': 'Top frame full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'bottomfr': {
            'expression': 'l',
            'description': 'Bottom frame full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'sidefr': {
            'expression': 'h * 2',
            'description': 'Side frames both sides',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'topsht': {
            'expression': 'l',
            'description': 'Top shutter',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'bottomsht': {
            'expression': 'l',
            'description': 'Bottom shutter',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'sidesht': {
            'expression': f'{sldht} * 2',
            'description': 'Side shutters for sliding section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'interlocksht': {
            'expression': f'{sldht} * 2',
            'description': 'Interlock for sliding section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '11b': {
            'expression': 'l',
            'description': '11B profile full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '13d': {
            'expression': 'l',
            'description': '13D profile full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '13': {
            'expression': f'{fixht} * 2',
            'description': '13 profile for fixed section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '18': {
            'expression': f'{fixht}',
            'description': '18 profile for fixed section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'clip': {
            'expression': f'(l * 2) + ({fixht} * 4)',
            'description': 'Clips for frame',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'glass': {
            'expression': 'l * h',
            'description': 'Total glass area',
            'unit': 'sqft',
            'constraints': {'min': 0}
        },
        'gasket': {
            'expression': '(l * 8) + (h * 8)',
            'description': 'Gasket perimeter',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'red_brush': {
            'expression': 'l * 2',
            'description': 'Red brush for tracks',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'brush': {
            'expression': f'(l * 2) + ({sldht} * 4)',
            'description': 'Brush seal for sliding section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'guide': {
            'expression': '8',
            'description': 'Guide blocks',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'roller': {
            'expression': '4',
            'description': 'Rollers for sliding panels',
            'unit': 'nos',
            'constraints': {'min': 2, 'max': 20}
        },
        'lock': {
            'expression': '1',
            'description': 'Lock mechanism',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'silicon': {
            'expression': '1',
            'description': 'Silicon sealant',
            'unit': 'set',
            'constraints': {'min': 0}
        },
        'screw': {
            'expression': 'l * h',
            'description': 'Screws based on area',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'labour': {
            'expression': 'l * h',
            'description': 'Labour cost based on area',
            'unit': 'sqft',
            'constraints': {'min': 0}
        },
        'jali': {
            'expression': f'l * ({sldht} * 0.5)',
            'description': 'Jali for half sliding section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jali_gasket': {
            'expression': f'l + ({sldht} * 2)',
            'description': 'Jali gasket',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jali_angle': {
            'expression': '4',
            'description': 'Jali corner angles',
            'unit': 'nos',
            'constraints': {'min': 4}
        },
        'jali_handle': {
            'expression': '1',
            'description': 'Jali handle',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'jali_roller': {
            'expression': '2',
            'description': 'Jali rollers',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
    },
    
    "3_pnl_topfix": {
        'topfr': {
            'expression': 'l',
            'description': 'Top frame full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'bottomfr': {
            'expression': 'l',
            'description': 'Bottom frame full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'sidefr': {
            'expression': 'h * 2',
            'description': 'Side frames both sides',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'topsht': {
            'expression': 'l',
            'description': 'Top shutter',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'bottomsht': {
            'expression': 'l',
            'description': 'Bottom shutter',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'sidesht': {
            'expression': f'{sldht} * 2',
            'description': 'Side shutters for sliding section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'interlocksht': {
            'expression': f'{sldht} * 4',
            'description': 'Interlocks for multiple panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '11b': {
            'expression': 'l',
            'description': '11B profile',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '13d': {
            'expression': 'l',
            'description': '13D profile',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '13': {
            'expression': f'{fixht} * 2',
            'description': '13 profile for fixed section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '18': {
            'expression': f'{fixht} * 2',
            'description': '18 profile for fixed section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'clip': {
            'expression': f'(l * 2) + ({fixht} * 6)',
            'description': 'Clips for frame',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'glass': {
            'expression': 'l * h',
            'description': 'Total glass area',
            'unit': 'sqft',
            'constraints': {'min': 0}
        },
        'gasket': {
            'expression': '(l * 8) + (h * 12)',
            'description': 'Gasket for 3 panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'red_brush': {
            'expression': 'l * 2',
            'description': 'Red brush for tracks',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'brush': {
            'expression': f'(l * 2) + ({sldht} * 4)',
            'description': 'Brush seal',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'guide': {
            'expression': '12',
            'description': 'Guide blocks for 3 panels',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'roller': {
            'expression': '4',
            'description': 'Rollers for sliding panels',
            'unit': 'nos',
            'constraints': {'min': 2, 'max': 20}
        },
        'lock': {
            'expression': '1',
            'description': 'Lock mechanism',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'silicon': {
            'expression': '1',
            'description': 'Silicon sealant',
            'unit': 'set',
            'constraints': {'min': 0}
        },
        'screw': {
            'expression': 'l * h',
            'description': 'Screws based on area',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'labour': {
            'expression': 'l * h',
            'description': 'Labour cost based on area',
            'unit': 'sqft',
            'constraints': {'min': 0}
        },
        'jali': {
            'expression': f'l * {sldht} * 0.33',
            'description': 'Jali for 1/3 section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jali_gasket': {
            'expression': f'(l * 0.66) + ({sldht} * 2)',
            'description': 'Jali gasket',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jali_angle': {
            'expression': '4',
            'description': 'Jali corner angles',
            'unit': 'nos',
            'constraints': {'min': 4}
        },
        'jali_handle': {
            'expression': '1',
            'description': 'Jali handle',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'jali_roller': {
            'expression': '2',
            'description': 'Jali rollers',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
    },
    
    "4_pnl_topfix": {
        'topfr': {
            'expression': 'l',
            'description': 'Top frame full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'bottomfr': {
            'expression': 'l',
            'description': 'Bottom frame full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'sidefr': {
            'expression': 'h * 2',
            'description': 'Side frames both sides',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'topsht': {
            'expression': 'l',
            'description': 'Top shutter',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'bottomsht': {
            'expression': 'l',
            'description': 'Bottom shutter',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'sidesht': {
            'expression': f'{sldht} * 4',
            'description': 'Side shutters for 4 panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'interlocksht': {
            'expression': f'{sldht} * 4',
            'description': 'Interlocks for 4 panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '11b': {
            'expression': 'l',
            'description': '11B profile',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '13d': {
            'expression': 'l',
            'description': '13D profile',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '13': {
            'expression': f'{fixht} * 2',
            'description': '13 profile for fixed section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '18': {
            'expression': f'{fixht} * 3',
            'description': '18 profile for fixed section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'clip': {
            'expression': f'(l * 2) + ({fixht} * 8)',
            'description': 'Clips for frame',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'jointsht': {
            'expression': f'{sldht}',
            'description': 'Joint shutter',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'glass': {
            'expression': 'l * h',
            'description': 'Total glass area',
            'unit': 'sqft',
            'constraints': {'min': 0}
        },
        'gasket': {
            'expression': '(l * 8) + (h * 16)',
            'description': 'Gasket for 4 panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'red_brush': {
            'expression': 'l * 2',
            'description': 'Red brush for tracks',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'brush': {
            'expression': f'(l * 2) + ({sldht} * 6)',
            'description': 'Brush seal',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'guide': {
            'expression': '16',
            'description': 'Guide blocks for 4 panels',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'roller': {
            'expression': '8',
            'description': 'Rollers for 4 panels',
            'unit': 'nos',
            'constraints': {'min': 4, 'max': 20}
        },
        'lock': {
            'expression': '2',
            'description': 'Lock mechanisms',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'silicon': {
            'expression': '3',
            'description': 'Silicon for 4 panels',
            'unit': 'set',
            'constraints': {'min': 0}
        },
        'screw': {
            'expression': 'l * h',
            'description': 'Screws based on area',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'labour': {
            'expression': 'l * h',
            'description': 'Labour cost based on area',
            'unit': 'sqft',
            'constraints': {'min': 0}
        },
        'jali': {
            'expression': f'l * {sldht} * 0.5',
            'description': 'Jali for half section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jali_gasket': {
            'expression': f'l + ({sldht} * 4)',
            'description': 'Jali gasket',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jali_angle': {
            'expression': '8',
            'description': 'Jali corner angles (double)',
            'unit': 'nos',
            'constraints': {'min': 4}
        },
        'jali_handle': {
            'expression': '2',
            'description': 'Jali handles',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'jali_roller': {
            'expression': '4',
            'description': 'Jali rollers',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
    },
    
    "2_pnl_topbtmfix": {
        'topfr': {
            'expression': 'l',
            'description': 'Top frame full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'bottomfr': {
            'expression': 'l',
            'description': 'Bottom frame full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'sidefr': {
            'expression': 'h * 2',
            'description': 'Side frames both sides',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'topsht': {
            'expression': 'l',
            'description': 'Top shutter',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'bottomsht': {
            'expression': 'l',
            'description': 'Bottom shutter',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'sidesht': {
            'expression': f'{sldtbmht} * 2',
            'description': 'Side shutters for sliding section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'interlocksht': {
            'expression': f'{sldtbmht} * 2',
            'description': 'Interlock for sliding section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '11b': {
            'expression': 'l * 2',
            'description': '11B profile (top and bottom)',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '13d': {
            'expression': 'l * 2',
            'description': '13D profile (top and bottom)',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '13': {
            'expression': f'{fixtbmht} * 2',
            'description': '13 profile for fixed sections',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '18': {
            'expression': f'{fixtbmht}',
            'description': '18 profile for fixed section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'clip': {
            'expression': f'(l * 4) + ({fixtbmht} * 4)',
            'description': 'Clips for both fixed sections',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'glass': {
            'expression': 'l * h',
            'description': 'Total glass area',
            'unit': 'sqft',
            'constraints': {'min': 0}
        },
        'gasket': {
            'expression': '(l * 12) + (h * 8)',
            'description': 'Gasket perimeter',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'red_brush': {
            'expression': 'l * 2',
            'description': 'Red brush for tracks',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'brush': {
            'expression': f'(l * 2) + ({sldtbmht} * 4)',
            'description': 'Brush seal',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'guide': {
            'expression': '8',
            'description': 'Guide blocks',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'roller': {
            'expression': '4',
            'description': 'Rollers for sliding panels',
            'unit': 'nos',
            'constraints': {'min': 2, 'max': 20}
        },
        'lock': {
            'expression': '1',
            'description': 'Lock mechanism',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'silicon': {
            'expression': '1.5',
            'description': 'Silicon sealant',
            'unit': 'set',
            'constraints': {'min': 0}
        },
        'screw': {
            'expression': 'l * h',
            'description': 'Screws based on area',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'labour': {
            'expression': 'l * h',
            'description': 'Labour cost based on area',
            'unit': 'sqft',
            'constraints': {'min': 0}
        },
        'jali': {
            'expression': f'0.5 * l * {sldtbmht}',
            'description': 'Jali for half sliding section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jali_gasket': {
            'expression': f'l + ({sldtbmht} * 2)',
            'description': 'Jali gasket',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jali_angle': {
            'expression': '4',
            'description': 'Jali corner angles',
            'unit': 'nos',
            'constraints': {'min': 4}
        },
        'jali_handle': {
            'expression': '1',
            'description': 'Jali handle',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'jali_roller': {
            'expression': '2',
            'description': 'Jali rollers',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
    },
    
    "3_pnl_topbtmfix": {
        'topfr': {
            'expression': 'l',
            'description': 'Top frame full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'bottomfr': {
            'expression': 'l',
            'description': 'Bottom frame full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'sidefr': {
            'expression': 'h * 2',
            'description': 'Side frames both sides',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'topsht': {
            'expression': 'l',
            'description': 'Top shutter',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'bottomsht': {
            'expression': 'l',
            'description': 'Bottom shutter',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'sidesht': {
            'expression': f'{sldtbmht} * 2',
            'description': 'Side shutters for sliding section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'interlocksht': {
            'expression': f'{sldtbmht} * 4',
            'description': 'Interlocks for 3 panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '11b': {
            'expression': 'l * 2',
            'description': '11B profile (top and bottom)',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '13d': {
            'expression': 'l * 2',
            'description': '13D profile (top and bottom)',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '13': {
            'expression': f'{fixtbmht} * 2',
            'description': '13 profile for fixed sections',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '18': {
            'expression': f'{fixtbmht} * 2',
            'description': '18 profile for fixed sections',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'clip': {
            'expression': f'(l * 4) + ({fixtbmht} * 6)',
            'description': 'Clips for both fixed sections',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'glass': {
            'expression': 'l * h',
            'description': 'Total glass area',
            'unit': 'sqft',
            'constraints': {'min': 0}
        },
        'gasket': {
            'expression': '(l * 12) + (h * 12)',
            'description': 'Gasket for 3 panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'red_brush': {
            'expression': 'l * 2',
            'description': 'Red brush for tracks',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'brush': {
            'expression': f'(l * 2) + ({sldtbmht} * 4)',
            'description': 'Brush seal',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'guide': {
            'expression': '12',
            'description': 'Guide blocks for 3 panels',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'roller': {
            'expression': '4',
            'description': 'Rollers for sliding panels',
            'unit': 'nos',
            'constraints': {'min': 2, 'max': 20}
        },
        'lock': {
            'expression': '1',
            'description': 'Lock mechanism',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'silicon': {
            'expression': '2',
            'description': 'Silicon for 3 panels',
            'unit': 'set',
            'constraints': {'min': 0}
        },
        'screw': {
            'expression': 'l * h',
            'description': 'Screws based on area',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'labour': {
            'expression': 'l * h',
            'description': 'Labour cost based on area',
            'unit': 'sqft',
            'constraints': {'min': 0}
        },
        'jali': {
            'expression': f'(l * 0.33) + {sldtbmht}',
            'description': 'Jali for 1/3 section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jali_gasket': {
            'expression': f'(l * 0.66) + ({sldtbmht} * 2)',
            'description': 'Jali gasket',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jali_angle': {
            'expression': '4',
            'description': 'Jali corner angles',
            'unit': 'nos',
            'constraints': {'min': 4}
        },
        'jali_handle': {
            'expression': '1',
            'description': 'Jali handle',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'jali_roller': {
            'expression': '2',
            'description': 'Jali rollers',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
    },
    
    "4_pnl_topbtmfix": {
        'topfr': {
            'expression': 'l',
            'description': 'Top frame full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'bottomfr': {
            'expression': 'l',
            'description': 'Bottom frame full length',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'sidefr': {
            'expression': 'h * 2',
            'description': 'Side frames both sides',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'topsht': {
            'expression': 'l',
            'description': 'Top shutter',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'bottomsht': {
            'expression': 'l',
            'description': 'Bottom shutter',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'sidesht': {
            'expression': f'{sldtbmht} * 4',
            'description': 'Side shutters for 4 panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'interlocksht': {
            'expression': f'{sldtbmht} * 4',
            'description': 'Interlocks for 4 panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '11b': {
            'expression': 'l * 2',
            'description': '11B profile (top and bottom)',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '13d': {
            'expression': 'l * 2',
            'description': '13D profile (top and bottom)',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '13': {
            'expression': f'{fixtbmht} * 2',
            'description': '13 profile for fixed sections',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        '18': {
            'expression': f'{fixtbmht} * 3',
            'description': '18 profile for fixed sections',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'clip': {
            'expression': f'(l * 4) + ({fixtbmht} * 8)',
            'description': 'Clips for both fixed sections',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'jointsht': {
            'expression': f'{sldtbmht}',
            'description': 'Joint shutter',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'glass': {
            'expression': 'l * h',
            'description': 'Total glass area',
            'unit': 'sqft',
            'constraints': {'min': 0}
        },
        'gasket': {
            'expression': '(l * 12) + (h * 16)',
            'description': 'Gasket for 4 panels',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'red_brush': {
            'expression': 'l * 2',
            'description': 'Red brush for tracks',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'brush': {
            'expression': f'(l * 2) + ({sldtbmht} * 6)',
            'description': 'Brush seal',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'guide': {
            'expression': '16',
            'description': 'Guide blocks for 4 panels',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'roller': {
            'expression': '8',
            'description': 'Rollers for 4 panels',
            'unit': 'nos',
            'constraints': {'min': 4, 'max': 20}
        },
        'lock': {
            'expression': '2',
            'description': 'Lock mechanisms',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'silicon': {
            'expression': '2',
            'description': 'Silicon for 4 panels',
            'unit': 'set',
            'constraints': {'min': 0}
        },
        'screw': {
            'expression': 'l * h',
            'description': 'Screws based on area',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'labour': {
            'expression': 'l * h',
            'description': 'Labour cost based on area',
            'unit': 'sqft',
            'constraints': {'min': 0}
        },
        'jali': {
            'expression': f'l + (4 * {sldtbmht})',
            'description': 'Jali for sliding section',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jali_gasket': {
            'expression': f'l + ({sldtbmht} * 4)',
            'description': 'Jali gasket',
            'unit': 'ft',
            'constraints': {'min': 0}
        },
        'jali_angle': {
            'expression': '8',
            'description': 'Jali corner angles (double)',
            'unit': 'nos',
            'constraints': {'min': 4}
        },
        'jali_handle': {
            'expression': '2',
            'description': 'Jali handles',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
        'jali_roller': {
            'expression': '4',
            'description': 'Jali rollers',
            'unit': 'nos',
            'constraints': {'min': 0}
        },
    },
}