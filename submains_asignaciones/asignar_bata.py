from common import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import *  # Importar los paths
from strings_consultas_db import registrar_nueva_bata_esd
from submains_asignaciones.usuario_a_asignar import mostrar_usuarios_disponibles
from strings_consultas_db import obtener_tamanos_unicos, obtener_tipos_unicos

# Variables globales para manejar la paginación
current_page = 1
items_per_page = 10


def obtener_batas_disponibles(tamano, tipo):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """SELECT id, numero_serie, tamaño, comentarios FROM esd_items 
               WHERE estatus != 'Asignada' and estatus != 'Eliminada'
               AND (tamaño = ? OR ? = '') 
               AND (tipo_elemento = ? OR ? = '') 
               ORDER BY tamaño
               LIMIT ? OFFSET ?;"""
    cursor.execute(query, (tamano, tamano, tipo, tipo, items_per_page, (current_page - 1) * items_per_page))
    results = cursor.fetchall()
    conn.close()
    return results


def contar_batas_disponibles(tamano, tipo):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """SELECT COUNT(*) FROM esd_items 
               WHERE estatus != 'Asignada' and estatus != 'Eliminada'
               AND (tamaño = ? OR ? = '') 
               AND (tipo_elemento = ? OR ? = '');"""
    cursor.execute(query, (tamano, tamano, tipo, tipo))
    count = cursor.fetchone()[0]
    conn.close()
    return count


def asignar_bata(ventana_batas_esd, root):
    global current_page

    asignar_batas_esd = tk.Toplevel(root)
    configurar_ventana(asignar_batas_esd, "Asignación de batas ESD")

    # Función para salir del programa
    def salir_programa():
        asignar_batas_esd.destroy()
        ventana_batas_esd.deiconify()

    # Crear el marco para la tabla
    frame_tabla = tk.Frame(asignar_batas_esd)
    frame_tabla.pack(pady=10)

    # Crear el árbol de la tabla
    columns = ("ID", "Número Serial", "Tamaño", "Comentarios")
    tabla_batas = ttk.Treeview(frame_tabla, columns=columns, show='headings', height=10)
    tabla_batas.heading("ID", text="ID")
    tabla_batas.heading("Número Serial", text="Número Serial")
    tabla_batas.heading("Tamaño", text="Tamaño")
    tabla_batas.heading("Comentarios", text="Comentarios")
    tabla_batas.pack(side=tk.LEFT)

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla_batas.yview)
    tabla_batas.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Obtener listas dinámicas de tamaño y tipo
    tamanos = obtener_tamanos_unicos() + [""]
    tipos = obtener_tipos_unicos() + [""]

    # Crear opciones de tamaño y tipo
    lbl_tamano = tk.Label(asignar_batas_esd, text="Tamaño:")
    lbl_tamano.pack(pady=5)
    entry_tamano = ttk.Combobox(asignar_batas_esd, values=tamanos)
    entry_tamano.pack(pady=5)

    # Filtrar la lista para eliminar valores vacíos
    tipos = [tipo for tipo in tipos if tipo.strip()]

    lbl_tipo = tk.Label(asignar_batas_esd, text="Tipo de Bata:")
    lbl_tipo.pack(pady=5)
    entry_tipo = ttk.Combobox(asignar_batas_esd, values=tipos)
    entry_tipo.set("Bata ESD")  # Establece "Bata ESD" como valor por defecto
    entry_tipo.pack(pady=5)

    # Función para actualizar la tabla
    def actualizar_tabla():
        tamano = entry_tamano.get()
        tipo = entry_tipo.get()

        # Limpiar tabla
        tabla_batas.delete(*tabla_batas.get_children())

        # Obtener y mostrar datos
        batas = obtener_batas_disponibles(tamano, tipo)
        for bata in batas:
            tabla_batas.insert("", "end", values=bata)

        # Actualizar la paginación
        total_batas = contar_batas_disponibles(tamano, tipo)
        btn_siguiente["state"] = "normal" if current_page * items_per_page < total_batas else "disabled"
        btn_anterior["state"] = "normal" if current_page > 1 else "disabled"

    # Función para cambiar la página
    def cambiar_pagina(direccion):
        global current_page
        current_page += direccion
        actualizar_tabla()

    # Botón de buscar
    btn_buscar = tk.Button(asignar_batas_esd, text="Buscar", command=actualizar_tabla,
                           font=("Arial", 12, "bold"), bg="#3498db", fg="white", width=20, height=2,
                           compound=tk.LEFT, relief=tk.RAISED, borderwidth=2)
    btn_buscar.pack(pady=10, padx=20)

    # Mejorar presentación de los botones de paginación
    btn_anterior = tk.Button(asignar_batas_esd, text="Página Anterior", command=lambda: cambiar_pagina(-1),
                             font=("Arial", 10, "bold"), bg="#3498db", fg="white", width=15, height=2)
    btn_anterior.pack(side=tk.LEFT, padx=20, pady=10)

    btn_siguiente = tk.Button(asignar_batas_esd, text="Siguiente Página", command=lambda: cambiar_pagina(1),
                              font=("Arial", 10, "bold"), bg="#3498db", fg="white", width=15, height=2)
    btn_siguiente.pack(side=tk.RIGHT, padx=20, pady=10)

    # Crear el botón "Salir"
    btn_salir = tk.Button(asignar_batas_esd, text="Salir", command=salir_programa, font=("Arial", 14), bg="red",
                          fg="white", height=2, width=10)
    btn_salir.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # Posiciona el botón en la esquina inferior derecha

    # Crear el botón "Asignar" con mejor presentación
    btn_asignar = tk.Button(asignar_batas_esd, text="Asignar Bata", command=lambda: asignar_bata_a_usuario(tabla_batas),
                            font=("Arial", 12, "bold"), bg="#2ecc71", fg="white", width=20, height=3)
    btn_asignar.pack(pady=20)

    # Función para asignar una bata a un usuario
    def asignar_bata_a_usuario(tabla):
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una bata para asignar.")
            return
        # Obtener ID de la bata seleccionada
        bata_id = tabla.item(seleccion[0])['values'][0]

        # Obtener el tipo de bata seleccionado
        tipo_elemento = entry_tipo.get()  # Asegúrate de que `entry_tipo` esté accesible aquí

        # Abrir la ventana para seleccionar el usuario
        mostrar_usuarios_disponibles(bata_id, asignar_batas_esd, tipo_elemento)

        asignar_batas_esd.after(500, actualizar_tabla)  # Retraso para permitir que la ventana de usuario se cierre

    # Función para actualizar la tabla cuando la ventana se muestra
    def al_mostrar_ventana(event):
        actualizar_tabla()

    # Asociar el evento <<Show>> para actualizar la tabla al mostrar la ventana
    asignar_batas_esd.bind("<Map>", al_mostrar_ventana)

    # Ocultar la ventana principal al abrir la ventana de asignación
    ventana_batas_esd.withdraw()
    asignar_batas_esd.protocol("WM_DELETE_WINDOW", salir_programa)
    asignar_batas_esd.mainloop()


