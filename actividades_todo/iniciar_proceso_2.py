from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path
from actividades_todo.estatus_proceso2 import manejo_de_estatus2


def iniciar_p2(ventana_procedimiento_actividad, global_estatus_titulo):
    respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas iniciar esta tarea? Al continuar, el estatus de la actividad cambiará a 'Realizando'.")

    if respuesta:  # Si el usuario elige 'Sí'
        manejo_de_estatus2()
        proceso_2 = tk.Toplevel()  # Crear una nueva ventana
        ventana_procedimiento_actividad.withdraw()  # Ocultar la ventana principal al abrir la ventana de cumplimiento
        configurar_ventana(proceso_2, "Procedimiento dos", "1100x700")

        # Obtener la fecha y hora actual en Guadalajara, México
        tz = pytz.timezone('America/Mexico_City')

        # Obtener el usuario de Windows actual
        usuario_windows = os.getlogin()

        # Título de la ventana
        tk.Label(proceso_2, text=f"Procedimiento interno ID: {global_estatus_titulo}", font=("Arial", 14, "bold")).pack(pady=10)

        # Mostrar la fecha y hora actual
        fecha_hora_label = tk.Label(proceso_2, font=("Arial", 12))
        fecha_hora_label.pack()

        # Mostrar el usuario de Windows
        tk.Label(proceso_2, text=f"Usuario: {usuario_windows}", font=("Arial", 12)).pack()

        def salir_programa():
            proceso_2.withdraw()
            ventana_procedimiento_actividad.deiconify()

        # Crear el botón de salir
        btn_salir = tk.Button(proceso_2, text="Salir", command=salir_programa,
                              font=("Arial", 12, "bold"), bg="red", fg="white", height=1, width=10, relief="flat",
                              bd=0)
        btn_salir.pack(pady=10)


        def actualizar_fecha_hora():
            fecha_hora_actual = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
            fecha_hora_label.config(text=f"Fecha y hora: {fecha_hora_actual}")
            proceso_2.after(1000, actualizar_fecha_hora)  # Actualizar cada segundo


