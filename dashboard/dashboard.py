import streamlit as st
import pandas as pd
import plotly.express as px

# Load data mentah
@st.cache_data
def load_data():
    hour = pd.read_csv('dashboard/hour_clean.csv')
    day = pd.read_csv('dashboard/day_clean.csv')
    
    # Ubah tipe data
    hour['dteday'] = pd.to_datetime(hour['dteday'])
    day['dteday'] = pd.to_datetime(day['dteday'])
    
    # Ekstrak tahun
    hour['year'] = hour['dteday'].dt.year
    day['year'] = day['dteday'].dt.year
    
    # Mapping musim
    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    hour['season_name'] = hour['season'].map(season_map)
    day['season_name'] = day['season'].map(season_map)
    
    return hour, day

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
hour_df, day_df = load_data()

st.title("Dashboard Analisis Penyewaan Sepeda")

# Sidebar filters
st.sidebar.header("Filter Data")

# Filter tahun
years = st.sidebar.multiselect(
    "Pilih Tahun",
    options=sorted(hour_df['year'].unique()),
    default=sorted(hour_df['year'].unique())
)

# Filter musim
seasons = st.sidebar.multiselect(
    "Pilih Musim",
    options=['Spring', 'Summer', 'Fall', 'Winter'],
    default=['Spring', 'Summer', 'Fall', 'Winter']
)

# Filter tipe hari (berlaku untuk kedua chart)
workingday = st.sidebar.radio(
    "Tipe Hari",
    options=[0, 1],
    format_func=lambda x: "Libur" if x == 0 else "Kerja"
)

# Terapkan filter ke data per jam dan harian
filtered_hour = hour_df[
    (hour_df['year'].isin(years)) &
    (hour_df['season_name'].isin(seasons)) &
    (hour_df['workingday'] == workingday)
]

filtered_day = day_df[
    (day_df['year'].isin(years)) &
    (day_df['season_name'].isin(seasons)) &
    (day_df['workingday'] == workingday)
]

# --- Metrik Utama (menggunakan data per jam yang sudah difilter) ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Penyewaan", f"{filtered_hour['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata per Jam", f"{filtered_hour['cnt'].mean():.0f}")
with col3:
    st.metric("Rata-rata Registered/Jam", f"{filtered_hour['registered'].mean():.0f}")
with col4:
    st.metric("Rata-rata Casual/Jam", f"{filtered_hour['casual'].mean():.0f}")

st.markdown("---")

# --- Visualisasi 1: Pola Permintaan per Jam ---
st.subheader("Pola Permintaan per Jam")
hourly_avg = filtered_hour.groupby('hr')['cnt'].mean().reset_index()
fig1 = px.line(
    hourly_avg,
    x='hr',
    y='cnt',
    markers=True,
    title=f'Rata-rata Penyewaan per Jam ({ "Hari Kerja" if workingday==1 else "Hari Libur" })',
    labels={'hr': 'Jam', 'cnt': 'Rata-rata Penyewaan'}
)
fig1.update_xaxes(dtick=1)
st.plotly_chart(fig1, width='stretch')

# --- Visualisasi 2: Pengaruh Cuaca per Musim ---
st.subheader("Pengaruh Cuaca di Setiap Musim")
weather_musim = filtered_day.groupby(['season_name', 'weathersit'])['cnt'].mean().reset_index()

# Mapping deskripsi cuaca
weather_desc = {1: 'Cerah', 2: 'Berkabut', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}
weather_musim['weather_desc'] = weather_musim['weathersit'].map(weather_desc)

fig2 = px.bar(
    weather_musim,
    x='season_name',
    y='cnt',
    color='weather_desc',
    title=f'Rata-rata Penyewaan berdasarkan Cuaca dan Musim ({ "Hari Kerja" if workingday==1 else "Hari Libur" })',
    labels={'season_name': 'Musim', 'cnt': 'Rata-rata Penyewaan', 'weather_desc': 'Kondisi Cuaca'},
    barmode='group'
)
st.plotly_chart(fig2, width='stretch')

# Opsional: tampilkan data mentah
if st.checkbox("Tampilkan data mentah (per jam)"):
    st.dataframe(filtered_hour)