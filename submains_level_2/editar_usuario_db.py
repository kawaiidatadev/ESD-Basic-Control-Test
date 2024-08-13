from common import *
from settings import db_path
from settings.conf_ventana import configurar_ventana

# Función para buscar usuarios en la base de datos
def buscar_usuarios(ventana_editar, var_area, var_linea):
    area = var_area.get()  # Accede al área seleccionada
    linea = var_linea.get()  # Accede a la línea seleccionada
    tabla = ventana_editar.children['!treeview']  # Obtiene la tabla

    # Limpiar tabla existente
    for item in tabla.get_children():
        tabla.delete(item)

    if area == "Seleccione una opción" or linea == "Seleccione una opción":
        messagebox.showerror("Error", "Debes seleccionar un área y una línea válidas.")
        return

    try:
        # Conexión a la base de datos
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Consultar usuarios según área y línea
        cursor.execute(
            "SELECT nombre_usuario, rol, area, linea, puesto FROM personal_esd WHERE area = ? AND linea = ?",
            (area, linea))
        usuarios = cursor.fetchall()
        print(usuarios)  # Agrega esta línea para depurar

        # Insertar resultados en la tabla
        for usuario in usuarios:
            tabla.insert("", tk.END, values=usuario)  # Insertar los datos

    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"Se produjo un error al buscar usuarios: {e}")

    finally:
        if 'connection' in locals():
            connection.close()

# Función para editar el usuario seleccionado
def editar_usuario_seleccionado(ventana_editar, var_area, var_linea):
    tabla = ventana_editar.children['!treeview']  # Obtiene la tabla
    seleccionado = tabla.selection()
    if not seleccionado:
        messagebox.showerror("Error", "Debes seleccionar un usuario para editar.")
        return

    # Obtener datos del usuario seleccionado
    usuario = tabla.item(seleccionado)['values']

    nombre_usuario = usuario[0]  # Nombre de usuario
    rol = usuario[1]  # Rol
    area = usuario[2]  # Área
    linea = usuario[3]  # Línea
    puesto = usuario[4]  # Puesto

    # Conexión a la base de datos para obtener el ID del usuario seleccionado
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM personal_esd WHERE nombre_usuario = ? AND rol = ? AND area = ? AND linea = ? AND puesto = ?",
            (nombre_usuario, rol, area, linea, puesto))
        id_usuario = cursor.fetchone()
        if id_usuario:
            id_usuario = id_usuario[0]
        else:
            messagebox.showerror("Error", "No se encontró el ID del usuario seleccionado.")
            return

    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"Se produjo un error al buscar el ID del usuario: {e}")
        return

    finally:
        if 'connection' in locals():
            connection.close()

    # Crear ventana para editar datos del usuario
    ventana_editar_usuario = tk.Toplevel()
    configurar_ventana(ventana_editar_usuario, "Editar Usuario")

    # Crear los campos de edición
    tk.Label(ventana_editar_usuario, text="Nombre de Usuario:", font=("Arial", 12)).pack(pady=10)
    entry_nombre_usuario = tk.Entry(ventana_editar_usuario)
    entry_nombre_usuario.insert(0, nombre_usuario)
    entry_nombre_usuario.pack(pady=5)

    tk.Label(ventana_editar_usuario, text="Rol:", font=("Arial", 12)).pack(pady=10)
    entry_rol = tk.Entry(ventana_editar_usuario)
    entry_rol.insert(0, rol)
    entry_rol.pack(pady=5)

    tk.Label(ventana_editar_usuario, text="Área:", font=("Arial", 12)).pack(pady=10)
    entry_area = tk.Entry(ventana_editar_usuario)
    entry_area.insert(0, area)
    entry_area.pack(pady=5)

    tk.Label(ventana_editar_usuario, text="Línea:", font=("Arial", 12)).pack(pady=10)
    entry_linea = tk.Entry(ventana_editar_usuario)
    entry_linea.insert(0, linea)
    entry_linea.pack(pady=5)

    tk.Label(ventana_editar_usuario, text="Puesto:", font=("Arial", 12)).pack(pady=10)
    entry_puesto = tk.Entry(ventana_editar_usuario)
    entry_puesto.insert(0, puesto)
    entry_puesto.pack(pady=5)

    # Botón para actualizar datos
    tk.Button(ventana_editar_usuario, text="Actualizar Datos",
              command=lambda: actualizar_datos(id_usuario, entry_nombre_usuario.get(), entry_rol.get(),
                                               entry_area.get(), entry_linea.get(), entry_puesto.get(),
                                               ventana_editar_usuario, ventana_editar, var_area, var_linea)).pack(
        pady=20)

    # Ejecutar la ventana de edición de usuario
    ventana_editar_usuario.mainloop()

# Llama a la función buscar_usuarios para actualizar la tabla
def recargar_tabla(ventana_editar, var_area, var_linea):
    buscar_usuarios(ventana_editar, var_area, var_linea)

# Función para actualizar los datos del usuario en la base de datos
def actualizar_datos(id_usuario, nombre_usuario_nuevo, rol_nuevo, area_nueva, linea_nueva, puesto_nuevo, ventana_editar_usuario, ventana_editar, var_area, var_linea):
    try:
        # Conexión a la base de datos
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Actualizar datos del usuario
        cursor.execute('''
            UPDATE personal_esd
            SET nombre_usuario = ?, rol = ?, area = ?, linea = ?, puesto = ?, fecha_registro = ?
            WHERE id = ?
        ''', (nombre_usuario_nuevo, rol_nuevo, area_nueva, linea_nueva, puesto_nuevo,
              datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id_usuario))

        connection.commit()
        messagebox.showinfo("Éxito", "Los datos del usuario se han actualizado correctamente.")
        ventana_editar_usuario.destroy()  # Cierra la ventana de edición de usuario

        # Recargar la tabla con los datos actualizados
        recargar_tabla(ventana_editar, var_area, var_linea)

    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"Se produjo un error al actualizar los datos: {e}")

    finally:
        if 'connection' in locals():
            connection.close()
