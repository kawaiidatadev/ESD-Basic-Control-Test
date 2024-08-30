from common.__init__ import *
from settings.__init__ import db_path


def proceso1_procesar_datos(datos):
    # Verificar si el dato es un mensaje de error
    if isinstance(datos, str) and datos.startswith('Error'):
        return  # Ignorar mensajes de error

    # Si es una lista de diccionarios, filtramos los datos
    if isinstance(datos, list):
        for item in datos:
            if isinstance(item, dict) and item.get('Medición') != 'Seleccione':
                print(f"Procesando: {item}")


