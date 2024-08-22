from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path
from tkinter import filedialog
import os
import datetime
import pytz
import shutil

def evidencias_asignacion(asignaciones_window, root):
    ventana_evidencias = tk.Toplevel(asignaciones_window)
    asignaciones_window.withdraw()
    configurar_ventana(ventana_evidencias, "Evidencias de asignaciones")

    # Conectar a la base de datos y obtener los elementos únicos de `tipo_elemento`
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT tipo_elemento FROM esd_items")
    elementos = cursor.fetchall()

    conn.close()

    if not elementos:
        messagebox.showwarning("Advertencia", "No se encontraron elementos en la tabla esd_items.")
        salir_evidencias()
        return

    # Crear un combobox con los elementos únicos, seleccionando por defecto el primer elemento
    tipo_elemento_var = tk.StringVar(value=elementos[0][0])
    combobox_elementos = ttk.Combobox(ventana_evidencias, textvariable=tipo_elemento_var, values=[el[0] for el in elementos], state="readonly", font=("Arial", 14))
    combobox_elementos.pack(pady=10)

    # Función para salir de la ventana de asignación
    def salir_evidencias():
        ventana_evidencias.destroy()
        asignaciones_window.deiconify()

    # Crear el botón "Salir"
    btn_salir = tk.Button(ventana_evidencias, text="Salir", command=salir_evidencias, font=("Arial", 14), bg="red",
                          fg="white", height=2, width=15)
    btn_salir.pack(pady=10)

    # Mostrar ruta del archivo seleccionado y de destino
    lbl_ruta_archivo = tk.Label(ventana_evidencias, text="Ruta del archivo: ", font=("Arial", 12))
    lbl_ruta_archivo.pack(pady=10)

    lbl_ruta_destino = tk.Label(ventana_evidencias, text="Ruta de destino: ", font=("Arial", 12))
    lbl_ruta_destino.pack(pady=10)

    # Función para subir archivo de evidencia
    def subir_evidencia():
        archivo = filedialog.askopenfilename(title="Selecciona un archivo de evidencia")
        if not archivo:
            return

        lbl_ruta_archivo.config(text=f"Ruta del archivo: {archivo}")

        # Obtener año actual y construir ruta de destino
        now = datetime.datetime.now(pytz.timezone('America/Mexico_City'))
        anio_actual = now.year
        tipo_elemento_seleccionado = tipo_elemento_var.get()
        ruta_destino = f"\\\\10.0.0.9\\Mtto_Prod\\00_Departamento_Mantenimiento\\ESD\\Software\\Data\\Responsivas evidenciadas\\{anio_actual}\\{tipo_elemento_seleccionado}"

        # Crear carpetas si no existen
        os.makedirs(ruta_destino, exist_ok=True)

        # Definir nombre del archivo de destino
        nombre_archivo_destino = now.strftime("%d-%m-%Y_%H-%M-%S") + os.path.splitext(archivo)[1]
        ruta_completa_destino = os.path.join(ruta_destino, nombre_archivo_destino)

        # Copiar archivo a la ruta de destino
        shutil.copy2(archivo, ruta_completa_destino)
        lbl_ruta_destino.config(text=f"Ruta de destino: {ruta_completa_destino}")

        # Guardar registro en la base de datos
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Obtener `esd_item_id` basado en el `tipo_elemento`
            cursor.execute("SELECT id FROM esd_items WHERE tipo_elemento = ? LIMIT 1", (tipo_elemento_seleccionado,))
            esd_item_id = cursor.fetchone()

            if esd_item_id:
                cursor.execute("""
                    INSERT INTO evidencias_asignacion (esd_item_id, ruta_archivo, fecha_subida)
                    VALUES (?, ?, ?)
                """, (esd_item_id[0], ruta_completa_destino, now))

                conn.commit()
                messagebox.showinfo("Evidencia Registrada", "La evidencia ha sido registrada exitosamente.")
            else:
                messagebox.showerror("Error", "No se pudo encontrar un elemento correspondiente en la base de datos.")

        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"Ha ocurrido un error: {e}")
        finally:
            if conn:
                conn.close()

    # Crear el botón "Suba su archivo de evidencia"
    btn_subir = tk.Button(ventana_evidencias, text="Suba su archivo de evidencia", command=subir_evidencia, font=("Arial", 14), bg="green", fg="white", height=2, width=25)
    btn_subir.pack(pady=10)
