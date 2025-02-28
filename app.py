import streamlit as st
import pandas as pd
import altair as alt

# ✅ ตรวจสอบโหมด (ดูค่า mode จาก URL)
query_params = st.query_params
mode = query_params.get("mode", [""])[0]

# ✅ ตั้งค่าหน้า Dashboard
st.set_page_config(page_title="Multi-File Dashboard", page_icon="📊", layout="wide")

st.title("📊 Multi-File Dashboard")

# ✅ ซ่อนตัวอัปโหลดไฟล์ถ้าเป็นโหมด "view"
if mode != "view":
    uploaded_files = st.file_uploader("📂 อัปโหลดไฟล์ CSV (หลายไฟล์ได้)", type=["csv"], accept_multiple_files=True)
else:
    uploaded_files = []  # ถ้าอยู่ในโหมด view ไม่ต้องให้ผู้ใช้เห็นตัวอัปโหลดไฟล์

# ✅ ตรวจสอบว่ามีไฟล์หรือไม่
if uploaded_files:
    for file in uploaded_files:
        df = pd.read_csv(file)

        if df.empty:
            st.error(f"⚠️ ไฟล์ **{file.name}** ไม่มีข้อมูล!")
            continue

        # ✅ ตั้งค่ากราฟ
        st.write(f"✅ **ไฟล์: {file.name}**")
        st.write(df.head())

        columns = df.columns.tolist()
        x_axis = st.selectbox(f"📌 เลือกแกน X ({file.name})", columns, key=f"x_{file.name}")
        y_axis = st.selectbox(f"📌 เลือกแกน Y ({file.name})", columns, key=f"y_{file.name}")

        chart_title = st.text_input(f"📝 ตั้งชื่อกราฟ ({file.name})", f"กราฟของ {file.name}")
        sort_order = st.checkbox(f"🔽 เรียงจากมากไปน้อย ({file.name})", value=True, key=f"sort_{file.name}")

        if x_axis and y_axis and pd.api.types.is_numeric_dtype(df[y_axis]):
            if sort_order:
                df = df.sort_values(by=y_axis, ascending=False)

            st.write(f"### {chart_title}")

            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(x_axis, type="ordinal", sort=df[x_axis].tolist()),
                y=alt.Y(y_axis, type="quantitative")
            ).properties(title=chart_title, width=800, height=400)

            st.altair_chart(chart, use_container_width=True)

