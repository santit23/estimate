# config_categories.py

# Map every single item key to a Category
ITEM_CATEGORY_MAP = {
    # === PROFILES (Aluminium) ===
    'topfr': 'profile',
    'bottomfr': 'profile',
    'sidefr': 'profile',
    'topsht': 'profile',
    'bottomsht': 'profile',
    'sidesht': 'profile',
    'interlocksht': 'profile',
    'jali_track': 'profile',
    'jali_sutter': 'profile', # Note: check spelling from your formulas
    '11b' : 'profile',
    '13d' : 'profile',
    '13' : 'profile',
    '18' : 'profile',
    'clip' : 'profile',

    # === LINEAR ACCESSORIES (Rubber/Brush) ===
    'gasket': 'linear',
    'brush': 'linear',
    'red_brush': 'linear',
    'jali_gasket': 'linear',

    # === AREA BASED ===
    'glass': 'area',
    'jali_net': 'area',
    'labour': 'area',

    # === HARDWARE (Count based) ===
    'roller': 'hardware',
    'lock': 'hardware',
    'guide': 'hardware',
    'jali_roller': 'hardware',
    'jali_angle': 'hardware',
    'jali_handle': 'hardware',
    

    'screw': 'consumable',
    'silicon': 'consumable',
}