import streamlit as st
import pandas as pd
import altair as alt

# ตั้งค่าหน้า Dashboard
st.set_page_config(page_title="ข้อมูลสถิติ", page_icon="📊", layout="wide")

# ✅ เช็ก query parameter ว่าเป็น mode=view หรือไม่
query_params = st.query_params
mode = query_params.get("mode", [""])[0]  # ดึงค่าพารามิเตอร์ mode

# ✅ อัปโหลดไฟล์ได้เฉพาะถ้าไม่ได้อยู่ในโหมด "view"
if mode != "view":
    uploaded_files = st.file_uploader("📂 อัปโหลดไฟล์ CSV", type=["csv"], accept_multiple_files=True)

    if not uploaded_files:
        st.warning("📌 กรุณาอัปโหลดไฟล์ CSV")
        st.stop()
else:
    uploaded_files = []  # ถ้าอยู่ในโหมด view ไม่ให้มีไฟล์ใหม่

# ✅ โหลดไฟล์ที่เคยอัปโหลด
if uploaded_files:
    for file in uploaded_files:
        df = pd.read_csv(file)

        # ✅ ลบช่องว่างจากชื่อคอลัมน์
        df.columns = df.columns.str.strip()

        if df.empty:
            st.error(f"⚠️ ไฟล์ **{file.name}** ไม่มีข้อมูล!")
            continue

        columns = df.columns.tolist()

        # ✅ ซ่อนตัวเลือก X และ Y เมื่อเป็นโหมด view
        if mode != "view":
            x_axis = st.selectbox(f"📌 เลือกแกน X ({file.name})", columns, key=f"x_{file.name}")
            y_axis = st.selectbox(f"📌 เลือกแกน Y ({file.name})", columns, key=f"y_{file.name}")
        else:
            x_axis, y_axis = columns[0], columns[1]  # ตั้งค่า X, Y อัตโนมัติ

        # ✅ ตรวจสอบว่า Y เป็นตัวเลข
        if not pd.api.types.is_numeric_dtype(df[y_axis]):
            st.error(f"⚠️ คอลัมน์ {y_axis} ต้องเป็นตัวเลขเท่านั้น!")
            continue

        df = df.sort_values(by=y_axis, ascending=False)

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X(x_axis, type='nominal', sort=df[x_axis].tolist()),
            y=alt.Y(y_axis, type='quantitative')
        ).properties(title=f"กราฟของ {file.name}", width=800, height=400)

        st.altair_chart(chart, use_container_width=True)

