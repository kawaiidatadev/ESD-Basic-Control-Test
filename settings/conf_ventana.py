from settings.__init__ import inon_path
# Diccionario global para verificar si el icono ya ha sido cargado por ventana
iconos_cargados = {}

def configurar_ventana(ventana, titulo="Ventana", tamaño="800x800"):
    global iconos_cargados  # Declarar la variable como global

    ventana.title(titulo)
    ventana.geometry(tamaño)  # Define el tamaño de la ventana
    #ventana.resizable(0, 0)  # Bloquea el redimensionamiento de la ventana

    # Usar el nombre de la ventana como clave en el diccionario
    clave_ventana = str(ventana)  # Puedes usar un identificador único para cada ventana

    # Verificar si el icono ya ha sido cargado para esta ventana
    if clave_ventana not in iconos_cargados:
        ventana.iconbitmap(inon_path)
        ventana.focus_force()
        iconos_cargados[clave_ventana] = True  # Marcar el icono como cargado para esta ventana
        print(f'Cargado icono para la ventana: {clave_ventana}')

    # Centrar la ventana en la pantalla
    screen_width = ventana.winfo_screenwidth()  # Obtiene el ancho de la pantalla
    screen_height = ventana.winfo_screenheight()  # Obtiene la altura de la pantalla

    # Calcula las coordenadas para centrar la ventana
    x = (screen_width // 2) - (int(tamaño.split('x')[0]) // 2)  # Ancho de la ventana
    y = (screen_height // 2) - (int(tamaño.split('x')[1]) // 2)  # Altura de la ventana

    ventana.geometry(f"{tamaño}+{x}+{y}")  # Ajusta la posición de la ventana
