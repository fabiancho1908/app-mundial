import streamlit as st
import sqlite3
import pandas as pd

# Configuración de la App
st.set_page_config(page_title="Figuritas Colombia", page_icon="⚽", layout="centered")

# --- BASE DE DATOS ---
conn = sqlite3.connect('laminas.db', check_same_thread=False)
c = conn.cursor()
# Volvemos a la estructura simple de ciudad
c.execute('CREATE TABLE IF NOT EXISTS intercambio (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT, ciudad TEXT, repetida TEXT, contacto TEXT)')
conn.commit()

# --- LISTA EXTENSA DE CIUDADES DE COLOMBIA ---
todas_ciudades = sorted([
    "Bogotá D.C.", "Medellín", "Cali", "Barranquilla", "Cartagena", "Soledad", "Cúcuta", "Ibagué", "Soacha", "Bucaramanga",
    "Villavicencio", "Santa Marta", "Valledupar", "Pereira", "Bello", "Montería", "Pastos", "Buenaventura", "Manizales",
    "Neiva", "Palmira", "Riohacha", "Sincelejo", "Popayán", "Itagüí", "Floridablanca", "Envigado", "Tuluá", "San Andrés",
    "Dosquebradas", "Apartadó", "Tumaco", "Tunja", "Girón", "Uribia", "Maicao", "Florencia", "Chía", "Sogamoso", 
    "Duitama", "Cartago", "Facatativá", "Fusagasugá", "Ipiales", "Pitalito", "Zipaquirá", "Jamundí", "Yopal", "Malambo",
    "Mosquera", "Funza", "Madrid", "Cajicá", "Sabaneta", "La Estrella", "Caldas", "Rionegro", "Marinilla", "Caucasia",
    "Turbo", "Magangué", "Apartadó", "Quibdó", "Girardot", "Buga", "Aguachica", "Ocaña", "Piedecuesta", "Pamplona",
    "Barrancabermeja", "Arauca", "Leticia", "Mocoa", "Inírida", "San José del Guaviare", "Mitú", "Puerto Carreño", "Otra"
])

# --- DISEÑO CSS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(135deg, #8D1B3D 0%, #d32f2f 100%); color: white; font-weight: bold; }
    .cromo-card { border-radius: 15px; padding: 20px; background: white; box-shadow: 0 10px 20px rgba(0,0,0,0.05); margin-bottom: 20px; border-top: 5px solid #8D1B3D; text-align: center; }
    .whatsapp-btn { background-color: #25d366; color: white !important; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Figuritas Colombia 2026")

tab1, tab2 = st.tabs(["✨ PUBLICAR", "🔍 BUSCAR"])

with tab1:
    st.subheader("Registra tu repetida")
    with st.form("registro_simple"):
        u_nombre = st.text_input("👤 Tu Nombre")
        u_ciudad = st.selectbox("📍 Ciudad o Municipio", todas_ciudades)
        if u_ciudad == "Otra":
            u_ciudad = st.text_input("¿Cuál ciudad?")
            
        u_lamina = st.text_input("🆔 Número (Ej: ARG 10)").upper()
        u_cel = st.text_input("📞 WhatsApp (Sin el +)")
        
        if st.form_submit_button("¡PUBLICAR!"):
            if u_nombre and u_lamina and u_cel:
                c.execute('INSERT INTO intercambio (usuario, ciudad, repetida, contacto) VALUES (?,?,?,?)', 
                          (u_nombre, u_ciudad, u_lamina, u_cel))
                conn.commit()
                st.success(f"¡{u_lamina} publicada en {u_ciudad}!")
                st.rerun()

with tab2:
    df = pd.read_sql_query("SELECT * FROM intercambio", conn)
    
    if not df.empty:
        c1, c2 = st.columns(2)
        with c1:
            f_ciudad = st.selectbox("Filtrar por Ciudad", ["Todas"] + sorted(df['ciudad'].unique().tolist()))
        with c2:
            f_busq = st.text_input("🔎 Número de lámina").upper()

        res = df
        if f_ciudad != "Todas": res = res[res['ciudad'] == f_ciudad]
        if f_busq: res = res[res['repetida'].str.contains(f_busq, na=False)]

        for i, fila in res.iterrows():
            st.markdown(f"""
                <div class="cromo-card">
                    <h1 style="margin: 0; color: #8D1B3D; font-size: 45px;">{fila['repetida']}</h1>
                    <p style="margin: 10px 0; color: #333;">
                        <b>📍 {fila['ciudad']}</b><br>
                        👤 {fila['usuario']}
                    </p>
                    <a href="https://wa.me{fila['contacto']}" class="whatsapp-btn" target="_blank">📲 CONTACTAR</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aún no hay láminas. ¡Sé el primero!")
