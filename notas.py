import pandas as pd
from io import StringIO
from IPython.display import display, HTML, clear_output
from ipywidgets import widgets

# --- 1. BASE DE DATOS INTERNA ---
# La base de datos es creada a partir de los datos que proporcionaste.
# Esto elimina errores de lectura de archivos y rutas.
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

# Definición de columnas y carga de datos
COLUMNA_ID = 'ID'
# Se eliminan 'Nombre' y 'Nota definitiva' (la no redondeada)
COLUMNAS_A_BORRAR = ['Nombre', 'Nota definitiva'] 

df_copia = pd.DataFrame() 

try:
    # Cargar los datos desde el texto usando coma como delimitador (sep=',')
    df_original = pd.read_csv(StringIO(data_str), index_col=COLUMNA_ID, sep=',')
    
    df_copia = df_original.copy()
    
    # Borrar las columnas solicitadas
    for col in COLUMNAS_A_BORRAR:
        if col in df_copia.columns:
            df_copia = df_copia.drop(columns=[col])

    # Transformar el índice (ID) a número entero
    df_copia.index = pd.to_numeric(df_copia.index, errors='coerce').astype('Int64')
    
    display(HTML("<p style='color: green;'>✅ Base de datos interna creada correctamente. ¡Lista para buscar!</p>"))

except Exception as e:
    display(HTML(f"<p style='color: red;'>❌ ERROR en la creación de la base de datos interna. Detalle: {e}</p>"))
    df_copia = pd.DataFrame()


# --- 2. FUNCIÓN DE BÚSQUEDA Y VALIDACIÓN ---

def buscar_notas_por_id(id_buscado_str):
    """Busca y muestra las notas del estudiante, incluyendo la validación."""
    
    if df_copia.empty:
        display(HTML("<p style='color: red;'>La base de datos no está disponible. No se puede buscar.</p>"))
        return

    try:
        id_buscado_num = int(id_buscado_str) 
        
        # Validación: Si el ID no está en la lista
        if id_buscado_num not in df_copia.index:
             display(HTML(f"<p style='color: red;'>❌ ERROR: El ID **{id_buscado_num}** está equivocado. Inserte un número de ID correcto y pulse Buscar Notas.</p>"))
             return

        # Obtener la fila del estudiante
        fila_estudiante = df_copia.loc[[id_buscado_num]] 
        
        # Formatear el resultado: cambiar 'Nota definitiva redondeada' por un nombre más claro
        fila_estudiante = fila_estudiante.rename(columns={
            'Nota definitiva redondeada': 'Nota Final Redondeada'
        })
        
        # Formatear el resultado como HTML (tabla)
        html_output = f"""
        <div style='border: 2px solid #007bff; padding: 15px; border-radius: 8px; background-color: #e9f5ff;'>
            <h3 style='color: #0056b3;'>✅ Resultados para ID: {id_buscado_num}</h3>
            <p>Se muestran sus **4 notas** y la **Nota Final Redondeada**:</p>
            {fila_estudiante.to_html(index=True, float_format='%.2f', na_rep='', classes='pure-table')}
        </div>
        """
        display(HTML(html_output))

    except ValueError:
        display(HTML("<p style='color: red;'>❌ ERROR: Por favor, ingrese un número de ID válido (solo números).</p>"))


# --- 3. INTERFAZ INTERACTIVA (Widgets) ---

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
