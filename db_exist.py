from common import *
from settings import db_path, sql_file


def verify_db():
    # Verifica si la base de datos existe
    if not os.path.exists(db_path):
        # Crear conexión para crear la base de datos
        conn = sqlite3.connect(db_path)

        # Ejecutar archivo .sql si existe
        if os.path.exists(sql_file):
            with open(sql_file, 'r', encoding='utf-8') as sql_file_obj:
                sql_script = sql_file_obj.read()

            try:
                conn.executescript(sql_script)
                resultado = "Base de datos creada y tablas ejecutadas desde archivo .sql."
            except sqlite3.Error as e:
                resultado = f"Error al ejecutar el archivo .sql: {e}"
        else:
            resultado = "Archivo .sql no encontrado."

        conn.close()
    else:
        resultado = "Base de datos ya existe."

    return print(resultado)






