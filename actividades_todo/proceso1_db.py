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


def proceso1_procesar_datos(datos, registros_count, proceso_1, ventana_procedimiento_actividad):
    # Verificar si el dato es un mensaje de error
    if isinstance(datos, str) and datos.startswith('Error'):
        return  # Ignorar mensajes de error

    # Inicializar el contador y la lista de registros procesados
    contador = 0
    registros = []

    # Verificar que 'datos' sea una lista de diccionarios
    if isinstance(datos, list):
        for item in datos:
            # Solo contar si 'item' es un diccionario y tiene los campos requeridos
            if isinstance(item, dict) and item.get('Medición') != 'Seleccione':
                contador += 1
                usuario_nombre = item.get('Usuario')
                elemento_esd = item.get('Elemento ESD')

                # Obtener los IDs
                usuario_id, esd_item_id = obtener_ids(usuario_nombre, elemento_esd)

                # Añadir los IDs y demás datos al registro
                item.update({
                    'usuario_id': usuario_id,
                    'esd_item_id': esd_item_id
                })

                # Agregar el registro a la lista de registros
                registros.append(item)
            else:
                print(f"Elemento no válido encontrado: {item}")
    else:
        print("Error: 'datos' no es una lista de diccionarios.")

    # Imprimir la cantidad de datos procesados
    print(f"Cantidad de datos procesados: {contador}")
    print(f"Cantidad de registros recibidos: {registros_count}")

    # Verificar si la cantidad de datos procesados coincide con la cantidad de registros recibidos
    if contador != registros_count:
        # Crear una ventana de alerta
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal
        messagebox.showwarning("Alerta", "La cantidad de datos procesados no coincide con la cantidad de registros recibidos.")
        root.destroy()
    else:
        # Llamar a la función pdf_proceso1 con la lista completa de registros
        pdf_proceso1(registros, proceso_1, ventana_procedimiento_actividad)

