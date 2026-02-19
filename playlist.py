import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

# --- Variables Globales ---
# Se usan listas separadas para las entradas de cada campo por FILA/CANCION
entry_artistas = []
entry_canciones = []
entry_urls = []
# Lista para mantener los widgets de cabecera (etiquetas)
widgets_control = []

# --- Funciones de Lógica ---

def limpiar_campos():
    """Destruye los widgets de entrada dinámicos y limpia las listas de referencias."""
    global widgets_control
    
    # Destruye SOLO los widgets de la lista (entradas dinámicas)
    # y los widgets de control que no son los botones permanentes.
    
    # Creamos una lista de todos los widgets a destruir (las entradas y las etiquetas de encabezado)
    widgets_a_destruir = entry_artistas + entry_canciones + entry_urls + widgets_control
    
    for widget in widgets_a_destruir:
        widget.destroy()
        
    entry_artistas.clear()
    entry_canciones.clear()
    entry_urls.clear()
    widgets_control.clear()

def mostrar_encabezado_y_control(total_filas):
    """Muestra las etiquetas de encabezado (Artista, Canción, URL) y el botón de agregar."""
    
    # 1. Limpiamos solo los encabezados (si existen) y NO EL BOTÓN DE AGREGAR
    # Para la primera ejecución, widgets_control está vacío. Si se llama después de cargar_json, 
    # la limpieza ya se hizo en limpiar_campos, pero se añade una protección:
    for widget in widgets_control:
        widget.destroy()
    widgets_control.clear()
    
    # 2. Etiquetas de Encabezado
    # La fila del encabezado es siempre la fila 0
    
    widgets_control.append(tk.Label(frame_datos, text="Artista", font=('Arial', 10, 'bold')))
    widgets_control[-1].grid(row=0, column=0, padx=5, pady=5)
    
    widgets_control.append(tk.Label(frame_datos, text="Canción", font=('Arial', 10, 'bold')))
    widgets_control[-1].grid(row=0, column=1, padx=5, pady=5)
    
    widgets_control.append(tk.Label(frame_datos, text="URL", font=('Arial', 10, 'bold')))
    widgets_control[-1].grid(row=0, column=2, padx=5, pady=5)
    
    # 3. Botón para AGREGAR NUEVA FILA (siempre en la esquina superior derecha, fila 0)
    # No lo creamos ni lo destruimos, solo lo colocamos.
    boton_agregar_fila.grid(row=0, column=3, padx=10, pady=5, sticky="e")
    
    # 4. Muestra el botón de Guardar si hay datos
    if total_filas > 0 or len(entry_artistas) > 0:
        mostrar_boton_guardar(total_filas + 1)
    else:
        # Aseguramos que se oculte si se llama al inicio o después de limpiar sin cargar
        boton_guardar.grid_remove() 


def agregar_fila_vacia():
    """Añade un nuevo conjunto de campos (una fila) para una nueva canción."""
    
    # Calcula la fila donde se debe insertar la nueva entrada (es la longitud actual + 1 por el encabezado)
    new_row = len(entry_artistas) + 1 
    
    # Campos para Artista
    entry_a = tk.Entry(frame_datos, width=25)
    entry_a.grid(row=new_row, column=0, padx=5, pady=2)
    entry_artistas.append(entry_a)

    # Campos para Canción
    entry_c = tk.Entry(frame_datos, width=30)
    entry_c.grid(row=new_row, column=1, padx=5, pady=2)
    entry_canciones.append(entry_c)

    # Campos para URL
    entry_u = tk.Entry(frame_datos, width=60)
    entry_u.grid(row=new_row, column=2, padx=5, pady=2)
    entry_urls.append(entry_u)
    
    # Actualiza la posición y visibilidad del botón de guardar
    mostrar_boton_guardar(new_row + 1)
    # Forzar la actualización del scrollbar para la nueva fila
    frame_datos.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def mostrar_entradas_json(lista_datos):
    """Muestra todos los elementos de la lista JSON en la interfaz."""
    limpiar_campos()
    
    # Muestra los encabezados y el botón de agregar
    mostrar_encabezado_y_control(len(lista_datos))

    row_index = 1
    for item in lista_datos:
        # Asume la estructura Artista, Cancion, url
        artista = item.get("Artista", "")
        cancion = item.get("Cancion", "")
        url = item.get("url", "")
        
        # Entrada Artista
        entry_a = tk.Entry(frame_datos, width=25)
        entry_a.insert(0, artista)
        entry_a.grid(row=row_index, column=0, padx=5, pady=2)
        entry_artistas.append(entry_a)

        # Entrada Canción
        entry_c = tk.Entry(frame_datos, width=30)
        entry_c.insert(0, cancion)
        entry_c.grid(row=row_index, column=1, padx=5, pady=2)
        entry_canciones.append(entry_c)

        # Entrada URL
        entry_u = tk.Entry(frame_datos, width=60)
        entry_u.insert(0, url)
        entry_u.grid(row=row_index, column=2, padx=5, pady=2)
        entry_urls.append(entry_u)
        
        row_index += 1
        
    mostrar_boton_guardar(row_index)
    
    # Forzar la actualización del scrollbar después de cargar todos los datos
    frame_datos.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def cargar_json():
    """Permite seleccionar y cargar un archivo JSON (espera una LISTA)."""
    archivo = filedialog.askopenfilename(defaultextension=".json", filetypes=[("Archivos JSON", "*.json")])
    if archivo:
        try:
            with open(archivo, 'r') as json_file:
                datos = json.load(json_file)
             
            # Verificar si es una lista (estructura correcta)
            if not isinstance(datos, list):
                if isinstance(datos, dict):
                    datos = [datos] # Convierte el objeto único a una lista
                else:
                    messagebox.showerror("Error", "El archivo JSON no contiene una lista de objetos válida.")
                    return

            # Actualiza los campos superiores (solo para referencia)
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, os.path.basename(archivo).replace('.json', ''))
            
            # Muestra los datos en la interfaz
            mostrar_entradas_json(datos)
            
            # Guarda la ruta del archivo cargado 
            ventana.current_file_path = archivo 
            messagebox.showinfo("Éxito", f"Archivo {os.path.basename(archivo)} cargado exitosamente. Puede agregar filas y guardar.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")
            limpiar_campos() 

def guardar_json_desde_interfaz():
    """
    Recopila los datos de todos los campos de entrada como una LISTA DE DICCIONARIOS
    y llama a guardar_json.
    """
    nombre_base = entry_nombre.get().strip()
    
    if not nombre_base:
        messagebox.showerror("Error", "El nombre del archivo no puede estar vacío.")
        return

    # 1. Recopilar los datos de los campos en una LISTA
    lista_a_guardar = []
    
    # Asume que todas las listas de entradas tienen la misma longitud (mismo número de filas)
    for entry_a, entry_c, entry_u in zip(entry_artistas, entry_canciones, entry_urls):
        artista = entry_a.get().strip()
        cancion = entry_c.get().strip()
        url = entry_u.get()
        
        # Solo guardamos la fila si al menos tiene Artista o Canción
        if artista or cancion:
            lista_a_guardar.append({
                "Artista": artista,
                "Cancion": cancion,
                "url": url 
            })
            
    if not lista_a_guardar:
        messagebox.showwarning("Advertencia", "No hay datos de canciones para guardar.")
        return

    # 2. Determinar la ruta de guardado (misma lógica que antes)
    es_archivo_cargado_actual = hasattr(ventana, 'current_file_path') and \
                                ventana.current_file_path and \
                                nombre_base == os.path.basename(ventana.current_file_path).replace('.json', '')
    
    if es_archivo_cargado_actual:
        ruta_archivo = ventana.current_file_path
        guardar_json(ruta_archivo, lista_a_guardar)
    else:
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".json", 
            initialfile=nombre_base, 
            filetypes=[("Archivos JSON", "*.json")]
        )
        if ruta_archivo:
            guardar_json(ruta_archivo, lista_a_guardar)
            ventana.current_file_path = ruta_archivo 


def guardar_json(ruta_archivo, datos):
    """Escribe la lista de diccionarios en un archivo JSON."""
    try:
        with open(ruta_archivo, 'w') as json_file:
            json.dump(datos, json_file, indent=4)
        messagebox.showinfo("Éxito", f"Archivo {os.path.basename(ruta_archivo)} actualizado exitosamente con {len(datos)} elementos.")
    except Exception as e:
        messagebox.showerror("Error de guardado", f"No se pudo guardar el archivo: {e}")

def mostrar_boton_guardar(row_position):
    """Coloca el botón de Guardar en la posición correcta."""
    boton_guardar.grid(row=row_position, column=0, columnspan=3, pady=10)
    
# --- Configuración de la ventana principal ---
ventana = tk.Tk()
ventana.title("🎶 Editor de Listas de Canciones JSON")
ventana.geometry("900x700") 

# Inicializa la variable de la ruta del archivo actual
ventana.current_file_path = None

# Frame superior para el Nombre del archivo
frame_controles = tk.Frame(ventana, padx=10, pady=10)
frame_controles.pack(pady=10)

label_nombre = tk.Label(frame_controles, text="Nombre del archivo (sin .json):")
label_nombre.grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_nombre = tk.Entry(frame_controles, width=50)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

# Frame para los botones principales
frame_botones = tk.Frame(ventana, padx=10, pady=10)
frame_botones.pack(pady=5)

# Botones de acción
boton_cargar = tk.Button(frame_botones, text="Cargar Lista JSON Existente", command=cargar_json, width=30)
boton_cargar.grid(row=0, column=0, padx=10)

# --- Configuración del área de datos con Scroll ---
canvas = tk.Canvas(ventana, borderwidth=0, background="#ffffff")
v_scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)

# El frame_datos es donde se agregarán las filas dinámicas
frame_datos = tk.Frame(canvas, background="#ffffff", padx=10, pady=10)

canvas.create_window((0, 0), window=frame_datos, anchor="nw", tags="frame_datos_inner")
canvas.configure(yscrollcommand=v_scrollbar.set, scrollregion=canvas.bbox("all"))

v_scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

frame_datos.bind("<Configure>", lambda e: canvas.config(scrollregion = canvas.bbox("all")))

# --- Inicialización de Botones Dinámicos ---

# Botón para añadir una nueva fila (CRÍTICO para la funcionalidad de 'Agregar')
# NOTA: Este botón debe crearse FUERA de cualquier frame que se destruya, 
# o como un widget persistente. Al estar en frame_datos, debe ser manejado en la limpieza.
# Ahora se maneja NO DESTRUYÉNDOLO en limpiar_campos.
boton_agregar_fila = tk.Button(frame_datos, text="➕ Agregar Nueva Canción", command=agregar_fila_vacia, bg="#e3f2fd", fg="black")

# Botón de guardar/actualizar (se usa para colocarlo en la cuadrícula)
boton_guardar = tk.Button(frame_datos, text="💾 Guardar/Actualizar Lista JSON", command=guardar_json_desde_interfaz, bg="#e0f7fa", fg="black")


# Listas globales para almacenar las entradas de claves y valores dinámicas
entry_artistas = []
entry_canciones = []
entry_urls = []
widgets_control = [] # Para almacenar referencias a las etiquetas de encabezado

# --- INICIALIZACIÓN DE LA INTERFAZ DE DATOS ---

# Llamamos a esta función para mostrar los encabezados y el botón "Agregar" desde el inicio
mostrar_encabezado_y_control(0) 

ventana.mainloop()