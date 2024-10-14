from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from actividades_todo.conf_actividades1 import conf_a1
from settings.__init__ import poner_imagen_de_fondo, imagen_sub1_actividades
from actividades_todo.cumplimiento_act1 import cumplimiento_4_2

def ven1(root):
    sub_ventana_act = tk.Toplevel()  # Crear una nueva ventana
    root.withdraw()  # Ocultar la ventana principal al abrir la ventana de parámetros
    configurar_ventana(sub_ventana_act, "Sub menú de actividades")
    # Maximizar la ventana al final

    # Aplicar la imagen de fondo
    poner_imagen_de_fondo(sub_ventana_act, imagen_sub1_actividades, 700, 700, 40, 10)

    # Función para salir del programa
    def salir_programa():
        sub_ventana_act.withdraw()
        root.deiconify()

    # Crear un Frame principal para organizar los botones centrados
    main_frame = tk.Frame(sub_ventana_act, bg='')  # Sin bg transparente
    main_frame.pack(expand=True, pady=20)

    # Crear un estilo común para los botones
    button_style = {
        "font": ("Arial", 12, "bold"),
        "height": 2,  # Aumentar la altura para acomodar el texto envuelto
        "width": 20,  # Reducir el ancho
        "wraplength": 150,  # Longitud máxima antes de envolver el texto
        "relief": "flat",  # Usar 'flat' para evitar bordes innecesarios
        "bd": 0,  # Sin borde
        "highlightthickness": 0,  # Sin borde de resaltado
        "pady": 5,
        "anchor": "center",  # Justificación del texto centrada
    }

    # # Botón de Configuración de Actividades
    # btn_conf_actividades = tk.Button(main_frame, text="Configuración de actividades",
    #                                  command=lambda: conf_a1(sub_ventana_act),
    #                                  bg="#007bff", fg="white",
    #                                  **button_style)
    # btn_conf_actividades.grid(row=0, column=0, padx=5, pady=5)

    # Botón de Cumplimiento de Actividades
    btn_cumplimiento = tk.Button(main_frame, text="Cumplimiento de actividades",
                                 command=lambda: cumplimiento_4_2(sub_ventana_act),
                                 bg="#28a745", fg="white", **button_style)
    btn_cumplimiento.grid(row=0, column=1, padx=5, pady=5)

    # Crear un Frame inferior para el botón de salir
    bottom_frame = tk.Frame(sub_ventana_act, bg='')  # Sin bg transparente
    bottom_frame.pack(side="bottom", pady=10)

    # Crear el botón de salir
    btn_salir = tk.Button(bottom_frame, text="Salir", command=salir_programa,
                          font=("Arial", 12, "bold"), bg="red", fg="white", height=1, width=10, relief="flat", bd=0)
    btn_salir.pack()
