from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path, poner_imagen_de_fondo, imagen_registro_parametros

def registrar_parametro(ventana_parametros):
    ventana_registro_parametros = tk.Toplevel()  # Crear una nueva ventana
    ventana_parametros.withdraw()  # Ocultar la ventana principal al abrir la ventana de parámetros
    configurar_ventana(ventana_registro_parametros, "Registro de parámetros de medición")

    # Conectar a la base de datos y obtener la lista de elementos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT tipo_elemento FROM esd_items")
    tipos_elementos = [item[0] for item in cursor.fetchall()]
    conn.close()

    # Función para salir del programa
    def salir_programa():
        ventana_registro_parametros.quit()
        ventana_registro_parametros.destroy()
        ventana_parametros.deiconify()

    # Función para guardar los parámetros en la base de datos
    def guardar_parametro():
        nombre_parametro = entry_nombre_parametro.get()
        descripcion = text_descripcion.get("1.0", "end-1c")
        tipo_elemento = combo_tipo_elemento.get()
        valor_minimo = entry_valor_minimo.get().strip()
        valor_maximo = entry_valor_maximo.get().strip()
        unidad_de_medida = entry_unidad_de_medida.get().strip()

        def convertir_a_numero(valor):
            try:
                return float(valor)
            except ValueError:
                if 'E' in valor.upper():
                    try:
                        return float(valor.upper().replace('E', 'e'))
                    except ValueError:
                        raise ValueError("Formato inválido de notación científica.")
                raise ValueError("Formato inválido.")

        try:
            valor_minimo = convertir_a_numero(valor_minimo)
            valor_maximo = convertir_a_numero(valor_maximo)
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los valores mínimo o máximo: {str(e)}")
            return

        if not nombre_parametro or not descripcion or not tipo_elemento or not unidad_de_medida:
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return

        # Validación para asegurar que 'unidad_de_medida' no sea un número
        if unidad_de_medida.isnumeric():
            messagebox.showerror("Error", "La unidad de medida no puede ser un número.")
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM parametros_esd
                WHERE nombre_parametro = ? AND esd_items_tipo_elemento = ?
            """, (nombre_parametro, tipo_elemento))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", "Ya existe un parámetro con este nombre y tipo de elemento.")
                conn.close()
                return

            cursor.execute("""
                INSERT INTO parametros_esd (nombre_parametro, descripcion, esd_items_tipo_elemento, valor_minimo, valor_maximo, unidad_de_medida)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nombre_parametro, descripcion, tipo_elemento, valor_minimo, valor_maximo, unidad_de_medida))
            conn.commit()
            messagebox.showinfo("Éxito", "Parámetro registrado correctamente.")
            salir_programa()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Hubo un error al guardar el parámetro: {str(e)}")
        finally:
            if conn:
                conn.close()

    marco_formulario = tk.Frame(ventana_registro_parametros, padx=20, pady=20)
    marco_formulario.pack(fill="both", expand=True)

    label_nombre_parametro = tk.Label(marco_formulario, text="Nombre del parámetro:", font=("Arial", 14))
    label_nombre_parametro.grid(row=0, column=0, sticky="e", pady=5)
    entry_nombre_parametro = tk.Entry(marco_formulario, font=("Arial", 14))
    entry_nombre_parametro.grid(row=0, column=1, pady=5, sticky="ew")

    label_descripcion = tk.Label(marco_formulario, text="Descripción:", font=("Arial", 14))
    label_descripcion.grid(row=1, column=0, sticky="ne", pady=5)
    text_descripcion = tk.Text(marco_formulario, font=("Arial", 14), height=10, wrap="word")
    text_descripcion.grid(row=1, column=1, pady=5, sticky="ew")

    label_tipo_elemento = tk.Label(marco_formulario, text="Seleccione el elemento al que pertenece:", font=("Arial", 14))
    label_tipo_elemento.grid(row=2, column=0, sticky="e", pady=5)
    combo_tipo_elemento = tk.StringVar(value="Bata ESD")
    dropdown_tipo_elemento = tk.OptionMenu(marco_formulario, combo_tipo_elemento, *tipos_elementos)
    dropdown_tipo_elemento.config(font=("Arial", 14))
    dropdown_tipo_elemento.grid(row=2, column=1, pady=5, sticky="ew")

    label_valor_minimo = tk.Label(marco_formulario, text="Valor Mínimo:", font=("Arial", 14))
    label_valor_minimo.grid(row=3, column=0, sticky="e", pady=5)
    entry_valor_minimo = tk.Entry(marco_formulario, font=("Arial", 14))
    entry_valor_minimo.insert(0, "0")
    entry_valor_minimo.grid(row=3, column=1, pady=5, sticky="ew")

    label_valor_maximo = tk.Label(marco_formulario, text="Valor Máximo:", font=("Arial", 14))
    label_valor_maximo.grid(row=4, column=0, sticky="e", pady=5)
    entry_valor_maximo = tk.Entry(marco_formulario, font=("Arial", 14))
    entry_valor_maximo.insert(0, "0")
    entry_valor_maximo.grid(row=4, column=1, pady=5, sticky="ew")

    label_unidad_de_medida = tk.Label(marco_formulario, text="Unidad de Medida:", font=("Arial", 14))
    label_unidad_de_medida.grid(row=5, column=0, sticky="e", pady=5)
    entry_unidad_de_medida = tk.Entry(marco_formulario, font=("Arial", 14))
    entry_unidad_de_medida.insert(0, "Megaohmio")
    entry_unidad_de_medida.grid(row=5, column=1, pady=5, sticky="ew")

    marco_botones = tk.Frame(marco_formulario)
    marco_botones.grid(row=6, column=0, columnspan=2, pady=20)

    # Crear el botón de guardar
    btn_guardar = tk.Button(marco_botones, text="Guardar", command=guardar_parametro, font=("Arial", 14), bg="green",
                            fg="white",
                            height=2, width=10)
    btn_guardar.pack(side="left", padx=10)

    # Función para abrir la página web en el navegador
    def abrir_pagina_conversion():
        webbrowser.open("https://www.translatorscafe.com/unit-converter/es-ES/electric-resistance/13-1/kiloohm-ohm/")

    # Crear el botón de conversión
    btn_conversion = tk.Button(marco_botones, text="Abrir convertidor de unidades", command=abrir_pagina_conversion,
                               font=("Arial", 14), bg="blue", fg="white", height=2, width=25)
    btn_conversion.pack(side="left", padx=10)

    # Crear el botón de salir
    btn_salir = tk.Button(marco_botones, text="Salir", command=salir_programa, font=("Arial", 14), bg="red", fg="white",
                          height=2, width=10)
    btn_salir.pack(side="left", padx=10)

    poner_imagen_de_fondo(ventana_registro_parametros, imagen_registro_parametros, 250, 450, x=-50, y=80)

    marco_formulario.grid_columnconfigure(1, weight=1)
    marco_formulario.grid_rowconfigure(1, weight=1)
