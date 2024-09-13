from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path
from actividades_todo.iniciar_proceso_1 import iniciar_p1

# Rutas de archivos
plantilla_form1 = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\plantilla_proceso1\form_1.xlsm'
ubicacion_copias = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Data\Formularios generados\proces1_form1'
# Ruta del archivo .bat original
ruta_original_bat =  r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\excel_error\ejecutable.bat'


def obtener_datos_usuarios_elementos():
    try:
        conn = sqlite3.connect(db_path)
        query = '''
        SELECT pe.id AS Id, 
               ei.tipo_elemento AS Elemento, 
               ei.numero_serie AS Numero_de_serie, 
               ei.tamaño AS Tamaño,
               pe.nombre_usuario AS nombre_usuario, 
               pe.rol, 
               pe.area, 
               pe.linea, 
               pe.puesto
        FROM usuarios_elementos ue
        INNER JOIN personal_esd pe ON ue.usuario_id = pe.id
        INNER JOIN esd_items ei ON ue.esd_item_id = ei.id
        WHERE ei.tipo_elemento IN ('Bata ESD', 'Bata Polar ESD');
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error al obtener datos de la base de datos: {e}")
        messagebox.showerror("Error", f"No se pudo obtener datos de la base de datos: {e}")
        return None

def llenar_excel_con_datos(ruta_excel, datos):
    try:
        excel = win32.Dispatch('Excel.Application')
        excel.Visible = False
        wb = excel.Workbooks.Open(ruta_excel)
        hoja = wb.Sheets(1)

        fila_inicial = 17

        encabezados = ['Id', 'Elemento', 'Numero de serie', 'Tamaño', 'nombre_usuario', 'rol', 'area', 'linea', 'puesto',
                       'Medicion', 'Criterio De Conformidad', 'Estado Final', 'Resguardo/Ubicación', 'Comentarios']

        for col_num, encabezado in enumerate(encabezados, start=2):  # Inicia desde columna B
            hoja.Cells(fila_inicial, col_num).Value = encabezado

        for idx, fila in datos.iterrows():
            for col_idx, valor in enumerate(fila, start=2):
                hoja.Cells(fila_inicial + idx + 1, col_idx).Value = valor

        ultima_fila = fila_inicial + len(datos)
        rango = f'B2:O{ultima_fila}'
        hoja.Range(rango).Select()
        hoja.PageSetup.PrintArea = rango
        excel.Windows(wb.Name).Activate()
        wb.Save()
        wb.Close()
        excel.Quit()

    except Exception as e:
        print(f"Error al llenar el archivo Excel: {e}")
        messagebox.showerror("Error", f"No se pudo llenar el archivo Excel: {e}")

def ejecutar_y_eliminar_bat(ruta_original_bat):
    ruta_temporal_bat = os.path.join(tempfile.gettempdir(), 'temp_script.bat')

    try:
        shutil.copy(ruta_original_bat, ruta_temporal_bat)
        subprocess.run([ruta_temporal_bat], check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el archivo batch: {e}")
        messagebox.showerror("Error", f"No se pudo ejecutar el archivo batch: {e}")
    finally:
        if os.path.exists(ruta_temporal_bat):
            os.remove(ruta_temporal_bat)

def iniciar_formulario_con_reintentos(max_intentos=3):
    intentos = 0
    while intentos < max_intentos:
        try:
            datos = obtener_datos_usuarios_elementos()
            if datos is None:
                return

            fecha_hora_actual = datetime.now().strftime("%d-%B-%Y %H-%M-%S")
            nuevo_nombre = f"{fecha_hora_actual} Proceso 1 - Form 1.xlsm"
            nueva_ruta = os.path.join(ubicacion_copias, nuevo_nombre)

            shutil.copy(plantilla_form1, nueva_ruta)
            llenar_excel_con_datos(nueva_ruta, datos)
            os.startfile(nueva_ruta)
            break

        except Exception as e:
            print(f"Error al iniciar el formulario: {e}")
            messagebox.showerror("Error", f"Hubo un error al iniciar el formulario: {e}")

            try:
                ejecutar_y_eliminar_bat(ruta_original_bat)
            except Exception as e:
                print(f"Error al ejecutar el archivo batch: {e}")
                messagebox.showerror("Error", f"No se pudo ejecutar el archivo batch: {e}")

            time.sleep(10)
            intentos += 1

    if intentos == max_intentos:
        print("Se alcanzó el número máximo de intentos.")
        messagebox.showerror("Error", "Se alcanzó el número máximo de intentos.")


