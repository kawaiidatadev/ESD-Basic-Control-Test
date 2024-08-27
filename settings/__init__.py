from common import *

# Path of data base sqlite
db_path = r'\\10.0.0.9\Mtto_Prod\00_Departamento_Mantenimiento\ESD\database.sqlite'

#SQL de creacion de tablas
sql_file = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Archivos db\create_db_sqlite.sql'

#Rows example
registros_ejemplo = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Archivos db\1_row_example.sql'

# Default ESD image path
default_image_path = r'\\10.0.0.9\Mtto_Prod\00_Departamento_Mantenimiento\ESD\ESD incono PNG.png'

# Defaul ICON
inon_path = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\girlrecort.ico'

# Default document PDF "ANSI S20.20" default
document_path = r'\\10.0.0.9\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Documentos\Manuales\97_ELE_0_ANSI-ESD-S20.20-2014.pdf'

imagen_fondo_registro_batas = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\registro_batas.png'

menu_azusa = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\azusa.png'

path_imagen_evidencias = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\u149.png'

path_imagen_registro_personal = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\umi.png'

path_imagen_consulta_personal = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\shinobu.png'

path_imagen_eliminar_personal = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\koneko.png'

imagen_fondo_desasignar_batas = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\azusa2.png'

imagen_registro_parametros = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\blend.png'

imagen_modificacion_parametros = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\usagi_2.png'

imagen_sub1_actividades = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\homu1.png'

imagen_sub2_actividades = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\game1.png'

def poner_imagen_de_fondo(ventana, path_imagen, ancho=None, alto=None, x=0, y=0, resize=True):
    # Cargar la imagen de fondo
    imagen_fondo = Image.open(path_imagen)

    # Redimensionar la imagen si se especifican las dimensiones o si resize es True
    if resize or (ancho and alto):
        ancho = ancho if ancho else ventana.winfo_width()
        alto = alto if alto else ventana.winfo_height()
        imagen_fondo = imagen_fondo.resize((ancho, alto),
                                           Image.LANCZOS)  # Usar Image.LANCZOS en lugar de Image.ANTIALIAS

    fondo = ImageTk.PhotoImage(imagen_fondo)

    # Crear un label para la imagen de fondo
    label_fondo = tk.Label(ventana, image=fondo)
    label_fondo.image = fondo  # Necesario para evitar que el garbage collector elimine la imagen
    label_fondo.place(x=x, y=y, width=ancho if ancho else ventana.winfo_width(),
                      height=alto if alto else ventana.winfo_height())


def cambiar_imagen(label):
    new_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if new_image_path:
        image = Image.open(new_image_path)
        image = image.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo

# Función para abrir el documento PDF
def abrir_documento():
    if os.path.exists(document_path):
        subprocess.Popen([document_path], shell=True)
    else:
        messagebox.showerror("Error", "El documento no se encuentra en la ruta especificada.")


# Función para abrir ventanas nuevas y ocultar el menú principal
def abrir_ventana(nombre_ventana, root):
    nueva_ventana = tk.Toplevel(root)
    nueva_ventana.title(nombre_ventana)
    nueva_ventana.state('zoomed')

    # Evento para cuando la ventana secundaria se cierra
    nueva_ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(nueva_ventana, root))

    root.withdraw()  # Ocultar el menú principal mientras la ventana secundaria está abierta

def cerrar_ventana(nueva_ventana, root):
    nueva_ventana.destroy()  # Cierra la ventana secundaria
    root.deiconify()  # Muestra nuevamente el menú principal
    root.state('zoomed')


# Función para manejar clics en la imagen
def manejar_clic_imagen(event, label):
    if event.state & 0x0001:  # Shift key is pressed
        cambiar_imagen(label)
    else:
        abrir_documento()
