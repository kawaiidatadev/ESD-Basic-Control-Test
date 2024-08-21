from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path  # Importar la ruta de la base de datos


def asignaciones_taloneras(taloneras_asignaciones, root):
    ventana_asignaciones = tk.Toplevel(root)
    taloneras_asignaciones.withdraw()  # Ocultar la ventana anterior
    configurar_ventana(ventana_asignaciones, "Asignar Talonera ESD")

    # Frame principal para contener la tabla y los botones
    frame_principal = tk.Frame(ventana_asignaciones)
    frame_principal.pack(fill=tk.BOTH, expand=True)

    # Crear un Treeview para mostrar la tabla con Scrollbars
    columnas = ("id", "nombre_usuario", "rol", "area", "linea", "puesto", "talonera_estatus")
    tree = ttk.Treeview(frame_principal, columns=columnas, show='headings', height=15)

    # Configurar Scrollbars
    scrollbar_x = ttk.Scrollbar(frame_principal, orient=tk.HORIZONTAL, command=tree.xview)
    scrollbar_y = ttk.Scrollbar(frame_principal, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

    # Definir los encabezados de la tabla
    tree.heading("id", text="ID")
    tree.heading("nombre_usuario", text="Nombre Usuario")
    tree.heading("rol", text="Rol")
    tree.heading("area", text="Área")
    tree.heading("linea", text="Línea")
    tree.heading("puesto", text="Puesto")
    tree.heading("talonera_estatus", text="Talonera Estatus")

    # Ajustar el tamaño de las columnas
    for col in columnas:
        tree.column(col, anchor=tk.CENTER, width=100)

    tree.pack(fill=tk.BOTH, expand=True)

    # Conectar a la base de datos y obtener los datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre_usuario, rol, area, linea, puesto, talonera_estatus 
        FROM personal_esd 
        WHERE estatus_usuario = 'Activo' AND talonera_estatus != 'Asignada'
    """)
    rows = cursor.fetchall()

    # Insertar los datos en la tabla
    for row in rows:
        tree.insert("", tk.END, values=row)

    cursor.close()
    conn.close()

    # Botón para salir del registro sin hacer cambios
    def salir_programa():
        ventana_asignaciones.destroy()
        taloneras_asignaciones.deiconify()

    # Botón para salir
    btn_salir = tk.Button(ventana_asignaciones, text="Salir", command=salir_programa, font=("Arial", 14), bg="red",
                          fg="white", height=2, width=15)
    btn_salir.pack(side=tk.BOTTOM, padx=10, pady=10, anchor='e')

    # Botón para asignar talonera (sin funcionalidad aún)
    btn_asignar = tk.Button(ventana_asignaciones, text="Asignar", font=("Arial", 14), bg="green", fg="white", height=2,
                            width=15)
    btn_asignar.pack(side=tk.BOTTOM, padx=10, pady=10, anchor='e')

    ventana_asignaciones.protocol("WM_DELETE_WINDOW", salir_programa)
