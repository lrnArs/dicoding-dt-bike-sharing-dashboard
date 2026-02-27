# Bike Sharing Data Analysis Project

## Cara Menjalankan Dashboard

1. Pastikan Python 3.8 atau lebih baru sudah terinstal.
2. Install semua dependensi dengan perintah: pip install -r requirements.txt 
3. Jalankan aplikasi Streamlit: streamlit run dashboard/dashboard.py
4. Dashboard akan terbuka di browser Anda.

## Struktur Proyek

- `data/` : berisi dataset asli `day.csv` dan `hour.csv`
- `dashboard/` : berisi file data olahan dan kode dashboard
- `notebook.ipynb` : analisis data lengkap
- `README.md` : dokumentasi ini
- `requirements.txt` : daftar library
- `url.txt` : tautan jika di-deploy online

## Deskripsi

Proyek ini menganalisis pola penyewaan sepeda di Washington D.C. tahun 2011-2012 menggunakan data per jam dan harian. Dua pertanyaan utama dijawab:
- Pola permintaan per jam pada hari kerja vs libur.
- Pengaruh cuaca terhadap penyewaan di setiap musim.

Dashboard interaktif dibuat dengan Streamlit untuk memudahkan eksplorasi.