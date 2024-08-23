from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path

def evidencias_asignacion(asignaciones_window, root):
    ventana_evidencias = tk.Toplevel(asignaciones_window)
    asignaciones_window.withdraw()
    configurar_ventana(ventana_evidencias, "Evidencias de asignaciones")


    # Conectar a la base de datos y obtener los elementos únicos de `tipo_elemento`
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT tipo_elemento FROM esd_items")
        elementos = cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"Error al conectar con la base de datos: {e}")
        ventana_evidencias.destroy()
        asignaciones_window.deiconify()
        return
    finally:
        conn.close()

    if not elementos:
        messagebox.showwarning("Advertencia", "No se encontraron elementos en la tabla esd_items.")
        ventana_evidencias.destroy()
        asignaciones_window.deiconify()
        return

    # Crear un combobox con los elementos únicos, seleccionando por defecto el primer elemento
    tipo_elemento_var = tk.StringVar(value=elementos[0][0])
    combobox_elementos = ttk.Combobox(ventana_evidencias, textvariable=tipo_elemento_var,
                                      values=[el[0] for el in elementos], state="readonly", font=("Arial", 14))
    combobox_elementos.pack(pady=10)

    # Etiqueta y entrada para el ID del usuario
    lbl_usuario_id = tk.Label(ventana_evidencias, text="ID del Usuario:", font=("Arial", 12))
    lbl_usuario_id.pack(pady=10)

    usuario_id_var = tk.StringVar()
    entry_usuario_id = tk.Entry(ventana_evidencias, textvariable=usuario_id_var, font=("Arial", 14))
    entry_usuario_id.pack(pady=10)

    # Función para salir de la ventana de asignación
    def salir_evidencias():
        ventana_evidencias.destroy()
        asignaciones_window.deiconify()

    # Función para validar el ID del usuario y el estatus del elemento
    def validar_usuario_y_elemento():
        global usuario_id, esd_item_id
        try:
            usuario_id = int(usuario_id_var.get())
        except ValueError:
            messagebox.showerror("Error", "El ID del usuario debe ser un número entero.")
            btn_subir.config(state="disabled")
            return

        if not usuario_id_var.get():
            messagebox.showerror("Error", "El ID del usuario no puede estar vacío.")
            btn_subir.config(state="disabled")
            return

        tipo_elemento_seleccionado = tipo_elemento_var.get()

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Obtener los esd_item_id asociados al usuario
            cursor.execute("""
                SELECT esd_item_id
                FROM usuarios_elementos
                WHERE usuario_id = ?
            """, (usuario_id,))
            esd_items_usuario = cursor.fetchall()

            if not esd_items_usuario:
                messagebox.showerror("Error", "No se encontraron elementos asociados al usuario.")
                btn_subir.config(state="disabled")
                return

            # Comparar cada esd_item_id del usuario con el tipo de elemento seleccionado
            esd_item_id = None
            for item_id in esd_items_usuario:
                cursor.execute("""
                    SELECT e.id, u.id_evidencias_asignacion
                    FROM esd_items e
                    JOIN usuarios_elementos u ON e.id = u.esd_item_id
                    WHERE e.id = ? AND e.tipo_elemento = ?
                """, (item_id[0], tipo_elemento_seleccionado))
                match = cursor.fetchone()
                if match and match[1] == 0:  # Verificar que id_evidencias_asignacion sea 0
                    esd_item_id = match[0]
                    break

            if esd_item_id is None:
                messagebox.showerror("Error",
                                     "No se encontró un esd_item_id que coincida con el tipo de elemento seleccionado o ya tiene una evidencia asignada.")
                btn_subir.config(state="disabled")
            else:
                btn_subir.config(state="normal")

        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"Error al realizar la validación: {e}")
            btn_subir.config(state="disabled")
        finally:
            conn.close()

    # Crear el botón "Validar Usuario y Elemento"
    btn_validar = tk.Button(ventana_evidencias, text="Validar Usuario y Elemento", command=validar_usuario_y_elemento,
                            font=("Arial", 14), bg="blue", fg="white", height=2, width=25)
    btn_validar.pack(pady=10)

    # Mostrar ruta del archivo seleccionado y de destino
    lbl_ruta_archivo = tk.Label(ventana_evidencias, text="Ruta del archivo: ", font=("Arial", 12))
    lbl_ruta_archivo.pack(pady=10)

    lbl_ruta_destino = tk.Label(ventana_evidencias, text="Ruta de destino: ", font=("Arial", 12))
    lbl_ruta_destino.pack(pady=10)

    # Función para eliminar el archivo
    def eliminar_archivo(ruta_archivo):
        if os.path.exists(ruta_archivo):
            try:
                os.remove(ruta_archivo)
                print(f"Archivo {ruta_archivo} eliminado correctamente.")
            except OSError as e:
                messagebox.showerror("Error al Eliminar Archivo", f"Error al eliminar el archivo: {e}")

    # Función para subir archivo de evidencia
    def subir_evidencia():
        archivo = filedialog.askopenfilename(title="Selecciona un archivo de evidencia")
        if not archivo:
            return

        lbl_ruta_archivo.config(text=f"Ruta del archivo: {archivo}")

        # Obtener año actual y construir ruta de destino
        now = datetime.now(pytz.timezone('America/Mexico_City'))
        anio_actual = now.year
        tipo_elemento_seleccionado = tipo_elemento_var.get()
        ruta_destino = f"\\\\10.0.0.9\\Mtto_Prod\\00_Departamento_Mantenimiento\\ESD\\Software\\Data\\Responsivas evidenciadas\\{anio_actual}\\{tipo_elemento_seleccionado}"

        # Crear carpetas si no existen
        os.makedirs(ruta_destino, exist_ok=True)

        # Definir nombre del archivo de destino
        nombre_archivo_destino = now.strftime("%d-%m-%Y_%H-%M-%S") + os.path.splitext(archivo)[1]
        ruta_completa_destino = os.path.join(ruta_destino, nombre_archivo_destino)

        try:
            # Copiar archivo a la ruta de destino
            shutil.copy2(archivo, ruta_completa_destino)
            lbl_ruta_destino.config(text=f"Ruta de destino: {ruta_completa_destino}")

            # Registrar la evidencia en la base de datos
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                cursor.execute("""
                           INSERT INTO evidencias_asignacion (esd_item_id, ruta_archivo, fecha_subida)
                           VALUES (?, ?, ?)
                       """, (esd_item_id, ruta_completa_destino, now.strftime("%Y-%m-%d %H:%M:%S")))

                # Obtener el ID del nuevo registro de evidencia
                nueva_evidencia_id = cursor.lastrowid

                # Actualizar la tabla usuarios_elementos
                cursor.execute("""
                           UPDATE usuarios_elementos
                           SET id_evidencias_asignacion = ?
                           WHERE usuario_id = ? AND esd_item_id = ?
                       """, (nueva_evidencia_id, usuario_id, esd_item_id))

                conn.commit()
                messagebox.showinfo("Éxito", "Evidencia subida y registrada correctamente.")
                salir_evidencias()
            except sqlite3.Error as e:
                messagebox.showerror("Error de Base de Datos", f"Error al registrar evidencia: {e}")
                eliminar_archivo(ruta_completa_destino)  # Eliminar archivo en caso de error
                salir_evidencias()
        except (shutil.Error, OSError) as e:
            messagebox.showerror("Error al Copiar Archivo", f"Error al copiar archivo: {e}")

    # Crear el botón "Suba su archivo de evidencia", inicialmente deshabilitado
    btn_subir = tk.Button(ventana_evidencias, text="Suba su archivo de evidencia", command=subir_evidencia,
                          font=("Arial", 14), bg="green", fg="white", height=2, width=25, state="disabled")
    btn_subir.pack(pady=10)

    # Crear el botón "Salir"
    btn_salir = tk.Button(ventana_evidencias, text="Salir", command=salir_evidencias, font=("Arial", 14), bg="red",
                          fg="white", height=2, width=15)
    btn_salir.pack(pady=10)
