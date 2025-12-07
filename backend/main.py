from fastapi import FastAPI
from pydantic import BaseModel
from estimator import get_estimator_by_design
from config import MATERIAL_RATES
from typing import List

app = FastAPI()

class DesignInput(BaseModel):
    design: str
    series: str
    quality: str
    width: float
    height: float
    quantity: int

class EstimateRequest(BaseModel):
    items: List[DesignInput]
    

@app.post("/estimate_int")
def calculate_estimate(request: EstimateRequest):
    estimator = get_estimator_by_design(request.design, MATERIAL_RATES)
    result = estimator.estimate(request.series, request.quality, request.width_ft, request.height_ft, request.quantity)
    return result

@app.post("/estimate")
def estimate_all(req: EstimateRequest):
    results = []
    grand_total = 0
    grand_area = 0
    total_qty = 0

    for idx, item in enumerate(req.items,start=1):
        estimator = get_estimator_by_design(item.design, MATERIAL_RATES)
        data = estimator.estimate(item.series, item.quality, item.width, item.height, item.quantity)

        t_area = item.width * item.height
        unit_rate = data['total_cost'] / t_area if t_area!=0 else 0
        amount = unit_rate *t_area

        results.append({
            'S.No.': idx,
            'Particulars': item.design,
            'Length(ft)': item.width,
            'Height(ft)': item.height,
            'Qnty': item.quantity,
            'T.Area': t_area,
            'Unit Rate': unit_rate,
            'Amount': amount
        })
        grand_total += amount
        grand_area += t_area
        total_qty += item.quantity

        summary = {
        'Total Qnty': total_qty,
        'Total Area': grand_area,
        'Avg Unit Rate': round(grand_total / grand_area, 2) if grand_area != 0 else 0,
        'Grand Total': round(grand_total, 2)
    }
        
    return {'details': results, 'summary': summary}