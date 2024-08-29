from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path
from strings_consultas_db import consulta_de_iniciar_proceso_1


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
        fecha_hora_actual = datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        fecha_hora_label.config(text=f"Fecha y hora: {fecha_hora_actual}")
        proceso_1.after(1000, actualizar_fecha_hora)  # Actualizar cada segundo

    def cargar_datos():
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

            comentarios_entry = tk.Text(frame_datos, height=3, width=30)
            comentarios_entry.insert(tk.END, registro[5])
            comentarios_entry.grid(row=i * 2 + 1, column=6, padx=5, pady=5, sticky='ew')

            # Crear un Canvas más grande para el LED y dibujar un círculo más grande
            led_canvas = tk.Canvas(frame_datos, width=50, height=50)  # Aumentar el tamaño del Canvas
            led_canvas.led = led_canvas.create_oval(10, 10, 40, 40, fill="gray")  # Aumentar el tamaño del círculo
            led_canvas.grid(row=i * 2 + 1, column=7, padx=5, pady=5)

            # Asociar el cambio de selección en el Combobox con la actualización del LED
            medicion_combobox.bind("<<ComboboxSelected>>",
                                   lambda event, canvas=led_canvas, combobox=medicion_combobox: actualizar_led(canvas,
                                                                                                               combobox.get()))

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
