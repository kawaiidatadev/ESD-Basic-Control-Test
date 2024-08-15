consulta_de_usuarios = """
        SELECT 
            p.nombre_usuario, 
            p.area, 
            p.linea, 
            p.rol, 
            p.estatus_usuario,
            u.bata_estatus, 
            u.bata_polar_estatus, 
            u.pulsera_estatus, 
            u.talonera_estatus
        FROM 
            personal_esd p
        LEFT JOIN 
            usuarios_elementos u ON p.id = u.usuario_id
        WHERE
            p.estatus_usuario != 'Baja'
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