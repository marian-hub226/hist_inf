import streamlit as st
from streamlit_drawable_canvas import st_canvas

# Configuración
st.set_page_config(page_title='Tablero Inteligente')
st.title('🎨 Tablero Inteligente')

with st.sidebar:
    st.subheader("Acerca de:")
    st.write("Dibuja algo y crea una historia a partir de tu imaginación.")
    stroke_width = st.slider('Ancho de línea', 1, 30, 5)
    stroke_color = "#000000"
    bg_color = '#FFFFFF'

st.subheader("✏️ Dibuja algo en el panel")

# Canvas
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=300,
    width=400,
    drawing_mode="freedraw",
    key="canvas",
)

# 🔹 NUEVO: el usuario describe el dibujo
st.subheader("🧠 Describe tu dibujo")
descripcion = st.text_input("Ej: Un dragón volando sobre una montaña")

# 🔹 GENERACIÓN DE HISTORIA
if descripcion:
    st.divider()
    st.subheader("📚 Crear historia")

    tipo_historia = st.selectbox(
        "Selecciona el tipo de historia:",
        ["Infantil", "Terror", "Ciencia ficción", "Educativa"]
    )

    if st.button("✨ Generar historia"):
        
        if tipo_historia == "Infantil":
            historia = f"""
Había una vez {descripcion}.
Era un mundo lleno de magia y aventuras.
Un día, algo sorprendente ocurrió y todo cambió.
Al final, todos aprendieron una gran lección y vivieron felices.
"""
        
        elif tipo_historia == "Terror":
            historia = f"""
Todo comenzó con {descripcion}.
Pero algo no estaba bien...
En la oscuridad, una presencia misteriosa observaba.
Y desde ese día, nadie volvió a ser el mismo.
"""
        
        elif tipo_historia == "Ciencia ficción":
            historia = f"""
En el año 3025, {descripcion}.
La tecnología había cambiado todo.
Un evento inesperado desencadenó una gran misión.
El destino del universo estaba en juego.
"""
        
        elif tipo_historia == "Educativa":
            historia = f"""
Había una vez {descripcion}.
A través de su experiencia, aprendió algo importante.
Con esfuerzo y valentía, logró superar los desafíos.
La enseñanza fue clara: nunca rendirse.
"""

        st.markdown("### 📖 Tu historia:")
        st.write(historia)
