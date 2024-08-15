# En eliminar_usuario.py
from common import *
from settings.__init__ import db_path
from submains_personal.confirmar_eliminacion_de_usuario import confirmar_eliminacion, cargar_datos
from settings.conf_ventana import configurar_ventana
from strings_consultas_db import cargar_datos_usuario_eliminar


# Función para eliminar un usuario
def eliminar_usuario(root, ventana_personal_esd):
    ventana_personal_esd.withdraw()  # Oculta la ventana de Personal ESD
    ventana_eliminar = tk.Toplevel(root)  # Crear una nueva ventana hija de root
    configurar_ventana(ventana_eliminar, "Eliminar Usuario")

    # Conexión a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Variables para la paginación
    page_size = 10
    current_page = 1

    # Obtener áreas y líneas para los combobox
    cursor.execute("SELECT DISTINCT area FROM personal_esd WHERE estatus_usuario = 'Activo'")
    areas = [row[0] for row in cursor.fetchall()]

    def update_lineas(event):
        selected_area = combo_area.get()
        cursor.execute("SELECT DISTINCT linea FROM personal_esd WHERE estatus_usuario = 'Activo' AND area = ?", (selected_area,))
        lineas = [row[0] for row in cursor.fetchall()]
        combo_linea['values'] = lineas
        combo_linea.set('')

    # Widgets para selección de área y línea
    tk.Label(ventana_eliminar, text="Selecciona el Área:").pack(pady=5)
    combo_area = ttk.Combobox(ventana_eliminar, values=areas)
    combo_area.pack(pady=5)
    combo_area.bind("<<ComboboxSelected>>", update_lineas)

    tk.Label(ventana_eliminar, text="Selecciona la Línea:").pack(pady=5)
    combo_linea = ttk.Combobox(ventana_eliminar)
    combo_linea.pack(pady=5)

    # Botón para buscar usuarios
    def buscar_usuarios():
        nonlocal current_page
        current_page = 1
        area_seleccionada = combo_area.get()
        linea_seleccionada = combo_linea.get()
        cargar_datos(cursor, tree, label_pagina, btn_siguiente, btn_anterior, area_seleccionada, linea_seleccionada, page_size, current_page, cargar_datos_usuario_eliminar)

    btn_buscar = tk.Button(ventana_eliminar, text="Buscar", command=buscar_usuarios)
    btn_buscar.pack(pady=10)

    # Crear un marco para el Treeview y la barra de desplazamiento
    frame = tk.Frame(ventana_eliminar)
    frame.pack(pady=10)

    # Crear un Treeview para mostrar los datos
    tree = ttk.Treeview(frame, columns=("ID", "Nombre Usuario", "Rol", "Área", "Línea", "Puesto"), show='headings')
    tree.heading("ID", text="ID")  # Columna para ID, oculta
    tree.heading("Nombre Usuario", text="Nombre Usuario")
    tree.heading("Rol", text="Rol")
    tree.heading("Área", text="Área")
    tree.heading("Línea", text="Línea")
    tree.heading("Puesto", text="Puesto")

    # Opcionalmente, puedes ocultar la columna ID
    tree.column("ID", width=0, stretch=tk.NO)  # Ocultar la columna ID

    # Crear una barra de desplazamiento
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    # Colocar el Treeview y la barra de desplazamiento
    tree.pack(side=tk.LEFT)
    scrollbar.pack(side=tk.RIGHT, fill='y')

    # Crear botones para la paginación
    def siguiente_pagina():
        nonlocal current_page
        current_page += 1
        buscar_usuarios()

    def anterior_pagina():
        nonlocal current_page
        current_page -= 1
        buscar_usuarios()

    btn_siguiente = tk.Button(ventana_eliminar, text="Siguiente", command=siguiente_pagina)
    btn_siguiente.pack(side=tk.RIGHT, padx=5, pady=5)

    btn_anterior = tk.Button(ventana_eliminar, text="Anterior", command=anterior_pagina)
    btn_anterior.pack(side=tk.RIGHT, padx=5, pady=5)

    label_pagina = tk.Label(ventana_eliminar, text="")
    label_pagina.pack(side=tk.RIGHT, padx=5, pady=5)

    # Función para salir del programa
    def salir_eliminar():
        ventana_eliminar.destroy()
        ventana_personal_esd.deiconify()  # Mostrar la ventana Personal ESD

    # Botón para eliminar usuario
    boton_eliminar = tk.Button(ventana_eliminar, text="Eliminar Usuario",
                               command=lambda: confirmar_eliminacion(tree, ventana_eliminar, db_path))
    boton_eliminar.pack(pady=10)

    # Crear el botón "Salir"
    btn_salir = tk.Button(ventana_eliminar, text="Salir", command=salir_eliminar, font=("Arial", 14),
                          bg="red", fg="white", height=2, width=10)

    btn_salir.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

    # Asegúrate de cerrar correctamente al cerrar la ventana
    ventana_eliminar.protocol("WM_DELETE_WINDOW", salir_eliminar)

    # Ocultar la ventana principal al abrir la ventana de eliminación
    root.withdraw()

    # Ejecutar la ventana de eliminación
    ventana_eliminar.mainloop()
