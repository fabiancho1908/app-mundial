import streamlit as st
import sqlite3
import pandas as pd

# 1. Configuración de Marca Mundial 2026
st.set_page_config(page_title="Figuritas Pro 2026", layout="centered")

# CSS Personalizado con Colores del Mundial 2026
st.markdown("""
    <style>
    /* Colores oficiales: Morado, Verde Lima y Azul */
    :root {
        --purple: #612D8A;
        --lime: #D6FF00;
        --blue: #00A3E0;
    }
    
    .stApp { background-color: #FFFFFF; }
    
    /* Encabezado con degradado mundialista */
    .main-header {
        background: linear-gradient(135deg, #612D8A 0%, #00A3E0 100%);
        padding: 20px;
        border-radius: 0px 0px 25px 25px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* Estilo de los números del álbum (Cromos) */
    .stButton>button {
        border-radius: 12px;
        border: 2px solid #612D8A;
        background-color: white;
        color: #612D8A;
        font-weight: bold;
        transition: 0.3s;
        height: 50px;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #D6FF00;
        border-color: #D6FF00;
        color: black;
    }

    /* Tarjetas de Intercambio */
    .swap-card {
        background: white;
        border-radius: 15px;
        padding: 15px;
        border-left: 8px solid #D6FF00;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 15px;
    }

    /* Barra de Navegación Inferior Fija */
    .nav-bottom {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #612D8A;
        display: flex;
        justify-content: space-around;
        padding: 12px;
        z-index: 1000;
        border-top: 3px solid #D6FF00;
    }
    .nav-item { color: white; font-size: 10px; text-align: center; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de Datos
conn = sqlite3.connect('laminas_pro.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS intercambio (id INTEGER PRIMARY KEY, usuario TEXT, ciudad TEXT, repetida TEXT, contacto TEXT)')
conn.commit()

# --- INTERFAZ ---
st.markdown('<div class="main-header"><h1>⚽ MUNDIAL 2026</h1><p>INTERCAMBIO COLOMBIA</p></div>', unsafe_allow_html=True)

# Pestañas al estilo de la app que mostraste
tab1, tab2, tab3 = st.tabs(["🗂️ MI ÁLBUM", "🤝 CAMBIOS", "📊 PROGRESO"])

with tab1:
    st.subheader("🇨🇴 Selección Colombia")
    # Generamos cuadrícula de 12 láminas de ejemplo
    laminas = [f"COL {i}" for i in range(1, 13)]
    cols = st.columns(4)
    for i, num in enumerate(laminas):
        with cols[i % 4]:
            if st.button(num, key=num):
                st.toast(f"¡Añadida a repetidas: {num}!")

with tab2:
    st.subheader("🔄 Intercambios en tu zona")
    ciudades_col = ["Bogotá", "Medellín", "Cali", "Barranquilla", "Bucaramanga", "Pereira", "Cúcuta", "Otra"]
    f_ciudad = st.selectbox("📍 Filtrar Ciudad", ciudades_col)
    
    # Formulario para publicar
    with st.expander("➕ PUBLICAR MI REPETIDA"):
        with st.form("pub"):
            u_nom = st.text_input("Nombre")
            u_lam = st.text_input("Número de lámina").upper()
            u_wha = st.text_input("WhatsApp")
            if st.form_submit_button("¡PUBLICAR!"):
                c.execute('INSERT INTO intercambio (usuario, ciudad, repetida, contacto) VALUES (?,?,?,?)', (u_nom, f_ciudad, u_lam, u_wha))
                conn.commit()
                st.success("¡Listo para cambiar!")
                st.rerun()

    # Mostrar cambios reales
    df = pd.read_sql_query("SELECT * FROM intercambio", conn)
    if not df.empty:
        for _, fila in df.iterrows():
            st.markdown(f"""
                <div class="swap-card">
                    <h3 style="margin:0; color:#612D8A;">{fila['repetida']}</h3>
                    <p style="margin:5px 0;">📍 {fila['ciudad']} | 👤 {fila['usuario']}</p>
                    <a href="https://wa.me{fila['contacto']}" style="color:#00A3E0; font-weight:bold; text-decoration:none;">📲 CONTACTAR</a>
                </div>
            """, unsafe_allow_html=True)

with tab3:
    st.subheader("Tu Camino al Éxito")
    val = st.slider("¿Cuántas láminas tienes ya?", 0, 980, 150)
    porcentaje = round((val / 980) * 100, 1)
    st.metric("Progreso Total", f"{porcentaje}%")
    st.progress(val / 980)
    st.write(f"Te faltan **{980 - val}** láminas para llenar el álbum.")

# Navegación inferior (Visual)
st.markdown("""
    <div class="nav-bottom">
        <div class="nav-item">🏠<br>INICIO</div>
        <div class="nav-item">🗂️<br>ÁLBUM</div>
        <div class="nav-item">🤝<br>CAMBIOS</div>
        <div class="nav-item">📊<br>META</div>
    </div>
    <br><br>
    """, unsafe_allow_html=True)
