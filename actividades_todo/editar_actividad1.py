from common.__init__ import *
from settings.__init__ import db_path
from settings.conf_ventana import configurar_ventana
from actividades_todo.db_editar_act import actualizar_datos
from settings.__init__ import poner_imagen_de_fondo, imagen_editar_actividad1

def limpiar_fecha(fecha_str):
    """
    Limpia y convierte la fecha del formato 'YYYY-MM-DD HH:MM:SS' o 'YYYY-MM-DD' al formato 'YYYY/MM/DD'.
    """
    formatos = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]
    for formato in formatos:
        try:
            fecha = datetime.strptime(fecha_str, formato)
            return fecha.strftime("%Y/%m/%d")
        except ValueError:
            continue
    messagebox.showerror("Error", "La fecha es inválida.")
    return None

def editar_act(conf1):
    editar_actividades = tk.Toplevel()  # Crear una nueva ventana
    conf1.withdraw()  # Ocultar la ventana principal al abrir la ventana de edición
    configurar_ventana(editar_actividades, "Edición de actividades")

    poner_imagen_de_fondo(editar_actividades, imagen_editar_actividad1, 400, 600, x=80, y=200)

    # Función para cargar las actividades en el combobox
    def cargar_actividades():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre_actividad FROM actividades")
        actividades = cursor.fetchall()
        conn.close()
        return actividades

    # Función para cargar los datos de la actividad seleccionada
    def cargar_datos_actividad(event):
        global actividad_id
        actividad_id = combo_actividades.get().split(" - ")[0]
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nombre_actividad, descripcion, frecuencia, fecha_ultima, equipo_de_medicion 
            FROM actividades WHERE id=?
        """, (actividad_id,))
        actividad = cursor.fetchone()
        conn.close()

        if actividad:
            entry_nombre_actividad.delete(0, tk.END)
            entry_nombre_actividad.insert(0, actividad[0])
            entry_descripcion.delete(0, tk.END)
            entry_descripcion.insert(0, actividad[1])
            combo_frecuencia.set(actividad[2])
            entry_equipo_medicion.delete(0, tk.END)
            entry_equipo_medicion.insert(0, actividad[4])

            if actividad[3] is not None:
                fecha_limpia = limpiar_fecha(actividad[3])
                if fecha_limpia:
                    try:
                        fecha_ultima = datetime.strptime(fecha_limpia, "%Y/%m/%d").date()
                        date_entry_fecha_ultima.set_date(fecha_ultima)
                    except ValueError:
                        messagebox.showerror("Error", "La fecha de última actividad es inválida.")
                else:
                    date_entry_fecha_ultima.set_date(None)
            else:
                date_entry_fecha_ultima.set_date(None)

    # Crear combobox para seleccionar la actividad
    actividades = cargar_actividades()
    combo_actividades = ttk.Combobox(editar_actividades, values=[f"{act[0]} - {act[1]}" for act in actividades],
                                     state="readonly", width=50)
    combo_actividades.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
    combo_actividades.bind("<<ComboboxSelected>>", cargar_datos_actividad)

    # Crear los campos editables
    tk.Label(editar_actividades, text="Nombre de la actividad:", font=("Arial", 12)).grid(row=1, column=0, sticky="e",
                                                                                          padx=10, pady=5)
    entry_nombre_actividad = tk.Entry(editar_actividades, font=("Arial", 12), width=50)
    entry_nombre_actividad.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(editar_actividades, text="Descripción:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=10,
                                                                               pady=5)
    entry_descripcion = tk.Entry(editar_actividades, font=("Arial", 12), width=50)
    entry_descripcion.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(editar_actividades, text="Frecuencia:", font=("Arial", 12)).grid(row=3, column=0, sticky="e", padx=10,
                                                                              pady=5)
    combo_frecuencia = ttk.Combobox(editar_actividades, values=[
        "Diario", "Semanal", "Mensual", "Cada 2 meses", "Cada 3 meses", "Cada 4 meses", "Cada 5 meses", "Cada 6 meses",
        "Cada 7 meses", "Cada 8 meses", "Cada 9 meses", "Cada 10 meses", "Cada 11 meses", "Anual", "Cada dos años",
        "Cada 3 años", "Autónomo"
    ], state="readonly", width=47)
    combo_frecuencia.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(editar_actividades, text="Fecha última:", font=("Arial", 12)).grid(row=4, column=0, sticky="e", padx=10,
                                                                                 pady=5)
    date_entry_fecha_ultima = DateEntry(editar_actividades, font=("Arial", 12), width=47, date_pattern='yyyy-mm-dd',
                                        state="normal")
    date_entry_fecha_ultima.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(editar_actividades, text="Equipo de medición:", font=("Arial", 12)).grid(row=5, column=0, sticky="e",
                                                                                      padx=10, pady=5)
    entry_equipo_medicion = tk.Entry(editar_actividades, font=("Arial", 12), width=50)
    entry_equipo_medicion.grid(row=5, column=1, padx=10, pady=5)

    # Crear el botón Actualizar
    btn_actualizar = tk.Button(editar_actividades, text="Actualizar", command=lambda: actualizar_datos(
        actividad_id,
        nombre_actividad=entry_nombre_actividad.get(),
        descripcion=entry_descripcion.get(),
        frecuencia=combo_frecuencia.get(),
        fecha_ultima=date_entry_fecha_ultima.get_date(),
        equipo_de_medicion=entry_equipo_medicion.get()
    ), font=("Arial", 14), bg="green", fg="white", height=2, width=10)
    btn_actualizar.grid(row=6, column=1, padx=10, pady=10, sticky='e')

    # Crear el botón Salir
    btn_salir = tk.Button(editar_actividades, text="Salir", command=lambda: (editar_actividades.withdraw(), conf1.deiconify()),
                          font=("Arial", 14), bg="red", fg="white", height=2, width=10)
    btn_salir.grid(row=6, column=0, padx=10, pady=10, sticky='w')

    # Configurar el grid para centrar los elementos
    for i in range(2):
        editar_actividades.grid_columnconfigure(i, weight=1)
    for i in range(7):
        editar_actividades.grid_rowconfigure(i, weight=1)
