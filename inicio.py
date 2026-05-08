import streamlit as st
import sqlite3
import pandas as pd

# 1. Configuración de Marca Mundial 2026
st.set_page_config(page_title="Repetidas Colombia 2026", layout="centered")

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
        width: 100%; border-radius: 12px;
        background: linear-gradient(135deg, #612D8A 0%, #00A3E0 100%);
        color: white; font-weight: bold; height: 3.5em;
    }
    .swap-card {
        background: white; border-radius: 15px; padding: 15px;
        border-left: 8px solid #D6FF00; box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de Datos
conn = sqlite3.connect('repetidas_colombia.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS intercambio (id INTEGER PRIMARY KEY, usuario TEXT, ciudad TEXT, seleccion TEXT, numero TEXT, contacto TEXT)')
conn.commit()

# --- LISTA EXTENSA DE CIUDADES COLOMBIANAS ---
ciudades_col = sorted([
    "Bogotá D.C.", "Medellín", "Cali", "Barranquilla", "Cartagena", "Soledad", "Cúcuta", "Ibagué", "Soacha", "Bucaramanga",
    "Villavicencio", "Santa Marta", "Valledupar", "Pereira", "Bello", "Montería", "Pasto", "Buenaventura", "Manizales",
    "Neiva", "Palmira", "Riohacha", "Sincelejo", "Popayán", "Itagüí", "Floridablanca", "Envigado", "Tuluá", "San Andrés",
    "Dosquebradas", "Apartadó", "Tumaco", "Tunja", "Girón", "Uribia", "Maicao", "Florencia", "Chía", "Sogamoso", 
    "Duitama", "Cartago", "Facatativá", "Fusagasugá", "Ipiales", "Pitalito", "Zipaquirá", "Jamundí", "Yopal", "Malambo",
    "Mosquera", "Funza", "Madrid", "Cajicá", "Sabaneta", "La Estrella", "Caldas", "Rionegro", "Marinilla", "Caucasia",
    "Turbo", "Magangué", "Quibdó", "Girardot", "Buga", "Aguachica", "Ocaña", "Piedecuesta", "Pamplona", "Leticia", 
    "Arauca", "Mocoa", "San José del Guaviare", "Puerto Carreño", "Inírida", "Mitú", "Barrancabermeja", "San Gil", "Otra"
])

# --- INTERFAZ ---
st.markdown('<div class="main-header"><h1>⚽ REPETIDAS COLOMBIA</h1><p>INTERCAMBIO MUNDIAL 2026</p></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["➕ PUBLICAR REPETIDA", "🔍 BUSCAR CAMBIOS"])

with tab1:
    st.subheader("Anuncia tu lámina extra")
    with st.form("form_publicar"):
        u_nom = st.text_input("👤 Tu Nombre")
        u_ciu = st.selectbox("📍 Tu Ciudad", ciudades_col)
        if u_ciu == "Otra": u_ciu = st.text_input("¿Cuál es tu ciudad?")
        
        col1, col2 = st.columns(2)
        with col1:
            u_sel = st.selectbox("🏳️ Selección", ["Especiales (FWC)", "Sedes/Estadios", "Argentina", "Brasil", "Colombia", "México", "USA", "Canadá", "España", "Francia", "Alemania", "Italia", "Otra"])
        with col2:
            u_num = st.text_input("🆔 Número")
            
        u_wha = st.text_input("📞 WhatsApp (Ej: 3001234567)")
        
        if st.form_submit_button("✨ PUBLICAR AHORA"):
            if u_nom and u_num and u_wha:
                # Limpiamos el número de whatsapp por si ponen + o espacios
                clean_wha = u_wha.replace("+", "").replace(" ", "")
                c.execute('INSERT INTO intercambio (usuario, ciudad, seleccion, numero, contacto) VALUES (?,?,?,?,?)', 
                          (u_nom, u_ciu, u_sel, u_num, clean_wha))
                conn.commit()
                st.success(f"¡{u_sel} {u_num} publicada en {u_ciu}!")
                st.rerun()

with tab2:
    df = pd.read_sql_query("SELECT * FROM intercambio", conn)
    
    if not df.empty:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            f_ciu = st.selectbox("📍 Filtrar por Ciudad", ["Todas"] + sorted(df['ciudad'].unique().tolist()))
        with col_f2:
            f_busq = st.text_input("🔍 Buscar selección o número").upper()
            
        res = df
        if f_ciu != "Todas": res = res[res['ciudad'] == f_ciu]
        if f_busq:
            res = res[res['seleccion'].str.upper().str.contains(f_busq) | res['numero'].str.contains(f_busq)]

        for _, fila in res.iterrows():
            # Mensaje automático para WhatsApp
            msj_wa = f"Hola {fila['usuario']}, vi en la App que tienes la repetida de {fila['seleccion']} número {fila['numero']}. ¿Te interesa cambiarla?"
            link_wa = f"https://wa.me{fila['contacto']}?text={msj_wa.replace(' ', '%20')}"
            
            st.markdown(f"""
                <div class="swap-card">
                    <h3 style="margin:0; color:#612D8A;">{fila['seleccion']} - {fila['numero']}</h3>
                    <p style="margin:5px 0; font-size:14px;">📍 {fila['ciudad']} | 👤 {fila['usuario']}</p>
                    <a href="{link_wa}" target="_blank" style="text-decoration:none; background-color:#25d366; color:white; padding:8px 15px; border-radius:10px; font-size:13px; font-weight:bold; display:inline-block;">📲 CONTACTAR WHATSAPP</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Todavía no hay repetidas. ¡Publica la primera!")
