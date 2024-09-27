import os
import shutil
import subprocess
import tempfile
import time
from datetime import datetime
from tkinter import simpledialog, messagebox
from tkinter import Tk
import openpyxl
import getpass
from common.__init__ import *
from settings.conf_ventana import configurar_ventana

# Rutas de archivos
plantilla_form4 = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\plantilla_proceso4\form_4.xlsx'
ubicacion_copias = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Data\Formularios generados\proces4_form4'
ruta_original_bat = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\excel_error\ejecutable.bat'

import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")



def obtener_numero_de_registros():
    """Abre una ventana para ingresar un número entero entre 1 y 100."""

    while True:
        try:
            entrada = simpledialog.askinteger("Registros", "Ingresa la cantidad de puntos ESD:             ",
                                              minvalue=1, maxvalue=100)
            if entrada is not None:
                return entrada  # Devuelve el número ingresado
            else:
                messagebox.showinfo("Información", "Operación cancelada.")  # Mensaje si se cancela
                return None  # Devuelve None si se cancela
        except Exception as e:
            messagebox.showerror("Error", f"Error al ingresar el número: {e}")
            break


import threading


def contador_tiempo(limite):
    """Función que cuenta hasta el límite y lo imprime cada segundo."""
    for i in range(limite):
        time.sleep(1)
        print(f"Tiempo transcurrido: {i + 1} segundo(s)")

    # Detener la ejecución de Python forzosamente al llegar al límite
    print("El tiempo ha alcanzado el límite de 20 segundos. Finalizando la ejecución de Python.")
    os._exit(1)

def ejecutar_y_eliminar_bat(ruta_original_bat):
    """Copia el archivo batch a la carpeta del usuario actual, lo ejecuta y lo elimina después con un límite de tiempo."""

    # Obtener el nombre del usuario actual
    usuario_actual = getpass.getuser()

    # Ruta de destino en la carpeta del usuario actual
    ruta_temporal_bat = os.path.join(f'C:\\Users\\{usuario_actual}', 'temp_script.bat')

    # Iniciar el conteo de tiempo total
    inicio_total = time.time()

    # Iniciar el hilo para contar el tiempo
    hilo_contador = threading.Thread(target=contador_tiempo, args=(20,))
    hilo_contador.start()

    try:
        # Copiar el archivo batch original al destino en la carpeta del usuario
        print(f"Copiando {ruta_original_bat} a {ruta_temporal_bat}")
        shutil.copy(ruta_original_bat, ruta_temporal_bat)

        # Ejecutar el archivo batch y capturar stdout y stderr para diagnóstico, con un timeout de 15 segundos
        print(f"Ejecutando {ruta_temporal_bat}")
        proceso = subprocess.Popen([ruta_temporal_bat], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True)

        # Leer la salida en tiempo real
        inicio = time.time()
        while True:
            salida = proceso.stdout.readline()
            if salida == '' and proceso.poll() is not None:
                break
            if salida:
                print(salida.strip())
            if time.time() - inicio > 15:
                proceso.terminate()
                raise subprocess.TimeoutExpired(ruta_temporal_bat, 15)

        # Mostrar errores (en caso de que los haya)
        errores = proceso.stderr.read()
        if errores:
            print("Errores estándar:", errores)

    except subprocess.TimeoutExpired:
        print(f"El archivo batch ha tardado más de 15 segundos. Finalizando ejecución de Python.")
        messagebox.showerror("Timeout", "El archivo batch tardó más de 15 segundos en ejecutarse.")
        sys.exit(1)

    except subprocess.CalledProcessError as e:
        # Si hay error, muestra el código de error y cualquier mensaje de stderr
        print(f"Error al ejecutar el archivo batch: {e}")
        print(f"Salida del error: {e.stderr}")
        messagebox.showerror("Error", f"No se pudo ejecutar el archivo batch: {e}")

    finally:
        # Eliminar el archivo batch temporal
        if os.path.exists(ruta_temporal_bat):
            os.remove(ruta_temporal_bat)
            print(f"Archivo batch temporal {ruta_temporal_bat} eliminado correctamente.")
        else:
            print("El archivo batch temporal no existe o ya fue eliminado.")

from openpyxl.utils import column_index_from_string

def llenar_excel_con_datos(ruta_archivo, numero_de_registros):
    """Llena la tabla 'Tabla3' en la columna 'Numero De Serie' con el número de registros."""

    wb = openpyxl.load_workbook(ruta_archivo)
    sheet = wb.active

    # Buscar la tabla "Tabla4"
    tabla_encontrada = None
    for table in sheet.tables.values():
        if table.name == "Tabla4":
            tabla_encontrada = table
            break

    if tabla_encontrada is None:
        messagebox.showerror("Error", "No se encontró la tabla 'Tabla4'.")
        return

    # Identificar las celdas que pertenecen a la columna "Numero De Serie"
    inicio_fila, fin_fila = int(tabla_encontrada.ref.split(":")[0][1:]), int(tabla_encontrada.ref.split(":")[1][1:])
    inicio_columna = column_index_from_string(tabla_encontrada.ref.split(":")[0][:1])

    # Buscar la columna "Numero De Serie"
    cabeceras = sheet[inicio_fila]
    indice_columna_serie = None
    for idx, celda in enumerate(cabeceras, start=1):
        if celda.value == "Numero De Serie":
            indice_columna_serie = idx
            break

    if indice_columna_serie is None:
        messagebox.showerror("Error", "No se encontró la columna 'Numero De Serie' en la tabla 'Tabla4'.")
        return

    # Llenar los registros en la columna "Numero De Serie"
    for i in range(numero_de_registros):
        celda = sheet.cell(row=inicio_fila + 1 + i, column=indice_columna_serie)
        celda.value = i + 1  # Número de registro

    # Actualizar el rango de la tabla para incluir las nuevas filas
    ultima_fila = inicio_fila + numero_de_registros
    nueva_referencia = f"{tabla_encontrada.ref.split(':')[0]}:{tabla_encontrada.ref.split(':')[1][:1]}{ultima_fila}"
    tabla_encontrada.ref = nueva_referencia

    # Establecer área de impresión (desde B2 hasta donde esté el último registro)
    sheet.print_area = f'B2:F{ultima_fila}'

    wb.save(ruta_archivo)  # Guarda los cambios
    wb.close()  # Cierra el archivo



def iniciar_formulario_con_reintentos_f4(max_intentos=3):
    """Inicia el formulario y gestiona los reintentos en caso de error."""
    intentos = 0
    while intentos < max_intentos:
        try:
            datos = obtener_numero_de_registros()
            if datos is None:
                return

            fecha_hora_actual = datetime.now().strftime("%d-%B-%Y %H-%M-%S")
            nuevo_nombre = f"{fecha_hora_actual} Proceso 4 - Form 4.xlsx"
            nueva_ruta = os.path.join(ubicacion_copias, nuevo_nombre)

            shutil.copy(plantilla_form4, nueva_ruta)
            llenar_excel_con_datos(nueva_ruta, datos)
            os.startfile(nueva_ruta)  # Abre el archivo en Excel
            break

        except Exception as e:
            print(f"Error al iniciar el formulario: {e}")
            messagebox.showerror("Error", f"Hubo un error al iniciar el formulario: {e}")

            try:
                ejecutar_y_eliminar_bat(ruta_original_bat)
            except Exception as e:
                print(f"Error al ejecutar el archivo batch: {e}")
                messagebox.showerror("Error", f"No se pudo ejecutar el archivo batch: {e}")

            time.sleep(10)  # Espera antes de reintentar
            intentos += 1

    if intentos == max_intentos:
        print("Se alcanzó el número máximo de intentos.")
        messagebox.showerror("Error", "Se alcanzó el número máximo de intentos.")