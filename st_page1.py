import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='Event Stream - Home Page', 
    layout='wide'
)

st.markdown(
"""
<style>
div[data-testid="stSidebarNav"] {display: none;}
.stButton > button {
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
""", 
unsafe_allow_html=True)

with st.sidebar:
    st.title('Event Streaming')
    st.divider()

    if st.button('**Profile Proyek**', width="stretch"):
        st.switch_page('st_page1.py')
    
    if st.button('**Hasil Distribusi Data**', width="stretch"):
        st.switch_page('pages/st_page2.py')
    
    if st.button('**EDA dengan Visualisasi**', width="stretch"):
        st.switch_page('pages/st_page3.py')

    if st.button('**Streaming Data Insights**', width="stretch"):
        st.switch_page('pages/st_page4.py')

st.title('Event Streaming')
st.divider()

st.write("""**Tujuan Proyek dari**
         streaming event ini dilakukan untuk melakukan monitoring terhadap
         keamanan data dengan memantau aktivitas pengguna dalam perusahaan secara real time
         untuk mendeteksi aktivitas yang mencurigakan terhadap sistem perusahaan.
         Sistem akan menghasilkan stream event yang memuat informasi pengguna, aset yang diakses, klasifikasi,
         serta risk score yang bisa digunakan untuk mendeteksi alert.
         """)
st.divider()

st.title("Konsep yang Digunakan")
st.divider()
st.markdown("""
1. **Data Discovery**: menemukan pola risiko dalam data melalui proses pre-processing, identifikasi user paling aktif, aset yang paling sering diakses, serta penyusunan data dictionary.

2. **Data Science**: melakukan Exploratory Data Analysis (EDA), membuat fitur analitik, membangun model klasifikasi/anomali, dan melakukan evaluasi model.

3. **Data Security**: mengidentifikasi pola risiko, membuat level alert keamanan, mensimulasikan streaming data, serta memberikan rekomendasi keamanan berdasarkan hasil analisis.
""")
st.divider()

st.write("""<p style= font-size: 30px;text-align:center;>Dataset yang Digunakan:</p>""", unsafe_allow_html=True)
st.write("""<p style= font-size: 22px; text-align:left;>Dataset 1</p>""", unsafe_allow_html=True)

header = ['asset_id', 'asset_type', 'data_classification']
df = pd.read_csv("assets.csv", names=header)
df = df.head(10)
st.dataframe(df)

st.markdown("""
1. **asset_id**: identitas unik dari aset yang akan diakses oleh user
            
2. **asset_type**: jenis aset yang diakses

3. **data_classification**: tingkat sensitivitas data pada aset
""")
st.divider()

st.write("""<p style= font-size: 22px; text-align:left;>Dataset 2</p>""", unsafe_allow_html=True)

header = ['user_id', 'employee_id', 'dept','role', 'clearance', 'location', 'status']
df = pd.read_csv("users.csv", names=header)
df = df.head(150)
st.dataframe(df)

st.markdown("""
1. **user_id**: identitas unik pengguna yang melakukan aktivitas
2. **employee_id**: identitas unik pekerja
3. **dept**: departemen tempat user bekerja
4. **role**: jabatan user dalam perusahaan
5. **clearance**: tingkatan user dalam mengakses sitem berdasarkan sensitivitas informasi
6. **location**: tempat user melakukan akses sitem
7. **status**: status user dalam perusahaan
""")
st.divider()

st.write("""<p style= font-size: 22px; text-align:left;>Dataset 3</p>""", unsafe_allow_html=True)

header = ['event_id', 'event_time','user_id', 'dept', 'role', 'device_type', 'source_ip', 'asset_id', 'asset_type' , 'data_classification', 'action', 'status' , 'bytes_out', 'records_accessed' , 'latency_ms' , 'risk_score', 'label', 'failed_login_count', 'alert_level']
df = pd.read_csv("event_alert_stream.csv", names=header)
df = df.head(100)
st.dataframe(df)

st.markdown("""
1. **event_id**: identitas unik yang dimiliki oleh event</li>
2. **event_time**: waktu terjadinya event untuk analisis kronologi aktivitas</li>
3. **user_id**: identitas unik yang dimiliki oleh setiap pengguna yang melakukan aktivitas</li>
4. **dept**: departemen tempat user bekerja</li>
5. **role**: jabatan user dalam perusahaan</li>
6. **device_type**: jenis perangkat yang digunakan untuk mengakses sistem</li>
7. **source_ip**: alamat ip pengguna saat mengakses sistem</li>
8. **asset_id**: identitas jenis aset yang diakses pengguna</li>
9. **asset_type:** : jenis aset yang diakses</li>
10. **data_classification**: tingkat klasfikasi data yang diakses</li>
11. **action**: jenis aktivitas yang dilakukan pengguna</li>
12. **status**: status hasil dari aktivitas</li>
13. **bytes_out**: jumlah data yang ditransfer keluar dari sistem</li>
14. **records_accessed** : jumlah data yang diakses dalam 1 aktivitas</li>
15. **latency_ms**: waktu sistem merespon terhadap aktivitas pengguna</li>
16. **risk_score**: risiko yang menunjukkan seberapa tinggi ancaman tindakan terhadap sistem</li>
17. **label**: kategori akhir suatu aktivitas</li>
18. **failed_login_count** : jumlah percobaan gagal login oleh pengguna</li>
19. **alert_level**: tingkat alert keamanan yang diberikan ke suatu aktivitas berdasarkan tingkat risikonya</li>
""")
