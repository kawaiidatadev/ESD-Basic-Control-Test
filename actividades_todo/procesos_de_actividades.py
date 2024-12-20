from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path
from actividades_todo.iniciar_proceso_1 import iniciar_p1
from actividades_todo.iniciar_proceso_2 import iniciar_p2
from actividades_todo.iniciar_proceso_3 import iniciar_p3
from actividades_todo.iniciar_proceso_4 import iniciar_p4
from actividades_todo.instructivo1 import abrir_pdf
from actividades_todo.instructivo_2 import abrir_pdf2
from actividades_todo.instructivo_3 import abrir_pdf3
from actividades_todo.instructivo_4 import abrir_pdf4
from actividades_todo.formulario_proceso1 import iniciar_formulario_con_reintentos
from actividades_todo.formulario_proceso_2 import iniciar_formulario_con_reintentos_f2
from actividades_todo.formulario_proceso_3 import iniciar_formulario_con_reintentos_f3
from actividades_todo.formulario_proceso_4 import iniciar_formulario_con_reintentos_f4


# Variable global para el estatus del título

global_estatus_titulo = None

def cumplimiento_4_2_1(sub_ventana_cumplimiento, actividad_id):
    ventana_procedimiento_actividad = tk.Toplevel()  # Crear una nueva ventana
    sub_ventana_cumplimiento.withdraw()  # Ocultar la ventana principal al abrir la ventana de cumplimiento
    configurar_ventana(ventana_procedimiento_actividad, "Procedimientos de cumplimiento")

    def asignar_titulo(actividad_id):
        global global_estatus_titulo
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Buscar en la tabla actividades por el id dado
        cursor.execute("SELECT nombre_actividad, descripcion FROM actividades WHERE id = ?", (actividad_id,))
        actividad = cursor.fetchone()
        conn.close()

        if actividad:
            nombre_actividad, descripcion = actividad
            if "bata" in nombre_actividad.lower() or "bata" in descripcion.lower():
                ventana_procedimiento_actividad.title("Proceso Batas ESD")
                global_estatus_titulo = 1
            elif "tapetes" in nombre_actividad.lower() or "tapetes" in descripcion.lower():
                ventana_procedimiento_actividad.title("Proceso Tapetes ESD")
                global_estatus_titulo = 2
            elif "carritos" in nombre_actividad.lower() or "carritos" in descripcion.lower():
                ventana_procedimiento_actividad.title("Proceso Carritos ESD")
                global_estatus_titulo = 3
            elif "puntos" in nombre_actividad.lower() or "puntos" in descripcion.lower():
                ventana_procedimiento_actividad.title("Proceso Puntos de Conexion ESD")
                global_estatus_titulo = 4
            else:
                global_estatus_titulo = None  # No se encontró palabra clave

    # Llamar a la función para asignar el título basado en el id de actividad
    asignar_titulo(actividad_id)

    # Función para el botón de formulario
    def abrir_formulario():
        if global_estatus_titulo == 1:
            print('formulario 1')
            iniciar_formulario_con_reintentos()
        elif global_estatus_titulo == 2:
            print('formulario 2')
            iniciar_formulario_con_reintentos_f2()
        elif global_estatus_titulo == 3:
            iniciar_formulario_con_reintentos_f3()
            print('formulario 3')
        elif global_estatus_titulo == 4:
            iniciar_formulario_con_reintentos_f4()
            print('formulario 4')
        else:
            print('Global estatus erroneo')


    # Función para el botón de proceso
    def abrir_proceso():
        if global_estatus_titulo == 1:
            print('proceso 1')
            abrir_pdf()
        elif global_estatus_titulo == 2:
            print('proceso 2')
            abrir_pdf2()
        elif global_estatus_titulo == 3:
            print('proceso 3')
            abrir_pdf3()
        elif global_estatus_titulo == 4:
            print('proceso 4')
            abrir_pdf4()
        else:
            print('Global estatus erroneo')


    # Función para el botón de iniciar proceso
    def iniciar_proceso():
        print(f"Iniciar Proceso: {global_estatus_titulo}")
        if global_estatus_titulo == 1:
            iniciar_p1(ventana_procedimiento_actividad, global_estatus_titulo)
        elif global_estatus_titulo == 2:
            iniciar_p2(ventana_procedimiento_actividad, global_estatus_titulo)
        elif global_estatus_titulo == 3:
            iniciar_p3(ventana_procedimiento_actividad, global_estatus_titulo)
        elif global_estatus_titulo == 4:
            iniciar_p4(ventana_procedimiento_actividad, global_estatus_titulo)
        else:
            print('Global estatus erroneo')

    # Crear botones y asignarles las funciones correspondientes
    btn_formulario = tk.Button(ventana_procedimiento_actividad, text="Formulario", command=abrir_formulario,
                               font=("Arial", 12, "bold"), bg="blue", fg="white", height=1, width=20, relief="flat", bd=0)
    btn_formulario.pack(pady=10)

    btn_proceso = tk.Button(ventana_procedimiento_actividad, text="Proceso", command=abrir_proceso,
                            font=("Arial", 12, "bold"), bg="green", fg="white", height=1, width=20, relief="flat", bd=0)
    btn_proceso.pack(pady=10)

    btn_iniciar_proceso = tk.Button(ventana_procedimiento_actividad, text="Iniciar Proceso", command=iniciar_proceso,
                                    font=("Arial", 12, "bold"), bg="orange", fg="white", height=1, width=20, relief="flat", bd=0)
    btn_iniciar_proceso.pack(pady=10)

    # Función para salir del programa
    def salir_programa():
        ventana_procedimiento_actividad.withdraw()
        sub_ventana_cumplimiento.deiconify()

    # Crear el botón de salir
    btn_salir = tk.Button(ventana_procedimiento_actividad, text="Salir", command=salir_programa,
                          font=("Arial", 12, "bold"), bg="red", fg="white", height=1, width=10, relief="flat", bd=0)
    btn_salir.pack(pady=10)
