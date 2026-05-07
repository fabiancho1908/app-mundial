import streamlit as st
import sqlite3
import pandas as pd

# 1. Configuración de Estilo y Base de Datos
st.set_page_config(page_title="Figuritas 2026", page_icon="⚽", layout="centered")

conn = sqlite3.connect('laminas.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS intercambio 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT, ciudad TEXT, repetida TEXT, contacto TEXT)''')
conn.commit()

# Estilo visual estilo APK
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #8D1B3D; color: white; height: 3em; font-weight: bold; }
    .card { border-radius: 15px; padding: 15px; background-color: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; border-left: 10px solid #8D1B3D; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Figuritas Mundial 2026")

# 2. Navegación por pestañas
tab1, tab2 = st.tabs(["➕ Publicar", "🔍 Buscar Cambios"])

with tab1:
    st.subheader("Registra tus repetidas")
    with st.form("registro_form"):
        u_nombre = st.text_input("Tu Nombre")
        u_ciudad = st.selectbox("📍 Ciudad", ["Bogotá", "Medellín", "Cali", "Barranquilla", "Bucaramanga", "Otra"])
        u_lamina = st.text_input("Número (Ej: ARG 10)").upper()
        u_cel = st.text_input("WhatsApp (Solo números)")
        if st.form_submit_button("✨ ¡PUBLICAR AHORA!"):
            if u_nombre and u_lamina and u_cel:
                c.execute('INSERT INTO intercambio (usuario, ciudad, repetida, contacto) VALUES (?,?,?,?)', (u_nombre, u_ciudad, u_lamina, u_cel))
                conn.commit()
                st.success("¡Lámina publicada!")
                st.rerun()

with tab2:
    st.subheader("Encuentra coleccionistas")
    df = pd.read_sql_query("SELECT * FROM intercambio", conn)
    
    if not df.empty:
        f_ciudad = st.selectbox("Filtrar por Ciudad", ["Todas"] + sorted(df['ciudad'].unique().tolist()))
        f_busq = st.text_input("🔎 ¿Cuál buscas?").upper()

        res = df
        if f_ciudad != "Todas": res = res[res['ciudad'] == f_ciudad]
        if f_busq: res = res[res['repetida'].str.contains(f_busq, na=False)]

        for i, fila in res.iterrows():
            st.markdown(f"""
                <div class="card">
                    <h2 style="margin:0; color:#8D1B3D;">{fila['repetida']}</h2>
                    <p style="margin:5px 0;">📍 {fila['ciudad']} | 👤 {fila['usuario']}</p>
                    <a href="https://wa.me{fila['contacto']}" target="_blank" style="color:#25d366; text-decoration:none; font-weight:bold;">📲 CONTACTAR WHATSAPP</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aún no hay láminas. ¡Sé el primero en publicar!")
