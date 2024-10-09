from common.__init__ import *
from reporte_grande.limpieza import ejecutar_y_eliminar_bat, ruta_original_bat


def abrir_archivo(ruta_origen):
    try:
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.Visible = False  # No mostrar la aplicación Excel
        libro = excel.Workbooks.Open(ruta_origen)
        print("Archivo abierto correctamente.")
        return libro, excel
    except Exception as e:
        print(f"Ocurrió un error al abrir el archivo: {e}")
        return None, None

def actualizar_archivo(libro, excel):
    try:
        libro.RefreshAll()
        excel.CalculateUntilAsyncQueriesDone()  # Esperar a que las consultas se completen
        time.sleep(2)  # Espera para asegurar que se complete la actualización
        libro.Save()  # Guardar el archivo
        print("Archivo actualizado correctamente.")
    except Exception as e:
        print(f"Ocurrió un error al actualizar el archivo: {e}")

def cerrar_archivo(libro, excel):
    try:
        libro.Close(SaveChanges=True)
        excel.Quit()
        print("Archivo cerrado correctamente.")
    except Exception as e:
        print(f"Ocurrió un error al cerrar el archivo: {e}")

def copiar_archivo(ruta_origen, ruta_destino):
    try:
        shutil.copy(ruta_origen, ruta_destino)
        print(f"Archivo copiado correctamente a {ruta_destino}.")
    except Exception as e:
        print(f"Ocurrió un error al copiar el archivo: {e}")

def abrir_archivo_maximizado(ruta_destino):
    try:
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        libro_abierto = excel.Workbooks.Open(ruta_destino)
        excel.Visible = True
        excel.WindowState = win32.constants.xlMaximized  # Maximizar ventana
        print("Archivo abierto y maximizado correctamente.")
        return libro_abierto  # Devolver el libro abierto
    except Exception as e:
        print(f"Ocurrió un error al abrir el archivo maximizado: {e}")
        return None  # Asegúrate de manejar el caso de error


def abrir_reporte_central():
    try:
        ejecutar_y_eliminar_bat(ruta_original_bat)
        # Definir la ruta del archivo original y la ruta de destino
        ruta_origen = r"\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\plantilla_reporte_central\Reporte Central.xlsx"
        usuario_windows = os.getlogin()
        timestamp = datetime.now().strftime('%d-%m-%Y _ %H_%M_%S')
        ruta_destino = f"C:\\Users\\{usuario_windows}\\Downloads\\Reporte Central ESD {timestamp}.xlsx"

        # Abrir el archivo
        libro, excel = abrir_archivo(ruta_origen)
        if libro and excel:
            # Actualizar el archivo
            actualizar_archivo(libro, excel)
            # Cerrar el archivo y la aplicación Excel
            cerrar_archivo(libro, excel)

            # Copiar el archivo actualizado a la carpeta de Descargas
            copiar_archivo(ruta_origen, ruta_destino)
            ejecutar_y_eliminar_bat(ruta_original_bat)

            # Abrir el archivo copiado en Excel y maximizar la ventana
            abrir_archivo_maximizado(ruta_destino)
            ejecutar_y_eliminar_bat(ruta_original_bat)
            print('Acebe papi')

            # Abrir la carpeta de Descargas en una ventana maximizada
            subprocess.run(f'explorer /select,"{ruta_destino}"')

        else:
            print("No se pudo abrir el archivo para continuar con el proceso.")
    except Exception as e:
        print(f"Ocurrió un error en el proceso: {e}")
