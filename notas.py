import pandas as pd
from io import StringIO
import streamlit as st

# --- 1. BASE DE DATOS INTERNA (Oculta del Usuario Final) ---
# La base de datos es creada a partir de los datos que proporcionaste.
data_str = """
ID,Nombre,Quiz (25%),Taller (25%),Parcial (40%),Asistencia (10%),Nota definitiva,Nota definitiva redondeada
202220003610,ALMEIDA OLIVO DUMAN ENRIQUE,40,32.5,37.5,44.4,37.565,38
202220005610,JIMENEZ GARAY ROGER ADRIANY,45,40,50,50,46.25,46
202220014610,MARTINEZ MARTINEZ NERIETH PATRICIA,40,22.5,37.5,44.4,35.065,35
202229901610,MEDINA PEDROZO KEVIN DAVID,30,39.5,42,38.8,38.055,38
202210005610,MENDEZ CONDE ESTEBAN ANDRES,40,40,37.5,44.4,39.44,39
202220010610,MONTERROZA MORALES MOISES DAVID,50,42.5,0,50,28.125,28
202220016610,PADILLA TELLEZ SEBASTIAN,30,39.5,0,50,22.375,22
202210012610,ALIAB DAVID PINTO GENES,40,37.5,45,38.8,41.255,41
"""

COLUMNA_ID = 'ID'
COLUMNAS_A_BORRAR = ['Nombre', 'Nota definitiva'] 

# Usamos st.cache_data para cargar la base de datos solo una vez.
@st.cache_data
def load_data():
    try:
        df_original = pd.read_csv(StringIO(data_str), index_col=COLUMNA_ID, sep=',')
        df_copia = df_original.copy()
        
        for col in COLUMNAS_A_BORRAR:
            if col in df_copia.columns:
                df_copia = df_copia.drop(columns=[col])

        df_copia.index = pd.to_numeric(df_copia.index, errors='coerce').astype('Int64')
        return df_copia
    except Exception as e:
        st.error(f"Error al cargar la base de datos interna: {e}")
        return pd.DataFrame()

df_copia = load_data()

# --- 2. FUNCIÓN DE BÚSQUEDA Y VALIDACIÓN ---

def buscar_notas_por_id(id_buscado_str, df_notas):
    """Busca y muestra las notas del estudiante."""
    
    if df_notas.empty:
        st.warning("La base de datos no está disponible. Intente más tarde.")
        return

    try:
        id_buscado_num = int(id_buscado_str) 
        
        if id_buscado_num not in df_notas.index:
             st.error(f"❌ ERROR: El ID **{id_buscado_num}** está equivocado. Inserte un número de ID correcto.")
             return

        # Obtener la fila del estudiante
        fila_estudiante = df_notas.loc[[id_buscado_num]] 
        
        # Renombrar columnas para claridad
        fila_estudiante = fila_estudiante.rename(columns={
            'Nota definitiva redondeada': 'Nota Final Redondeada'
        })
        
        st.success(f"✅ Resultados para ID: {id_buscado_num}")
        st.markdown("<p>Se muestran sus **4 notas** y la **Nota Final Redondeada**:</p>", unsafe_allow_html=True)
        
        # Mostrar la tabla de resultados
        st.dataframe(fila_estudiante.style.format('{:.2f}'), use_container_width=True)

    except ValueError:
        st.error("❌ ERROR: Por favor, ingrese un número de ID válido (solo números).")

# --- 3. INTERFAZ DE STREAMLIT ---

# --- 3. INTERFAZ INTERACTIVA (Widgets) ---

from IPython.display import clear_output # Necesario aquí para clear_output

# Función para mostrar la interfaz (el título, el campo y el botón)
def mostrar_interfaz():
    """Muestra el título y los widgets de entrada."""
    display(HTML("<h2>Consulta de Calificaciones Finales</h2>"))
    display(id_input, boton_buscar)


# Crear el campo de texto para el ID
id_input = widgets.Text(
    value='',
    placeholder='Escribe tu número de ID aquí',
    description='Tu ID:',
    disabled=False
)

# Crear el botón de búsqueda
boton_buscar = widgets.Button(
    description='Buscar Notas',
    disabled=False,
    button_style='info', 
    tooltip='Clic para buscar tus notas'
)


# Definir la acción al hacer clic en el botón
def on_button_click(b):
    # Limpiar cualquier salida previa antes de mostrar el nuevo resultado
    clear_output(wait=True) 
    
    # Reimprimir la interfaz
    mostrar_interfaz()
    
    # Ejecutar la búsqueda
    buscar_notas_por_id(id_input.value)


# Asociar la acción al botón
boton_buscar.on_click(on_button_click)

# Mostrar la interfaz al ejecutar la celda por primera vez (ESTO INICIA EL FORMULARIO)
mostrar_interfaz()
