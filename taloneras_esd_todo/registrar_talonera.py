from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path  # Importar la ruta de la base de datos

# Funcion para registrar taloneras
def registrar_talonera(taloneras_asignaciones, root):
    ventana_registro = tk.Toplevel(root)
    taloneras_asignaciones.withdraw()  # Ocultar la ventana anterior
    configurar_ventana(ventana_registro, "Registrar Nueva Talonera ESD")

    # Crear el frame para la entrada de datos
    frame = tk.Frame(ventana_registro)
    frame.pack(pady=20)

    # Label y Entry para la cantidad
    tk.Label(frame, text="Cantidad:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
    cantidad_entry = tk.Entry(frame, font=("Arial", 12))
    cantidad_entry.grid(row=0, column=1, padx=10, pady=10)

    # Label y Text para comentarios (puede quedar vacío)
    tk.Label(frame, text="Comentarios:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
    comentarios_text = tk.Text(frame, font=("Arial", 12), height=4, width=30)
    comentarios_text.grid(row=1, column=1, padx=10, pady=10)

    # Función para registrar la talonera
    def registrar():
        cantidad = cantidad_entry.get().strip()
        comentarios = comentarios_text.get("1.0", "end").strip()

        # Validar que la cantidad sea un número entero
        if not cantidad.isdigit():
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            return

        cantidad = int(cantidad)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            # Registrar la cantidad de taloneras ESD en la tabla esd_items
            for _ in range(cantidad):
                cursor.execute(
                    "INSERT INTO esd_items (tipo_elemento, numero_serie, tamaño, estatus, comentarios) VALUES (?, ?, ?, ?, ?)",
                    ("Talonera ESD", "", "", "Sin asignar", comentarios))

            conn.commit()
            messagebox.showinfo("Éxito", f"Se han registrado {cantidad} taloneras ESD correctamente.")
            ventana_registro.destroy()
            taloneras_asignaciones.deiconify()
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"Ha ocurrido un error al registrar las taloneras: {e}")
        finally:
            cursor.close()
            conn.close()

    # Botón para registrar la talonera
    tk.Button(frame, text="Registrar", command=registrar, font=("Arial", 14), bg="green", fg="white", height=2,
              width=20).grid(row=2, columnspan=2, pady=20)

    # Función para salir del registro sin hacer cambios
    def salir_programa():
        ventana_registro.destroy()
        taloneras_asignaciones.deiconify()

    # Botón para salir
    tk.Button(ventana_registro, text="Salir", command=salir_programa, font=("Arial", 14), bg="red", fg="white",
              height=2, width=15).place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

    ventana_registro.protocol("WM_DELETE_WINDOW", salir_programa)

