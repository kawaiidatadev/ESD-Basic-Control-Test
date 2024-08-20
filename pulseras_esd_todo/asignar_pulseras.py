from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path
from pulseras_esd_todo.responsiva_pulseras import generar_responsiva_pulseras
def ventana_asignar_pulseras(pulseras_asignaciones):
    ventana_asignar = tk.Toplevel(pulseras_asignaciones)
    pulseras_asignaciones.withdraw()
    configurar_ventana(ventana_asignar, "Asignación de pulseras ESD")

    # Frame para la tabla de usuarios con barras de desplazamiento
    frame = tk.Frame(ventana_asignar)
    frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=("ID", "Nombre", "Rol", "Área", "Línea", "Puesto", "Pulsera"), show="headings", height=15)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscroll=scrollbar_y.set)

    scrollbar_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscroll=scrollbar_x.set)

    # Configurar encabezados de columnas
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre Usuario")
    tree.heading("Rol", text="Rol")
    tree.heading("Área", text="Área")
    tree.heading("Línea", text="Línea")
    tree.heading("Puesto", text="Puesto")
    tree.heading("Pulsera", text="Pulsera Estatus")

    # Ajustar el ancho de las columnas
    tree.column("ID", width=50, anchor=tk.CENTER)
    tree.column("Nombre", width=150, anchor=tk.W)
    tree.column("Rol", width=100, anchor=tk.W)
    tree.column("Área", width=100, anchor=tk.W)
    tree.column("Línea", width=100, anchor=tk.W)
    tree.column("Puesto", width=150, anchor=tk.W)
    tree.column("Pulsera", width=100, anchor=tk.W)

    # Obtener la lista de usuarios activos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre_usuario, rol, area, linea, puesto, pulsera_estatus 
        FROM personal_esd 
        WHERE estatus_usuario = 'Activo'  and pulsera_estatus != 'Asignada'
        ORDER BY nombre_usuario
    """)

    usuarios = cursor.fetchall()

    for usuario in usuarios:
        tree.insert("", tk.END, values=usuario)

    conn.close()

    # Función para asignar la pulsera
    def asignar_pulsera():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un usuario.")
            return

        usuario_seleccionado = tree.item(seleccion[0], "values")
        usuario_id = usuario_seleccionado[0]
        nombre_usuario = usuario_seleccionado[1]
        area = usuario_seleccionado[3]
        linea = usuario_seleccionado[4]
        puesto = usuario_seleccionado[5]  # Suponiendo que 'puesto' se usa como tipo_elemento

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Buscar una pulsera disponible
            cursor.execute("""
                SELECT id, numero_serie 
                FROM esd_items 
                WHERE tipo_elemento = 'Pulsera ESD' AND estatus = 'Sin asignar' 
                LIMIT 1
            """)
            pulsera = cursor.fetchone()

            if not pulsera:
                messagebox.showwarning("Advertencia", "No hay pulseras disponibles para asignar.")
                return

            pulsera_id, numero_serie = pulsera

            # Asignar la pulsera y actualizar la base de datos
            cursor.execute("""
                UPDATE esd_items 
                SET estatus = 'Asignada' 
                WHERE id = ?
            """, (pulsera_id,))

            cursor.execute("""
                INSERT INTO usuarios_elementos (usuario_id, esd_item_id, fecha_asignacion)
                VALUES (?, ?, ?)
            """, (usuario_id, pulsera_id, datetime.now()))

            cursor.execute("""
                UPDATE personal_esd 
                SET pulsera_estatus = 'Asignada' 
                WHERE id = ?
            """, (usuario_id,))

            conn.commit()
            messagebox.showinfo("Asignación Exitosa", "La pulsera ha sido asignada exitosamente.")

            # Eliminar la fila del Treeview
            tree.delete(seleccion[0])

            # Llamar a la función para generar la responsiva de pulseras
            generar_responsiva_pulseras(usuario_id, nombre_usuario, area, linea, "Pulsera ESD", numero_serie)

        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"Ha ocurrido un error al asignar la pulsera: {e}")
        finally:
            conn.close()

    # Crear el botón "Asignar"
    btn_asignar = tk.Button(ventana_asignar, text="Asignar", command=asignar_pulsera, font=("Arial", 14), bg="green",
                            fg="white", height=2, width=15)
    btn_asignar.pack(pady=10)

    # Función para salir de la ventana de asignación
    def salir_asignacion():
        ventana_asignar.destroy()
        pulseras_asignaciones.deiconify()

    # Crear el botón "Salir"
    btn_salir = tk.Button(ventana_asignar, text="Salir", command=salir_asignacion, font=("Arial", 14), bg="red",
                          fg="white", height=2, width=15)
    btn_salir.pack(pady=10)