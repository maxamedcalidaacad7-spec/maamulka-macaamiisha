import streamlit as st
import pandas as pd
import os

# Magaca faylka xogta lagu kaydinayo
DB_FILE = "database.csv"

# Habaynta guud ee bogga
st.set_page_config(page_title="Maamulka Lacagta", layout="wide")

# Soo rar xogta haddii ay jirto, haddii kalena abuur mid cusub
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=["Taariikhda", "Macmiilka", "Total ($)", "Bixiyey ($)", "Baqiga ($)"])

st.title("📊 Maamulka Lacagaha Macaamiisha")

# --- QAYBTA SIDBARD-KA (Xog Gelinta) ---
with st.sidebar:
    st.header("➕ Ku dar Macmiil")
    with st.form("entry_form", clear_on_submit=True):
        magaca = st.text_input("Magaca Macmiilka")
        total = st.number_input("Lacagta Guud ($)", min_value=0.0)
        bixiyey = st.number_input("Lacagta la Bixiyey ($)", min_value=0.0)
        submit = st.form_submit_button("Keydi")
        
        if submit and magaca:
            baqi = total - bixiyey
            today = pd.Timestamp.now().strftime("%Y-%m-%d")
            new_data = pd.DataFrame([[today, magaca, total, bixiyey, baqi]], columns=df.columns)
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success(f"Waa la keydiyey {magaca}")
            st.rerun()

# --- QAYBTA DASHBOARD-KA (Metrics) ---
c1, c2, c3 = st.columns(3)
c1.metric("LACAGTA GUUD", f"${df['Total ($)'].sum():,.2f}")
c2.metric("INTA XEROOTAY", f"${df['Bixiyey ($)'].sum():,.2f}")
c3.metric("DEYNTA MAQAN", f"${df['Baqiga ($)'].sum():,.2f}")

# --- SHAXDA XOGTA ---
st.divider()
st.subheader("📋 Liiska Xogta")
st.dataframe(df, use_container_width=True)
