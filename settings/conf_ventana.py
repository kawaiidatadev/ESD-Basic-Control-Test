from settings.__init__ import inon_path
# Diccionario global para verificar si el icono ya ha sido cargado por ventana
iconos_cargados = {}

def configurar_ventana(ventana, titulo="Ventana", tamaño=None, pantalla_completa=False):
    global iconos_cargados  # Declarar la variable como global

    ventana.title(titulo)

    # Obtener el tamaño de la pantalla principal (ignorar otras pantallas)
    screen_width = ventana.winfo_screenwidth()  # Ancho disponible de la pantalla principal
    screen_height = ventana.winfo_screenheight()  # Altura disponible de la pantalla principal

    if tamaño is None:
        tamaño = f"{screen_width}x{screen_height}"  # Usar tamaño completo de la pantalla principal por defecto

    ventana.geometry(tamaño)  # Define el tamaño de la ventana

    # Usar el nombre de la ventana como clave en el diccionario
    clave_ventana = str(ventana)  # Puedes usar un identificador único para cada ventana

    # Verificar si el icono ya ha sido cargado para esta ventana
    if clave_ventana not in iconos_cargados:
        ventana.iconbitmap(inon_path)
        ventana.focus_force()
        iconos_cargados[clave_ventana] = True  # Marcar el icono como cargado para esta ventana
        print(f'Cargado icono para la ventana: {clave_ventana}')

    # Si no está en pantalla completa, centrar la ventana en la pantalla principal
    if not pantalla_completa:
        ancho, alto = map(int, tamaño.split('x'))  # Convertir cada parte del tamaño a entero
        x = (screen_width // 2) - (ancho // 2)  # Centrar la ventana en el ancho
        y = (screen_height // 2) - (alto // 2)  # Centrar la ventana en la altura
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")  # Ajusta la posición de la ventana

    # Si se desea pantalla completa sin bordes
    if pantalla_completa:
        ventana.attributes('-fullscreen', True)  # Poner en pantalla completa sin bordes


    # Forzar pantalla completa sin bordes y siempre encima
    ventana.attributes('-fullscreen', True)
    ventana.wm_attributes('-topmost', True)
