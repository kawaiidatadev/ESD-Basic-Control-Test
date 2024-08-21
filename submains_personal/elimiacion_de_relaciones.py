from common.__init__ import *
from settings.__init__ import db_path
from settings.conf_ventana import configurar_ventana
from strings_consultas_db import tipos_elementos_del_usuario_id


def eliminar_elementos_relacionados(usuario_seleccionado, ventana_personal_esd, root, ventana_eliminar):
    print(f'Usuario ID: {usuario_seleccionado}')

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar si el usuario tiene al menos un elemento asignado
        cursor.execute(tipos_elementos_del_usuario_id, (usuario_seleccionado,))
        rows = cursor.fetchall()

        if not rows:
            messagebox.showwarning("Advertencia",
                                   "El usuario no tiene elementos asignados. Volviendo a la ventana anterior.")
            ventana_eliminar.deiconify()  # Mostrar la ventana de eliminar
            ventana_personal_esd.deiconify()  # Mostrar la ventana Personal ESD
            return  # Salir de la función

        ventana_personal_esd.withdraw()  # Oculta la ventana de Personal ESD
        ventana_eliminar.withdraw()
        ventana_elementos_relacionados = tk.Toplevel(root)  # Crear una nueva ventana hija de root
        configurar_ventana(ventana_elementos_relacionados, "Disposición de los elementos relacionados al usuario")

        # Crear un marco para contener los elementos
        marco = tk.Frame(ventana_elementos_relacionados)
        marco.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        elementos = []  # Lista para guardar los datos de los elementos y sus comboboxes

        # Función para manejar la selección en el Combobox
        def manejar_seleccion(event, item_id):
            seleccion = event.widget.get()
            for elemento in elementos:
                if elemento['item_id'] == item_id:
                    elemento['accion'] = seleccion

        def confirmar_cambios():
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                cambios_realizados = []
                actualizaciones_personal = {
                    'bata_estatus': 'Baja',
                    'bata_polar_estatus': 'Baja',
                    'pulsera_estatus': 'Baja',
                    'talonera_estatus': 'Baja'
                }

                # Actualizar el estado de los elementos en esd_items
                for elemento in elementos:
                    item_id = elemento['item_id']
                    accion = elemento['accion']
                    nuevo_estado = 'Baja'  # Cambia el estado por defecto a 'Baja'

                    cursor.execute("""
                        UPDATE esd_items
                        SET estatus = ?
                        WHERE id = ?
                    """, (nuevo_estado, item_id))

                    cambios_realizados.append(f"Elemento ID {item_id}: {accion}")

                    # Actualizar estatus en personal_esd
                    tipo_elemento = cursor.execute("""
                        SELECT tipo_elemento
                        FROM esd_items
                        WHERE id = ?
                    """, (item_id,)).fetchone()[0]

                    if tipo_elemento == 'Bata':
                        actualizaciones_personal['bata_estatus'] = nuevo_estado
                    elif tipo_elemento == 'Bata Polar':
                        actualizaciones_personal['bata_polar_estatus'] = nuevo_estado
                    elif tipo_elemento == 'Pulsera':
                        actualizaciones_personal['pulsera_estatus'] = nuevo_estado
                    elif tipo_elemento == 'Talonera':
                        actualizaciones_personal['talonera_estatus'] = nuevo_estado

                # Eliminar todos los registros relacionados en usuarios_elementos
                cursor.execute("""
                    DELETE FROM usuarios_elementos
                    WHERE usuario_id = ?
                """, (usuario_seleccionado,))

                # Actualizar los estatus del usuario en personal_esd
                cursor.execute("""
                    UPDATE personal_esd
                    SET estatus_usuario = 'Baja',
                        bata_estatus = ?,
                        bata_polar_estatus = ?,
                        pulsera_estatus = ?,
                        talonera_estatus = ?
                    WHERE id = ?
                """, (
                    actualizaciones_personal['bata_estatus'],
                    actualizaciones_personal['bata_polar_estatus'],
                    actualizaciones_personal['pulsera_estatus'],
                    actualizaciones_personal['talonera_estatus'],
                    usuario_seleccionado
                ))

                conn.commit()
                conn.close()

                # Mostrar el mensaje de confirmación
                mensaje = "Cambios confirmados y registros eliminados.\n\nDetalles de los cambios:\n" + "\n".join(
                    cambios_realizados)
                messagebox.showinfo("Confirmación de Cambios", mensaje)
                salir_eliminar()

            except Exception as e:
                print(f"Error al confirmar los cambios: {e}")

        try:
            conn = sqlite3.connect(db_path)
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
                    elementos.append({'item_id': item_id, 'accion': 'Eliminar'})  # Valor inicial de 'accion'

                    # Etiqueta para el nombre del usuario
                    label_nombre = tk.Label(marco, text=nombre_usuario, font=("Arial", 12))
                    label_nombre.grid(row=index, column=0, padx=10, pady=5)

                    # Etiqueta para el tipo de elemento
                    label_tipo = tk.Label(marco, text=tipo_elemento, font=("Arial", 12))
                    label_tipo.grid(row=index, column=1, padx=10, pady=5)

                    # Combobox para acciones con "Eliminar" como opción predeterminada
                    combo = ttk.Combobox(marco, values=["Eliminar", "Desasignar"], state="readonly")
                    combo.set("Eliminar")  # Establece "Eliminar" como la opción predeterminada
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

        # Crear el marco para los botones
        marco_botones = tk.Frame(ventana_elementos_relacionados)
        marco_botones.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Crear el botón "Confirmar cambios" a la izquierda
        btn_confirmar = tk.Button(marco_botones, text="Confirmar Cambios", command=confirmar_cambios,
                                  font=("Arial", 14),
                                  bg="green", fg="white", height=2, width=20)
        btn_confirmar.pack(side=tk.LEFT, padx=5)

        # Crear el botón "Salir" a la derecha
        btn_salir = tk.Button(marco_botones, text="Salir", command=salir_eliminar, font=("Arial", 14),
                              bg="red", fg="white", height=2, width=15)
        btn_salir.pack(side=tk.RIGHT, padx=5)

        # Asegúrate de cerrar correctamente al cerrar la ventana
        ventana_elementos_relacionados.protocol("WM_DELETE_WINDOW", salir_eliminar)

    except Exception as e:
        print(f"Error general: {e}")
