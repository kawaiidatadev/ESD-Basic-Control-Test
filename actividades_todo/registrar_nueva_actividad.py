from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from actividades_todo.db_registrar_nueva_actividad import recibir_datos_a_registrar_actividad

def registar_actividad(conf1):
    re_act = tk.Toplevel()  # Crear una nueva ventana
    conf1.withdraw()  # Ocultar la ventana principal al abrir la ventana de parámetros
    configurar_ventana(re_act, "Registro de actividades")

    username = getpass.getuser()

    # Función para salir del programa
    def salir_programa():
        re_act.withdraw()
        conf1.deiconify()

    # Crear un Frame principal para organizar los widgets
    main_frame = tk.Frame(re_act)
    main_frame.pack(expand=True, pady=20)

    # Crear un estilo común para los campos y botones
    label_style = {
        "font": ("Arial", 12, "bold"),
    }

    entry_style = {
        "font": ("Arial", 12),
        "width": 40,
    }

    button_style = {
        "font": ("Arial", 12, "bold"),
        "height": 2,
        "width": 20,
        "relief": "flat",
        "bd": 0,
        "highlightthickness": 0,
        "pady": 10,
    }

    # Nombre de la actividad
    tk.Label(main_frame, text="Nombre de la actividad:", **label_style).grid(row=0, column=0, sticky="e", padx=10, pady=5)
    nombre_actividad = tk.Entry(main_frame, **entry_style)
    nombre_actividad.grid(row=0, column=1, padx=10, pady=5)

    # Descripción
    tk.Label(main_frame, text="Descripción:", **label_style).grid(row=1, column=0, sticky="e", padx=10, pady=5)
    descripcion = tk.Entry(main_frame, **entry_style)
    descripcion.grid(row=1, column=1, padx=10, pady=5)

    # Frecuencia de realización
    tk.Label(main_frame, text="Frecuencia de realización:", **label_style).grid(row=2, column=0, sticky="e", padx=10, pady=5)
    frecuencia = ttk.Combobox(main_frame, values=[
        "Diario", "Semanal", "Mensual", "Cada 2 meses", "Cada 3 meses", "Cada 4 meses", "Cada 5 meses", "Cada 6 meses",
        "Cada 7 meses", "Cada 8 meses", "Cada 9 meses", "Cada 10 meses", "Cada 11 meses", "Anual", "Cada dos años", "Cada 3 años", "Autónomo"
    ], state="readonly", width=38)
    frecuencia.set("Semanal")
    frecuencia.grid(row=2, column=1, padx=10, pady=5)

    # Fecha de inicio
    tk.Label(main_frame, text="Fecha de inicio:", **label_style).grid(row=3, column=0, sticky="e", padx=10, pady=5)
    fecha_inicio = DateEntry(main_frame, width=37, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
    fecha_inicio.set_date(datetime.now())
    fecha_inicio.grid(row=3, column=1, padx=10, pady=5)
    fecha_inicio.bind("<<DateEntrySelected>>", lambda e: fecha_inicio.set_date(datetime.now()) if fecha_inicio.get_date() < datetime.now().date() else None)


    # Equipo de medición
    tk.Label(main_frame, text="Equipo de medición:", **label_style).grid(row=4, column=0, sticky="e", padx=10, pady=5)
    equipo_medicion = tk.Entry(main_frame, **entry_style)
    equipo_medicion.grid(row=4, column=1, padx=10, pady=5)

    # Crear un Frame inferior para los botones
    bottom_frame = tk.Frame(re_act)
    bottom_frame.pack(side="bottom", pady=10, padx=20, fill='x')

    # Función de validación
    def validar_datos():
        nombre = nombre_actividad.get().strip()
        desc = descripcion.get().strip()
        fecha = fecha_inicio.get_date()
        equipo = equipo_medicion.get().strip()

        # Verificar que el nombre de la actividad tenga al menos 3 caracteres y no sea solo números
        if len(nombre) < 3 or nombre.isdigit():
            messagebox.showerror("Error",
                                 "El nombre de la actividad es inválido.")
            return False

        # Verificar que la descripción tenga al menos 5 caracteres y no sea solo números
        if len(desc) < 5 or desc.isdigit():
            messagebox.showerror("Error",
                                 "La descripción es inválida.")
            return False

        # Verificar que la fecha no sea anterior a la fecha actual
        if fecha < datetime.now().date():
            messagebox.showerror("Error", "La fecha de inicio no puede ser anterior a la fecha actual.")
            return False

        # Verificar que el equipo de medición tenga al menos 3 caracteres y no sea solo números
        if len(equipo) < 3 or equipo.isdigit():
            messagebox.showerror("Error",
                                 "El equipo de medición es inválido.")
            return False

        return True

        # Botón de registrar

    btn_registrar = tk.Button(bottom_frame, text="Registrar", command=lambda: (
        recibir_datos_a_registrar_actividad(
            nombre_actividad.get(), descripcion.get(), frecuencia.get(), fecha_inicio.get_date().strftime('%d/%m/%Y'),
            equipo_medicion.get(), username, re_act, conf1)
        if validar_datos() else None), **button_style, bg="#007bff", fg="white")
    btn_registrar.pack(side="left", padx=10)

    # Botón de salir
    btn_salir = tk.Button(bottom_frame, text="Salir", command=salir_programa, font=("Arial", 12, "bold"), bg="red", fg="white", height=2, width=10, relief="flat", bd=0)
    btn_salir.pack(side="right", padx=10)

    # Mostrar el nombre de usuario de Windows en la esquina superior derecha
    tk.Label(re_act, text=f"Usuario: {username}", font=("Arial", 10, "italic"), anchor='e').pack(side="top", fill='x', padx=10, pady=5)

    # Mostrar la fecha y hora actual en la esquina inferior derecha
    def actualizar_fecha_hora():
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fecha_hora_label.config(text=f"Fecha y Hora: {now}")
        re_act.after(1000, actualizar_fecha_hora)  # Actualizar cada segundo

    fecha_hora_label = tk.Label(re_act, font=("Arial", 10, "italic"), anchor='e')
    fecha_hora_label.pack(side="bottom", fill='x', padx=10, pady=5)
    actualizar_fecha_hora()