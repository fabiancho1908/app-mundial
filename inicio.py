import streamlit as st
import sqlite3
import pandas as pd

# 1. Configuración de Marca Mundial 2026
st.set_page_config(page_title="Álbum Panini 2026", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .main-header {
        background: linear-gradient(135deg, #612D8A 0%, #00A3E0 100%);
        padding: 20px;
        border-radius: 0px 0px 25px 25px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton>button {
        border-radius: 8px;
        border: 1px solid #612D8A;
        background-color: white;
        color: #612D8A;
        font-weight: bold;
        height: 50px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #D6FF00;
        color: #612D8A;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de Datos
conn = sqlite3.connect('panini_2026.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS intercambio (id INTEGER PRIMARY KEY, usuario TEXT, ciudad TEXT, seccion TEXT, numero TEXT, contacto TEXT)')
conn.commit()

# --- DATOS OFICIALES PANINI 2026 ---
secciones = {
    "✨ Especiales (FWC)": [f"FWC {i}" for i in range(1, 10)],
    "🏟️ Sedes y Estadios": [f"ST {i}" for i in range(1, 17)],
    "🇦🇷 Argentina": [str(i) for i in range(1, 21)],
    "🇧🇷 Brasil": [str(i) for i in range(1, 21)],
    "🇨🇴 Colombia": [str(i) for i in range(1, 21)],
    "🇲🇽 México": [str(i) for i in range(1, 21)],
    "🇺🇸 USA": [str(i) for i in range(1, 21)],
    "🇨🇦 Canadá": [str(i) for i in range(1, 21)],
    "🇪🇸 España": [str(i) for i in range(1, 21)],
    "🇫🇷 Francia": [str(i) for i in range(1, 21)],
    "🇩🇪 Alemania": [str(i) for i in range(1, 21)],
    "🇮🇹 Italia": [str(i) for i in range(1, 21)]
}

st.markdown('<div class="main-header"><h1>⚽ ÁLBUM PANINI 2026</h1><p>INTERCAMBIO OFICIAL</p></div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🗂️ MI ÁLBUM", "🤝 CAMBIOS", "📊 PROGRESO"])

with tab1:
    # Selector de Sección del Álbum
    seccion_actual = st.selectbox("📂 Selecciona una sección del álbum:", list(secciones.keys()))
    
    st.subheader(f"Láminas: {seccion_actual}")
    
    # Cuadrícula dinámica
    numeros = secciones[seccion_actual]
    cols = st.columns(4)
    for i, num in enumerate(numeros):
        with cols[i % 4]:
            if st.button(num, key=f"{seccion_actual}_{num}"):
                st.toast(f"Marcada como repetida: {seccion_actual} - {num}")

with tab2:
    st.subheader("🔄 Intercambios Realizados")
    with st.expander("➕ PUBLICAR REPETIDA"):
        with st.form("pub_form"):
            u_nom = st.text_input("Tu Nombre")
            u_ciu = st.text_input("Tu Ciudad")
            u_sec = st.selectbox("Sección", list(secciones.keys()))
            u_num = st.text_input("Número exacto")
            u_wha = st.text_input("WhatsApp de contacto")
            if st.form_submit_button("Publicar"):
                c.execute('INSERT INTO intercambio (usuario, ciudad, seccion, numero, contacto) VALUES (?,?,?,?,?)', 
                          (u_nom, u_ciu, u_sec, u_num, u_wha))
                conn.commit()
                st.success("¡Publicado!")
                st.rerun()

    # Mostrar cambios
    df = pd.read_sql_query("SELECT * FROM intercambio", conn)
    if not df.empty:
        for _, fila in df.iterrows():
            st.markdown(f"""
                <div style="border:1px solid #ddd; border-radius:10px; padding:15px; margin-bottom:10px; border-left: 8px solid #612D8A;">
                    <h4 style="margin:0;">{fila['seccion']} - {fila['numero']}</h4>
                    <p style="margin:5px 0; font-size:14px;">📍 {fila['ciudad']} | 👤 {fila['usuario']}</p>
                    <a href="https://wa.me{fila['contacto']}" style="text-decoration:none; color:#00A3E0; font-weight:bold;">📲 CONTACTAR</a>
                </div>
            """, unsafe_allow_html=True)

with tab3:
    st.subheader("Tu avance Panini")
    obtenidas = st.number_input("¿Cuántas láminas tienes ya?", 0, 980, 0)
    st.progress(obtenidas / 980)
    st.metric("Completado", f"{round((obtenidas/980)*100, 1)}%")
