from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path

def cumplimiento_4_2(sub_ventana_act):
    sub_ventana_cumplimiento = tk.Toplevel()  # Crear una nueva ventana
    sub_ventana_act.withdraw()  # Ocultar la ventana principal al abrir la ventana de cumplimiento
    configurar_ventana(sub_ventana_cumplimiento, "Actividades de cumplimiento", "1100x900")

    # Título centrado
    lbl_titulo = tk.Label(sub_ventana_cumplimiento, text="Cumplimiento de actividades", font=("Arial", 16, "bold"))
    lbl_titulo.pack(pady=10)

    # Crear un marco para contener la tabla y las barras de desplazamiento
    frame_tabla = tk.Frame(sub_ventana_cumplimiento)
    frame_tabla.pack(padx=10, pady=10, fill="both", expand=True)

    # Crear una tabla (Treeview) para mostrar las actividades
    columnas = ("id", "actividad", "frecuencia", "ultima_fecha", "proxima_fecha", "estatus")
    tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

    for col in columnas:
        tree.heading(col, text=col.capitalize().replace("_", " "))
        tree.column(col, anchor="center")

    # Crear las barras de desplazamiento
    scrollbar_vertical = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
    scrollbar_horizontal = ttk.Scrollbar(frame_tabla, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)

    # Ubicar la tabla y las barras de desplazamiento en el marco
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar_vertical.grid(row=0, column=1, sticky="ns")
    scrollbar_horizontal.grid(row=1, column=0, sticky="ew")

    # Hacer que el marco se expanda con la ventana
    frame_tabla.grid_rowconfigure(0, weight=1)
    frame_tabla.grid_columnconfigure(0, weight=1)

    # Ajustar el ancho de las columnas automáticamente
    def ajustar_columnas(event):
        for col in columnas:
            tree.column(col, width=tkfont.Font().measure(col.capitalize().replace("_", " ")))
        for item in tree.get_children():
            for col in columnas:
                col_width = tkfont.Font().measure(tree.set(item, col))
                if tree.column(col, width=None) < col_width:
                    tree.column(col, width=col_width)

    tree.bind("<Configure>", ajustar_columnas)

    # Cargar los datos de la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre_actividad, frecuencia, fecha_ultima, proxima_fecha, estatus FROM actividades")
    actividades = cursor.fetchall()
    conn.close()

    for act in actividades:
        tree.insert("", "end", values=act)

    # Función para salir del programa
    def salir_programa():
        sub_ventana_cumplimiento.withdraw()
        sub_ventana_act.deiconify()

    # Botón para ir a la nueva ventana e imprimir el ID de la actividad seleccionada
    def abrir_nueva_ventana():
        selected_item = tree.selection()
        if selected_item:
            actividad_id = tree.item(selected_item)["values"][0]
            print(f"nueva ventana pendiente para ID: {actividad_id}")

    # Crear botón "Ir a detalles" deshabilitado al inicio
    btn_ir_a_detalles = tk.Button(sub_ventana_cumplimiento, text="Ir a detalles", command=abrir_nueva_ventana,
                                  font=("Arial", 12, "bold"), bg="blue", fg="white", height=1, width=20, relief="flat", bd=0)
    btn_ir_a_detalles.pack(pady=10)
    btn_ir_a_detalles.config(state="disabled")

    # Función para habilitar el botón al seleccionar una actividad
    def habilitar_boton(event):
        selected_item = tree.selection()
        if selected_item:
            btn_ir_a_detalles.config(state="normal")
        else:
            btn_ir_a_detalles.config(state="disabled")

    tree.bind("<<TreeviewSelect>>", habilitar_boton)

    # Crear el botón de salir
    btn_salir = tk.Button(sub_ventana_cumplimiento, text="Salir", command=salir_programa,
                          font=("Arial", 12, "bold"), bg="red", fg="white", height=1, width=10, relief="flat", bd=0)
    btn_salir.pack(pady=10)