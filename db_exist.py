from common import *
from settings import db_path, sql_file, registros_ejemplo

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

    print(resultado)
    if resultado != 'Base de datos ya existe.':

        # Preguntar al usuario si quiere ejecutar los inserts de ejemplo
        ejecutar_inserts = messagebox.askyesno("Ejecutar Registros de Ejemplo",
                                               "¿Desea ejecutar los registros de ejemplo?")

        if ejecutar_inserts:
            if os.path.exists(registros_ejemplo):
                with open(registros_ejemplo, 'r', encoding='utf-8') as registros_obj:
                    registros_script = registros_obj.read()

                try:
                    conn = sqlite3.connect(db_path)
                    conn.executescript(registros_script)
                    conn.close()
                    messagebox.showinfo("Éxito", "Registros de ejemplo ejecutados correctamente.")
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Error al ejecutar los registros de ejemplo: {e}")
            else:
                messagebox.showerror("Error", "Archivo de registros de ejemplo no encontrado.")
        else:
            messagebox.showinfo("Información", "No se ejecutaron los registros de ejemplo.")
