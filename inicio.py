import streamlit as st
import sqlite3
import pandas as pd

# Configuración Pro
st.set_page_config(page_title="Figuritas Colombia Pro", page_icon="⚽", layout="centered")

# --- BASE DE DATOS ---
conn = sqlite3.connect('laminas.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS intercambio (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT, depto TEXT, ciudad TEXT, repetida TEXT, contacto TEXT)')
conn.commit()

# --- DATOS DE COLOMBIA ---
colombia_datos = {
    "Amazonas": ["Leticia", "Puerto Nariño"],
    "Antioquia": ["Medellín", "Bello", "Itagüí", "Envigado", "Apartadó", "Rionegro", "Turbo", "Caucasia"],
    "Arauca": ["Arauca", "Tame", "Saravena"],
    "Atlántico": ["Barranquilla", "Soledad", "Malambo", "Sabanalarga"],
    "Bogotá D.C.": ["Bogotá D.C."],
    "Bolívar": ["Cartagena", "Magangué", "Turbaco", "El Carmen de Bolívar"],
    "Boyacá": ["Tunja", "Duitama", "Sogamoso", "Chiquinquirá"],
    "Caldas": ["Manizales", "La Dorada", "Riosucio"],
    "Caquetá": ["Florencia", "San Vicente del Caguán"],
    "Casanare": ["Yopal", "Aguazul", "Paz de Ariporo"],
    "Cauca": ["Popayán", "Santander de Quilichao", "Puerto Tejada"],
    "Cesar": ["Valledupar", "Aguachica", "Agustín Codazzi"],
    "Chocó": ["Quibdó", "Istmina"],
    "Córdoba": ["Montería", "Cereté", "Sahagún", "Lorica"],
    "Cundinamarca": ["Soacha", "Chía", "Zipaquirá", "Facatativá", "Fusagasugá", "Girardot", "Mosquera", "Funza"],
    "Guainía": ["Inírida"],
    "Guaviare": ["San José del Guaviare"],
    "Huila": ["Neiva", "Pitalito", "Garzón"],
    "La Guajira": ["Riohacha", "Maicao", "Uribia"],
    "Magdalena": ["Santa Marta", "Ciénaga", "Fundación"],
    "Meta": ["Villavicencio", "Acacías", "Granada"],
    "Nariño": ["Pasto", "Ipiales", "Tumaco"],
    "Norte de Santander": ["Cúcuta", "Ocaña", "Villa del Rosario", "Pamplona"],
    "Putumayo": ["Mocoa", "Puerto Asís", "Orito"],
    "Quindío": ["Armenia", "Calarcá", "Quimbaya"],
    "Risaralda": ["Pereira", "Dosquebradas", "Santa Rosa de Cabal"],
    "San Andrés": ["San Andrés", "Providencia"],
    "Santander": ["Bucaramanga", "Floridablanca", "Barrancabermeja", "Girón", "Piedecuesta"],
    "Sucre": ["Sincelejo", "Corozal"],
    "Tolima": ["Ibagué", "Espinal", "Melgar"],
    "Valle del Cauca": ["Cali", "Buenaventura", "Palmira", "Tuluá", "Yumbo", "Cartago", "Buga"],
    "Vaupés": ["Mitú"],
    "Vichada": ["Puerto Carreño"]
}

# --- DISEÑO CSS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(135deg, #8D1B3D 0%, #d32f2f 100%); color: white; font-weight: bold; }
    .cromo-card { border-radius: 15px; padding: 20px; background: white; box-shadow: 0 10px 20px rgba(0,0,0,0.05); margin-bottom: 20px; border-top: 5px solid #8D1B3D; text-align: center; }
    .whatsapp-btn { background-color: #25d366; color: white !important; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Figuritas Colombia 2026")

tab1, tab2 = st.tabs(["✨ PUBLICAR", "🔍 BUSCAR MATCH"])

with tab1:
    st.subheader("Registra tu repetida")
    with st.form("registro_pro"):
        u_nombre = st.text_input("👤 Tu Nombre")
        u_depto = st.selectbox("🗺️ Departamento", sorted(colombia_datos.keys()))
        u_ciudad = st.selectbox("📍 Ciudad", sorted(colombia_datos[u_depto]))
        u_lamina = st.text_input("🆔 Número (Ej: ARG 10)").upper()
        u_cel = st.text_input("📞 WhatsApp (Sin el +)")
        
        if st.form_submit_button("¡SUBIR AL ÁLBUM!"):
            if u_nombre and u_lamina and u_cel:
                c.execute('INSERT INTO intercambio (usuario, depto, ciudad, repetida, contacto) VALUES (?,?,?,?,?)', 
                          (u_nombre, u_depto, u_ciudad, u_lamina, u_cel))
                conn.commit()
                st.success("¡Lámina publicada!")
                st.rerun()

with tab2:
    df = pd.read_sql_query("SELECT * FROM intercambio", conn)
    
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        with c1:
            f_depto = st.selectbox("Filtrar Depto", ["Todos"] + sorted(df['depto'].unique().tolist()))
        with c2:
            f_ciudad = st.selectbox("Filtrar Ciudad", ["Todas"] + sorted(df['ciudad'].unique().tolist()))
        with c3:
            f_busq = st.text_input("🔎 Número").upper()

        res = df
        if f_depto != "Todos": res = res[res['depto'] == f_depto]
        if f_ciudad != "Todas": res = res[res['ciudad'] == f_ciudad]
        if f_busq: res = res[res['repetida'].str.contains(f_busq, na=False)]

        for i, fila in res.iterrows():
            st.markdown(f"""
                <div class="cromo-card">
                    <h1 style="margin: 0; color: #8D1B3D; font-size: 45px;">{fila['repetida']}</h1>
                    <p style="margin: 10px 0; color: #333;">
                        <b>📍 {fila['ciudad']}, {fila['depto']}</b><br>
                        👤 {fila['usuario']}
                    </p>
                    <a href="https://wa.me{fila['contacto']}" class="whatsapp-btn" target="_blank">📲 CONTACTAR</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aún no hay láminas. ¡Registra la primera!")
