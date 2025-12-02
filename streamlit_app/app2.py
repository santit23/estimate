import streamlit as st
import requests
import pandas as pd

st.title("Aluminium Estimation Tool")

design = st.selectbox("Select Design", ["2panel", "3panel"])
series = st.selectbox("Select Series", ["90mm", "78mm"])
quality = st.selectbox("Select Quality", ["mount", "rohit"])
width_ft = st.number_input("Width (ft)", min_value=0.0, format="%.2f")
height_ft = st.number_input("Height (ft)", min_value=0.0, format="%.2f")
quantity = st.number_input("Quantity", min_value=0, format="%d")

if st.button("Estimate"):
    payload = {
        "design": design,
        "series": series,
        "quality": quality,
        "width_ft": width_ft,
        "height_ft": height_ft,
        "quantity": quantity
    }
    # response = requests.post("http://localhost:8000/estimate", json=payload)
    # if response.status_code == 200:
    #     st.json(response.json())
    # else:
    #     st.error("Error: " + response.text)
    try:
        response = requests.post("http://localhost:8000/estimate", json=payload)

        result = response.json()
        if response.status_code != 200:
            raise ValueError(f"Error: {result['detail']}")
        

        # Check if result is empty
        if not result or 'total_cost' not in result:
            raise ValueError("No estimate received from backend.")

        # ✅ Display in a readable table
        materials = result.copy()
        total_cost = materials.pop('total_cost')

        # Add width and height to each material row
        # for mat in materials:
        #     materials[mat]['length_ft'] = width_ft
        #     materials[mat]['height_ft'] = height_ft
        #     materials[mat]['quantity'] = quantity 

        df = pd.DataFrame.from_dict(materials, orient='index')
        df.reset_index(inplace=True)
        # df.columns = ['Material', 'Required (ft²/unit)', 'Rate (Rs)', 'Cost (Rs)']
        df.columns = ['Material', 'Required(ft^2/unit)', 'Rate(rs)', 'Total Cost']

        st.subheader("Material Estimate")
        st.table(df)

        st.subheader("Total Cost")
        st.success(f"₹ {round(total_cost, 2)}")

    except Exception as e:
        st.error(f"Error fetching estimate: {e}")