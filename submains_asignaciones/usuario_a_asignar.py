from settings.__init__ import *  # Importar los paths
from settings.conf_ventana import configurar_ventana


import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from settings.__init__ import *  # Importar los paths
from settings.conf_ventana import configurar_ventana


def mostrar_usuarios_disponibles(bata_id, asignar_batas_esd, tipo_elemento):
    # Crear la ventana
    ventana = tk.Toplevel()
    configurar_ventana(ventana, "Seleccionar usuario para asignar")

    # Conectar a la base de datos
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()

    # Crear marco para la tabla y la barra de desplazamiento
    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(fill=tk.BOTH, expand=True)

    # Crear tabla para mostrar usuarios
    tabla = ttk.Treeview(frame_tabla, columns=("id", "nombre_usuario", "bata_estatus", "bata_polar_estatus"),
                         show="headings")
    tabla.heading("id", text="ID")
    tabla.heading("nombre_usuario", text="Nombre Usuario")
    tabla.heading("bata_estatus", text="Bata ESD Estatus")
    tabla.heading("bata_polar_estatus", text="Bata Polar Estatus")

    # Añadir scrollbar vertical y horizontal
    scrollbar_vertical = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar_vertical.set)
    scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)

    scrollbar_horizontal = ttk.Scrollbar(frame_tabla, orient="horizontal", command=tabla.xview)
    tabla.configure(xscrollcommand=scrollbar_horizontal.set)
    scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)

    tabla.pack(fill=tk.BOTH, expand=True)

    # Función para actualizar la tabla
    def actualizar_tabla():
        tabla.delete(*tabla.get_children())  # Limpiar tabla

        # Filtrar usuarios según el tipo de bata
        if tipo_elemento == "Bata ESD":
            query = "SELECT id, nombre_usuario, bata_estatus, bata_polar_estatus FROM personal_esd WHERE bata_estatus != 'Asignada'"
        elif tipo_elemento == "Bata Polar ESD":
            query = "SELECT id, nombre_usuario, bata_estatus, bata_polar_estatus FROM personal_esd WHERE bata_polar_estatus != 'Asignada'"
        else:
            messagebox.showerror("Error", "Tipo de elemento no válido.")
            ventana.destroy()
            return

        cursor.execute(query)
        usuarios = cursor.fetchall()

        for usuario in usuarios:
            tabla.insert("", tk.END, values=usuario)

    # Llamar a la función para actualizar la tabla al abrir la ventana
    actualizar_tabla()

    def verificar_estatus(usuario_id):
        # Verificar el estatus del usuario
        cursor.execute("SELECT bata_estatus, bata_polar_estatus FROM personal_esd WHERE id = ?", (usuario_id,))
        estatus = cursor.fetchone()

        if not estatus:
            return "No existe el usuario."

        bata_esd_estatus, bata_polar_estatus = estatus

        if tipo_elemento == "Bata ESD" and bata_esd_estatus == 'Asignada':
            return "El usuario ya tiene una Bata ESD asignada."
        elif tipo_elemento == "Bata Polar ESD" and bata_polar_estatus == 'Asignada':
            return "El usuario ya tiene una Bata Polar ESD asignada."
        return None

    def asignar_bata():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un usuario para asignar la bata.")
            return

        usuario_id = tabla.item(seleccion[0])['values'][0]

        # Verificar el estatus del usuario
        mensaje_error = verificar_estatus(usuario_id)
        if mensaje_error:
            messagebox.showwarning("Advertencia", mensaje_error)
            return

        # Actualizar estatus en personal_esd
        if tipo_elemento == "Bata ESD":
            cursor.execute("UPDATE personal_esd SET bata_estatus = 'Asignada' WHERE id = ?", (usuario_id,))
            cursor.execute("UPDATE esd_items SET estatus = 'Asignada' WHERE id = ?", (bata_id,))
        elif tipo_elemento == "Bata Polar ESD":
            cursor.execute("UPDATE personal_esd SET bata_polar_estatus = 'Asignada' WHERE id = ?", (usuario_id,))
            cursor.execute("UPDATE esd_items SET estatus = 'Asignada' WHERE id = ?", (bata_id,))

        # Registrar la asignación en usuarios_elementos
        cursor.execute("INSERT INTO usuarios_elementos (usuario_id, esd_item_id) VALUES (?, ?)", (usuario_id, bata_id))

        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", "Bata asignada correctamente.")
        ventana.destroy()
        asignar_batas_esd.deiconify()  # Muestra nuevamente la ventana principal

    # Botón para asignar la bata
    boton_asignar = tk.Button(ventana, text="Asignar", command=asignar_bata, font=("Arial", 12, "bold"), bg="#2ecc71",
                             fg="white", width=15, height=2)
    boton_asignar.pack(pady=10)

    # Función para salir del programa
    def salir_programa():
        ventana.destroy()  # Destruye el objeto
        asignar_batas_esd.deiconify()  # Muestra nuevamente la ventana principal

    # Crear el botón "Salir"
    btn_salir = tk.Button(ventana, text="Salir", command=salir_programa, font=("Arial", 14), bg="red",
                          fg="white", height=2, width=10)
    btn_salir.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # Posiciona el botón en la esquina inferior derecha

    # Ocultar la ventana principal al abrir la ventana de asignación
    asignar_batas_esd.withdraw()
    ventana.protocol("WM_DELETE_WINDOW", salir_programa)
    ventana.mainloop()

