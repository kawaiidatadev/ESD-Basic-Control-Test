from common.__init__ import *
ruta_original_bat = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\excel_error\limpieza_excel_central.bat'

def ejecutar_y_eliminar_bat(ruta_original_bat):
    """Copia el archivo batch a la carpeta del usuario actual, lo ejecuta y lo elimina después con un límite de tiempo."""

    # Obtener el nombre del usuario actual
    usuario_actual = getpass.getuser()

    # Ruta de destino en la carpeta del usuario actual
    ruta_temporal_bat = os.path.join(f'C:\\Users\\{usuario_actual}', 'temp_script.bat')

    try:
        # Copiar el archivo batch original al destino en la carpeta del usuario
        print(f"Copiando {ruta_original_bat} a {ruta_temporal_bat}")
        shutil.copy(ruta_original_bat, ruta_temporal_bat)

        # Ejecutar el archivo batch y capturar stdout y stderr para diagnóstico
        print(f"Ejecutando {ruta_temporal_bat}")
        proceso = subprocess.Popen([ruta_temporal_bat], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Esperar a que el proceso termine y obtener la salida
        salida, errores = proceso.communicate()

        # Mostrar salida estándar
        if salida:
            print("Salida estándar:\n", salida)

        # Mostrar errores (en caso de que los haya)
        if errores:
            print("Errores estándar:\n", errores)

    except Exception as e:
        print(f"Error al ejecutar el script: {e}")

    finally:
        # Eliminar el archivo batch temporal
        if os.path.exists(ruta_temporal_bat):
            os.remove(ruta_temporal_bat)
            print(f"Archivo batch temporal {ruta_temporal_bat} eliminado correctamente.")
        else:
            print("El archivo batch temporal no existe o ya fue eliminado.")

    print('Proceso finalizado.')
