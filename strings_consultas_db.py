from common import *
from settings.__init__ import *

consulta_de_usuarios = """
    SELECT 
        nombre_usuario AS Nombre, 
        area AS Área, 
        linea AS Línea, 
        rol AS Rol, 
        estatus_usuario AS Estatus, 
        bata_estatus AS "Bata Estatus",
        bata_polar_estatus AS "Bata Polar Estatus",
        pulsera_estatus AS "Pulsera Estatus",
        talonera_estatus AS "Talonera Estatus"
    FROM 
        personal_esd
    WHERE
        estatus_usuario != 'Baja'
    LIMIT ? OFFSET ?
"""


actualizar_un_usuario = '''
            UPDATE personal_esd
            SET nombre_usuario = ?, rol = ?, area = ?, linea = ?, puesto = ?, fecha_registro = ?
            WHERE id = ?
        '''

cargar_datos_usuario_eliminar = """
            SELECT id, nombre_usuario, rol, area, linea, puesto 
            FROM personal_esd 
            WHERE estatus_usuario = 'Activo' AND area = ? AND linea = ?
            LIMIT ? OFFSET ?
        """


registrar_nueva_bata_esd = """
                INSERT INTO esd_items (tipo_elemento, numero_serie, tamaño, estatus, comentarios)
                VALUES (?, ?, ?, 'Sin asignar', ?)
            """


def obtener_tamanos_unicos():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT DISTINCT tamaño FROM esd_items WHERE estatus = 'Sin asignar';"
    cursor.execute(query)
    tamanos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tamanos

def obtener_tipos_unicos():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT DISTINCT tipo_elemento FROM esd_items WHERE estatus = 'Sin asignar';"
    cursor.execute(query)
    tipos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tipos

