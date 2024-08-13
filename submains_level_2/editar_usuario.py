from common import *
from settings.conf_ventana import configurar_ventana
from settings import db_path
from submains_level_2.editar_usuario_db import *

# Función para abrir la ventana de edición de usuarios
def editar_usuario(root, ventana_personal_esd):
    ventana_personal_esd.withdraw()  # Oculta la ventana de Personal ESD
    ventana_editar = tk.Toplevel(root)  # Crear una nueva ventana
    configurar_ventana(ventana_editar, "Edición de Usuario")

    # Variables para selección
    var_area = tk.StringVar(value="Seleccione una opción")
    var_linea = tk.StringVar(value="Seleccione una opción")

    # Consultar áreas y líneas únicas de la base de datos
    areas = obtener_areas_unicas()
    lineas = obtener_lineas_unicas()

    # Crear marco para las selecciones
    frame_selecciones = tk.Frame(ventana_editar)
    frame_selecciones.pack(pady=20)

    # Etiquetas y entradas para seleccionar área y línea
    tk.Label(frame_selecciones, text="Selecciona un área:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    tk.OptionMenu(frame_selecciones, var_area, *areas).grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame_selecciones, text="Selecciona una línea:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    tk.OptionMenu(frame_selecciones, var_linea, *lineas).grid(row=1, column=1, padx=10, pady=5)

    # Tabla para mostrar resultados
    columns = ("Nombre de Usuario", "Rol", "Área", "Línea", "Puesto")
    tabla = ttk.Treeview(ventana_editar, columns=columns, show='headings')

    # Configurar encabezados de la tabla
    tabla.heading("Nombre de Usuario", text="Nombre de Usuario")
    tabla.heading("Rol", text="Rol")
    tabla.heading("Área", text="Área")
    tabla.heading("Línea", text="Línea")
    tabla.heading("Puesto", text="Puesto")

    # Configurar columnas de la tabla (opcional: para ajustar tamaños)
    tabla.column("Nombre de Usuario", width=150)
    tabla.column("Rol", width=100)
    tabla.column("Área", width=100)
    tabla.column("Línea", width=100)
    tabla.column("Puesto", width=150)

    tabla.pack(pady=20, fill=tk.BOTH, expand=True)

    # Crear marco para los botones
    frame_botones = tk.Frame(ventana_editar)
    frame_botones.pack(pady=10)

    # Crear botones
    tk.Button(frame_botones, text="Buscar Usuarios",
              command=lambda: buscar_usuarios(ventana_editar, var_area, var_linea),
              font=("Arial", 14), bg="sky blue", height=2, width=20).grid(row=0, column=0, padx=10)

    tk.Button(frame_botones, text="Editar Usuario",
              command=lambda: editar_usuario_seleccionado(ventana_editar, var_area, var_linea),
              font=("Arial", 14), bg="sky blue", height=2, width=20).grid(row=0, column=1, padx=10)

    # Función para salir del programa
    def salir_editar():
        ventana_editar.destroy()  # Cierra la ventana de edición
        ventana_personal_esd.deiconify()  # Muestra nuevamente la ventana de Personal ESD

    # Crear el botón "Salir"
    btn_salir = tk.Button(ventana_editar, text="Salir", command=salir_editar, font=("Arial", 14), bg="red", fg="white",
                          height=2, width=10)
    btn_salir.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # Posiciona el botón en la esquina inferior derecha

    # Configuración del protocolo para el cierre de ventana
    ventana_editar.protocol("WM_DELETE_WINDOW", salir_editar)

    # Ejecutar la ventana de edición
    ventana_editar.mainloop()


# Función para cancelar la edición y volver a la ventana anterior
def cancelar_edicion(ventana_editar, ventana_personal_esd):
    ventana_editar.destroy()  # Cierra la ventana de edición
    ventana_personal_esd.deiconify()  # Muestra nuevamente la ventana de Personal ESD


# Función para obtener áreas únicas de la base de datos
def obtener_areas_unicas():
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT area FROM personal_esd")
        areas = [row[0] for row in cursor.fetchall()]
        return areas
    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"Se produjo un error al obtener áreas: {e}")
        return []
    finally:
        if 'connection' in locals():
            connection.close()


# Función para obtener líneas únicas de la base de datos
def obtener_lineas_unicas():
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT linea FROM personal_esd")
        lineas = [row[0] for row in cursor.fetchall()]
        return lineas
    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"Se produjo un error al obtener líneas: {e}")
        return []
    finally:
        if 'connection' in locals():
            connection.close()
