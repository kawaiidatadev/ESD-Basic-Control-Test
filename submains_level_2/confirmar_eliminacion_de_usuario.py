from common.__init__ import *
def cargar_datos(cursor, tree, label_pagina, btn_siguiente, btn_anterior, area, linea, page_size, current_page, cargar_datos_usuario_eliminar):
    cursor.execute(cargar_datos_usuario_eliminar, (area, linea, page_size, (current_page - 1) * page_size))
    rows = cursor.fetchall()

    # Limpiar el Treeview antes de cargar nuevos datos
    for row in tree.get_children():
        tree.delete(row)

    for row in rows:
        # Supongamos que el ID del usuario está en la primera columna de la consulta
        tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))  # Incluye ID como parte de los valores

    # Actualiza el label de la página
    label_pagina.config(text=f"Página {current_page}")

    # Verificar si hay más páginas
    cursor.execute("SELECT COUNT(*) FROM personal_esd WHERE estatus_usuario = 'Activo' AND area = ? AND linea = ?", (area, linea))
    total_users = cursor.fetchone()[0]
    if current_page * page_size >= total_users:
        btn_siguiente.config(state="disabled")
    else:
        btn_siguiente.config(state="normal")

    if current_page > 1:
        btn_anterior.config(state="normal")
    else:
        btn_anterior.config(state="disabled")


def confirmar_eliminacion(tree, ventana_eliminar, db_path):
    conn = None  # Asegúrate de inicializar conn aquí
    try:
        # Obtener el ID seleccionado en el Treeview
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un usuario.")
            return

        # Obtener el usuario seleccionado (suponiendo que el ID está en la primera columna)
        usuario_seleccionado = tree.item(seleccionado[0], 'values')[0]
        print(f"ID del usuario seleccionado: {usuario_seleccionado}")

        # Preguntar si realmente desea eliminar al usuario
        respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que deseas eliminar este usuario?")
        if respuesta:
            conn = sqlite3.connect(db_path)  # Conectar a la base de datos
            cursor = conn.cursor()

            # Ejecutar la consulta de actualización
            cursor.execute("UPDATE personal_esd SET estatus_usuario = 'Baja' WHERE id = ?", (usuario_seleccionado,))
            conn.commit()

            # Verificar si se actualizó alguna fila
            if cursor.rowcount == 0:
                messagebox.showwarning("Advertencia", "No se encontró ningún usuario con ese ID.")
            else:
                messagebox.showinfo("Éxito", "El usuario ha sido eliminado.")
                ventana_eliminar.destroy()  # Cerrar la ventana

    except sqlite3.Error as e:
        # Manejo de errores de la base de datos
        messagebox.showerror("Error de Base de Datos", f"Ocurrió un error al eliminar el usuario: {e}")

    except Exception as e:
        # Manejo de cualquier otro tipo de error
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

    finally:
        # Cerrar la conexión a la base de datos si está abierta
        try:
            if conn:
                conn.close()
        except NameError:
            pass  # Si conn no está definida, no hacer nada
