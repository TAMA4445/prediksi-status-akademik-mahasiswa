import streamlit as st
import joblib
import numpy as np
import pandas as pd

# 1. Konfigurasi halaman
st.set_page_config(page_title="Prediksi Dropout Mahasiswa", page_icon="🎓", layout="centered")

# 2. Load model, scaler, dan label encoder
@st.cache_resource
def load_models():
    model = joblib.load('model_dropout.pkl')
    scaler = joblib.load('scaler.pkl')
    le = joblib.load('label_encoder.pkl')
    return model, scaler, le

model, scaler, le = load_models()

# 3. Judul & deskripsi
st.title("Prediksi Status Akademik Mahasiswa")
st.write("Aplikasi ini memprediksi apakah seorang mahasiswa berpotensi **Dropout** atau **Graduate** berdasarkan nilai, kehadiran, status ekonomi, dan usia saat masuk kuliah.")

st.divider()

# 4. Form input
st.subheader("Masukkan Data Mahasiswa")

col1, col2 = st.columns(2)

with col1:
    admission_grade = st.number_input("Nilai Ujian Masuk (Admission Grade)", min_value=0.0, max_value=100.0, value=0.0)
    grade_sem1 = st.number_input("Rata-rata Nilai Semester gasal", min_value=0.0, max_value=100.0, value=0.0)
    grade_sem2 = st.number_input("Rata-rata Nilai Semester genap", min_value=0.0, max_value=100.0, value=0.0)
    approved_sem1 = st.number_input("Jumlah Mata Kuliah Lulus Semester gasal", min_value=0, max_value=30, value=0)
    approved_sem2 = st.number_input("Jumlah Mata Kuliah Lulus Semester genap", min_value=0, max_value=30, value=0)

with col2:
    attendance = st.selectbox("Waktu Kuliah", options=["Siang (Daytime)", "Malam (Evening)"])
    debtor = st.selectbox("Status Tunggakan (Debtor)", options=["Tidak", "Ya"])
    tuition_paid = st.selectbox("Uang Kuliah Sudah Lunas?", options=["Ya", "Tidak"])
    scholarship = st.selectbox("Penerima Beasiswa?", options=["Tidak", "Ya"])
    age = st.number_input("Usia Saat Masuk Kuliah", min_value=15, max_value=70, value=19)

st.divider()

# 5. Tombol prediksi
if st.button("Prediksi Sekarang", use_container_width=True):

    # Konversi input kategorikal ke format angka sesuai dataset asli
    attendance_val = 1 if attendance == "Siang (Daytime)" else 0
    debtor_val = 1 if debtor == "Ya" else 0
    tuition_val = 1 if tuition_paid == "Ya" else 0
    scholarship_val = 1 if scholarship == "Ya" else 0

    # Susun data sesuai urutan fitur saat training
    input_data = pd.DataFrame([[
        admission_grade,
        grade_sem1,
        grade_sem2,
        approved_sem1,
        approved_sem2,
        attendance_val,
        debtor_val,
        tuition_val,
        scholarship_val,
        age
    ]], columns=[
        'Admission grade',
        'Curricular units 1st sem (grade)',
        'Curricular units 2nd sem (grade)',
        'Curricular units 1st sem (approved)',
        'Curricular units 2nd sem (approved)',
        'Daytime/evening attendance',
        'Debtor',
        'Tuition fees up to date',
        'Scholarship holder',
        'Age at enrollment'
    ])

    # Scaling input sesuai scaler yang dipakai saat training
    input_scaled = scaler.transform(input_data)

    # Prediksi
    prediction = model.predict(input_scaled)[0]
    prediction_proba = model.predict_proba(input_scaled)[0]
    hasil_label = le.inverse_transform([prediction])[0]

    st.subheader("Hasil Prediksi")

    if hasil_label == "Dropout":
        st.error("⚠️ Mahasiswa berpotensi **DROPOUT**")
    else:
        st.success("✅ Mahasiswa berpotensi **LULUS (GRADUATE)**")

    # Tampilkan probabilitas
    st.write("Tingkat keyakinan model:")
    prob_df = pd.DataFrame({
        'Status': le.classes_,
        'Probabilitas': prediction_proba
    })
    st.bar_chart(prob_df.set_index('Status'))