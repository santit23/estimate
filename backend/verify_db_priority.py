
import sys
import os

# Add paths
backend_dir = os.path.dirname(os.path.abspath(__file__))
estimate_dir = os.path.dirname(backend_dir)
sys.path.append(backend_dir)

from app.core.database import SessionLocal
from app.models.models import MaterialRate, User
from app.services.core_engine_service import calculate_estimate_with_core_engine
from config import MATERIAL_RATES

def verify():
    db = SessionLocal()
    try:
        # 1. Get a test user (assuming user_id 1 exists)
        user = db.query(User).first()
        if not user:
            print("No user found in DB. Please register first.")
            return

        series = "90mm"
        quality = "mount"
        material = "topfr"
        
        # Get JSON default price safely
        data = MATERIAL_RATES[series][quality]
        json_price = data.get('rates', {}).get(material) if 'rates' in data else data.get(material)
        
        test_price = 9999.0  # Obviously different from standard ~178

        print(f"--- Verification Test ---")
        print(f"JSON Default Price for {material}: ₹{json_price}")

        # 2. Add/Update rate in DB
        db_rate = db.query(MaterialRate).filter(
            MaterialRate.user_id == user.id,
            MaterialRate.series == series,
            MaterialRate.quality == quality,
            MaterialRate.material_name == material,
            MaterialRate.color == "mill"
        ).first()

        if db_rate:
            db_rate.rate = test_price
        else:
            db_rate = MaterialRate(
                user_id=user.id,
                series=series,
                quality=quality,
                color="mill",
                material_name=material,
                rate=test_price,
                unit="20ft",
                category="profile"
            )
            db.add(db_rate)
        db.commit()

        print(f"Injected DB Price: ₹{test_price}")

        # 3. Run Calculation
        result = calculate_estimate_with_core_engine(
            product_type="window",
            design="2panel",
            series=series,
            quality=quality,
            width=4,
            height=4,
            quantity=1,
            user_id=user.id,
            db=db,
            color="mill"
        )

        # 4. Check breakdown
        actual_price_used = 0
        for item in result['breakdown']:
            if item['item'] == material:
                actual_price_used = item['rate']
                break

        print(f"Price used in actual calculation: ₹{actual_price_used}")

        if actual_price_used == test_price:
            print("\nSUCCESS: The calculation used the DATABASE price!")
        else:
            print("\nFAILURE: The calculation still used the JSON price.")

    finally:
        db.close()

if __name__ == "__main__":
    verify()
