from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path

def eliminar_parametro(ventana_parametros):
    ventana_eliminar_parametros = tk.Toplevel()  # Crear una nueva ventana
    ventana_parametros.withdraw()  # Ocultar la ventana principal al abrir la ventana de eliminación
    configurar_ventana(ventana_eliminar_parametros, "Eliminación de parámetros")

    # Función para salir del programa
    def salir_programa():
        ventana_eliminar_parametros.withdraw()
        ventana_parametros.deiconify()

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
            # Selecciona el primer tipo de elemento
            if tipos_elemento:
                variable_tipo_elemento.set(tipos_elemento[0][0])
            conn.close()
        except sqlite3.Error as e:
            tk.messagebox.showerror("Error", f"Error al cargar tipos de elemento: {e}")

    # Función para mostrar los detalles del parámetro seleccionado
    def mostrar_detalles(*args):
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
                lbl_descripcion_var.set(parametro[0])
                lbl_valor_minimo_var.set(parametro[1])
                lbl_valor_maximo_var.set(parametro[2])
                lbl_unidad_medida_var.set(parametro[3])
            else:
                # Limpiar campos si no se encuentra el parámetro
                lbl_descripcion_var.set("")
                lbl_valor_minimo_var.set("")
                lbl_valor_maximo_var.set("")
                lbl_unidad_medida_var.set("")
        except sqlite3.Error as e:
            tk.messagebox.showerror("Error", f"Error al mostrar detalles del parámetro: {e}")

    # Función para eliminar el parámetro seleccionado
    def eliminar_parametro():
        if tk.messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar el parámetro seleccionado?"):
            try:
                parametro_seleccionado = variable_parametro.get()
                tipo_elemento_seleccionado = variable_tipo_elemento.get()
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM parametros_esd
                    WHERE nombre_parametro = ? AND esd_items_tipo_elemento = ?
                """, (parametro_seleccionado, tipo_elemento_seleccionado))
                conn.commit()
                conn.close()
                tk.messagebox.showinfo("Éxito", "Parámetro eliminado exitosamente")
                print(f"Usuario de Windows: {getpass.getuser()}")
                salir_programa()
            except sqlite3.Error as e:
                tk.messagebox.showerror("Error", f"Error al eliminar el parámetro: {e}")

    # Crear widgets para la selección de parámetros
    tk.Label(ventana_eliminar_parametros, text="Selecciona un parámetro:").pack(pady=10)
    variable_parametro = tk.StringVar(ventana_eliminar_parametros)
    menu_parametros = tk.OptionMenu(ventana_eliminar_parametros, variable_parametro, [])
    menu_parametros.pack(pady=10)
    variable_parametro.trace("w", cargar_tipos_elemento)

    tk.Label(ventana_eliminar_parametros, text="Selecciona un tipo de elemento:").pack(pady=10)
    variable_tipo_elemento = tk.StringVar(ventana_eliminar_parametros)
    menu_tipos_elemento = tk.OptionMenu(ventana_eliminar_parametros, variable_tipo_elemento, [])
    menu_tipos_elemento.pack(pady=10)
    variable_tipo_elemento.trace("w", mostrar_detalles)

    # Crear un frame para las etiquetas de detalles
    frame_detalles = tk.Frame(ventana_eliminar_parametros)
    frame_detalles.pack(pady=10, padx=10, fill=tk.X)

    # Etiquetas para mostrar los detalles del parámetro seleccionado
    tk.Label(frame_detalles, text="Descripción:", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
    lbl_descripcion_var = tk.StringVar()
    lbl_descripcion = tk.Label(frame_detalles, textvariable=lbl_descripcion_var, font=("Arial", 12), anchor="w")
    lbl_descripcion.grid(row=0, column=1, sticky="w", padx=10)

    tk.Label(frame_detalles, text="Valor mínimo:", anchor="w").grid(row=1, column=0, sticky="w", pady=5)
    lbl_valor_minimo_var = tk.StringVar()
    lbl_valor_minimo = tk.Label(frame_detalles, textvariable=lbl_valor_minimo_var, font=("Arial", 12), anchor="w")
    lbl_valor_minimo.grid(row=1, column=1, sticky="w", padx=10)

    tk.Label(frame_detalles, text="Valor máximo:", anchor="w").grid(row=2, column=0, sticky="w", pady=5)
    lbl_valor_maximo_var = tk.StringVar()
    lbl_valor_maximo = tk.Label(frame_detalles, textvariable=lbl_valor_maximo_var, font=("Arial", 12), anchor="w")
    lbl_valor_maximo.grid(row=2, column=1, sticky="w", padx=10)

    tk.Label(frame_detalles, text="Unidad de medida:", anchor="w").grid(row=3, column=0, sticky="w", pady=5)
    lbl_unidad_medida_var = tk.StringVar()
    lbl_unidad_medida = tk.Label(frame_detalles, textvariable=lbl_unidad_medida_var, font=("Arial", 12), anchor="w")
    lbl_unidad_medida.grid(row=3, column=1, sticky="w", padx=10)

    # Crear el botón "Eliminar"
    btn_eliminar = tk.Button(ventana_eliminar_parametros, text="Eliminar", command=eliminar_parametro, font=("Arial", 14), bg="red",
                            fg="white", height=2, width=10)
    btn_eliminar.pack(pady=20)

    # Crear el botón "Salir"
    btn_salir = tk.Button(ventana_eliminar_parametros, text="Salir", command=salir_programa, font=("Arial", 14),
                          bg="red",
                          fg="white", height=2, width=10)
    btn_salir.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # Posiciona el botón en la esquina inferior derecha

    cargar_parametros()  # Cargar la lista de parámetros al iniciar la ventana
