from common.__init__ import *
from settings.__init__ import db_path

# Función para calcular la próxima fecha basada en la frecuencia
def calcular_proxima_fecha(fecha_ultima, frecuencia):
    if frecuencia == "Diario":
        return fecha_ultima + timedelta(days=1)
    elif frecuencia == "Semanal":
        return fecha_ultima + timedelta(weeks=1)
    elif frecuencia == "Mensual":
        return fecha_ultima + relativedelta(months=1)
    elif frecuencia == "Cada 2 meses":
        return fecha_ultima + relativedelta(months=2)
    elif frecuencia == "Cada 3 meses":
        return fecha_ultima + relativedelta(months=3)
    elif frecuencia == "Cada 4 meses":
        return fecha_ultima + relativedelta(months=4)
    elif frecuencia == "Cada 5 meses":
        return fecha_ultima + relativedelta(months=5)
    elif frecuencia == "Cada 6 meses":
        return fecha_ultima + relativedelta(months=6)
    elif frecuencia == "Cada 7 meses":
        return fecha_ultima + relativedelta(months=7)
    elif frecuencia == "Cada 8 meses":
        return fecha_ultima + relativedelta(months=8)
    elif frecuencia == "Cada 9 meses":
        return fecha_ultima + relativedelta(months=9)
    elif frecuencia == "Cada 10 meses":
        return fecha_ultima + relativedelta(months=10)
    elif frecuencia == "Cada 11 meses":
        return fecha_ultima + relativedelta(months=11)
    elif frecuencia == "Anual":
        return fecha_ultima + relativedelta(years=1)
    elif frecuencia == "Cada dos años":
        return fecha_ultima + relativedelta(years=2)
    elif frecuencia == "Cada 3 años":
        return fecha_ultima + relativedelta(years=3)
    elif frecuencia == "Autónomo":
        return None  # No se asigna próxima fecha
    else:
        return None  # Frecuencia no reconocida

# Función para actualizar una actividad existente
def actualizar_datos(actividad_id=None, nombre_actividad=None, descripcion=None, frecuencia=None,
                     fecha_ultima=None, equipo_de_medicion=None):
    try:
        print(f"{actividad_id} {nombre_actividad} {descripcion} {frecuencia} {fecha_ultima} {equipo_de_medicion}")

        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Calcular la próxima fecha
        proxima_fecha = calcular_proxima_fecha(fecha_ultima, frecuencia)
        print(proxima_fecha)

        # Actualizar el registro en la base de datos
        cursor.execute("""
            UPDATE actividades
            SET nombre_actividad = ?, descripcion = ?, frecuencia = ?, fecha_ultima = ?, proxima_fecha = ?, equipo_de_medicion = ?
            WHERE id = ?
        """, (
            nombre_actividad, descripcion, frecuencia, fecha_ultima,
            proxima_fecha.strftime('%Y-%m-%d %H:%M:%S') if proxima_fecha else None,
            equipo_de_medicion, actividad_id
        ))

        # Confirmar los cambios y cerrar la conexión
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", f"Actividad con ID {actividad_id} actualizada exitosamente.")


    except sqlite3.Error as e:
        messagebox.showerror("Error de base de datos", f"Ha ocurrido un error con la base de datos: {e}")

    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

    finally:
        if conn:
            conn.close()
