
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Beban Kerja Guru", layout="wide")

# Load data
df = pd.read_csv("beban_kerja_guru.csv")

# Kira skor beban kerja
df['Jumlah_Tugas'] = df['Tugas_Tambahan'].apply(lambda x: len(x.split(',')) if pd.notna(x) else 0)
df['Skor_Beban'] = df['Jam_Mingguan'] + (df['Jumlah_Tugas'] * 2)

st.title("📊 Dashboard Beban Kerja Guru")

# Pilih sekolah
sekolah = st.selectbox("Pilih Sekolah", df['Sekolah'].unique())
df_sekolah = df[df['Sekolah'] == sekolah]

# Bar chart: Jam Pengajaran Mingguan
fig1 = px.bar(df_sekolah, x="Nama_Guru", y="Jam_Mingguan", title="Jam Pengajaran Mingguan")
st.plotly_chart(fig1, use_container_width=True)

# Pie chart: Beban kerja tinggi vs biasa
beban_tinggi = df_sekolah[df_sekolah['Skor_Beban'] > 25]
fig2 = px.pie(values=[len(beban_tinggi), len(df_sekolah) - len(beban_tinggi)],
              names=["Beban Tinggi", "Biasa"],
              title="Peratus Guru Mengikut Tahap Beban")
st.plotly_chart(fig2, use_container_width=True)

# Papar jadual
st.subheader("Maklumat Penuh Guru")
st.dataframe(df_sekolah)

# Fungsi syor agihan tugas
def syor_agihan_tugas(df, ambang_tinggi=25, ambang_rendah=20):
    cadangan = []
    guru_terbeban = df[df['Skor_Beban'] > ambang_tinggi]
    guru_kurang_beban = df[df['Skor_Beban'] < ambang_rendah]

    for _, row in guru_terbeban.iterrows():
        nama = row['Nama_Guru']
        tugas = row['Tugas_Tambahan'].split(', ') if pd.notna(row['Tugas_Tambahan']) else []

        if len(tugas) == 0 or guru_kurang_beban.empty:
            continue

        for t in tugas:
            calon = guru_kurang_beban.sample(1).iloc[0]
            cadangan.append({
                "Tugas": t,
                "Asal": nama,
                "Dicadang_Kepada": calon["Nama_Guru"],
                "Sekolah": row["Sekolah"]
            })

    return pd.DataFrame(cadangan)

# Butang jana cadangan
if st.button("Jana Pengesyoran Tugas Semula"):
    syor_df = syor_agihan_tugas(df_sekolah)
    if syor_df.empty:
        st.info("Tiada cadangan semula — beban kerja seimbang.")
    else:
        st.subheader("📌 Cadangan Agihan Semula Tugas")
        st.dataframe(syor_df)
