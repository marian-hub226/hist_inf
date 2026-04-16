import os
import streamlit as st
import base64
from openai import OpenAI
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
from streamlit_drawable_canvas import st_canvas

Expert=" "
profile_imgenh=" "

# Inicializar session_state
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'full_response' not in st.session_state:
    st.session_state.full_response = ""
if 'base64_image' not in st.session_state:
    st.session_state.base64_image = ""
    
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error: La imagen no se encontró en la ruta especificada."


# Streamlit 
st.set_page_config(page_title='Tablero Inteligente')
st.title('Tablero Inteligente')
with st.sidebar:
    st.subheader("Acerca de:")
    st.subheader("En esta aplicación veremos la capacidad que ahora tiene una máquina de interpretar un boceto")
st.subheader("Dibuja el boceto en el panel y presiona el botón para analizarla")

# Add canvas component
drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('Selecciona el ancho de línea', 1, 30, 5)
stroke_color = "#000000" 
bg_color = '#FFFFFF'

# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=300,
    width=400,
    drawing_mode=drawing_mode,
    key="canvas",
)

ke = st.text_input('Ingresa tu Clave', type="password")
if not ke:
    st.warning("Por favor ingresa tu API key.")
    st.stop()
client = OpenAI(api_key=ke)

analyze_button = st.button("Analiza la imagen", type="secondary")

# Check if an image has been uploaded, if the API key is available, and if the button has been pressed
if canvas_result.image_data is not None and analyze_button:

    with st.spinner("Analizando ..."):
        # Encode the image
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8')).convert('RGBA')
        input_image.save('img.png')
        
        # Cambio: mostrar imagen dibujada
        st.image("img.png", caption="Tu dibujo")
        
        base64_image = encode_image_to_base64("img.png")
        st.session_state.base64_image = base64_image
            
        # Cambio: mejor prompt de interpretación
        prompt_text = """
        Describe en español el dibujo de forma clara e interpretativa.
        Si es un boceto simple, intenta imaginar qué representa.
        """
    
        # Make the request to the OpenAI API
        try:
            full_response = ""
            message_placeholder = st.empty()
            response = client.responses.create(
                model="gpt-4o-mini",
                input=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": prompt_text},
                            {
                                "type": "input_image",
                                "image_url": f"data:image/png;base64,{base64_image}",
                            },
                        ],
                    }
                ],
                max_output_tokens=500,
            )

            full_response = response.output[0].content[0].text
            message_placeholder.markdown(full_response)
            
            # Final update to placeholder after the stream ends
            message_placeholder.markdown(full_response)
            
            # Guardar en session_state
            st.session_state.full_response = full_response
            st.session_state.analysis_done = True
    
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Mostrar la funcionalidad de crear historia si ya se hizo el análisis
if st.session_state.analysis_done:
    st.divider()
    st.subheader("📚 ¿Quieres crear una historia?")
    
    # Cambio: selector de tipo de historia
    tipo_historia = st.selectbox(
        "Selecciona el tipo de historia:",
        ["Infantil", "Terror", "Ciencia ficción", "Educativa"]
    )

    if st.button("✨ Crear historia"):
        with st.spinner("Creando historia..."):
            
            # Cambio: lógica dinámica
            if tipo_historia == "Infantil":
                estilo = "una historia infantil breve, creativa y apropiada para niños"
            elif tipo_historia == "Terror":
                estilo = "una historia corta de terror, con suspenso y un final impactante"
            elif tipo_historia == "Ciencia ficción":
                estilo = "una historia breve de ciencia ficción, futurista e imaginativa"
            elif tipo_historia == "Educativa":
                estilo = "una historia breve educativa que deje una enseñanza clara"
                
            # Cambio: prompt dinámico
            story_prompt = f"""
            Basándote en esta descripción: '{st.session_state.full_response}',
            crea {estilo}.
            """

            story_response = client.responses.create(
                model="gpt-4o-mini",
                input=story_prompt,
                max_output_tokens=500,
            )

            st.write(story_response.output[0].content[0].text)

