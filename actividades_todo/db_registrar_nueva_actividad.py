from common.__init__ import *
from settings.__init__ import db_path
def recibir_datos_a_registrar_actividad(nombre_actividad, descripcion, frecuencia, fecha_inicio, equipo_medicion, username):
    print('Datos recividos para registrar nueva actividad: ' + nombre_actividad + '  ' + descripcion + '  '  + frecuencia + '  '  + fecha_inicio + ' ' + equipo_medicion + ' ' + username)