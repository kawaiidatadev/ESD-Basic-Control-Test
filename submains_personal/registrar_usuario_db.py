from common.__init__ import *
from settings.__init__ import *


def guardar_usuario(root, entry_nombre_usuario, var_rol, var_area, var_linea, var_puesto,
                    entry_otro_rol, entry_otro_area, entry_otro_linea, entry_otro_puesto, fecha_inicio, ventana_registro):
    try:
        print(fecha_inicio)
        print(type(fecha_inicio))
        fecha_ingresada = fecha_inicio



        # Obtener valores de los campos
        rol = entry_otro_rol.get() if var_rol == "Otro" else var_rol
        area = entry_otro_area.get() if var_area == "Otro" else var_area
        linea = entry_otro_linea.get() if var_linea == "Otro" else var_linea
        puesto = entry_otro_puesto.get() if var_puesto == "Otro" else var_puesto

        # Validar campos
        if not entry_nombre_usuario or not rol or not area or not linea or not puesto:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Validar si algún dato es "Seleccione una opción"
        if rol == "Seleccione una opción" or area == "Seleccione una opción" or linea == "Seleccione una opción" or puesto == "Seleccione una opción":
            messagebox.showerror("Error", "Debes seleccionar un valor válido en todos los campos.")
            return

        # Validar fecha

        if fecha_ingresada is None or fecha_ingresada == "dd/mm/aaaa":  # Validar si la fecha está vacía o es la por defecto
            messagebox.showerror("Error", "Debes ingresar una fecha válida.")
            return

        # Obtener la fecha actual en Guadalajara, Jalisco
        timezone = pytz.timezone('America/Mexico_City')  # Zona horaria de Guadalajara
        fecha_actual = datetime.now(timezone).date()  # Obtiene la fecha actual

        # Convertir la fecha ingresada a un objeto de fecha
        fecha_ingresada_datetime = datetime.strptime(fecha_ingresada, "%d/%m/%Y").date()

        # Validar que la fecha ingresada no sea mayor a la fecha actual
        if fecha_ingresada_datetime > fecha_actual:
            messagebox.showerror("Error", "La fecha no puede ser mayor a la fecha actual.")
            return

        # Conexión a la base de datos
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Verificar si el usuario ya existe
        cursor.execute("SELECT COUNT(*) FROM personal_esd WHERE nombre_usuario = ?", (entry_nombre_usuario,))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Error", "El usuario ya existe.")
            return

        # Insertar el usuario en la base de datos
        cursor.execute('''
            INSERT INTO personal_esd (nombre_usuario, rol, area, linea, puesto, estatus_usuario, fecha_ingreso)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (entry_nombre_usuario, rol, area, linea, puesto, "Activo", fecha_ingresada))

        connection.commit()
        messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")

        # Cerrar la ventana de registro
        ventana_registro.destroy()
        ventana_registro.quit()
        root.deiconify()  # Muestra nuevamente la ventana principal


    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"Se produjo un error al guardar el usuario: {e}")

    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error inesperado: {e}")

    finally:
        # Cerrar la conexión a la base de datos
        if 'connection' in locals():
            connection.close()