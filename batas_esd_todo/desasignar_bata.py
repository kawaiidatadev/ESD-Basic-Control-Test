from common import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import *
from strings_consultas_db import cargar_usuarios_desasignar


def desasignar_bata(ventana_batas_esd, root):
    ventana_desasignar = tk.Toplevel(root)
    ventana_batas_esd.withdraw()
    configurar_ventana(ventana_desasignar, "Desasignar Bata ESD")

    poner_imagen_de_fondo(ventana_desasignar, imagen_fondo_desasignar_batas, 300, 600, x=500, y=270, )  # Aquí usas la variable de tu path

    table_frame = tk.Frame(ventana_desasignar)
    table_frame.pack(pady=20)

    columns = ("ID", "Nombre", "Rol", "Puesto", "Bata Estatus", "Bata Polar Estatus")
    tree = ttk.Treeview(table_frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
    tree.pack()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    def cargar_usuarios():
        try:
            cursor.execute(cargar_usuarios_desasignar)
            usuarios = cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"Ha ocurrido un error al cargar los usuarios: {e}")
            return

        for item in tree.get_children():
            tree.delete(item)

        for usuario in usuarios:
            tree.insert("", "end", values=usuario)

    cargar_usuarios()

    bata_frame = tk.Frame(ventana_desasignar)
    bata_frame.pack(pady=20)

    tk.Label(bata_frame, text="Seleccione Bata:", font=("Arial", 12)).grid(row=0, column=0, padx=10)
    bata_combobox = ttk.Combobox(bata_frame, font=("Arial", 12), state='disabled')
    bata_combobox.grid(row=0, column=1, padx=10)

    causas_frame = tk.Frame(ventana_desasignar)
    causas_frame.pack(pady=20)

    tk.Label(causas_frame, text="Causa:", font=("Arial", 12)).grid(row=0, column=0, padx=10)
    causa_combobox = ttk.Combobox(causas_frame, font=("Arial", 12), state='disabled')
    causa_combobox['values'] = ["Daño físico", "No pasa las mediciones", "Otra"]
    causa_combobox.grid(row=0, column=1, padx=10)
    causa_combobox.current(0)

    comentarios_label = tk.Label(causas_frame, text="Comentarios:", font=("Arial", 12))
    comentarios_text = tk.Text(causas_frame, font=("Arial", 12), height=4, width=40)

    def mostrar_comentarios(event):
        if causa_combobox.get() == "Otra":
            comentarios_label.grid(row=1, column=0, padx=10, pady=10)
            comentarios_text.grid(row=1, column=1, padx=10, pady=10)
        else:
            comentarios_label.grid_forget()
            comentarios_text.grid_forget()

    causa_combobox.bind("<<ComboboxSelected>>", mostrar_comentarios)

    def habilitar_opciones(event):
        if tree.selection():
            bata_combobox.config(state='normal')
            causa_combobox.config(state='normal')

            seleccion = tree.selection()[0]
            usuario_info = tree.item(seleccion)['values']

            opciones_bata = []
            if usuario_info[4] == "Asignada":
                opciones_bata.append("Bata ESD")
            if usuario_info[5] == "Asignada":
                opciones_bata.append("Bata Polar ESD")

            bata_combobox['values'] = opciones_bata

            if len(opciones_bata) == 1:
                bata_combobox.current(0)
            else:
                bata_combobox.set('')
        else:
            bata_combobox.config(state='disabled')
            causa_combobox.config(state='disabled')
            bata_combobox.set('')

    tree.bind("<<TreeviewSelect>>", habilitar_opciones)

    def desasignar():
        seleccion = tree.selection()
        if seleccion:
            usuario_id = tree.item(seleccion)['values'][0]
            bata_seleccionada = bata_combobox.get()
            causa_seleccionada = causa_combobox.get()
            comentarios = comentarios_text.get("1.0", "end").strip() if causa_seleccionada == "Otra" else None

            if causa_seleccionada == "Otra" and not comentarios:
                messagebox.showwarning("Advertencia", "Debe escribir un comentario para la causa seleccionada.")
                return

            try:
                esd_item_id = None  # Variable para almacenar el ID del ítem ESD que se va a eliminar o desasignar

                if bata_seleccionada == "Bata ESD":
                    # Obtener el esd_item_id desde usuarios_elementos
                    cursor.execute("SELECT esd_item_id FROM usuarios_elementos WHERE usuario_id = ?",
                                   (usuario_id,))
                    resultado = cursor.fetchone()
                    if resultado:
                        esd_item_id = resultado[0]
                        cursor.execute("UPDATE personal_esd SET bata_estatus = 'Sin asignar' WHERE id = ?",
                                       (usuario_id,))
                        decision = messagebox.askquestion("Acción sobre la Bata",
                                                          "¿Desea eliminar la Bata ESD? Si selecciona No se desasignara.",
                                                          icon='warning')
                        if decision == 'yes':
                            cursor.execute("UPDATE esd_items SET estatus = 'Eliminada' WHERE id = ?", (esd_item_id,))
                        else:
                            cursor.execute("UPDATE esd_items SET estatus = 'Desasignada' WHERE id = ?", (esd_item_id,))
                    else:
                        messagebox.showerror("Error", "No se encontró una Bata ESD asignada a este usuario.")
                        return

                elif bata_seleccionada == "Bata Polar ESD":
                    # Obtener el esd_item_id desde usuarios_elementos
                    cursor.execute("SELECT esd_item_id FROM usuarios_elementos WHERE usuario_id = ?",
                                   (usuario_id,))
                    resultado = cursor.fetchone()
                    if resultado:
                        esd_item_id = resultado[0]
                        cursor.execute("UPDATE personal_esd SET bata_polar_estatus = 'Sin asignar' WHERE id = ?",
                                       (usuario_id,))
                        decision = messagebox.askquestion("Acción sobre la Bata Polar",
                                                          "¿Desea eliminar la Bata Polar ESD o solo desasignarla?",
                                                          icon='warning')
                        if decision == 'yes':
                            cursor.execute("UPDATE esd_items SET estatus = 'Eliminada' WHERE id = ?", (esd_item_id,))
                        else:
                            cursor.execute("UPDATE esd_items SET estatus = 'Desasignada' WHERE id = ?", (esd_item_id,))
                    else:
                        messagebox.showerror("Error", "No se encontró una Bata Polar ESD asignada a este usuario.")
                        return

                if esd_item_id:
                    # Eliminar la relación en la tabla usuarios_elementos
                    cursor.execute("DELETE FROM usuarios_elementos WHERE usuario_id = ? AND esd_item_id = ?",
                                   (usuario_id, esd_item_id))

                conn.commit()
                messagebox.showinfo("Éxito", "La bata ha sido desasignada correctamente.")
                cargar_usuarios()
            except sqlite3.Error as e:
                messagebox.showerror("Error de Base de Datos", f"Ha ocurrido un error al desasignar la bata: {e}")

    tk.Button(ventana_desasignar, text="Desasignar", command=desasignar, font=("Arial", 14), bg="red", fg="white",
              height=2, width=20).pack(pady=20)

    def salir_programa():
        ventana_desasignar.destroy()
        ventana_batas_esd.deiconify()

    tk.Button(ventana_desasignar, text="Salir", command=salir_programa, font=("Arial", 14), bg="red", fg="white",
              height=2, width=10).place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

    ventana_desasignar.protocol("WM_DELETE_WINDOW", salir_programa)

    ventana_desasignar.mainloop()

    cursor.close()
    conn.close()