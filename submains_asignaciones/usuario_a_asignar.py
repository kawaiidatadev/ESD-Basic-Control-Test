from settings.__init__ import *  # Importar los paths
from settings.conf_ventana import configurar_ventana

def mostrar_usuarios_disponibles(bata_id):
    # Crear la ventana para seleccionar usuario
    ventana_usuarios = tk.Toplevel()
    configurar_ventana(ventana_usuarios, "Seleccionar Usuario para Asignar")

    # Crear tabla para mostrar usuarios
    columns = ("ID", "Nombre", "Rol", "Estatus de Bata")
    tabla_usuarios = ttk.Treeview(ventana_usuarios, columns=columns, show='headings', height=10)
    for col in columns:
        tabla_usuarios.heading(col, text=col)
    tabla_usuarios.pack(side=tk.LEFT)

    # Scrollbar
    scrollbar = ttk.Scrollbar(ventana_usuarios, orient="vertical", command=tabla_usuarios.yview)
    tabla_usuarios.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Obtener usuarios disponibles
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """SELECT id, nombre_usuario, rol, bata_estatus FROM personal_esd 
               WHERE (bata_estatus = 'Sin asignar' OR bata_estatus = 'Disponible') 
               AND estatus_usuario = 'Activo';"""
    cursor.execute(query)
    usuarios = cursor.fetchall()
    conn.close()

    # Insertar usuarios en la tabla
    for usuario in usuarios:
        tabla_usuarios.insert("", "end", values=usuario)

    # Función para asignar la bata al usuario seleccionado
    def asignar_bata():
        seleccion = tabla_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un usuario para asignar la bata.")
            return

        usuario_id = tabla_usuarios.item(seleccion[0])['values'][0]

        # Aquí puedes agregar la lógica para actualizar los estatus en la base de datos
        # por ejemplo, actualizando el estatus de la bata y del usuario en la base de datos.

        messagebox.showinfo("Éxito", f"Bata con ID {bata_id} asignada a usuario con ID {usuario_id}.")
        ventana_usuarios.destroy()

    btn_asignar = tk.Button(ventana_usuarios, text="Asignar Bata", command=asignar_bata)
    btn_asignar.pack(pady=10)

    ventana_usuarios.mainloop()
