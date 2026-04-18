# Bike Sharing Dashboard

## Deskripsi
Dashboard interaktif untuk analisis data penyewaan sepeda menggunakan Streamlit. Dashboard ini menyajikan berbagai visualisasi dan insights dari data penyewaan sepeda tahun 2011-2012, termasuk analisis berdasarkan musim, waktu (per jam), dan kondisi cuaca.

## Fitur Utama

- **Filter Data Dinamis**: Filter berdasarkan tahun, musim, rentang tanggal, dan rentang jam
- **Ringkasan Utama**: Menampilkan metrik kunci seperti rata-rata sewa, total sewa, jumlah hari data, dan rata-rata per jam
- **Visualisasi Berdasarkan Musim**: Bar chart menunjukkan pola penyewaan untuk setiap musim
- **Analisis Per Jam**: Line chart dengan area fill untuk melihat pola penyewaan setiap jam dalam sehari
- **Pengaruh Cuaca**: Bar chart menunjukkan dampak kondisi cuaca terhadap jumlah penyewaan
- **Total Penyewaan Per Tahun**: Perbandingan total penyewaan antara tahun 2011 dan 2012
- **Cluster Aktivitas**: Segmentasi aktivitas berdasarkan waktu (Morning, Evening, Daytime, Low Activity)


## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit App
```
streamlit run dashboard.py
```

## Dataset

### Deskripsi Data
Dataset berisi data penyewaan sepeda dari tahun 2011-2012 dengan dua tingkat agregasi:

- **day.csv**: Data agregat per hari
- **hour.csv**: Data agregat per jam

### Kolom Utama
- `dteday`: Tanggal
- `cnt`: Jumlah penyewaan (target)
- `season`: Musim (Winter, Spring, Summer, Fall)
- `yr`: Tahun (2011, 2012)
- `weathersit`: Kondisi cuaca (Clear, Cloudy, Rain)
- `hr`: Jam (untuk data per jam)
- `temp`: Temperatur
- `hum`: Kelembaban
- `windspeed`: Kecepatan angin

##  Library

- **pandas**: Data manipulation dan analisis
- **matplotlib**: Visualisasi dasar
- **seaborn**: Visualisasi statistik
- **streamlit**: Framework untuk membuat web app interaktif

Lihat `requirements.txt` untuk versi lengkap.

## 📝 Catatan

- Filter tanggal biasa digunakan untuk menganalisis tren dalam periode tertentu
- Cluster aktivitas membantu mengidentifikasi jam ramai dan jam sepi
- Data mencakup variabel cuaca, suhu, dan kelembaban yang dapat mempengaruhi jumlah penyewaan


