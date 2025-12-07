from typing import Dict, List
from config import MATERIAL_RATES


MATERIAL_FORMULAS = {
    'topfr': lambda l, h:l,
    'bottomfr': lambda l, h:l,
    'sidefr': lambda l, h:h*2,
    'topsht': lambda l, h:l,
    'bottomsht': lambda l, h:l,
    'sidesht': lambda l, h:h*2,
    'interlocksht': lambda l, h:h*2,
    'jali': lambda l, h:l+(h*2),
    'glass': lambda l, h: l*h,
    'gasket': lambda l, h: (l*4)+(h*8),
    'red_brush': lambda l, h: l*2,
    'brush': lambda l, h: l*2+h*5, 
    'guide': lambda l, h: MATERIAL_RATES['90mm']['mount']['guide'],
    'jali_gasket': lambda l, h: l+(h*2),
    'jali_angle': lambda l, h: MATERIAL_RATES['90mm']['mount']['jali_angle'],
    'jali_handle': lambda l, h: MATERIAL_RATES['90mm']['mount']['jali_handle'],
    'jali_roller': lambda l, h: MATERIAL_RATES['90mm']['mount']['jali_roller'],
    'roller': lambda l, h: MATERIAL_RATES['90mm']['mount']['roller'],
    'lock': lambda l, h: MATERIAL_RATES['90mm']['mount']['lock'],
    'silicon': lambda l, h: MATERIAL_RATES['90mm']['mount']['silicon'],
    'labour': lambda l, h: l*h,
    'screw': lambda l, h: MATERIAL_RATES['90mm']['mount']['screw'],
}
class MasterFormula:
    def get_master_formula(self):
        return MATERIAL_FORMULAS
    
def get_rates(series, quality, material, rates_config):
    try:
        return rates_config[series][quality][material]
    except KeyError:
        raise ValueError(f"Material {material} not found for series {series} and quality {quality}.")
    
class BaseEstimator(MasterFormula):
    def __init__(self, rate_config):
        self.rate_config = rate_config

    def get_formula(self,l, h):
        return self.get_master_formula()
    
    def get_required_materials(self):
        raise NotImplementedError("Each design must define required materials.")
    
    def estimate(self, series, quality, width_ft, height_ft, quantity):
        formulas = self.get_formula(width_ft, height_ft)
        result = {}
        total_cost = 0
        # get material dynamically
        materials = self.get_required_materials()
        for mat in materials:
            if mat not in formulas:
                raise ValueError(f"No formula for {mat} in {self.__class__.__name__}.")
            


            required = formulas[mat](width_ft, height_ft)*quantity
            rate = get_rates(series, quality, mat, self.rate_config)
            cost = required * rate


            result[mat] = {
                'required_ft': required,
                'rate': rate,
                'cost': cost
            }
            total_cost += cost
        result['total_cost'] = round(total_cost, 2)
        return result
    
class TwoPanel(BaseEstimator):
    def get_required_materials(self):
        return ['topfr', 'bottomfr', 'sidefr', 'topsht', 'bottomsht', 'sidesht', 'interlocksht', 'jali', 'glass', 'gasket', 'red_brush', 'brush', 'guide', 'jali_gasket', 'jali_angle', 'jali_handle', 'jali_roller', 'roller', 'lock', 'silicon', 'labour']

class ThreePanel(BaseEstimator):
    def get_required_materials(self):
        return ['topfr', 'bottomfr', 'sidefr', 'topsht', 'bottomsht', 'sidesht', 'interlocksht', 'jali', 'glass', 'gasket', 'red_brush', 'brush', 'guide', 'jali_gasket', 'jali_angle', 'jali_handle', 'jali_roller', 'roller', 'lock', 'silicon', 'labour']
    def get_formula(self, l, h):
        formula = self.get_master_formula()
        formula.update({
            'interlocksht': lambda l, h: h*4,  # Adjusted for three panels
            'jali': lambda l, h: (l*0.66)+(h*2),  # Adjusted for three panels
            'gasket': lambda l, h: (l*4)+(h*12),  # Adjusted for three panels
            'brush': lambda l, h: l*2+h*6,  # Adjusted for three panels
            'guide': lambda l, h: 12,  # Adjusted for three panels
            'jali_gasket': lambda l, h: (l*0.66)+(h*2),
            'silicon': lambda l, h: 1.5,  # Adjusted for three panels
            'screw': lambda l, h: 125 # rs
        })
        return formula
    
    
# test
def get_estimator_by_design(design, rates_config):
    estimators = {
        "2panel": TwoPanel,
        "3panel": ThreePanel,
    }
    if design not in estimators:
        raise ValueError(f"Unsupported design: {design}")
    return estimators[design](rates_config)
  
if __name__  == "__main__":
    rates_config = MATERIAL_RATES
    estimator = get_estimator_by_design("3panel", rates_config)
    result = estimator.estimate("90mm", "rohit", 5, 4, 1)  #  series, quality, width_ft, height_ft, quantity
    from pprint import pprint
    pprint(result)

