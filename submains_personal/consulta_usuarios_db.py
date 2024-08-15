from common import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path
from strings_consultas_db import consulta_de_usuarios


# Función para abrir la ventana de consulta de usuarios
def consultar_usuario(root, ventana_personal_esd):
    ventana_personal_esd.withdraw()
    ventana_consulta = tk.Toplevel(root)
    configurar_ventana(ventana_consulta, "Consulta de Usuarios ESD")

    # Conexión a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Variables para la paginación
    page_size = 10
    current_page = 1

    # Función para cargar los datos de los usuarios en la tabla
    def cargar_datos(page):
        query = consulta_de_usuarios
        cursor.execute(query, (page_size, (page - 1) * page_size))
        rows = cursor.fetchall()

        for row in tree.get_children():
            tree.delete(row)

        for row in rows:
            tree.insert("", tk.END, values=row)

        # Actualiza el label de la página
        label_pagina.config(text=f"Página {current_page}")

        # Verificar si hay más páginas
        cursor.execute("SELECT COUNT(*) FROM personal_esd")
        total_users = cursor.fetchone()[0]
        if current_page * page_size >= total_users:
            btn_siguiente.config(state=tk.DISABLED)
        else:
            btn_siguiente.config(state=tk.NORMAL)

        if current_page > 1:
            btn_anterior.config(state=tk.NORMAL)
        else:
            btn_anterior.config(state=tk.DISABLED)

    # Crear un marco para el Treeview y la barra de desplazamiento
    frame = tk.Frame(ventana_consulta)
    frame.pack(pady=10)

    # Crear un Treeview para mostrar los datos
    tree = ttk.Treeview(frame, columns=("Nombre", "Área", "Línea", "Rol", "Estatus", "Bata Estatus", "Bata Polar Estatus", "Pulsera Estatus", "Talonera Estatus"), show='headings')
    tree.heading("Nombre", text="Nombre")
    tree.heading("Área", text="Área")
    tree.heading("Línea", text="Línea")
    tree.heading("Rol", text="Rol")
    tree.heading("Estatus", text="Estatus")
    tree.heading("Bata Estatus", text="Bata Estatus")
    tree.heading("Bata Polar Estatus", text="Bata Polar Estatus")
    tree.heading("Pulsera Estatus", text="Pulsera Estatus")
    tree.heading("Talonera Estatus", text="Talonera Estatus")

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
        cargar_datos(current_page)

    def anterior_pagina():
        nonlocal current_page
        current_page -= 1
        cargar_datos(current_page)

    btn_siguiente = tk.Button(ventana_consulta, text="Siguiente", command=siguiente_pagina)
    btn_siguiente.pack(side=tk.RIGHT, padx=5, pady=5)

    btn_anterior = tk.Button(ventana_consulta, text="Anterior", command=anterior_pagina)
    btn_anterior.pack(side=tk.RIGHT, padx=5, pady=5)

    label_pagina = tk.Label(ventana_consulta, text="")
    label_pagina.pack(side=tk.RIGHT, padx=5, pady=5)

    # Cargar la primera página de datos
    cargar_datos(current_page)

    # Función para salir de la consulta de usuarios y regresar a la ventana de Personal ESD
    def salir_consulta():
        ventana_consulta.destroy()  # Cierra y destruye la ventana de consulta
        ventana_personal_esd.deiconify()  # Muestra nuevamente la ventana de Personal ESD

    # Crear el botón "Salir"
    btn_salir = tk.Button(ventana_consulta, text="Salir", command=salir_consulta, font=("Arial", 14), bg="red", fg="white", height=2, width=10)
    btn_salir.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

    # Ocultar la ventana principal al abrir la ventana de consulta
    root.withdraw()  # Oculta la ventana principal

    # Ejecutar la ventana de consulta
    ventana_consulta.protocol("WM_DELETE_WINDOW", salir_consulta)  # Asegúrate de cerrar correctamente
    ventana_consulta.mainloop()