from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path  # Importar la ruta de la base de datos

def asignaciones_taloneras(taloneras_asignaciones, root):
    try:
        # Crear una nueva ventana para la asignación de taloneras
        ventana_asignaciones = tk.Toplevel(root)
        taloneras_asignaciones.withdraw()  # Ocultar la ventana anterior
        configurar_ventana(ventana_asignaciones, "Asignar Talonera ESD")

        # Frame principal para contener la tabla y los botones
        frame_principal = tk.Frame(ventana_asignaciones)
        frame_principal.pack(fill=tk.BOTH, expand=True)

        # Crear un Treeview para mostrar la tabla con Scrollbars
        columnas = ("id", "nombre_usuario", "rol", "area", "linea", "puesto", "talonera_estatus")
        tree = ttk.Treeview(frame_principal, columns=columnas, show='headings', height=15)

        # Configurar Scrollbars
        scrollbar_x = ttk.Scrollbar(frame_principal, orient=tk.HORIZONTAL, command=tree.xview)
        scrollbar_y = ttk.Scrollbar(frame_principal, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Definir los encabezados de la tabla
        for col in columnas:
            tree.heading(col, text=col.replace('_', ' ').title())
            tree.column(col, anchor=tk.CENTER, width=100)

        tree.pack(fill=tk.BOTH, expand=True)

        # Conectar a la base de datos y obtener los datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nombre_usuario, rol, area, linea, puesto, talonera_estatus 
            FROM personal_esd 
            WHERE estatus_usuario = 'Activo' AND talonera_estatus != 'Asignada'
        """)
        rows = cursor.fetchall()

        # Insertar los datos en la tabla
        for row in rows:
            tree.insert("", tk.END, values=row)

    except sqlite3.Error as e:
        messagebox.showerror("Error de base de datos", f"Se produjo un error al conectar con la base de datos: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error inesperado: {e}")
    finally:
        cursor.close()
        conn.close()

    # Función para salir sin hacer cambios
    def salir_programa():
        try:
            ventana_asignaciones.destroy()
            taloneras_asignaciones.deiconify()
        except Exception as e:
            messagebox.showerror("Error al cerrar", f"Se produjo un error al intentar cerrar la ventana: {e}")

    # Función para asignar talonera
    def asignar_talonera():
        try:
            # Obtener la selección actual en el Treeview
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Advertencia", "Por favor, selecciona un usuario.")
                return

            # Obtener el ID del usuario seleccionado
            user_id = tree.item(selected_item)['values'][0]

            # Conectar a la base de datos
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Verificar si el usuario ya tiene una talonera asignada
            cursor.execute("SELECT talonera_estatus FROM personal_esd WHERE id = ?", (user_id,))
            talonera_estatus = cursor.fetchone()[0]

            if talonera_estatus == "Asignada":
                messagebox.showerror("Error", "El usuario ya tiene una talonera asignada.")
                return

            # Buscar una talonera disponible en la tabla esd_items
            cursor.execute("""
                SELECT id FROM esd_items 
                WHERE tipo_elemento = 'Talonera ESD' 
                AND (estatus = 'Sin asignar' OR estatus = 'Desasignada') 
                LIMIT 1
            """)
            talonera = cursor.fetchone()

            if not talonera:
                messagebox.showerror("Error", "No hay taloneras disponibles.")
                return

            talonera_id = talonera[0]

            # Actualizar el estatus del usuario
            cursor.execute("""
                UPDATE personal_esd 
                SET talonera_estatus = 'Asignada' 
                WHERE id = ?
            """, (user_id,))

            # Insertar en la tabla usuarios_elementos
            mexico_tz = pytz.timezone('America/Mexico_City')
            fecha_asignacion = datetime.now(mexico_tz).strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute("""
                INSERT INTO usuarios_elementos (usuario_id, esd_item_id, fecha_asignacion) 
                VALUES (?, ?, ?)
            """, (user_id, talonera_id, fecha_asignacion))

            # Actualizar el estatus de la talonera en la tabla esd_items
            cursor.execute("""
                UPDATE esd_items 
                SET estatus = 'Asignada' 
                WHERE id = ?
            """, (talonera_id,))

            # Confirmar cambios
            conn.commit()

            # Eliminar el usuario asignado de la tabla
            tree.delete(selected_item)

            messagebox.showinfo("Éxito", f"Talonera asignada exitosamente al usuario {user_id}.")

        except sqlite3.Error as e:
            conn.rollback()
            messagebox.showerror("Error de base de datos", f"Se produjo un error al interactuar con la base de datos: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Se produjo un error inesperado: {e}")
        finally:
            cursor.close()
            conn.close()


    # Botón para salir
    btn_salir = tk.Button(ventana_asignaciones, text="Salir", command=salir_programa, font=("Arial", 14), bg="red",
                          fg="white", height=2, width=15)
    btn_salir.pack(side=tk.BOTTOM, padx=10, pady=10, anchor='e')

    # Botón para asignar talonera
    btn_asignar = tk.Button(ventana_asignaciones, text="Asignar", command=asignar_talonera, font=("Arial", 14), bg="green",
                            fg="white", height=2, width=15)
    btn_asignar.pack(side=tk.BOTTOM, padx=10, pady=10, anchor='e')

    ventana_asignaciones.protocol("WM_DELETE_WINDOW", salir_programa)

