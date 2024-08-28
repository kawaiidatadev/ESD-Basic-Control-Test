from common.__init__ import *
from settings.__init__ import db_path  # Asegúrate de que la ruta esté correcta

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


# Función para registrar una nueva actividad
def recibir_datos_a_registrar_actividad(
        nombre_actividad, descripcion, frecuencia, fecha_inicio, equipo_medicion, username, re_act, conf1):
    try:
        re_act.withdraw()  # Ocultar la ventana principal al abrir la ventana de parámetros
        # Zona horaria de Guadalajara, México
        tz = pytz.timezone('America/Mexico_City')
        fecha_registro = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

        # Formatear la fecha de inicio para incluir la hora actual
        fecha_ultima = datetime.strptime(fecha_inicio, '%d/%m/%Y')
        fecha_ultima = fecha_ultima.replace(hour=datetime.now(tz).hour, minute=datetime.now(tz).minute,
                                            second=datetime.now(tz).second)

        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar si ya existe un registro con los mismos valores en los campos relevantes
        cursor.execute("""
            SELECT * FROM actividades WHERE 
            nombre_actividad = ? AND descripcion = ? AND frecuencia = ? AND equipo_de_medicion = ?
        """, (nombre_actividad, descripcion, frecuencia, equipo_medicion))

        if cursor.fetchone():
            messagebox.showerror("Error", f"Ya existe una actividad registrada con estos datos:\n"
                                          f"Nombre: {nombre_actividad}\nDescripción: {descripcion}\n"
                                          f"Frecuencia: {frecuencia}\nEquipo de medición: {equipo_medicion}")
            conn.close()
            return

        # Calcular la próxima fecha
        proxima_fecha = calcular_proxima_fecha(fecha_ultima, frecuencia)

        if proxima_fecha is None and frecuencia != "Autónomo":
            messagebox.showerror("Error", "No se pudo calcular la próxima fecha. Verifique la frecuencia ingresada.")
            conn.close()
            return

        # Insertar el nuevo registro en la base de datos
        cursor.execute("""
            INSERT INTO actividades (
                nombre_actividad, descripcion, frecuencia, fecha_ultima, proxima_fecha, 
                estatus, usuario_windows, fecha_registro, equipo_de_medicion
            ) VALUES (?, ?, ?, ?, ?, 'No iniciada', ?, ?, ?)
        """, (
            nombre_actividad, descripcion, frecuencia, fecha_ultima.strftime('%Y-%m-%d %H:%M:%S'),
            proxima_fecha.strftime('%Y-%m-%d %H:%M:%S') if proxima_fecha else None, username, fecha_registro,
            equipo_medicion))

        # Confirmar los cambios y cerrar la conexión
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", f"Actividad {nombre_actividad} registrada exitosamente.")
        conf1.deiconify()


    except sqlite3.Error as e:
        messagebox.showerror("Error de base de datos", f"Ha ocurrido un error con la base de datos: {e}")

    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

    finally:
        if conn:
            conn.close()
