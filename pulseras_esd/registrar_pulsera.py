from common import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import *  # Importar los paths

def abrir_ventana_registro(pulseras_asignaciones):
    ventana_registro = tk.Toplevel(pulseras_asignaciones)
    configurar_ventana(ventana_registro, "Registrar Nueva Pulsera")

    # Función para salir de la ventana de registro
    def salir_registro():
        ventana_registro.destroy()
        pulseras_asignaciones.deiconify()

    # Crear el botón "Salir"
    btn_salir = tk.Button(ventana_registro, text="Salir", command=salir_registro, font=("Arial", 14), bg="red", fg="white",
                          height=2, width=15)
    btn_salir.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

    # Crear entradas para la cantidad y comentario
    tk.Label(ventana_registro, text="Cantidad de Pulseras:", font=("Arial", 12)).place(relx=0.3, rely=0.3, anchor='e')
    cantidad_entry = tk.Entry(ventana_registro, font=("Arial", 12))
    cantidad_entry.place(relx=0.4, rely=0.3, anchor='w')

    tk.Label(ventana_registro, text="Comentario:", font=("Arial", 12)).place(relx=0.3, rely=0.4, anchor='e')
    comentario_entry = tk.Entry(ventana_registro, font=("Arial", 12))
    comentario_entry.place(relx=0.4, rely=0.4, anchor='w')

    # Función para registrar las pulseras en la base de datos
    def registrar_pulseras():
        try:
            # Intentar convertir la entrada de cantidad a un entero
            cantidad = int(cantidad_entry.get())
            comentario = comentario_entry.get()

            # Conectar a la base de datos y registrar las pulseras
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            for _ in range(cantidad):
                cursor.execute("""
                    INSERT INTO esd_items (tipo_elemento, numero_serie, tamaño, estatus, comentarios)
                    VALUES (?, ?, ?, ?, ?)
                """, ('Pulsera ESD', '', 'N-A', 'Sin asignar', comentario))

            conn.commit()
            conn.close()

            # Mostrar un mensaje de éxito
            tk.messagebox.showinfo("Registro Exitoso", f"Se registraron {cantidad} pulseras exitosamente.")
            ventana_registro.destroy()
            pulseras_asignaciones.deiconify()

        except ValueError:
            # Manejar el error si la cantidad no es un número válido
            tk.messagebox.showerror("Error de entrada", "Por favor, ingresa un número válido para la cantidad.")

        except sqlite3.OperationalError as e:
            # Manejar errores relacionados con la base de datos
            tk.messagebox.showerror("Error de base de datos", f"Ha ocurrido un error al registrar las pulseras: {e}")

        except Exception as e:
            # Capturar cualquier otro tipo de excepción inesperada
            tk.messagebox.showerror("Error inesperado", f"Ha ocurrido un error inesperado: {e}")

    # Crear botón para confirmar el registro
    btn_confirmar = tk.Button(ventana_registro, text="Registrar", command=registrar_pulseras, font=("Arial", 14), bg="green",
                              fg="white", height=2, width=15)
    btn_confirmar.place(relx=0.5, rely=0.6, anchor='center')
