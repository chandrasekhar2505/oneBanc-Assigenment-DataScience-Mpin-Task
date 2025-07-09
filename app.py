

import streamlit as st
from validator import evaluate_mpin
from datetime import date

# ---- Streamlit UI ----

st.title("🔐 MPIN Strength Validator")
st.markdown("Check if your 4 or 6-digit MPIN is secure or easily guessable.")

mpin = st.text_input("Enter your MPIN (4 or 6 digits)", max_chars=6)

col1, col2 = st.columns(2)
with col1:
    self_dob = st.date_input("Your DOB", value=None, min_value=date(1950, 1, 1))
with col2:
    spouse_dob = st.date_input("Spouse's DOB", value=None, min_value=date(1950, 1, 1))

anniversary = st.date_input("Wedding Anniversary", value=None, min_value=date(1950, 1, 1))

if st.button("Validate MPIN"):
    if not mpin.isdigit() or len(mpin) not in [4, 6]:
        st.error("Please enter a valid 4 or 6-digit numeric MPIN.")
    else:
        strength, reasons = evaluate_mpin(
            mpin,
            self_dob.isoformat() if self_dob else None,
            spouse_dob.isoformat() if spouse_dob else None,
            anniversary.isoformat() if anniversary else None
        )
        st.subheader(f"Result: **{strength}**")
        if reasons:
            st.write("Reasons for WEAK MPIN:")
            st.code(reasons)
        else:
            st.success("Your MPIN is strong and doesn't match any common or personal patterns.")
