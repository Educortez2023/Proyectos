from app.database.conexion import Conexion
from datetime import date


class PrestamoModel:

    # =====================================================
    # LISTAR PRÉSTAMOS
    # =====================================================

    def listar(self):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
                SELECT
                    p.id_prestamo,
                    p.id_equipo,
                    e.codigo,
                    e.nombre AS equipo,
                    p.id_responsable,
                    CONCAT(
                        r.nombres,
                        ' ',
                        r.apellidos
                    ) AS responsable,
                    p.fecha_prestamo,
                    p.fecha_devolucion,
                    p.estado,
                    p.observaciones,
                    p.fecha_creacion

                FROM prestamos p

                INNER JOIN equipos e
                    ON p.id_equipo = e.id_equipo

                INNER JOIN responsables r
                    ON p.id_responsable = r.id_responsable

                ORDER BY p.id_prestamo DESC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        finally:

            cursor.close()
            conexion.close()

    # =====================================================
    # BUSCAR PRÉSTAMOS
    # =====================================================

    def buscar(self, texto):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
                SELECT
                    p.id_prestamo,
                    p.id_equipo,
                    e.codigo,
                    e.nombre AS equipo,
                    p.id_responsable,
                    CONCAT(
                        r.nombres,
                        ' ',
                        r.apellidos
                    ) AS responsable,
                    p.fecha_prestamo,
                    p.fecha_devolucion,
                    p.estado,
                    p.observaciones,
                    p.fecha_creacion

                FROM prestamos p

                INNER JOIN equipos e
                    ON p.id_equipo = e.id_equipo

                INNER JOIN responsables r
                    ON p.id_responsable = r.id_responsable

                WHERE
                    e.codigo LIKE %s
                    OR e.nombre LIKE %s
                    OR r.nombres LIKE %s
                    OR r.apellidos LIKE %s
                    OR CONCAT(
                        r.nombres,
                        ' ',
                        r.apellidos
                    ) LIKE %s
                    OR p.estado LIKE %s
                    OR p.observaciones LIKE %s

                ORDER BY p.id_prestamo DESC
            """

            texto_busqueda = f"%{texto}%"

            parametros = (
                texto_busqueda,
                texto_busqueda,
                texto_busqueda,
                texto_busqueda,
                texto_busqueda,
                texto_busqueda,
                texto_busqueda
            )

            cursor.execute(
                sql,
                parametros
            )

            return cursor.fetchall()

        finally:

            cursor.close()
            conexion.close()

    # =====================================================
    # VERIFICAR SI EL EQUIPO TIENE PRÉSTAMO ACTIVO
    # =====================================================

    def equipo_tiene_prestamo_activo(
        self,
        id_equipo,
        excluir_id_prestamo=None
    ):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
                SELECT
                    id_prestamo,
                    id_responsable,
                    estado

                FROM prestamos

                WHERE id_equipo = %s

                AND estado IN (
                    'PENDIENTE',
                    'ENTREGADO'
                )
            """

            parametros = [id_equipo]

            if excluir_id_prestamo is not None:

                sql += """
                    AND id_prestamo <> %s
                """

                parametros.append(
                    excluir_id_prestamo
                )

            sql += """
                LIMIT 1
            """

            cursor.execute(
                sql,
                tuple(parametros)
            )

            return cursor.fetchone()

        finally:

            cursor.close()
            conexion.close()

    # =====================================================
    # REGISTRAR PRÉSTAMO
    # =====================================================

    def guardar(
        self,
        id_equipo,
        id_responsable,
        fecha_prestamo,
        fecha_devolucion,
        estado,
        observaciones
    ):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            # ---------------------------------------------
            # VALIDAR PRÉSTAMO ACTIVO
            # ---------------------------------------------

            sql_validar = """
                SELECT
                    id_prestamo

                FROM prestamos

                WHERE id_equipo = %s

                AND estado IN (
                    'PENDIENTE',
                    'ENTREGADO'
                )

                LIMIT 1
            """

            cursor.execute(
                sql_validar,
                (id_equipo,)
            )

            prestamo_existente = cursor.fetchone()

            if prestamo_existente:

                raise Exception(
                    "El equipo seleccionado ya tiene "
                    "un préstamo activo."
                )

            # ---------------------------------------------
            # INSERTAR PRÉSTAMO
            # ---------------------------------------------

            sql_insertar = """
                INSERT INTO prestamos (
                    id_equipo,
                    id_responsable,
                    fecha_prestamo,
                    fecha_devolucion,
                    estado,
                    observaciones
                )

                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """

            valores = (
                id_equipo,
                id_responsable,
                fecha_prestamo,
                fecha_devolucion,
                estado,
                observaciones
            )

            cursor.execute(
                sql_insertar,
                valores
            )

            # ---------------------------------------------
            # ACTUALIZAR RESPONSABLE DEL EQUIPO
            # ---------------------------------------------

            if estado == "ENTREGADO":

                sql_equipo = """
                    UPDATE equipos

                    SET
                        id_responsable = %s

                    WHERE id_equipo = %s
                """

                cursor.execute(
                    sql_equipo,
                    (
                        id_responsable,
                        id_equipo
                    )
                )

            # ---------------------------------------------
            # COMMIT
            # ---------------------------------------------

            conexion.commit()

        except Exception:

            conexion.rollback()

            raise

        finally:

            cursor.close()
            conexion.close()

    # =====================================================
    # ACTUALIZAR PRÉSTAMO
    # =====================================================

    def actualizar(
        self,
        id_prestamo,
        id_equipo,
        id_responsable,
        fecha_prestamo,
        fecha_devolucion,
        estado,
        observaciones
    ):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            # ---------------------------------------------
            # OBTENER DATOS ANTERIORES
            # ---------------------------------------------

            sql_anterior = """
                SELECT
                    id_equipo,
                    id_responsable,
                    estado

                FROM prestamos

                WHERE id_prestamo = %s
            """

            cursor.execute(
                sql_anterior,
                (id_prestamo,)
            )

            prestamo_anterior = cursor.fetchone()

            if prestamo_anterior is None:

                raise Exception(
                    "El préstamo seleccionado "
                    "no existe."
                )

            equipo_anterior = prestamo_anterior[0]

            # ---------------------------------------------
            # VALIDAR NUEVO EQUIPO
            # ---------------------------------------------

            sql_validar = """
                SELECT
                    id_prestamo

                FROM prestamos

                WHERE id_equipo = %s

                AND estado IN (
                    'PENDIENTE',
                    'ENTREGADO'
                )

                AND id_prestamo <> %s

                LIMIT 1
            """

            cursor.execute(
                sql_validar,
                (
                    id_equipo,
                    id_prestamo
                )
            )

            prestamo_existente = cursor.fetchone()

            if prestamo_existente:

                raise Exception(
                    "El equipo seleccionado ya tiene "
                    "otro préstamo activo."
                )

            # ---------------------------------------------
            # ACTUALIZAR PRÉSTAMO
            # ---------------------------------------------

            sql_actualizar = """
                UPDATE prestamos

                SET
                    id_equipo = %s,
                    id_responsable = %s,
                    fecha_prestamo = %s,
                    fecha_devolucion = %s,
                    estado = %s,
                    observaciones = %s

                WHERE id_prestamo = %s
            """

            valores = (
                id_equipo,
                id_responsable,
                fecha_prestamo,
                fecha_devolucion,
                estado,
                observaciones,
                id_prestamo
            )

            cursor.execute(
                sql_actualizar,
                valores
            )

            # ---------------------------------------------
            # SI CAMBIÓ EL EQUIPO
            # LIBERAR EL ANTERIOR
            # ---------------------------------------------

            if equipo_anterior != id_equipo:

                sql_liberar_anterior = """
                    UPDATE equipos

                    SET
                        id_responsable = NULL

                    WHERE id_equipo = %s
                """

                cursor.execute(
                    sql_liberar_anterior,
                    (equipo_anterior,)
                )

            # ---------------------------------------------
            # EQUIPO ENTREGADO
            # ASIGNAR RESPONSABLE
            # ---------------------------------------------

            if estado == "ENTREGADO":

                sql_asignar = """
                    UPDATE equipos

                    SET
                        id_responsable = %s

                    WHERE id_equipo = %s
                """

                cursor.execute(
                    sql_asignar,
                    (
                        id_responsable,
                        id_equipo
                    )
                )

            # ---------------------------------------------
            # EQUIPO DEVUELTO
            # LIBERAR RESPONSABLE
            # ---------------------------------------------

            elif estado == "DEVUELTO":

                sql_liberar = """
                    UPDATE equipos

                    SET
                        id_responsable = NULL

                    WHERE id_equipo = %s
                """

                cursor.execute(
                    sql_liberar,
                    (id_equipo,)
                )

            # ---------------------------------------------
            # COMMIT
            # ---------------------------------------------

            conexion.commit()

        except Exception:

            conexion.rollback()

            raise

        finally:

            cursor.close()
            conexion.close()

    # =====================================================
    # REGISTRAR DEVOLUCIÓN
    # =====================================================

    def registrar_devolucion(
        self,
        id_prestamo
    ):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            # ---------------------------------------------
            # OBTENER INFORMACIÓN DEL PRÉSTAMO
            # ---------------------------------------------

            sql_obtener = """
                SELECT
                    id_equipo,
                    estado

                FROM prestamos

                WHERE id_prestamo = %s
            """

            cursor.execute(
                sql_obtener,
                (id_prestamo,)
            )

            prestamo = cursor.fetchone()

            if prestamo is None:

                raise Exception(
                    "El préstamo seleccionado "
                    "no existe."
                )

            id_equipo = prestamo[0]

            estado_actual = prestamo[1]

            # ---------------------------------------------
            # VERIFICAR SI YA FUE DEVUELTO
            # ---------------------------------------------

            if estado_actual == "DEVUELTO":

                raise Exception(
                    "Este préstamo ya fue registrado "
                    "como devuelto."
                )

            # ---------------------------------------------
            # FECHA ACTUAL
            # ---------------------------------------------

            fecha_devolucion = date.today()

            # ---------------------------------------------
            # ACTUALIZAR PRÉSTAMO
            # ---------------------------------------------

            sql_devolucion = """
                UPDATE prestamos

                SET
                    fecha_devolucion = %s,
                    estado = 'DEVUELTO'

                WHERE id_prestamo = %s
            """

            cursor.execute(
                sql_devolucion,
                (
                    fecha_devolucion,
                    id_prestamo
                )
            )

            # ---------------------------------------------
            # LIBERAR RESPONSABLE DEL EQUIPO
            # ---------------------------------------------

            sql_liberar = """
                UPDATE equipos

                SET
                    id_responsable = NULL

                WHERE id_equipo = %s
            """

            cursor.execute(
                sql_liberar,
                (id_equipo,)
            )

            # ---------------------------------------------
            # COMMIT
            # ---------------------------------------------

            conexion.commit()

        except Exception:

            conexion.rollback()

            raise

        finally:

            cursor.close()
            conexion.close()

    # =====================================================
    # ELIMINAR PRÉSTAMO
    # =====================================================

    def eliminar(
        self,
        id_prestamo
    ):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            # ---------------------------------------------
            # OBTENER DATOS DEL PRÉSTAMO
            # ---------------------------------------------

            sql_obtener = """
                SELECT
                    id_equipo,
                    estado

                FROM prestamos

                WHERE id_prestamo = %s
            """

            cursor.execute(
                sql_obtener,
                (id_prestamo,)
            )

            prestamo = cursor.fetchone()

            if prestamo is None:

                raise Exception(
                    "El préstamo seleccionado "
                    "no existe."
                )

            id_equipo = prestamo[0]

            estado = prestamo[1]

            # ---------------------------------------------
            # ELIMINAR PRÉSTAMO
            # ---------------------------------------------

            sql_eliminar = """
                DELETE FROM prestamos

                WHERE id_prestamo = %s
            """

            cursor.execute(
                sql_eliminar,
                (id_prestamo,)
            )

            # ---------------------------------------------
            # SI ESTABA ENTREGADO
            # LIBERAR RESPONSABLE
            # ---------------------------------------------

            if estado == "ENTREGADO":

                sql_liberar = """
                    UPDATE equipos

                    SET
                        id_responsable = NULL

                    WHERE id_equipo = %s
                """

                cursor.execute(
                    sql_liberar,
                    (id_equipo,)
                )

            # ---------------------------------------------
            # COMMIT
            # ---------------------------------------------

            conexion.commit()

        except Exception:

            conexion.rollback()

            raise

        finally:

            cursor.close()
            conexion.close()