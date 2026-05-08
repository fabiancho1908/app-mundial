import streamlit as st
import sqlite3
import pandas as pd

# 1. Configuración de Marca Mundial 2026
st.set_page_config(page_title="Repetidas Mundial 2026", layout="centered")

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
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #612D8A 0%, #00A3E0 100%);
        color: white;
        font-weight: bold;
        height: 3em;
    }
    .swap-card {
        background: white;
        border-radius: 15px;
        padding: 15px;
        border-left: 8px solid #D6FF00;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de Datos
conn = sqlite3.connect('repetidas_2026.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS intercambio (id INTEGER PRIMARY KEY, usuario TEXT, ciudad TEXT, seleccion TEXT, numero TEXT, contacto TEXT)')
conn.commit()

# --- INTERFAZ ---
st.markdown('<div class="main-header"><h1>⚽ REPETIDAS 2026</h1><p>CENTRO DE INTERCAMBIO</p></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["➕ PUBLICAR MI REPETIDA", "🔍 BUSCAR CAMBIOS"])

with tab1:
    st.subheader("Anuncia tu lámina extra")
    with st.form("form_publicar"):
        u_nom = st.text_input("👤 Tu Nombre")
        u_ciu = st.selectbox("📍 Ciudad", ["Bogotá", "Medellín", "Cali", "Barranquilla", "Bucaramanga", "Pereira", "Otra"])
        
        col1, col2 = st.columns(2)
        with col1:
            u_sel = st.selectbox("🏳️ Selección", ["Especiales (FWC)", "Argentina", "Brasil", "Colombia", "México", "USA", "España", "Francia", "Otra"])
        with col2:
            u_num = st.text_input("🆔 Número")
            
        u_wha = st.text_input("📞 WhatsApp de contacto (Ej: 573001234567)")
        
        submit = st.form_submit_button("✨ PUBLICAR AHORA")
        
        if submit:
            if u_nom and u_num and u_wha:
                c.execute('INSERT INTO intercambio (usuario, ciudad, seleccion, numero, contacto) VALUES (?,?,?,?,?)', 
                          (u_nom, u_ciu, u_sel, u_num, u_wha))
                conn.commit()
                st.success(f"¡Lámina {u_sel} {u_num} publicada con éxito!")
            else:
                st.error("Por favor llena todos los campos.")

with tab2:
    st.subheader("Encuentra la que te falta")
    
    # Filtros de búsqueda
    df = pd.read_sql_query("SELECT * FROM intercambio", conn)
    
    if not df.empty:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            f_ciu = st.selectbox("📍 Filtrar por Ciudad", ["Todas"] + sorted(df['ciudad'].unique().tolist()))
        with col_f2:
            f_busq = st.text_input("🔍 Buscar por número o equipo").upper()
            
        # Lógica de filtrado
        res = df
        if f_ciu != "Todas":
            res = res[res['ciudad'] == f_ciu]
        if f_busq:
            res = res[res['seleccion'].str.upper().str.contains(f_busq) | res['numero'].str.contains(f_busq)]

        # Mostrar resultados
        for _, fila in res.iterrows():
            st.markdown(f"""
                <div class="swap-card">
                    <h3 style="margin:0; color:#612D8A;">{fila['seleccion']} - {fila['numero']}</h3>
                    <p style="margin:5px 0; font-size:14px;">📍 {fila['ciudad']} | 👤 {fila['usuario']}</p>
                    <a href="https://wa.me{fila['contacto']}" target="_blank" style="text-decoration:none; background-color:#25d366; color:white; padding:5px 10px; border-radius:8px; font-size:12px; font-weight:bold;">📲 CONTACTAR WHATSAPP</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Todavía no hay repetidas publicadas. ¡Sé el primero!")
