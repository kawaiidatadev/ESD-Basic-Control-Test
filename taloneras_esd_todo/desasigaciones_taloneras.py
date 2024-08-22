from common.__init__ import *
from settings.__init__ import db_path
from settings.conf_ventana import configurar_ventana

def ventana_desasignar_taloneras(taloneras_asignaciones):
    ventana_desasignar_talonera = tk.Toplevel(taloneras_asignaciones)
    taloneras_asignaciones.withdraw()
    configurar_ventana(ventana_desasignar_talonera, "Desasignación de taloneras ESD")

    # Frame para la tabla de usuarios con barras de desplazamiento
    frame = tk.Frame(ventana_desasignar_talonera)
    frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=("ID", "Nombre", "Rol", "Área", "Línea", "Puesto", "Talonera"), show="headings", height=15)
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
    tree.heading("Talonera", text="Pulsera Estatus")

    # Ajustar el ancho de las columnas
    tree.column("ID", width=50, anchor=tk.CENTER)
    tree.column("Nombre", width=150, anchor=tk.W)
    tree.column("Rol", width=100, anchor=tk.W)
    tree.column("Área", width=100, anchor=tk.W)
    tree.column("Línea", width=100, anchor=tk.W)
    tree.column("Puesto", width=150, anchor=tk.W)
    tree.column("Talonera", width=100, anchor=tk.W)

    # Obtener la lista de usuarios activos con taloneras asignadas
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.id, p.nombre_usuario, p.rol, p.area, p.linea, p.puesto, p.talonera_estatus
        FROM personal_esd p
        WHERE p.estatus_usuario = 'Activo' AND p.talonera_estatus = 'Asignada'
        ORDER BY p.nombre_usuario
    """)

    usuarios = cursor.fetchall()

    for usuario in usuarios:
        tree.insert("", tk.END, values=usuario)

    conn.close()

    # Función para desasignar o eliminar la talonera
    def desasignar_una_talonera():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un usuario.")
            return

        usuario_seleccionado = tree.item(seleccion[0], "values")
        usuario_id = usuario_seleccionado[0]
        nombre_usuario = usuario_seleccionado[1]

        # Preguntar si se quiere eliminar o solo desasignar
        respuesta = messagebox.askquestion("Confirmación",
                                           "¿Deseas eliminar la talonera o solo desasignarla? (Selecciona 'Sí' para eliminar, 'No' para desasignar)")

        conn = None
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Buscar la talonera asignada al usuario
            cursor.execute("""
                SELECT ei.id
                FROM esd_items ei
                JOIN usuarios_elementos ue ON ei.id = ue.esd_item_id
                WHERE ue.usuario_id = ? AND ei.tipo_elemento = 'Talonera ESD' AND ei.estatus = 'Asignada'
            """, (usuario_id,))
            talonera = cursor.fetchone()

            if not talonera:
                messagebox.showwarning("Advertencia", "No se encontró ninguna talonera asignada para este usuario.")
                return

            talonera_esd = talonera[0]

            if respuesta == 'yes':
                # Eliminar la talonera del inventario
                cursor.execute("""
                    UPDATE esd_items
                    SET estatus = 'Eliminada'
                    WHERE id = ?
                """, (talonera_esd,))

            else:
                # Solo desasignar la talonera
                cursor.execute("""
                    UPDATE esd_items
                    SET estatus = 'Sin asignar'
                    WHERE id = ?
                """, (talonera_esd,))

            # Eliminar el registro de la relación en usuarios_elementos
            cursor.execute("""
                DELETE FROM usuarios_elementos
                WHERE usuario_id = ? AND esd_item_id = ?
            """, (usuario_id, talonera_esd))

            # Actualizar el estatus de la talonera en personal_esd
            cursor.execute("""
                UPDATE personal_esd
                SET talonera_estatus = 'Sin asignar'
                WHERE id = ?
            """, (usuario_id,))

            conn.commit()
            messagebox.showinfo("Desasignación Exitosa", "La talonera ha sido desasignada o eliminada exitosamente.")

            # Eliminar la fila del Treeview
            tree.delete(seleccion[0])

            # Actualizar la lista de usuarios
            # (Podrías recargar la lista completa si lo consideras necesario)

        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos",
                                 f"Ha ocurrido un error al desasignar o eliminar la talonera: {e}")
        finally:
            if conn:
                conn.close()

    # Crear el botón "Desasignar"
    btn_desasignar = tk.Button(ventana_desasignar_talonera, text="Desasignar", command=desasignar_una_talonera, font=("Arial", 14), bg="orange",
                               fg="white", height=2, width=15)
    btn_desasignar.pack(pady=10)

    # Función para salir de la ventana de desasignación
    def salir_desasignacion():
        ventana_desasignar_talonera.destroy()
        taloneras_asignaciones.deiconify()

    # Crear el botón "Salir"
    btn_salir = tk.Button(ventana_desasignar_talonera, text="Salir", command=salir_desasignacion, font=("Arial", 14), bg="red",
                          fg="white", height=2, width=15)
    btn_salir.pack(pady=10)
