import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# Load Data
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

# Preprosesing
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

season_map = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
weather_map = {1: 'Clear', 2: 'Cloudy', 3: 'Rain'}
year_map = {0: 2011, 1: 2012}

day_df['season'] = day_df['season'].map(season_map)
day_df['weathersit'] = day_df['weathersit'].map(weather_map)
day_df['yr'] = day_df['yr'].map(year_map)

hour_df['season'] = hour_df['season'].map(season_map)
hour_df['weathersit'] = hour_df['weathersit'].map(weather_map)
hour_df['yr'] = hour_df['yr'].map(year_map)

# Title
st.markdown("# Bike Sharing Dashboard")
st.markdown("### Analisis Penyewaan Sepeda")
st.markdown("*Eksplorasi pola penyewaan sepeda berdasarkan waktu, musim, dan kondisi cuaca*")
st.divider()

#Dataset
st.subheader("Dataset")
st.dataframe(day_df)

# Sidebar Filters
st.sidebar.markdown("## Filter Data")

selected_year = st.sidebar.multiselect(
    "Pilih Tahun",
    options=sorted(day_df['yr'].unique()),
    default=sorted(day_df['yr'].unique())
)

selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    options=day_df['season'].unique(),
    default=day_df['season'].unique()
)

date_range = st.sidebar.date_input(
    "Rentang Tanggal",
    [day_df['dteday'].min(), day_df['dteday'].max()]
)

selected_hours = st.sidebar.slider(
    "Rentang Jam",
    0, 23, (0, 23)
)


# Filter data
filtered_day = day_df[
    (day_df['yr'].isin(selected_year)) &
    (day_df['season'].isin(selected_season))
]

if len(date_range) == 2:
    filtered_day = filtered_day[
        (filtered_day['dteday'] >= pd.to_datetime(date_range[0])) &
        (filtered_day['dteday'] <= pd.to_datetime(date_range[1]))
    ]

filtered_hour = hour_df[
    (hour_df['hr'] >= selected_hours[0]) &
    (hour_df['hr'] <= selected_hours[1])
]

if filtered_day.empty or filtered_hour.empty:
    st.warning("Data tidak tersedia untuk filter yang dipilih")
    st.stop()


# Metricts
st.markdown("## Ringkasan Utama")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Rata-rata Sewa",
        f"{int(filtered_day['cnt'].mean()):,}",
        delta="sepeda/hari"
    )

with col2:
    st.metric(
        "Total Sewa",
        f"{int(filtered_day['cnt'].sum()):,}",
        delta="keseluruhan"
    )

with col3:
    st.metric(
        "Hari Data",
        f"{filtered_day.shape[0]}",
        delta="hari"
    )

with col4:
    st.metric(
        "Rata-rata per Jam",
        f"{int(filtered_hour['cnt'].mean()):,}",
        delta="sepeda/jam"
    )

st.divider()

#Visualisasi berdasarkan pertanyaan
tab1, tab2, tab3 = st.tabs(["Musim", "Jam", "Cuaca"])

# TAB 1 - Musim
with tab1:
    st.subheader("Penyewaan Berdasarkan Musim")
    
    season_rent = filtered_day.groupby('season')['cnt'].mean().reset_index().sort_values('cnt', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(season_rent['season'], season_rent['cnt'], 
                   color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'], 
                   edgecolor='black', linewidth=1.5)
    
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontweight='bold')
    
    ax.set_title("Rata-rata Penyewaan per Musim", fontsize=14, fontweight='bold', pad=20)
    ax.set_ylabel("Rata-rata Jumlah Sewa", fontweight='bold')
    ax.set_xlabel("Musim", fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)

# TAB 2 - Jam 
with tab2:
    st.subheader("Pola Penyewaan per Jam")

    hour_rent = filtered_hour.groupby('hr')['cnt'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.fill_between(hour_rent['hr'], hour_rent['cnt'], alpha=0.3, color='#45B7D1')
    ax.plot(hour_rent['hr'], hour_rent['cnt'], marker='o', linewidth=2.5, 
            markersize=6, color='#0066cc')
    
    ax.set_title("Pola Penyewaan Sepeda per Jam", fontsize=14, fontweight='bold', pad=20)
    ax.set_ylabel("Rata-rata Jumlah Sewa", fontweight='bold')
    ax.set_xlabel("Jam", fontweight='bold')
    ax.grid(alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)

# TAB 3 - Cuaca
with tab3:
    st.subheader("Pengaruh Kondisi Cuaca")

    weather_rent = filtered_day.groupby('weathersit')['cnt'].mean().reset_index().sort_values('cnt', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(weather_rent['weathersit'], weather_rent['cnt'],
                color=['#2ECC71', '#3498DB', '#F39C12'],
                edgecolor='black', linewidth=1.5)

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height):,}',
            ha='center', va='bottom', fontweight='bold', fontsize=10)

    ax.set_title("Rata-rata Penyewaan Berdasarkan Cuaca", fontsize=14, fontweight='bold', pad=20)
    ax.set_ylabel("Rata-rata Jumlah Sewa", fontweight='bold')
    ax.set_xlabel("Kondisi Cuaca", fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

st.divider()

# hitung total penyewaan per tahun
st.markdown("## Total Penyewaan Pertahun")
year_total = day_df.groupby('yr')['cnt'].sum()

if set(year_total.index) <= set(year_map.values()):
    year_total.index = year_total.index.map({2011: '2011', 2012: '2012'})
else:
    year_total.index = year_total.index.astype(str)

fig_year, ax_year = plt.subplots(figsize=(10, 5))
ax_year.bar(year_total.index, year_total.values, color=['#4ECDC4', '#FF6B6B'], edgecolor='black', linewidth=1.2)

for i, value in enumerate(year_total.values):
    ax_year.text(i, value, f'{int(value):,}', ha='center', va='bottom', fontweight='bold')

ax_year.set_title("Total Penyewaan per Tahun", fontsize=14, fontweight='bold', pad=20)
ax_year.set_xlabel("Tahun", fontweight='bold')
ax_year.set_ylabel("Total Penyewaan", fontweight='bold')
ax_year.grid(axis='y', alpha=0.3)
plt.tight_layout()
st.pyplot(fig_year)

#Activity Cluster
def activity_cluster(hr):
    if 7 <= hr <= 9:
        return ' Morning Activity (7-9 AM)'
    elif 17 <= hr <= 19:
        return ' Evening Activity (5-7 PM)'
    elif 10 <= hr <= 16:
        return ' Daytime Activity (10 AM-4 PM)'
    else:
        return ' Low Activity'

hour_df['activity_cluster'] = hour_df['hr'].apply(activity_cluster)

st.markdown("## Cluster Aktivitas Berdasarkan Jam")

cluster_data = hour_df.groupby('activity_cluster')['cnt'].mean().reset_index().sort_values('cnt', ascending=False)

col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = plt.subplots(figsize=(10, 5))
    colors_cluster = ['#E74C3C', '#F39C12', '#27AE60', '#8E44AD']
    bars = ax.bar(range(len(cluster_data)), cluster_data['cnt'], 
                   color=colors_cluster[:len(cluster_data)],
                   edgecolor='black', linewidth=1.5)
    
   
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontweight='bold', fontsize=13)
    
    ax.set_xticks(range(len(cluster_data)))
    ax.set_xticklabels(cluster_data['activity_cluster'], fontweight='bold')
    ax.set_title("Rata-rata Sewa per Cluster Aktivitas", fontsize=13, fontweight='bold', pad=20)
    ax.set_ylabel("Rata-rata Jumlah Sewa", fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.markdown("### Summary")
    for idx, row in cluster_data.iterrows():
        st.metric(
            row['activity_cluster'],
            f"{int(row['cnt']):,}",
            help="Rata-rata penyewaan"
        )

st.divider()

# FOOTER
st.markdown("""
---
<div style='text-align: center'>
    <p style='color: #666; font-size: 12px;'>
    🚲 Dashboard Analisis Bike Sharing Dataset | Data dari 2011-2012
    </p>
</div>
""", unsafe_allow_html=True)

