from common.__init__ import *
from settings.__init__ import db_path
from conversion_megaohms import convertir_a_megaohms

def guardar_db_actividad1_terminada(registros):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Obtener el nombre de usuario de Windows
        usuario_windows = getpass.getuser()

        # Obtener la fecha y hora actual en la zona horaria de Guadalajara, México
        zona_horaria = pytz.timezone('America/Mexico_City')
        fecha_hora_registro = datetime.now(zona_horaria).strftime('%Y-%m-%d %H:%M:%S')

        # SQL para insertar datos en la tabla actividades_registradas
        sql_insert = """
        INSERT INTO actividades_registradas 
        (numero_serie, usuario, elemento_esd, area, linea, medicion, comentarios, color_led, usuario_windows, fecha_registro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Recorrer cada registro y guardar en la base de datos
        for registro in registros:
            # Convertir la medición a megaohms
            medicion_convertida = convertir_a_megaohms(registro.get('Medición'))

            # Insertar el registro en la base de datos con la medición convertida
            cursor.execute(sql_insert, (
                registro.get('N. Serie'),
                registro.get('Usuario'),
                registro.get('Elemento ESD'),
                registro.get('Área'),
                registro.get('Línea'),
                medicion_convertida,  # Guardar la medición convertida
                registro.get('Comentarios'),
                registro.get('Color LED'),
                usuario_windows,  # Añadir el nombre de usuario de Windows
                fecha_hora_registro  # Añadir la fecha y hora de registro
            ))

        # Confirmar cambios y cerrar la conexión
        conn.commit()
        print(f"Se han guardado {len(registros)} registros en la base de datos.")
        confirmacion_proceso1_db()

    except Exception as e:
        print(f"Error al guardar los registros en la base de datos: {e}")
    finally:
        conn.close()

def confirmacion_proceso1_db():
    return True