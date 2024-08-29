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
    query = "SELECT DISTINCT tamaño FROM esd_items WHERE estatus = 'Sin asignar' and estatus != 'Eliminada';"
    cursor.execute(query)
    tamanos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tamanos

def obtener_tipos_unicos():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT DISTINCT tipo_elemento FROM esd_items WHERE estatus = 'Sin asignar' and estatus != 'Eliminada';"
    cursor.execute(query)
    tipos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tipos


cargar_usuarios_desasignar = """
            SELECT id, nombre_usuario, rol, puesto, bata_estatus, bata_polar_estatus
            FROM personal_esd
            WHERE bata_estatus = 'Asignada' OR bata_polar_estatus = 'Asignada'
            ORDER BY nombre_usuario
        """


# Función para obtener los datos de los usuarios con pulseras asignadas
def obtener_usuarios_con_pulseras():
    conn = sqlite3.connect(db_path)  # Actualiza con la ruta correcta
    cursor = conn.cursor()
    query = """
        SELECT id, nombre_usuario, rol, area, linea, puesto, pulsera_estatus 
        FROM personal_esd 
        WHERE estatus_usuario = 'Activo' AND pulsera_estatus = 'Asignada'
        ORDER BY nombre_usuario
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

tipos_elementos_del_usuario_id ="""
                SELECT esd_items.id, esd_items.tipo_elemento
                FROM usuarios_elementos
                JOIN esd_items ON usuarios_elementos.esd_item_id = esd_items.id
                WHERE usuarios_elementos.usuario_id = ?
            """

# Consulta para obtener los datos ordenados alfabéticamente por nombre
consulta_de_iniciar_proceso_1 = """
        SELECT esd_items.numero_serie, personal_esd.nombre_usuario, esd_items.tipo_elemento, personal_esd.area, personal_esd.linea, esd_items.comentarios
        FROM usuarios_elementos
        JOIN esd_items ON usuarios_elementos.esd_item_id = esd_items.id
        JOIN personal_esd ON usuarios_elementos.usuario_id = personal_esd.id
        WHERE LOWER(esd_items.tipo_elemento) LIKE '%bata%'
        ORDER BY personal_esd.nombre_usuario
        """