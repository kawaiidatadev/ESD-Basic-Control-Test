from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from actividades_todo.registrar_nueva_actividad import registar_actividad
from settings.__init__ import poner_imagen_de_fondo, imagen_sub2_actividades
from actividades_todo.editar_actividad1 import editar_act
def conf_a1(sub_ventana_act):
    conf1 = tk.Toplevel()  # Crear una nueva ventana
    sub_ventana_act.withdraw()  # Ocultar la ventana principal al abrir la ventana de parámetros
    configurar_ventana(conf1, "Configuración de actividades")

    # Aplicar la imagen de fondo
    poner_imagen_de_fondo(conf1, imagen_sub2_actividades, 500, 700, x=120, y=100)

    # Crear un Frame principal para organizar los botones
    main_frame = tk.Frame(conf1, bg='')  # Sin bg transparente
    main_frame.pack(expand=True, pady=0)

    # Crear un estilo común para los botones
    button_style = {
        "font": ("Arial", 12, "bold"),
        "height": 2,
        "width": 20,
        "relief": "flat",
        "bd": 0,
        "highlightthickness": 0,
        "pady": 0,
    }

    # Botón de Registrar Nueva Actividad
    btn_registrar = tk.Button(main_frame, text="Registrar nueva actividad",
                              command=lambda: registar_actividad(conf1), bg="#007bff", fg="white",
                              **button_style)
    btn_registrar.grid(row=0, column=0, padx=0, pady=0)

    # Botón de Editar Actividad
    btn_editar = tk.Button(main_frame, text="Editar actividad", command=lambda: editar_act(conf1),
                           bg="#28a745", fg="white", **button_style)
    btn_editar.grid(row=0, column=1, padx=10, pady=10)


    # Crear un Frame inferior para el botón de salir
    bottom_frame = tk.Frame(conf1, bg='')  # Sin bg transparente
    bottom_frame.pack(side="bottom", pady=10)

    # Crear el botón de salir
    btn_salir = tk.Button(bottom_frame, text="Salir", command=lambda: salir_programa(),
                          font=("Arial", 12, "bold"), bg="red", fg="white", height=2, width=10, relief="flat", bd=0)
    btn_salir.pack(side="left", padx=10)

    # Función para salir del programa
    def salir_programa():
        conf1.withdraw()
        sub_ventana_act.deiconify()
