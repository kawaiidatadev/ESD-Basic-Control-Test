from common.__init__ import *
from settings.__init__ import db_path
from actividades_todo.db_editar_act import calcular_proxima_fecha

def manejo_de_estatus2(actividad_id=2):
    # Obtener la fecha y hora actual en Guadalajara, México
    tz = pytz.timezone('America/Mexico_City')
    fecha_ultima = datetime.now(tz)

    # Formatear las fechas a una cadena en formato ISO para evitar datos extraños
    fecha_ultima_str = fecha_ultima.strftime('%Y-%m-%d %H:%M:%S')

    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Obtener la frecuencia actual de la actividad
        cursor.execute("SELECT frecuencia FROM actividades WHERE id = ?", (actividad_id,))
        frecuencia = cursor.fetchone()[0]

        # Calcular la próxima fecha basada en la frecuencia
        proxima_fecha = calcular_proxima_fecha(fecha_ultima, frecuencia)

        # Convertir la próxima fecha a cadena si no es None
        proxima_fecha_str = proxima_fecha.strftime('%Y-%m-%d %H:%M:%S') if proxima_fecha else None

        # Actualizar el estatus, la fecha_ultima, y la proxima_fecha en la base de datos
        cursor.execute("""
            UPDATE actividades
            SET estatus = 'Realizando',
                fecha_ultima = ?,
                proxima_fecha = ?
            WHERE id = ?
        """, (fecha_ultima_str, proxima_fecha_str, actividad_id))

        # Guardar los cambios
        conn.commit()

        print(f"Actividad {actividad_id} actualizada a 'Realizando'. Fecha última: {fecha_ultima_str}, Próxima fecha: {proxima_fecha_str}")

    except Exception as e:
        print(f"Error al actualizar la actividad: {e}")
        conn.rollback()  # Revertir los cambios en caso de error

    finally:
        # Cerrar la conexión a la base de datos
        conn.close()

def manejo_de_estatus2_terminda(actividad_id=2):
    # Obtener la fecha y hora actual en Guadalajara, México
    tz = pytz.timezone('America/Mexico_City')
    fecha_ultima = datetime.now(tz)

    # Formatear las fechas a una cadena en formato ISO para evitar datos extraños
    fecha_ultima_str = fecha_ultima.strftime('%Y-%m-%d %H:%M:%S')

    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Obtener la frecuencia actual de la actividad
        cursor.execute("SELECT frecuencia FROM actividades WHERE id = ?", (actividad_id,))
        frecuencia = cursor.fetchone()[0]

        # Calcular la próxima fecha basada en la frecuencia
        proxima_fecha = calcular_proxima_fecha(fecha_ultima, frecuencia)

        # Convertir la próxima fecha a cadena si no es None
        proxima_fecha_str = proxima_fecha.strftime('%Y-%m-%d %H:%M:%S') if proxima_fecha else None

        # Actualizar el estatus, la fecha_ultima, y la proxima_fecha en la base de datos
        cursor.execute("""
            UPDATE actividades
            SET estatus = 'No iniciada',
                fecha_ultima = ?,
                proxima_fecha = ?
            WHERE id = ?
        """, (fecha_ultima_str, proxima_fecha_str, actividad_id))

        # Guardar los cambios
        conn.commit()

        print(f"Actividad {actividad_id} actualizada a 'Realizando'. Fecha última: {fecha_ultima_str}, Próxima fecha: {proxima_fecha_str}")

    except Exception as e:
        print(f"Error al actualizar la actividad: {e}")
        conn.rollback()  # Revertir los cambios en caso de error

    finally:
        # Cerrar la conexión a la base de datos
        conn.close()