from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path
from conversion_megaohms import convertir_a_megaohms
from actividades_todo.estatus_proceso3 import manejo_de_estatus3
from actividades_todo.db_write_registros_proceso_3 import db_proceso_3_registro

# Lista para almacenar los registros realizados
registros = []
# Zona horaria de Guadalajara, Jalisco, México
tz = pytz.timezone('America/Mexico_City')

def iniciar_p3(ventana_procedimiento_actividad, global_estatus_titulo):
    respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas iniciar esta tarea? Al continuar, el estatus de la actividad cambiará a 'Realizando'.")

    if respuesta:  # Si el usuario elige 'Sí'
        manejo_de_estatus3()
        proceso_3 = tk.Toplevel()  # Crear una nueva ventana
        ventana_procedimiento_actividad.withdraw()  # Ocultar la ventana principal al abrir la ventana de cumplimiento
        configurar_ventana(proceso_3, "Procedimiento tres", "1100x700")

        # Obtener la fecha y hora actual en Guadalajara, México
        tz = pytz.timezone('America/Mexico_City')

        # Obtener el usuario de Windows actual
        usuario_windows = os.getlogin()

        # Título de la ventana
        tk.Label(proceso_3, text=f"Procedimiento interno ID: {global_estatus_titulo}", font=("Arial", 14, "bold")).pack(pady=10)

        # Mostrar la fecha y hora actual
        fecha_hora_label = tk.Label(proceso_3, font=("Arial", 12))
        fecha_hora_label.pack()

        # Mostrar el usuario de Windows
        tk.Label(proceso_3, text=f"Usuario: {usuario_windows}", font=("Arial", 12)).pack()

        def salir_programa():
            proceso_3.withdraw()
            ventana_procedimiento_actividad.deiconify()

        # Crear el botón de salir
        btn_salir = tk.Button(proceso_3, text="Salir", command=salir_programa,
                              font=("Arial", 12, "bold"), bg="red", fg="white", height=1, width=10, relief="flat",
                              bd=0)
        btn_salir.pack(side=tk.RIGHT, anchor=tk.SW, padx=10, pady=10)

        def actualizar_fecha_hora():
            fecha_hora_actual = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
            fecha_hora_label.config(text=f"Fecha y hora: {fecha_hora_actual}")
            proceso_3.after(1000, actualizar_fecha_hora)  # Actualizar cada segundo

        # Frame para los registros con barra de desplazamiento
        frame_registros = tk.Frame(proceso_3)
        frame_registros.pack(pady=10, fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(frame_registros)
        scrollbar = tk.Scrollbar(frame_registros, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Vincular el evento de desplazamiento del ratón al Canvas
        def _on_mouse_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

        # Función para agregar un nuevo registro
        def nuevo_registro():
            top_nuevo = tk.Toplevel(proceso_3)
            configurar_ventana(top_nuevo, "Nuevo registro de medición", "500x400")

            registro_num = len(registros) + 1  # Número de registro
            tk.Label(top_nuevo, text=f"Registro #{registro_num}", font=("Arial", 12)).pack(pady=10)

            # Selección de la medición
            tk.Label(top_nuevo, text="Selecciona la medición:", font=("Arial", 12)).pack()
            medicion = tk.StringVar()
            medicion.set("10E3")  # Valor por defecto
            opciones_medicion = ["10E3", "10E4", "10E5", "10E6", "10E7", "10E8", "10E9", "10E10", "10E11", "10E12", "10E13"]
            tk.OptionMenu(top_nuevo, medicion, *opciones_medicion).pack(pady=5)

            # Campo de comentarios
            tk.Label(top_nuevo, text="Comentarios:", font=("Arial", 12)).pack()
            comentarios = tk.Text(top_nuevo, height=8, width=40)
            comentarios.pack(pady=5)

            # Función para guardar el registro
            def guardar_registro():
                valor = medicion.get()
                comentario_texto = comentarios.get("1.0", tk.END).strip()

                # Asignar color según la medición
                color = "green" if valor in ["10E3", "10E4", "10E5"] else \
                    "yellow" if valor in ["10E6", "10E7", "10E8", "10E9", "10E10", "10E11"] else \
                        "red" if valor in ["10E12", "10E13"] else "gray"

                # Convertir la medición a Megaohms
                medicion_megaohms = convertir_a_megaohms(valor)

                # Obtener la fecha y hora actual en Guadalajara, Jalisco, México
                fecha_registro = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

                # Guardar registro en la lista
                registro = {
                    "numero_registro": registro_num,
                    "elemento_esd": "Carrito ESD",
                    "medicion": medicion_megaohms,
                    "color_led": color,
                    "fecha_registro": fecha_registro,
                    "usuario_windows": usuario_windows,
                    "comentarios": comentario_texto
                }
                registros.append(registro)

                # Mostrar el registro en la ventana principal (proceso_3)
                frame_registro = tk.Frame(scrollable_frame)
                frame_registro.pack(fill=tk.X, pady=2)

                tk.Label(frame_registro, text=f"Registro #{registro_num}: {valor} - {comentario_texto}",
                         font=("Arial", 12), fg="black").pack(side=tk.LEFT)
                tk.Label(frame_registro, text=" ", bg=color, width=2, height=1).pack(side=tk.RIGHT, padx=5)

                top_nuevo.destroy()

            # Botón para guardar el registro
            btn_guardar = tk.Button(top_nuevo, text="Guardar", command=guardar_registro, font=("Arial", 12, "bold"), bg="blue", fg="white", height=1, width=10)
            btn_guardar.pack(pady=10)

            # Mover el cursor al botón "Guardar"
            top_nuevo.update_idletasks()  # Asegurarse de que la ventana esté completamente renderizada
            btn_guardar_x = btn_guardar.winfo_rootx() + btn_guardar.winfo_width() // 2
            btn_guardar_y = btn_guardar.winfo_rooty() + btn_guardar.winfo_height() // 2
            pyautogui.moveTo(btn_guardar_x, btn_guardar_y)

        # Botón para agregar un nuevo registro de medición
        btn_nuevo_registro = tk.Button(proceso_3, text="Nuevo registro de medición", command=nuevo_registro, font=("Arial", 12, "bold"), bg="green", fg="white", height=2, width=25)
        btn_nuevo_registro.pack(pady=10)

        # Función para confirmar los registros
        def confirmar_registros():
            # Verificar si hay registros en la lista
            if not registros:
                messagebox.showwarning("Sin registros", "No hay registros para confirmar.")
                return  # Salir de la función si no hay registros

            respuesta = messagebox.askyesno("Confirmar registros", "¿Deseas confirmar y guardar todos los registros?")
            if respuesta:
                db_proceso_3_registro(registros)  # Llamar a la función con los registros
                messagebox.showinfo("Éxito", "Todos los registros han sido guardados correctamente.")
                proceso_3.withdraw()
                ventana_procedimiento_actividad.deiconify()

        # Botón para confirmar registros
        btn_confirmar = tk.Button(proceso_3, text="Confirmar registros", command=confirmar_registros, font=("Arial", 12, "bold"), bg="orange", fg="white", height=2, width=25)
        btn_confirmar.pack(pady=10)

        # Iniciar la actualización automática de la fecha y hora
        actualizar_fecha_hora()