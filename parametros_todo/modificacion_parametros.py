from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path, poner_imagen_de_fondo, imagen_modificacion_parametros

def modificar_parametro(ventana_parametros):
    ventana_modificar_parametros = tk.Toplevel()  # Crear una nueva ventana
    ventana_parametros.withdraw()  # Ocultar la ventana principal al abrir la ventana de parámetros
    configurar_ventana(ventana_modificar_parametros, "Modificacion de parámetros")

    # Función para salir del programa
    def salir_programa():
        ventana_modificar_parametros.withdraw()
        ventana_parametros.deiconify()

    poner_imagen_de_fondo(ventana_modificar_parametros, imagen_modificacion_parametros, 900, 700, x=20, y=100)

    # Función para cargar parámetros en el OptionMenu
    def cargar_parametros():
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT nombre_parametro FROM parametros_esd")
            parametros = cursor.fetchall()
            menu_parametros['menu'].delete(0, tk.END)
            for parametro in parametros:
                menu_parametros['menu'].add_command(label=parametro[0], command=tk._setit(variable_parametro, parametro[0]))
            conn.close()
        except sqlite3.Error as e:
            tk.messagebox.showerror("Error", f"Error al cargar parámetros: {e}")

    # Función para cargar tipos de elemento en el OptionMenu
    def cargar_tipos_elemento(*args):
        try:
            parametro_seleccionado = variable_parametro.get()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT esd_items_tipo_elemento FROM parametros_esd WHERE nombre_parametro = ?",
                           (parametro_seleccionado,))
            tipos_elemento = cursor.fetchall()
            menu_tipos_elemento['menu'].delete(0, tk.END)
            for tipo in tipos_elemento:
                menu_tipos_elemento['menu'].add_command(label=tipo[0], command=tk._setit(variable_tipo_elemento, tipo[0]))
            # Selecciona el primer tipo de elemento y carga los datos asociados
            if tipos_elemento:
                variable_tipo_elemento.set(tipos_elemento[0][0])
                cargar_datos_parametro()  # Cargar datos del primer tipo de elemento
            conn.close()
        except sqlite3.Error as e:
            tk.messagebox.showerror("Error", f"Error al cargar tipos de elemento: {e}")

    # Función para cargar los datos del parámetro seleccionado
    def cargar_datos_parametro(*args):
        try:
            parametro_seleccionado = variable_parametro.get()
            tipo_elemento_seleccionado = variable_tipo_elemento.get()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT descripcion, valor_minimo, valor_maximo, unidad_de_medida
                FROM parametros_esd
                WHERE nombre_parametro = ? AND esd_items_tipo_elemento = ?
            """, (parametro_seleccionado, tipo_elemento_seleccionado))
            parametro = cursor.fetchone()
            conn.close()
            if parametro:
                text_descripcion.delete('1.0', tk.END)
                text_descripcion.insert(tk.END, parametro[0])
                entry_valor_minimo.delete(0, tk.END)
                entry_valor_minimo.insert(0, parametro[1])
                entry_valor_maximo.delete(0, tk.END)
                entry_valor_maximo.insert(0, parametro[2])
                entry_unidad_medida.delete(0, tk.END)
                entry_unidad_medida.insert(0, parametro[3])
            else:
                # Limpiar campos si no se encuentra el parámetro
                text_descripcion.delete('1.0', tk.END)
                entry_valor_minimo.delete(0, tk.END)
                entry_valor_maximo.delete(0, tk.END)
                entry_unidad_medida.delete(0, tk.END)
        except sqlite3.Error as e:
            tk.messagebox.showerror("Error", f"Error al cargar datos del parámetro: {e}")

    # Función para validar los datos antes de guardarlos
    def validar_datos():
        descripcion = text_descripcion.get('1.0', tk.END).strip()
        valor_minimo = entry_valor_minimo.get().strip()
        valor_maximo = entry_valor_maximo.get().strip()
        unidad_medida = entry_unidad_medida.get().strip()

        if not (descripcion and valor_minimo and valor_maximo and unidad_medida):
            tk.messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            return False

        if len(descripcion) < 5:
            tk.messagebox.showwarning("Advertencia", "La descripción debe tener al menos 5 caracteres")
            return False

        try:
            float(valor_minimo)
        except ValueError:
            tk.messagebox.showwarning("Advertencia", "El valor mínimo debe ser un número válido")
            return False

        try:
            float(valor_maximo)
        except ValueError:
            tk.messagebox.showwarning("Advertencia", "El valor máximo debe ser un número válido")
            return False

        if not unidad_medida.isalpha():
            tk.messagebox.showwarning("Advertencia", "La unidad de medida debe ser texto")
            return False

        return True

    # Función para guardar los cambios en la base de datos
    def guardar_cambios():
        if validar_datos():
            try:
                print("Validación de datos exitosa, guardando cambios...")
                parametro_seleccionado = variable_parametro.get()
                tipo_elemento_seleccionado = variable_tipo_elemento.get()
                descripcion = text_descripcion.get('1.0', tk.END).strip()
                valor_minimo = entry_valor_minimo.get()
                valor_maximo = entry_valor_maximo.get()
                unidad_medida = entry_unidad_medida.get()
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE parametros_esd
                    SET descripcion = ?, valor_minimo = ?, valor_maximo = ?, unidad_de_medida = ?
                    WHERE nombre_parametro = ? AND esd_items_tipo_elemento = ?
                """, (descripcion, valor_minimo, valor_maximo, unidad_medida, parametro_seleccionado,
                      tipo_elemento_seleccionado))
                conn.commit()
                conn.close()
                tk.messagebox.showinfo("Éxito", "Cambios guardados exitosamente")
                salir_programa()
            except sqlite3.Error as e:
                tk.messagebox.showerror("Error", f"Error al guardar cambios: {e}")
                print(f"Error al guardar cambios: {e}")

    # Crear widgets para la selección de parámetros
    tk.Label(ventana_modificar_parametros, text="Selecciona un parámetro:").pack(pady=10)
    variable_parametro = tk.StringVar(ventana_modificar_parametros)
    menu_parametros = tk.OptionMenu(ventana_modificar_parametros, variable_parametro, [])
    menu_parametros.pack(pady=10)
    variable_parametro.trace("w", cargar_tipos_elemento)

    tk.Label(ventana_modificar_parametros, text="Selecciona un tipo de elemento:").pack(pady=10)
    variable_tipo_elemento = tk.StringVar(ventana_modificar_parametros)
    menu_tipos_elemento = tk.OptionMenu(ventana_modificar_parametros, variable_tipo_elemento, [])
    menu_tipos_elemento.pack(pady=10)
    variable_tipo_elemento.trace("w", cargar_datos_parametro)

    tk.Label(ventana_modificar_parametros, text="Descripción:").pack(pady=5)
    text_descripcion = tk.Text(ventana_modificar_parametros, width=50, height=4)
    text_descripcion.pack(pady=5)

    tk.Label(ventana_modificar_parametros, text="Valor mínimo:").pack(pady=5)
    entry_valor_minimo = tk.Entry(ventana_modificar_parametros, width=50)
    entry_valor_minimo.pack(pady=5)

    tk.Label(ventana_modificar_parametros, text="Valor máximo:").pack(pady=5)
    entry_valor_maximo = tk.Entry(ventana_modificar_parametros, width=50)
    entry_valor_maximo.pack(pady=5)

    tk.Label(ventana_modificar_parametros, text="Unidad de medida:").pack(pady=5)
    entry_unidad_medida = tk.Entry(ventana_modificar_parametros, width=50)
    entry_unidad_medida.pack(pady=5)

    # Crear el botón "Guardar"
    btn_guardar = tk.Button(ventana_modificar_parametros, text="Guardar", command=guardar_cambios, font=("Arial", 14), bg="green",
                            fg="white", height=2, width=10)
    btn_guardar.pack(pady=20)

    # Crear el botón "Salir"
    btn_salir = tk.Button(ventana_modificar_parametros, text="Salir", command=salir_programa, font=("Arial", 14), bg="red",
                          fg="white", height=2, width=10)
    btn_salir.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # Posiciona el botón en la esquina inferior derecha

    cargar_parametros()  # Cargar la lista de parámetros al iniciar la ventana
