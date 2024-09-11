from common.__init__ import *
from settings.__init__ import db_path
from conversion_megaohms import convertir_a_megaohms
from actividades_todo.db_registrar_nueva_actividad import calcular_proxima_fecha


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
        actualizar_actividad_batas_esd()

    except Exception as e:
        print(f"Error al guardar los registros en la base de datos: {e}")
    finally:
        conn.close()


def actualizar_actividad_batas_esd():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Obtener la fecha y hora actual en la zona horaria de Guadalajara, México
        zona_horaria = pytz.timezone('America/Mexico_City')
        fecha_hora_actual = datetime.now(zona_horaria)

        # SQL para buscar la actividad con "batas ESD" y frecuencia "6 meses"
        sql_buscar_actividad = """
        SELECT * FROM actividades 
        WHERE LOWER(REPLACE(nombre_actividad, ' ', '')) LIKE '%batasesd%'
        AND LOWER(REPLACE(frecuencia, ' ', '')) LIKE '%6meses%'
        """

        cursor.execute(sql_buscar_actividad)
        actividad = cursor.fetchone()

        if actividad:
            # Actualizar el estatus y la fecha_ultima
            sql_actualizar = """
            UPDATE actividades
            SET estatus = ?, fecha_ultima = ?, proxima_fecha = ?
            WHERE id = ?
            """
            # Obtener la fecha_ultima y calcular la próxima fecha
            fecha_ultima = fecha_hora_actual
            proxima_fecha = calcular_proxima_fecha(fecha_ultima, "Cada 6 meses")

            # Ejecutar la actualización
            cursor.execute(sql_actualizar, (
                "No iniciada",
                fecha_ultima.strftime('%Y-%m-%d %H:%M:%S'),
                proxima_fecha.strftime('%Y-%m-%d %H:%M:%S'),
                actividad[0]  # El id de la actividad
            ))

            # Confirmar cambios
            conn.commit()

            # Mostrar mensaje al usuario
            msgbox.showinfo(
                "Actualización completada",
                f"La actividad de medición de batas ESD ha sido realizada por completo.\n"
                f"Ahora está reprogramada su próxima ejecución para el día {proxima_fecha.strftime('%d/%B/%Y')}."
            )
        else:
            print("No se encontró ninguna actividad de medición de batas ESD con frecuencia de 6 meses.")

    except Exception as e:
        print(f"Error al actualizar la actividad: {e}")
    finally:
        conn.close()


def confirmacion_proceso1_db():
    return True
