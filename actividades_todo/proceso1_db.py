from common.__init__ import *
from settings.__init__ import db_path
from strings_consultas_db import consulta_limpia_proceso_1
from actividades_todo.crear_pdf_proceso1 import pdf_proceso1


def obtener_ids(usuario_nombre, elemento_esd):
    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener el ID del usuario y del elemento ESD en base a la asignación
    cursor.execute(consulta_limpia_proceso_1, (usuario_nombre, elemento_esd))

    result = cursor.fetchone()
    conn.close()

    # Retornar los IDs, si existen
    return result if result else (None, None)


def proceso1_procesar_datos(datos, registros_count):
    # Verificar si el dato es un mensaje de error
    if isinstance(datos, str) and datos.startswith('Error'):
        return  # Ignorar mensajes de error

    # Inicializar el contador
    contador = 0

    # Si es una lista de diccionarios, filtramos los datos
    if isinstance(datos, list):
        for item in datos:
            if isinstance(item, dict) and item.get('Medición') != 'Seleccione':
                usuario_nombre = item.get('Usuario')
                elemento_esd = item.get('Elemento ESD')
                medicion_esd = item.get('Medición')

                # Obtener los IDs
                usuario_id, esd_item_id = obtener_ids(usuario_nombre, elemento_esd)

                # Pasar todos los contenidos del diccionario a la función pdf_proceso1
                print(f"Procesando: {item}")
                print(
                    f"ID del usuario: {usuario_id}, ID del elemento ESD: {esd_item_id}, valor de medicion: {medicion_esd}")

                # Llamar a la función pdf_proceso1 con los valores del diccionario
                pdf_proceso1(usuario_id=usuario_id, esd_item_id=esd_item_id, medicion_esd=medicion_esd,
                             n_serie=item.get('N. Serie'), usuario=item.get('Usuario'),
                             elemento_esd=item.get('Elemento ESD'), area=item.get('Área'),
                             linea=item.get('Línea'),
                             comentarios=item.get('Comentarios'), color_led=item.get('Color LED'))

                # Incrementar el contador
                contador += 1

    # Imprimir la cantidad de datos procesados
    print(f"Cantidad de datos procesados: {contador}")
    print(f"Cantidad de registros recibidos: {registros_count}")

    # Verificar si la cantidad de datos procesados coincide con la cantidad de registros recibidos
    if contador != registros_count:
        # Crear una ventana de alerta
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal
        messagebox.showwarning("Alerta",
                               "La cantidad de datos procesados no coincide con la cantidad de registros recibidos.")
        root.destroy()