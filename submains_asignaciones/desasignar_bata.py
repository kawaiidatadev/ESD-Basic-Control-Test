from common import *  # Asumimos que este archivo tiene funciones comunes que usas en otros módulos
from settings.conf_ventana import configurar_ventana
from settings.__init__ import *  # Importar los paths



def desasignar_bata(ventana_padre, root):
    ventana_desasignar = tk.Toplevel(root)
    configurar_ventana(ventana_desasignar, "Desasignar Bata ESD")

    # Ocultar la ventana padre al abrir la nueva ventana
    ventana_padre.withdraw()

    # Variables para los filtros
    area_seleccionada = tk.StringVar()
    linea_seleccionada = tk.StringVar()

    # Obtener áreas y líneas desde la base de datos
    areas = obtener_areas()
    lineas = obtener_lineas()

    # Widgets para seleccionar Área y Línea
    tk.Label(ventana_desasignar, text="Área:", font=("Arial", 12)).pack(pady=5)
    area_menu = ttk.Combobox(ventana_desasignar, textvariable=area_seleccionada, values=areas, state="readonly")
    area_menu.pack(pady=5)
    area_menu.current(0)  # Selecciona la primera área por defecto

    tk.Label(ventana_desasignar, text="Línea:", font=("Arial", 12)).pack(pady=5)
    linea_menu = ttk.Combobox(ventana_desasignar, textvariable=linea_seleccionada, values=lineas, state="readonly")
    linea_menu.pack(pady=5)
    linea_menu.current(0)  # Selecciona la primera línea por defecto

    # Tabla para mostrar los usuarios
    cols = ("ID", "Nombre Usuario", "Rol", "Puesto", "Bata Estatus", "Bata Polar Estatus")
    tabla_usuarios = ttk.Treeview(ventana_desasignar, columns=cols, show='headings')
    for col in cols:
        tabla_usuarios.heading(col, text=col)
        tabla_usuarios.column(col, width=150)

    tabla_usuarios.pack(pady=20, fill='x')

    # Función para cargar datos en la tabla
    def cargar_usuarios():
        for i in tabla_usuarios.get_children():
            tabla_usuarios.delete(i)
        usuarios = obtener_usuarios(area_seleccionada.get(), linea_seleccionada.get())
        for usuario in usuarios:
            tabla_usuarios.insert("", "end", values=usuario)

    # Cargar usuarios al seleccionar Área o Línea
    area_menu.bind("<<ComboboxSelected>>", lambda e: cargar_usuarios())
    linea_menu.bind("<<ComboboxSelected>>", lambda e: cargar_usuarios())

    cargar_usuarios()  # Cargar usuarios por defecto

    # Sección de Desasignación
    causa_var = tk.StringVar()
    causas = ["Daño físico", "No pasa las mediciones", "Otra"]

    tk.Label(ventana_desasignar, text="Causa:", font=("Arial", 12)).pack(pady=5)
    causa_menu = ttk.Combobox(ventana_desasignar, textvariable=causa_var, values=causas, state="readonly")
    causa_menu.pack(pady=5)
    causa_menu.current(0)

    comentario_text = tk.Text(ventana_desasignar, height=5, state='disabled')
    comentario_text.pack(pady=5, fill='x')

    def habilitar_comentario(*args):
        if causa_var.get() == "Otra":
            comentario_text.config(state='normal')
        else:
            comentario_text.config(state='disabled')
            comentario_text.delete('1.0', tk.END)

    causa_menu.bind("<<ComboboxSelected>>", habilitar_comentario)

    def desasignar():
        usuario_seleccionado = tabla_usuarios.selection()
        if not usuario_seleccionado:
            messagebox.showerror("Error", "Selecciona un usuario.")
            return

        causa = causa_var.get()
        comentario = comentario_text.get('1.0', tk.END).strip() if causa == "Otra" else ""

        if causa == "Otra" and not comentario:
            messagebox.showerror("Error", "El campo de comentario no puede estar vacío.")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Deseas desasignar la bata ESD o la bata Polar ESD?")
        if confirmar:
            tipo_bata = messagebox.askyesno("Tipo de Bata", "¿Desasignar Bata Polar ESD?")
            tipo_bata = "Polar" if tipo_bata else "ESD"

            # Actualizar la base de datos
            actualizar_estatus_bata(usuario_seleccionado, tipo_bata, "Sin asignar")
            if messagebox.askyesno("Eliminar Bata", f"¿Deseas eliminar la bata {tipo_bata}?"):
                eliminar_bata(usuario_seleccionado, tipo_bata)
            else:
                desasignar_usuario_elemento(usuario_seleccionado, tipo_bata, "Desasignada")

            messagebox.showinfo("Éxito", "Bata desasignada correctamente.")
            cargar_usuarios()

    # Botón de Desasignar
    btn_desasignar = tk.Button(ventana_desasignar, text="Desasignar", command=desasignar, font=("Arial", 14),
                               bg="green",
                               fg="white", height=2, width=20)
    btn_desasignar.pack(pady=10)

    # Función para salir del programa
    def salir_programa():
        ventana_desasignar.destroy()
        ventana_padre.deiconify()

    # Botón de Salir
    btn_salir = tk.Button(ventana_desasignar, text="Salir", command=salir_programa, font=("Arial", 14), bg="red",
                          fg="white", height=2, width=10)
    btn_salir.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

    # Configurar cierre de ventana
    ventana_desasignar.protocol("WM_DELETE_WINDOW", salir_programa)
    ventana_desasignar.mainloop()

