from common.__init__ import *
from settings.__init__ import db_path, imagen_eliminar_actividad1, imagen2_eliminar_actividad1
from settings.conf_ventana import configurar_ventana
from settings.__init__ import poner_imagen_de_fondo, imagen_editar_actividad1


def cargar_actividades():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre_actividad FROM actividades")
    actividades = cursor.fetchall()
    conn.close()
    return actividades


def eliminar_actividad(actividad_id, ventana):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM actividades WHERE id = ?", (actividad_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", f"Actividad con ID {actividad_id} eliminada exitosamente.")
        ventana.withdraw()

    except sqlite3.Error as e:
        messagebox.showerror("Error de base de datos", f"Ha ocurrido un error con la base de datos: {e}")


def eliminar_act(conf1):
    eliminar_actividades = tk.Toplevel()  # Crear una nueva ventana
    conf1.withdraw()  # Ocultar la ventana principal al abrir la ventana de eliminación
    configurar_ventana(eliminar_actividades, "Eliminar actividades")

    poner_imagen_de_fondo(eliminar_actividades, imagen_eliminar_actividad1, 200, 600, x=600, y=200)
    poner_imagen_de_fondo(eliminar_actividades, imagen2_eliminar_actividad1, 400, 600, x=50, y=200)


    # Crear combobox para seleccionar la actividad
    actividades = cargar_actividades()
    combo_actividades = ttk.Combobox(eliminar_actividades, values=[f"{act[0]} - {act[1]}" for act in actividades],
                                     state="readonly", width=50)
    combo_actividades.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

    # Crear etiquetas para mostrar los datos de la actividad seleccionada
    lbl_nombre = tk.Label(eliminar_actividades, text="Nombre de la Actividad:", font=("Arial", 12))
    lbl_nombre.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    lbl_nombre_val = tk.Label(eliminar_actividades, text="", font=("Arial", 12), relief="sunken", width=40)
    lbl_nombre_val.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    lbl_descripcion = tk.Label(eliminar_actividades, text="Descripción:", font=("Arial", 12))
    lbl_descripcion.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    lbl_descripcion_val = tk.Label(eliminar_actividades, text="", font=("Arial", 12), relief="sunken", width=40)
    lbl_descripcion_val.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    lbl_frecuencia = tk.Label(eliminar_actividades, text="Frecuencia:", font=("Arial", 12))
    lbl_frecuencia.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    lbl_frecuencia_val = tk.Label(eliminar_actividades, text="", font=("Arial", 12), relief="sunken", width=40)
    lbl_frecuencia_val.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    lbl_fecha_ultima = tk.Label(eliminar_actividades, text="Fecha Última:", font=("Arial", 12))
    lbl_fecha_ultima.grid(row=4, column=0, padx=10, pady=5, sticky="e")
    lbl_fecha_ultima_val = tk.Label(eliminar_actividades, text="", font=("Arial", 12), relief="sunken", width=40)
    lbl_fecha_ultima_val.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    lbl_equipo = tk.Label(eliminar_actividades, text="Equipo de Medición:", font=("Arial", 12))
    lbl_equipo.grid(row=5, column=0, padx=10, pady=5, sticky="e")
    lbl_equipo_val = tk.Label(eliminar_actividades, text="", font=("Arial", 12), relief="sunken", width=40)
    lbl_equipo_val.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    def cargar_datos_actividad(event):
        selected_value = combo_actividades.get()
        if selected_value:
            actividad_id = int(selected_value.split(" - ")[0])

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT nombre_actividad, descripcion, frecuencia, fecha_ultima, equipo_de_medicion FROM actividades WHERE id = ?", (actividad_id,))
            actividad = cursor.fetchone()
            conn.close()

            if actividad:
                lbl_nombre_val.config(text=actividad[0])
                lbl_descripcion_val.config(text=actividad[1])
                lbl_frecuencia_val.config(text=actividad[2])
                lbl_fecha_ultima_val.config(text=actividad[3])
                lbl_equipo_val.config(text=actividad[4])

    combo_actividades.bind("<<ComboboxSelected>>", cargar_datos_actividad)

    def confirmar_eliminacion():
        selected_value = combo_actividades.get()
        if selected_value:
            actividad_id = int(selected_value.split(" - ")[0])
            if messagebox.askyesno("Confirmación", f"¿Estás seguro de que deseas eliminar la actividad con ID {actividad_id}?"):
                eliminar_actividad(actividad_id, eliminar_actividades)
                conf1.deiconify()

    # Crear el botón Eliminar
    btn_eliminar = tk.Button(eliminar_actividades, text="Eliminar", command=confirmar_eliminacion,
                             font=("Arial", 14), bg="red", fg="white", height=2, width=10)
    btn_eliminar.grid(row=6, column=1, padx=10, pady=10, sticky='e')

    # Crear el botón Salir
    btn_salir = tk.Button(eliminar_actividades, text="Salir", command=lambda: (eliminar_actividades.withdraw(), conf1.deiconify()),
                          font=("Arial", 14), bg="red", fg="white", height=2, width=10)
    btn_salir.grid(row=6, column=0, padx=10, pady=10, sticky='w')


