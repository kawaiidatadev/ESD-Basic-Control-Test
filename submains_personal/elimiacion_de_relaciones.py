from common.__init__ import *
from settings.__init__ import db_path
from settings.conf_ventana import configurar_ventana
from strings_consultas_db import tipos_elementos_del_usuario_id

def eliminar_elementos_relacionados(usuario_seleccionado, ventana_personal_esd, root, ventana_eliminar):
    print(f'Usuario ID: {usuario_seleccionado}')

    ventana_personal_esd.withdraw()  # Oculta la ventana de Personal ESD
    ventana_eliminar.withdraw()

    ventana_elementos_relacionados = tk.Toplevel(root)  # Crear una nueva ventana hija de root
    configurar_ventana(ventana_elementos_relacionados, "Disposición de los elementos relacionados al usuario")

    # Crear un marco para contener los elementos
    marco = tk.Frame(ventana_elementos_relacionados)
    marco.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Función para manejar la selección en el Combobox
    def manejar_seleccion(event, item_id):
        seleccion = event.widget.get()
        if seleccion == "Eliminar":
            eliminar_elemento(item_id)
        elif seleccion == "Desasignar":
            desasignar_elemento(item_id)

    def eliminar_elemento(item_id):
        print(f"Eliminar elemento con ID: {item_id}")
        # Aquí puedes implementar la lógica para eliminar el elemento

    def desasignar_elemento(item_id):
        print(f"Desasignar elemento con ID: {item_id}")
        # Aquí puedes implementar la lógica para desasignar el elemento

    try:
        conn = sqlite3.connect(db_path)  # Ajusta esto si usas otro sistema de base de datos
        cursor = conn.cursor()

        # Paso 1: Obtener el nombre_usuario basado en el usuario_id
        cursor.execute("SELECT nombre_usuario FROM personal_esd WHERE id = ?", (usuario_seleccionado,))
        nombre_usuario = cursor.fetchone()

        if nombre_usuario:
            nombre_usuario = nombre_usuario[0]

            # Paso 2: Obtener los tipo_elemento para el usuario_id
            cursor.execute(tipos_elementos_del_usuario_id, (usuario_seleccionado,))

            rows = cursor.fetchall()

            # Crear los Labels y Comboboxes para cada elemento
            for index, (item_id, tipo_elemento) in enumerate(rows):
                # Etiqueta para el nombre del usuario
                label_nombre = tk.Label(marco, text=nombre_usuario, font=("Arial", 12))
                label_nombre.grid(row=index, column=0, padx=10, pady=5)

                # Etiqueta para el tipo de elemento
                label_tipo = tk.Label(marco, text=tipo_elemento, font=("Arial", 12))
                label_tipo.grid(row=index, column=1, padx=10, pady=5)

                # Combobox para acciones
                combo = ttk.Combobox(marco, values=["Eliminar", "Desasignar"], state="normal")
                combo.grid(row=index, column=2, padx=10, pady=5)
                combo.bind("<<ComboboxSelected>>", lambda event, item_id=item_id: manejar_seleccion(event, item_id))
        else:
            print("Usuario no encontrado.")

        conn.close()
    except Exception as e:
        print(f"Error al recuperar los datos: {e}")

    def salir_eliminar():
        ventana_elementos_relacionados.destroy()
        ventana_personal_esd.deiconify()  # Mostrar la ventana Personal ESD

    # Crear el botón "Salir"
    btn_salir = tk.Button(ventana_elementos_relacionados, text="Salir", command=salir_eliminar, font=("Arial", 14),
                          bg="red", fg="white", height=2, width=10)
    btn_salir.pack(side=tk.BOTTOM, pady=10)

    # Asegúrate de cerrar correctamente al cerrar la ventana
    ventana_elementos_relacionados.protocol("WM_DELETE_WINDOW", salir_eliminar)
