from common import *
from settings.conf_ventana import configurar_ventana
from settings import db_path, poner_imagen_de_fondo, path_imagen_registro_personal
from submains_personal.registrar_usuario_db import guardar_usuario

# Función para abrir la ventana de registro de usuarios
def registrar_usuario(root, ventana_personal_esd):  # Agrega ventana_personal_esd como argumento
    ventana_personal_esd.withdraw()  # Oculta la ventana de Personal ESD
    ventana_registro = tk.Toplevel(root)  # Crear una nueva ventana
    configurar_ventana(ventana_registro, "Registro de Usuario", "1100x500")


    # Variables para almacenar las entradas adicionales
    var_rol = tk.StringVar(value="Seleccione una opción")
    var_area = tk.StringVar(value="Seleccione una opción")
    var_linea = tk.StringVar(value="Seleccione una opción")
    var_puesto = tk.StringVar(value="Seleccione una opción")

    # Crear un marco para agrupar los elementos
    marco = tk.Frame(ventana_registro, padx=20, pady=20)
    marco.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    poner_imagen_de_fondo(ventana_registro, path_imagen_registro_personal, 200, 300, x=1000, y=200)

    # Campo para el nombre de usuario
    tk.Label(marco, text="Nombre de Usuario:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_nombre_usuario = tk.Entry(marco, font=("Arial", 12), width=50)
    entry_nombre_usuario.grid(row=0, column=1, padx=10, pady=10, sticky="w")



    # Función para salir de la ventana
    def salir_registro():
        ventana_registro.destroy()
        ventana_personal_esd.deiconify()  # Muestra de nuevo la ventana de Personal ESD

    # Función para manejar la selección de "Otro"
    def habilitar_otro(entry_var, entry_widget):
        if entry_var.get() == "Otro":
            entry_widget.config(state="normal")
        else:
            entry_widget.config(state="disabled")
            entry_widget.delete(0, tk.END)

    # Función para cargar opciones desde la base de datos
    def cargar_opciones():
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Obtener roles
        cursor.execute("SELECT DISTINCT rol FROM personal_esd")
        roles = [row[0] for row in cursor.fetchall()]
        if not roles:
            roles = ["Otro"]

        # Obtener áreas
        cursor.execute("SELECT DISTINCT area FROM personal_esd")
        areas = [row[0] for row in cursor.fetchall()]
        if not areas:
            areas = ["Otro"]

        # Obtener líneas
        cursor.execute("SELECT DISTINCT linea FROM personal_esd")
        lineas = [row[0] for row in cursor.fetchall()]
        if not lineas:
            lineas = ["Otro"]

        # Obtener puestos
        cursor.execute("SELECT DISTINCT puesto FROM personal_esd")
        puestos = [row[0] for row in cursor.fetchall()]
        if not puestos:
            puestos = ["Otro"]

        connection.close()

        return roles, areas, lineas, puestos

    # Cargar opciones de la base de datos
    opciones_rol, opciones_area, opciones_linea, opciones_puesto = cargar_opciones()

    # Asegúrate de incluir "Otro" en las opciones
    if "Otro" not in opciones_rol:
        opciones_rol.append("Otro")
    if "Otro" not in opciones_area:
        opciones_area.append("Otro")
    if "Otro" not in opciones_linea:
        opciones_linea.append("Otro")
    if "Otro" not in opciones_puesto:
        opciones_puesto.append("Otro")

    # Crear menús desplegables para rol, área, línea y puesto
    tk.Label(marco, text="Rol:", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    rol_menu = tk.OptionMenu(marco, var_rol, *opciones_rol, command=lambda _: habilitar_otro(var_rol, entry_otro_rol))
    rol_menu.config(font=("Arial", 12), width=28)
    rol_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    entry_otro_rol = tk.Entry(marco, font=("Arial", 12), state="disabled", width=30)
    entry_otro_rol.grid(row=1, column=2, padx=10, pady=10, sticky="w")

    tk.Label(marco, text="Área:", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=10, sticky="e")
    area_menu = tk.OptionMenu(marco, var_area, *opciones_area, command=lambda _: habilitar_otro(var_area, entry_otro_area))
    area_menu.config(font=("Arial", 12), width=28)
    area_menu.grid(row=2, column=1, padx=10, pady=10, sticky="w")
    entry_otro_area = tk.Entry(marco, font=("Arial", 12), state="disabled", width=30)
    entry_otro_area.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    tk.Label(marco, text="Línea:", font=("Arial", 12, "bold")).grid(row=3, column=0, padx=10, pady=10, sticky="e")
    linea_menu = tk.OptionMenu(marco, var_linea, *opciones_linea, command=lambda _: habilitar_otro(var_linea, entry_otro_linea))
    linea_menu.config(font=("Arial", 12), width=28)
    linea_menu.grid(row=3, column=1, padx=10, pady=10, sticky="w")
    entry_otro_linea = tk.Entry(marco, font=("Arial", 12), state="disabled", width=30)
    entry_otro_linea.grid(row=3, column=2, padx=10, pady=10, sticky="w")

    tk.Label(marco, text="Puesto:", font=("Arial", 12, "bold")).grid(row=4, column=0, padx=10, pady=10, sticky="e")
    puesto_menu = tk.OptionMenu(marco, var_puesto, *opciones_puesto, command=lambda _: habilitar_otro(var_puesto, entry_otro_puesto))
    puesto_menu.config(font=("Arial", 12), width=28)
    puesto_menu.grid(row=4, column=1, padx=10, pady=10, sticky="w")
    entry_otro_puesto = tk.Entry(marco, font=("Arial", 12), state="disabled", width=30)
    entry_otro_puesto.grid(row=4, column=2, padx=10, pady=10, sticky="w")

    # Botones
    btn_frame = tk.Frame(marco)
    btn_frame.grid(row=5, column=0, columnspan=3, pady=10)

    from tkcalendar import Calendar

    def agregar_calendario(marco):
        # Crear y agregar el widget de calendario
        label_fecha = tk.Label(marco, text="Fecha de Ingreso:", font=("Arial", 12, "bold"))
        label_fecha.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        cal = Calendar(marco, selectmode='day', date_pattern='dd/mm/yyyy')
        cal.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # Función para obtener la fecha seleccionada
        def obtener_fecha():
            return cal.get_date()

        return obtener_fecha

    # Guardamos la función de obtener fecha que se generó por agregar_calendario
    obtener_fecha = agregar_calendario(marco)
    btn_guardar = tk.Button(btn_frame, text="Registrar Usuario", command=lambda: guardar_usuario(
        root,
        entry_nombre_usuario.get(),
        var_rol.get(),
        var_area.get(),
        var_linea.get(),
        var_puesto.get(),
        entry_otro_rol,
        entry_otro_area,
        entry_otro_linea,
        entry_otro_puesto,
        obtener_fecha(),  # Aquí obtenemos la fecha seleccionada
        ventana_registro
    ), font=("Arial", 14, "bold"), bg="sky blue", height=2, width=20)
    btn_guardar.grid(row=0, column=0, padx=10)

    btn_salir = tk.Button(btn_frame, text="Salir", command=salir_registro, font=("Arial", 14, "bold"), bg="red",
                          fg="white", height=2, width=10)
    btn_salir.grid(row=0, column=1, padx=10)

    # Configuración del protocolo para el cierre de ventana
    ventana_registro.protocol("WM_DELETE_WINDOW", salir_registro)

    # Ejecutar la ventana de registro
    ventana_registro.mainloop()