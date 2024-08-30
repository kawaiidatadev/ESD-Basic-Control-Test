from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path
from strings_consultas_db import consulta_de_iniciar_proceso_1
from actividades_todo.proceso1_db import proceso1_procesar_datos

def iniciar_p1(ventana_procedimiento_actividad, global_estatus_titulo):
    proceso_1 = tk.Toplevel()  # Crear una nueva ventana
    ventana_procedimiento_actividad.withdraw()  # Ocultar la ventana principal al abrir la ventana de cumplimiento
    configurar_ventana(proceso_1, "Procedimiento uno", "1100x700")

    # Obtener la fecha y hora actual en Guadalajara, México
    tz = pytz.timezone('America/Mexico_City')

    # Obtener el usuario de Windows actual
    usuario_windows = os.getlogin()

    # Título de la ventana
    tk.Label(proceso_1, text=f"Procedimiento interno ID: {global_estatus_titulo}", font=("Arial", 14, "bold")).pack(pady=10)

    # Mostrar la fecha y hora actual
    fecha_hora_label = tk.Label(proceso_1, font=("Arial", 12))
    fecha_hora_label.pack()

    # Mostrar el usuario de Windows
    tk.Label(proceso_1, text=f"Usuario: {usuario_windows}", font=("Arial", 12)).pack()

    # Crear un contenedor para los datos
    contenedor = tk.Frame(proceso_1)
    contenedor.pack(pady=20, fill=tk.BOTH, expand=True)

    # Crear un canvas y una barra de desplazamiento
    canvas = tk.Canvas(contenedor)
    scrollbar_y = tk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
    scrollbar_x = tk.Scrollbar(contenedor, orient="horizontal", command=canvas.xview)
    frame_datos = tk.Frame(canvas)

    frame_datos.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=frame_datos, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")

    # Manejar el evento de la rueda del mouse para desplazar el canvas
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # Etiqueta para mostrar la cantidad total de registros
    total_registros_label = tk.Label(proceso_1, text="Total de registros: 0", font=("Arial", 12, "bold"))
    total_registros_label.pack(pady=10)

    def actualizar_fecha_hora():
        fecha_hora_actual = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        fecha_hora_label.config(text=f"Fecha y hora: {fecha_hora_actual}")
        proceso_1.after(1000, actualizar_fecha_hora)  # Actualizar cada segundo

    def cargar_datos():

        # Función para actualizar el tamaño del registro cuando se selecciona un valor específico en el Combobox
        def reducir_tamano_registro(medicion_combobox, comentarios_entry, led_canvas):
            valor_seleccionado = medicion_combobox.get()

            if valor_seleccionado != 'Seleccione':  # Definir los valores que reducirán el tamaño
                # Reducir la altura del campo de comentarios
                comentarios_entry.config(height=1, font=("Arial", 7))

                # Reducir el tamaño del LED
                led_canvas.config(width=20, height=20)
                led_canvas.coords(led_canvas.led, 5, 5, 15, 15)

                # Opcional: Cambiar la altura del Combobox y otros elementos si es necesario
                medicion_combobox.config(height=1, font=("Arial", 7))


        # Limpiar el marco de datos antes de agregar nuevos datos
        for widget in frame_datos.winfo_children():
            widget.destroy()

        # Conexión a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Consulta para obtener los datos ordenados alfabéticamente por nombre
        query = consulta_de_iniciar_proceso_1
        cursor.execute(query)
        registros = cursor.fetchall()
        conn.close()

        # Actualizar la etiqueta con el total de registros
        total_registros_label.config(text=f"Total de registros: {len(registros)}")

        # Encabezados de la tabla
        headers = ["N. Serie", "Usuario", "Elemento ESD", "Área", "Línea", "Medición", "Comentarios", "Indicador"]
        for col, header in enumerate(headers):
            tk.Label(frame_datos, text=header, font=("Arial", 12, "bold"), borderwidth=1, relief="solid", anchor='center').grid(row=0, column=col, padx=5, pady=5, sticky='ew')

        # Función para actualizar el color del LED
        def actualizar_led(led_canvas, valor):
            color = "green" if valor in ["10E3", "10E4", "10E5"] else \
                    "yellow" if valor in ["10E6", "10E7", "10E8", "10E9", "10E10", "10E11"] else \
                    "red" if valor in ["10E12", "10E13"] else "gray"
            led_canvas.itemconfig(led_canvas.led, fill=color)

        # Insertar los datos en el marco de datos
        for i, registro in enumerate(registros):
            tk.Label(frame_datos, text=registro[0], anchor='center').grid(row=i * 2 + 1, column=0, padx=5, pady=5,
                                                                          sticky='ew')
            tk.Label(frame_datos, text=registro[1], anchor='center').grid(row=i * 2 + 1, column=1, padx=5, pady=5,
                                                                          sticky='ew')
            tk.Label(frame_datos, text=registro[2], anchor='center').grid(row=i * 2 + 1, column=2, padx=5, pady=5,
                                                                          sticky='ew')
            tk.Label(frame_datos, text=registro[3], anchor='center').grid(row=i * 2 + 1, column=3, padx=5, pady=5,
                                                                          sticky='ew')
            tk.Label(frame_datos, text=registro[4], anchor='center').grid(row=i * 2 + 1, column=4, padx=5, pady=5,
                                                                          sticky='ew')

            medicion_combobox = ttk.Combobox(frame_datos,
                                             values=["10E3", "10E4", "10E5", "10E6", "10E7", "10E8", "10E9", "10E10",
                                                     "10E11", "10E12", "10E13"], state='readonly')
            medicion_combobox.set("Seleccione")
            medicion_combobox.grid(row=i * 2 + 1, column=5, padx=5, pady=5, sticky='ew')
            medicion_combobox.bind_class("TCombobox", "<MouseWheel>", lambda event: "break")  # Para Windows

            comentarios_entry = tk.Text(frame_datos, height=3, width=30)
            comentarios_entry.insert(tk.END, registro[5])
            comentarios_entry.grid(row=i * 2 + 1, column=6, padx=5, pady=5, sticky='ew')

            # Crear un Canvas más grande para el LED y dibujar un círculo más grande
            led_canvas = tk.Canvas(frame_datos, width=50, height=50)  # Aumentar el tamaño del Canvas
            led_canvas.led = led_canvas.create_oval(10, 10, 40, 40, fill="gray")  # Aumentar el tamaño del círculo
            led_canvas.grid(row=i * 2 + 1, column=7, padx=5, pady=5)

            # Asociar el cambio de selección en el Combobox con la actualización del tamaño del registro
            medicion_combobox.bind("<<ComboboxSelected>>",
                                   lambda event, combobox=medicion_combobox, entry=comentarios_entry,
                                          canvas=led_canvas: (actualizar_led(canvas, combobox.get()),
                                                              reducir_tamano_registro(combobox, entry, canvas)))

            # ...

            # Agregar una línea divisoria gruesa
            separator = tk.Frame(frame_datos, height=5, bd=1, relief="sunken", bg="black")
            separator.grid(row=i * 2 + 2, column=0, columnspan=8, sticky='ew', pady=5)

    # Cargar los datos iniciales
    cargar_datos()

    # Actualizar la fecha y hora cada segundo
    actualizar_fecha_hora()

    # Función para salir del programa
    def salir_programa():
        proceso_1.withdraw()
        ventana_procedimiento_actividad.deiconify()

    # Crear el botón de salir
    btn_salir = tk.Button(proceso_1, text="Salir", command=salir_programa,
                          font=("Arial", 12, "bold"), bg="red", fg="white", height=1, width=10, relief="flat", bd=0)
    btn_salir.pack(pady=10)

    def imprimir_widgets():
        for widget in frame_datos.winfo_children():
            print(widget.grid_info())  # Imprime información de la ubicación de cada widget

    # Función para recopilar los datos y llamar a la función externa
    def obtener_datos():
        datos = []

        # Iterar sobre cada fila en frame_datos
        for i in range(1, len(frame_datos.winfo_children()) // 2 + 1):
            try:
                # Obtener el combobox y la entrada de texto para la fila actual
                medicion_combobox = frame_datos.grid_slaves(row=i * 2 - 1, column=5)[0]
                comentarios_entry = frame_datos.grid_slaves(row=i * 2 - 1, column=6)[0]
                led_canvas = frame_datos.grid_slaves(row=i * 2 - 1, column=7)[0]

                # Obtener los valores del combobox y entrada de texto
                medicion = medicion_combobox.get()
                comentarios = comentarios_entry.get("1.0", tk.END).strip()

                # Puedes definir una forma para obtener el color del LED si es necesario
                led_color = led_canvas.itemcget(led_canvas.led, "fill")

                # Obtener los valores de otras columnas (puede que necesites ajustar los índices)
                n_serie = frame_datos.grid_slaves(row=i * 2 - 1, column=0)[0].cget("text")
                usuario = frame_datos.grid_slaves(row=i * 2 - 1, column=1)[0].cget("text")
                elemento_esd = frame_datos.grid_slaves(row=i * 2 - 1, column=2)[0].cget("text")
                area = frame_datos.grid_slaves(row=i * 2 - 1, column=3)[0].cget("text")
                linea = frame_datos.grid_slaves(row=i * 2 - 1, column=4)[0].cget("text")

                # Agregar los datos recopilados a la lista
                datos.append({
                    "N. Serie": n_serie,
                    "Usuario": usuario,
                    "Elemento ESD": elemento_esd,
                    "Área": area,
                    "Línea": linea,
                    "Medición": medicion,
                    "Comentarios": comentarios,
                    "Color LED": led_color
                })
            except IndexError as e:
                # print(f"Error al obtener datos para la fila {i}: {e}")
                continue

        from actividades_todo.proceso1_db import proceso1_procesar_datos
        proceso1_procesar_datos(datos)

    # Crear el botón de guardar
    btn_guardar = tk.Button(proceso_1, text="Guardar", command=obtener_datos,
                            font=("Arial", 12, "bold"), bg="blue", fg="white", height=1, width=10, relief="flat", bd=0)
    btn_guardar.pack(pady=10)


