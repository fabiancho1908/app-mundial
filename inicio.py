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

# --- DATOS AMPLIADOS DE COLOMBIA ---
colombia_datos = {
    "Amazonas": ["Leticia", "Puerto Nariño"],
    "Antioquia": ["Medellín", "Bello", "Itagüí", "Envigado", "Apartadó", "Rionegro", "Turbo", "Caucasia", "Sabaneta", "La Estrella", "Caldas", "Copacabana", "Girardota", "Marinilla"],
    "Arauca": ["Arauca", "Tame", "Saravena", "Arauquita"],
    "Atlántico": ["Barranquilla", "Soledad", "Malambo", "Sabanalarga", "Baranoa", "Puerto Colombia"],
    "Bogotá D.C.": ["Bogotá D.C."],
    "Bolívar": ["Cartagena", "Magangué", "Turbaco", "El Carmen de Bolívar", "Arjona", "Mompox"],
    "Boyacá": ["Tunja", "Duitama", "Sogamoso", "Chiquinquirá", "Puerto Boyacá", "Paipa"],
    "Caldas": ["Manizales", "La Dorada", "Riosucio", "Villamaría", "Anserma"],
    "Caquetá": ["Florencia", "San Vicente del Caguán", "Puerto Rico"],
    "Casanare": ["Yopal", "Aguazul", "Paz de Ariporo", "Villanueva"],
    "Cauca": ["Popayán", "Santander de Quilichao", "Puerto Tejada", "Piendamó", "Patía"],
    "Cesar": ["Valledupar", "Aguachica", "Agustín Codazzi", "Bosconia", "Curumaní"],
    "Chocó": ["Quibdó", "Istmina", "Condoto", "El Carmen de Atrato"],
    "Córdoba": ["Montería", "Cereté", "Sahagún", "Lorica", "Montelíbano", "Planeta Rica", "Tierralta"],
    "Cundinamarca": ["Soacha", "Chía", "Zipaquirá", "Facatativá", "Fusagasugá", "Girardot", "Mosquera", "Funza", "Madrid", "Cajicá", "Sibate", "Tocancipá"],
    "Guainía": ["Inírida"],
    "Guaviare": ["San José del Guaviare", "Calamar"],
    "Huila": ["Neiva", "Pitalito", "Garzón", "La Plata", "Campoalegre"],
    "La Guajira": ["Riohacha", "Maicao", "Uribia", "Manaure", "San Juan del Cesar"],
    "Magdalena": ["Santa Marta", "Ciénaga", "Fundación", "El Banco", "Plato"],
    "Meta": ["Villavicencio", "Acacías", "Granada", "Puerto López", "Cumaral"],
    "Nariño": ["Pasto", "Ipiales", "Tumaco", "Túquerres", "La Unión"],
    "Norte de Santander": ["Cúcuta", "Ocaña", "Villa del Rosario", "Pamplona", "Patios (Los)", "Tibú"],
    "Putumayo": ["Mocoa", "Puerto Asís", "Orito", "Valle del Guamuez"],
    "Quindío": ["Armenia", "Calarcá", "Quimbaya", "Montenegro", "La Tebaida"],
    "Risaralda": ["Pereira", "Dosquebradas", "Santa Rosa de Cabal", "La Virginia"],
    "San Andrés": ["San Andrés", "Providencia"],
    "Santander": ["Bucaramanga", "Floridablanca", "Barrancabermeja", "Girón", "Piedecuesta", "San Gil", "Socorro"],
    "Sucre": ["Sincelejo", "Corozal", "San Marcos", "Sampués", "Tolú"],
    "Tolima": ["Ibagué", "Espinal", "Melgar", "Mariquita", "Honda", "Líbano"],
    "Valle del Cauca": ["Cali", "Buenaventura", "Palmira", "Tuluá", "Yumbo", "Cartago", "Buga", "Jamundí", "Florida", "Pradera"],
    "Vaupés": ["Mitú"],
    "Vichada": ["Puerto Carreño", "La Primavera"]
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
        # Esta línea hace que la ciudad cambie según el departamento elegido
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
            # Filtro dinámico para ciudades en la búsqueda
            if f_depto != "Todos":
                ciudades_filtro = ["Todas"] + sorted(df[df['depto'] == f_depto]['ciudad'].unique().tolist())
            else:
                ciudades_filtro = ["Todas"] + sorted(df['ciudad'].unique().tolist())
            f_ciudad = st.selectbox("Filtrar Ciudad", ciudades_filtro)
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
