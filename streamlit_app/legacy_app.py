# --- Streamlit Frontend ---
import streamlit as st
import requests
import pandas as pd
import io
import plotly.graph_objects as go

# Download Functions
# Excel
# Create a downloadable Excel file
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Estimate')
    processed_data = output.getvalue()
    return processed_data
# PDF
def generate_pdf_table(df):
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df[col] for col in df.columns],
                   fill_color='lavender',
                   align='left'))
    ])

    pdf_bytes = io.BytesIO()
    fig.write_image(pdf_bytes, format='pdf', width=1000, height=400 + len(df) * 20)
    pdf_bytes.seek(0)
    return pdf_bytes



st.title("Aluminium Fabrication Estimator")

# Form to input multiple design entries
st.subheader("Add Design Entries")
design_entries = []

with st.form("design_form"):
    design = st.selectbox("Design", ["2panel", "3panel"])  # Add more as needed
    series = st.selectbox("Select Series", ["90mm", "78mm"])
    quality = st.selectbox("Select Quality", ["mount", "rohit"])
    width = st.number_input("Width (ft)", min_value=0.0, format="%.2f")
    height = st.number_input("Height (ft)", min_value=0.0, format="%.2f")
    quantity = st.number_input("Quantity", min_value=1, format="%d")
    submitted = st.form_submit_button("Add to List")

    if submitted:
        st.session_state.design_items = st.session_state.get("design_items", [])
        st.session_state.design_items.append({
            "design": design,
            "series": series,
            "quality": quality,
            "width": width,
            "height": height,
            "quantity": quantity
        })
        st.success(f"Added {design} to estimate list.")

# Display added entries
if "design_items" in st.session_state and st.session_state.design_items:
    st.subheader("Designs to Estimate")
    st.write(pd.DataFrame(st.session_state.design_items))

    if st.button("Get Estimate"):
        try:
            response = requests.post(
                "http://localhost:8000/estimate",
                json={"items": st.session_state.design_items}
            )
            if response.status_code != 200:
                raise ValueError("Backend returned an error")
            

            
            data = response.json()
            details = pd.DataFrame(data["details"])
            summary = data["summary"]


            # Compute totals row
            totals_row = {
                "S.No.": "",
                "Particulars": "Total",
                "Length(ft)": "",
                "Height(ft)": "",
                "Qnty": summary["Total Qnty"],
                "T.Area": summary["Total Area"],
                "Unit Rate": f"{summary['Avg Unit Rate']}",
                "Amount": round(summary["Grand Total"], 2)
            }

            # Append to the main DataFrame
            details_with_total = pd.concat([details, pd.DataFrame([totals_row])], ignore_index=True)

            excel = to_excel(details_with_total)
            
            pdf_data = generate_pdf_table(details_with_total)

            st.subheader("Estimation Summary")
            st.table(details_with_total)
        #     st.dataframe(details.style.format(subset=["T.Area", "Unit Rate", "Amount"], formatter="{:.2f}"))

            st.download_button(
                label="Download Excel",
                data=excel,
                file_name="estimate.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.download_button(
                label="Download PDF",
                data=pdf_data,
                file_name="estimate.pdf",
                mime="application/pdf"
            )
            st.markdown("---")
            st.markdown("### Totals")
            st.markdown(f"**Total Quantity:** {summary['Total Qnty']}")
            st.markdown(f"**Total Area (ft²):** {summary['Total Area']}")
            st.markdown(f"**Average Unit Rate (Rs):** ₹{summary['Avg Unit Rate']}")
            st.markdown(f"**Grand Total (Rs):** ₹{summary['Grand Total']}")
        #     summary_df = pd.DataFrame([{
        #     "Total Quantity": summary["Total Qnty"],
        #     "Total Area (ft²)": round(summary["Total Area"], 2),
        #     "Avg Unit Rate (Rs)": round(summary["Avg Unit Rate"], 2),
        #     "Grand Total (Rs)": round(summary["Grand Total"], 2)
        # }])
        #     st.subheader("Summary Table")
        #     st.table(summary_df)

        except Exception as e:
            st.error(f"Failed to get estimate: {e}")
else:
    st.info("Add at least one design to begin estimation.")
