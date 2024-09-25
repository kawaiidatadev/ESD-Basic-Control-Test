from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path
from actividades_todo.estatus_proceso2 import manejo_de_estatus2


# Función para limpiar y procesar los registros
def limpiar_y_procesar_registro(registro):
    # Verificar los campos obligatorios
    if not registro.get('elemento_esd') or not registro.get('medicion') or not registro.get('color_led'):
        return None  # Si falta algún campo requerido, no procesar

    # Limpiar campos opcionales
    registro['comentarios'] = registro.get('comentarios', '').strip()
    registro['fecha_registro'] = registro.get('fecha_registro', None)
    registro['usuario_windows'] = registro.get('usuario_windows', '').strip()

    return registro


# Función para insertar los registros en la base de datos
def db_proceso_2_registro(registros):
    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        for registro in registros:
            registro_limpio = limpiar_y_procesar_registro(registro)
            if registro_limpio:
                cursor.execute('''
                    INSERT INTO actividades_registradas 
                    (numero_serie, usuario, elemento_esd, area, linea, medicion, comentarios, color_led, fecha_registro, usuario_windows)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    registro_limpio.get('numero_registro'),
                    # Asumimos que 'numero_registro' es equivalente a 'numero_serie'
                    'usuario',  # Cambiar según la lógica de usuario actual
                    registro_limpio.get('elemento_esd'),
                    'area',  # Cambiar según lógica de área
                    'linea',  # Cambiar según lógica de línea
                    registro_limpio.get('medicion'),
                    registro_limpio.get('comentarios'),
                    registro_limpio.get('color_led'),
                    registro_limpio.get('fecha_registro'),
                    registro_limpio.get('usuario_windows')
                ))

        # Guardar los cambios en la base de datos
        conn.commit()
        print("Registros insertados correctamente.")

    except Exception as e:
        print(f"Error al insertar registros: {e}")
        conn.rollback()  # Revertir cambios si hay error

    finally:
        conn.close()  # Cerrar la conexión a la base de datos