import streamlit as st
import sqlite3
import pandas as pd

# Configuración Pro
st.set_page_config(page_title="Figuritas Pro 2026", page_icon="⚽", layout="centered")

# --- BASE DE DATOS ---
conn = sqlite3.connect('laminas.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS intercambio (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT, ciudad TEXT, repetida TEXT, contacto TEXT)')
conn.commit()

# --- DISEÑO CSS AVANZADO ---
st.markdown("""
    <style>
    /* Fondo y tipografía */
    .main { background-color: #f8f9fa; }
    
    /* Estilo de los Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff; border-radius: 10px 10px 0 0;
        padding: 10px 20px; font-weight: bold; color: #8D1B3D;
    }
    
    /* Botón Publicar */
    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background: linear-gradient(135deg, #8D1B3D 0%, #d32f2f 100%);
        color: white; border: none; font-size: 18px; font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Tarjetas de láminas (Cards) */
    .cromo-card {
        border-radius: 15px; padding: 20px; background: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        margin-bottom: 20px; border-top: 5px solid #8D1B3D;
        text-align: center;
    }
    
    .whatsapp-btn {
        background-color: #25d366; color: white !important;
        padding: 8px 15px; border-radius: 8px;
        text-decoration: none; font-weight: bold; display: inline-block;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Figuritas Mundial 2026")
st.write("Tu centro de intercambio profesional")

tab1, tab2 = st.tabs(["✨ PUBLICAR", "🔍 BUSCAR MATCH"])

with tab1:
    st.subheader("Registra tu repetida")
    with st.form("pro_form"):
        u_nombre = st.text_input("👤 Tu Nombre")
        u_ciudad = st.selectbox("📍 Ciudad", ["Bogotá", "Medellín", "Cali", "Barranquilla", "Bucaramanga", "Otra"])
        u_lamina = st.text_input("🆔 Número de Lámina (Ej: ARG 10)").upper()
        u_cel = st.text_input("📞 WhatsApp (Ej: 573001234567)")
        
        if st.form_submit_button("¡SUBIR AL ÁLBUM!"):
            if u_nombre and u_lamina and u_cel:
                c.execute('INSERT INTO intercambio (usuario, ciudad, repetida, contacto) VALUES (?,?,?,?)', (u_nombre, u_ciudad, u_lamina, u_cel))
                conn.commit()
                st.success("¡Lámina publicada con éxito!")
                st.rerun()

with tab2:
    df = pd.read_sql_query("SELECT * FROM intercambio", conn)
    
    # Buscador Pro
    col1, col2 = st.columns([1, 2])
    with col1:
        f_ciudad = st.selectbox("Filtrar Ciudad", ["Todas"] + sorted(df['ciudad'].unique().tolist()) if not df.empty else ["Todas"])
    with col2:
        f_busq = st.text_input("🔎 ¿Qué número buscas?").upper()

    if not df.empty:
        res = df
        if f_ciudad != "Todas": res = res[res['ciudad'] == f_ciudad]
        if f_busq: res = res[res['repetida'].str.contains(f_busq, na=False)]

        for i, fila in res.iterrows():
            st.markdown(f"""
                <div class="cromo-card">
                    <span style="color: #888; font-size: 12px; font-weight: bold;">MUNDIAL 2026</span>
                    <h1 style="margin: 0; color: #8D1B3D; font-size: 40px;">{fila['repetida']}</h1>
                    <p style="margin: 10px 0; color: #333;">📍 {fila['ciudad']} | 👤 {fila['usuario']}</p>
                    <a href="https://wa.me{fila['contacto']}" class="whatsapp-btn" target="_blank">📲 CONTACTAR</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("¡Sé el primero en publicar una lámina!")