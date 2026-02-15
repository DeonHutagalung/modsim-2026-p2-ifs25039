import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Dashboard Kuesioner",
    layout="wide"
)

# =====================================
# LOAD DATA
# =====================================

file = "data_kuesioner.xlsx"
df = pd.read_excel(file)

pertanyaan_cols = df.columns[1:]

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("📊 Dashboard Kuesioner")

selected_questions = st.sidebar.multiselect(
    "Filter Pertanyaan",
    pertanyaan_cols,
    default=pertanyaan_cols
)

# ===== CREATOR CARD (Nama + Github) =====

st.sidebar.markdown("---")

st.sidebar.markdown("""
<div style="background-color:#f5f5f5;
padding:15px;
border-radius:12px">

<h4>👨‍💻 Creator</h4>

<b>Deon</b><br>

<a href="https://github.com/settings/profile" target="_blank">
🔗 GitHub Profile
</a>

</div>
""", unsafe_allow_html=True)

# =====================================
# DATA PREPARATION
# =====================================

df_long = df.melt(
    id_vars=["Partisipan"],
    value_vars=selected_questions,
    var_name="Pertanyaan",
    value_name="Jawaban"
)

# Mapping Likert Score
score_map = {
    "SS":5,
    "S":4,
    "CS":3,
    "CTS":2,
    "TS":2,
    "STS":1
}

df_long["Skor"] = df_long["Jawaban"].map(score_map)

# Kategori jawaban
def kategori(j):
    if j in ["SS","S"]:
        return "Positif"
    elif j == "CS":
        return "Netral"
    else:
        return "Negatif"

df_long["Kategori"] = df_long["Jawaban"].apply(kategori)

# =====================================
# HEADER
# =====================================

st.title("📈 Visualisasi Data Kuesioner")

# =====================================
# ROW 1
# =====================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("📊 Distribusi Jawaban")

    dist = df_long["Jawaban"].value_counts().reset_index()
    dist.columns = ["Jawaban","Jumlah"]

    fig_bar = px.bar(dist,x="Jawaban",y="Jumlah")

    st.plotly_chart(fig_bar,use_container_width=True)

with col2:

    st.subheader("🥧 Proporsi Jawaban")

    fig_pie = px.pie(dist,names="Jawaban",values="Jumlah")

    st.plotly_chart(fig_pie,use_container_width=True)

# =====================================
# ROW 2
# =====================================

col3, col4 = st.columns(2)

with col3:

    st.subheader("📚 Distribusi per Pertanyaan")

    stacked = df_long.groupby(["Pertanyaan","Jawaban"]).size().reset_index(name="Jumlah")

    fig_stack = px.bar(
        stacked,
        x="Pertanyaan",
        y="Jumlah",
        color="Jawaban"
    )

    st.plotly_chart(fig_stack,use_container_width=True)

with col4:

    st.subheader("⭐ Rata-rata Skor")

    avg = df_long.groupby("Pertanyaan")["Skor"].mean().reset_index()

    fig_avg = px.bar(avg,x="Pertanyaan",y="Skor")

    st.plotly_chart(fig_avg,use_container_width=True)

# =====================================
# ROW 3
# =====================================

col5, col6 = st.columns(2)

with col5:

    st.subheader("😊 Kategori Jawaban")

    kat = df_long["Kategori"].value_counts().reset_index()
    kat.columns=["Kategori","Jumlah"]

    fig_kat = px.bar(kat,x="Kategori",y="Jumlah")

    st.plotly_chart(fig_kat,use_container_width=True)

with col6:

    st.subheader("🔥 BONUS — Heatmap Korelasi")

    df_score = df[selected_questions].replace(score_map)

    corr = df_score.corr()

    fig_heat = px.imshow(corr)

    st.plotly_chart(fig_heat,use_container_width=True)
