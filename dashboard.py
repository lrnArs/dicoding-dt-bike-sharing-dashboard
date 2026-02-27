import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
hourly = pd.read_csv('dashboard/hourly_pattern.csv')
season_weather = pd.read_csv('dashboard/season_weather.csv')

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("Dashboard Analisis Penyewaan Sepeda")

# Sidebar untuk filter
st.sidebar.header("Filter")
tipe_hari = st.sidebar.radio("Tipe Hari", options=[0, 1], format_func=lambda x: "Libur" if x == 0 else "Kerja")

# Filter data per jam berdasarkan tipe hari
hourly_filtered = hourly[hourly['workingday'] == tipe_hari]

# Metrik utama (diambil dari data asli, bisa juga ditampilkan statistik sederhana)
st.subheader("Ringkasan")
col1, col2, col3 = st.columns(3)
col1.metric("Rata-rata Penyewaan per Jam (hari terpilih)", f"{hourly_filtered['cnt'].mean():.0f}")
col2.metric("Jam Sibuk", f"{hourly_filtered.loc[hourly_filtered['cnt'].idxmax(), 'hr']}:00")
col3.metric("Jam Sepi", f"{hourly_filtered.loc[hourly_filtered['cnt'].idxmin(), 'hr']}:00")

# Visualisasi 1: Pola per jam
st.subheader("Pola Permintaan per Jam")
fig1 = px.line(hourly_filtered, x='hr', y='cnt', markers=True,
               title=f'Rata-rata Penyewaan per Jam ({ "Hari Kerja" if tipe_hari==1 else "Hari Libur" })')
fig1.update_xaxes(dtick=1)
st.plotly_chart(fig1, use_container_width=True)

# Visualisasi 2: Pengaruh cuaca per musim
st.subheader("Pengaruh Cuaca di Setiap Musim")
fig2 = px.bar(season_weather, x='season', y='cnt', color='weathersit',
              title='Rata-rata Penyewaan berdasarkan Cuaca dan Musim',
              labels={'season':'Musim', 'cnt':'Rata-rata Penyewaan', 'weathersit':'Kondisi Cuaca'})
st.plotly_chart(fig2, use_container_width=True)

# Tampilkan data mentah jika diinginkan
if st.checkbox("Tampilkan data mentah"):
    st.dataframe(hourly)