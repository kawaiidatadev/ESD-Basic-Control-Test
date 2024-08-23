from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path

def evidencias_asignacion(asignaciones_window, root):
    ventana_evidencias = tk.Toplevel(asignaciones_window)
    asignaciones_window.withdraw()
    configurar_ventana(ventana_evidencias, "Evidencias de asignaciones")

    # Conectar a la base de datos y obtener los elementos únicos de `tipo_elemento`
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT tipo_elemento FROM esd_items")
    elementos = cursor.fetchall()

    conn.close()

    if not elementos:
        messagebox.showwarning("Advertencia", "No se encontraron elementos en la tabla esd_items.")
        salir_evidencias()
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
        global usuario_id
        try:
            usuario_id = int(usuario_id_var.get())
        except ValueError:
            messagebox.showerror("Error", "El ID del usuario debe ser un número entero.")
            return

        if not usuario_id_var.get():
            messagebox.showerror("Error", "El ID del usuario no puede estar vacío.")
            return

        tipo_elemento_seleccionado = tipo_elemento_var.get()

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Define el campo del estatus basado en el tipo de elemento seleccionado
        estatus_campo = {
            'Bata ESD': 'bata_estatus',
            'Bata Polar ESD': 'bata_polar_estatus',
            'Pulsera ESD': 'pulsera_estatus',
            'Talonera ESD': 'talonera_estatus'
        }.get(tipo_elemento_seleccionado)

        if estatus_campo is None:
            messagebox.showerror("Error", "Tipo de elemento no válido.")
            conn.close()
            return

        # Consultar el estatus del elemento para el usuario
        sql_query = f"SELECT {estatus_campo} FROM personal_esd WHERE id = ?"
        cursor.execute(sql_query, (usuario_id,))
        resultado = cursor.fetchone()

        if not resultado or resultado[0] != "Asignada":
            messagebox.showerror("Error",
                                 f"El elemento '{tipo_elemento_seleccionado}' no ha sido asignado a este usuario.")
            btn_subir.config(state="disabled")
            conn.close()
            return

        # Verificar si el id_evidencias_asignacion es 0
        cursor.execute("""
            SELECT id_evidencias_asignacion
            FROM usuarios_elementos
            WHERE usuario_id = ? AND esd_item_id = (
                SELECT id FROM esd_items WHERE tipo_elemento = ?
            )
        """, (usuario_id, tipo_elemento_seleccionado))
        evidencia_id = cursor.fetchone()

        if evidencia_id and evidencia_id[0] != 0:
            messagebox.showerror("Error", "Ya se ha registrado evidencia para este usuario y elemento.")
            btn_subir.config(state="disabled")
        else:
            btn_subir.config(state="normal")

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

        # Copiar archivo a la ruta de destino
        shutil.copy2(archivo, ruta_completa_destino)
        lbl_ruta_destino.config(text=f"Ruta de destino: {ruta_completa_destino}")

        # Registrar la evidencia en la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO evidencias_asignacion (esd_item_id, ruta_archivo, fecha_subida)
            VALUES (?, ?, ?)
        """, (56, ruta_completa_destino, now.strftime("%Y-%m-%d %H:%M:%S")))

        # Obtener el ID del nuevo registro de evidencia
        nueva_evidencia_id = cursor.lastrowid

        # Actualizar la tabla usuarios_elementos
        cursor.execute("""
            UPDATE usuarios_elementos
            SET id_evidencias_asignacion = ?
            WHERE usuario_id = ? AND esd_item_id = ?
        """, (nueva_evidencia_id, 25, 56))

        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Evidencia subida y registrada correctamente.")

    # Crear el botón "Suba su archivo de evidencia", inicialmente deshabilitado
    btn_subir = tk.Button(ventana_evidencias, text="Suba su archivo de evidencia", command=subir_evidencia,
                          font=("Arial", 14), bg="green", fg="white", height=2, width=25, state="disabled")
    btn_subir.pack(pady=10)

    # Crear el botón "Salir"
    btn_salir = tk.Button(ventana_evidencias, text="Salir", command=salir_evidencias, font=("Arial", 14), bg="red",
                          fg="white", height=2, width=15)
    btn_salir.pack(pady=10)
