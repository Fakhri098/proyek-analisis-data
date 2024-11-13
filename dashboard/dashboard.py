import streamlit as st
import pandas as pd
import matplotlib as plt
import seaborn as sns

# Mengatur judul aplikasi
st.title("Dashboard Analisis Penyewaan Sepeda")

# Mengimpor data
data = pd.read_csv("main_data.csv")

# Menampilkan beberapa data untuk referensi
st.write("Data Penyewaan Sepeda")
st.write(data.head())

# Sidebar untuk memilih pertanyaan bisnis
st.sidebar.title("Analisis Pertanyaan Bisnis")
analysis_option = st.sidebar.selectbox(
    "Pilih Pertanyaan untuk Analisis:",
    ["Pertanyaan 1: Tren Penyewaan Berdasarkan Musim", 
     "Pertanyaan 2: Pengaruh Faktor Lingkungan terhadap Penyewaan"]
)

# Pertanyaan 1: Mengetahui tren penyewaan sepeda berdasarkan musim
if analysis_option == "Pertanyaan 1: Tren Penyewaan Berdasarkan Musim":
    st.header("Analisis Tren Penyewaan Berdasarkan Musim")

    # Memeriksa apakah kolom 'season_x' dan 'cnt' ada dan tidak memiliki nilai null
    if 'season_x' in data.columns and 'cnt' in data.columns:
        if data['season_x'].isnull().sum() == 0 and data['cnt'].isnull().sum() == 0:
            avg_season = data.groupby("season_x")["cnt"].mean()

            # Visualisasi rata-rata penyewaan per musim
            fig, ax = plt.subplots()
            avg_season.plot(kind='bar', color=['#4a90e2', '#50e3c2', '#e74c3c', '#f1c40f'], ax=ax)
            ax.set_title("Rata-Rata Penyewaan Sepeda per Musim")
            ax.set_xlabel("Musim")
            ax.set_ylabel("Rata-Rata Penyewaan (cnt)")
            st.pyplot(fig)

            # Deskripsi hasil
            st.write("Musim dengan rata-rata penyewaan tertinggi dapat membantu perusahaan "
                     "untuk mempersiapkan lebih banyak sepeda pada musim tersebut.")
        else:
            st.error("Data memiliki nilai kosong di kolom 'season_x' atau 'cnt'. Harap periksa data Anda.")
    else:
        st.error("Kolom 'cnt' atau 'season_x' tidak ditemukan dalam data.")

# Pertanyaan 2: Mengetahui pengaruh faktor lingkungan terhadap penyewaan
elif analysis_option == "Pertanyaan 2: Pengaruh Faktor Lingkungan terhadap Penyewaan":
    st.header("Pengaruh Faktor Lingkungan terhadap Penyewaan Sepeda")

    if all(col in data.columns for col in ['cnt', 'temp', 'hum', 'windspeed']):
        # Menghitung korelasi antara jumlah penyewaan dan faktor lingkungan
        correlations = data[['cnt', 'temp', 'hum', 'windspeed']].corr()
        st.write("Korelasi antara jumlah penyewaan dan faktor lingkungan:")
        st.write(correlations['cnt'].sort_values(ascending=False))

        # Visualisasi hubungan antara variabel lingkungan dan penyewaan
        plt.figure(figsize=(10, 15))
        sns.set(style="whitegrid")

        # Scatter plot antara suhu dan jumlah penyewaan dengan garis regresi
        plt.subplot(3, 1, 1)
        sns.regplot(data=data, x='temp', y='cnt', scatter_kws={'alpha':0.3}, line_kws={'color':'red'})
        plt.title('Hubungan antara Suhu dan Jumlah Penyewaan (Harian)')
        plt.xlabel('Suhu (°C)')
        plt.ylabel('Jumlah Penyewaan')

        # Scatter plot antara kelembaban dan jumlah penyewaan dengan garis regresi
        plt.subplot(3, 1, 2)
        sns.regplot(data=data, x='hum', y='cnt', scatter_kws={'alpha':0.3}, line_kws={'color':'blue'})
        plt.title('Hubungan antara Kelembaban dan Jumlah Penyewaan (Harian)')
        plt.xlabel('Kelembaban (%)')
        plt.ylabel('Jumlah Penyewaan')

        # Scatter plot antara kecepatan angin dan jumlah penyewaan dengan garis regresi
        plt.subplot(3, 1, 3)
        sns.regplot(data=data, x='windspeed', y='cnt', scatter_kws={'alpha':0.3}, line_kws={'color':'green'})
        plt.title('Hubungan antara Kecepatan Angin dan Jumlah Penyewaan (Harian)')
        plt.xlabel('Kecepatan Angin')
        plt.ylabel('Jumlah Penyewaan')
        
        plt.tight_layout()
        st.pyplot(plt)

        # RFM sederhana dengan pengelompokan bulanan
        data['month'] = pd.to_datetime(data['dteday']).dt.month
        rfm_df = data.groupby('month').agg({
            'cnt': 'sum',
            'temp': 'mean',
            'hum': 'mean',
            'windspeed': 'mean'
        }).reset_index()

        # Visualisasi RFM sederhana: Bulanan Jumlah Penyewaan dan Kondisi Cuaca Rata-rata
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=rfm_df, x='month', y='cnt', color='#4a90e2', label='Total Penyewaan', ax=ax)
        ax.plot(rfm_df['month'] - 1, rfm_df['temp'] * 100, color='red', marker='o', linestyle='--', label='Rata-rata Suhu x 100')
        ax.plot(rfm_df['month'] - 1, rfm_df['hum'] * 100, color='blue', marker='o', linestyle='--', label='Rata-rata Kelembaban x 100')
        ax.plot(rfm_df['month'] - 1, rfm_df['windspeed'] * 100, color='green', marker='o', linestyle='--', label='Rata-rata Kecepatan Angin x 100')
        ax.set_title("Analisis RFM Sederhana: Bulanan Penyewaan dan Kondisi Cuaca Rata-rata")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Jumlah Penyewaan")
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("Kolom 'cnt', 'temp', 'hum', atau 'windspeed' tidak ditemukan dalam data.")
