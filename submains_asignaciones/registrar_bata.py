from common import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import *  # Importar los paths
from strings_consultas_db import registrar_nueva_bata_esd

def registrar_nueva_bata(ventana_batas_esd, root):
    ventana_registrar_bata = tk.Toplevel(root)  # Crear una nueva ventana hija de root
    configurar_ventana(ventana_registrar_bata, "Registro de nueva bata ESD")
    poner_imagen_de_fondo(ventana_registrar_bata, imagen_fondo_registro_batas)  # Aquí usas la variable de tu path

    # Función para salir del programa
    def salir_programa():
        ventana_registrar_bata.destroy()  # Destruye el objeto
        ventana_batas_esd.deiconify()  # Muestra nuevamente la ventana principal

    # Crear el formulario
    lbl_serial = tk.Label(ventana_registrar_bata, text="Número Serial:", font=("Arial", 12))
    lbl_serial.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    entry_serial = tk.Entry(ventana_registrar_bata, font=("Arial", 12))
    entry_serial.grid(row=0, column=1, padx=10, pady=10)

    lbl_tamano = tk.Label(ventana_registrar_bata, text="Tamaño:", font=("Arial", 12))
    lbl_tamano.grid(row=1, column=0, padx=10, pady=10, sticky='w')
    entry_tamano = tk.Entry(ventana_registrar_bata, font=("Arial", 12))
    entry_tamano.grid(row=1, column=1, padx=10, pady=10)

    lbl_comentarios = tk.Label(ventana_registrar_bata, text="Comentarios:", font=("Arial", 12))
    lbl_comentarios.grid(row=2, column=0, padx=10, pady=10, sticky='w')
    entry_comentarios = tk.Entry(ventana_registrar_bata, font=("Arial", 12))
    entry_comentarios.grid(row=2, column=1, padx=10, pady=10)

    lbl_tipo_bata = tk.Label(ventana_registrar_bata, text="Tipo de Bata:", font=("Arial", 12))
    lbl_tipo_bata.grid(row=3, column=0, padx=10, pady=10, sticky='w')
    combo_tipo_bata = ttk.Combobox(ventana_registrar_bata, values=["Bata ESD", "Bata Polar ESD"], font=("Arial", 12), state='readonly')
    combo_tipo_bata.grid(row=3, column=1, padx=10, pady=10)
    combo_tipo_bata.current(0)

    # Función para registrar la bata en la base de datos
    def registrar_bata():
        numero_serial = entry_serial.get()
        tamano = entry_tamano.get().upper()  # Convertir tamaño a mayúsculas
        comentarios = entry_comentarios.get()
        tipo_bata = combo_tipo_bata.get()

        if not tamano:
            messagebox.showerror("Error", "Por favor, ingrese el tamaño.")
            return

        # Si el número de serie está vacío, asignar '0' y no mostrar un error
        if not numero_serial:
            numero_serial = 0
        elif not numero_serial.isdigit():  # Verificar que el número de serie contenga solo dígitos
            messagebox.showerror("Error", "El número de serie debe contener solo números.")
            return

        try:
            conn = sqlite3.connect(db_path)  # Reemplaza con la ruta correcta de tu base de datos
            cursor = conn.cursor()

            # Insertar la bata en la tabla esd_items
            cursor.execute(registrar_nueva_bata_esd, (tipo_bata, numero_serial, tamano, comentarios))
            conn.commit()
            messagebox.showinfo("Éxito", "La bata ha sido registrada exitosamente.")
            salir_programa()  # Cerrar la ventana después de registrar
        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"Error al registrar la bata: {e}")
        finally:
            if conn:
                conn.close()

    # Crear el botón "Registrar"
    btn_registrar = tk.Button(ventana_registrar_bata, text="Registrar", command=registrar_bata, font=("Arial", 14),
                              bg="green", fg="white", height=2, width=10)
    btn_registrar.grid(row=4, column=0, padx=10, pady=20, columnspan=2)

    # Crear el botón "Salir"
    btn_salir = tk.Button(ventana_registrar_bata, text="Salir", command=salir_programa, font=("Arial", 14), bg="red",
                          fg="white", height=2, width=10)
    btn_salir.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # Posiciona el botón en la esquina inferior derecha

    # Ocultar la ventana principal al abrir la ventana de registro de bata esd
    ventana_batas_esd.withdraw()  # Oculta la ventana principal

    # Ejecutar la ventana de registrar bata esd
    ventana_registrar_bata.protocol("WM_DELETE_WINDOW", salir_programa)  # Asegúrate de cerrar correctamente
    ventana_registrar_bata.mainloop()