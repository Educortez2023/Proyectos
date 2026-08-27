from app.database.conexion import Conexion


class MovimientoModel:

    # =====================================================
    # LISTAR MOVIMIENTOS
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
                    m.id_movimiento,
                    m.id_insumo,
                    i.codigo,
                    i.nombre AS insumo,
                    m.id_tipo_movimiento,
                    tm.nombre AS tipo_movimiento,
                    m.cantidad,
                    m.stock_anterior,
                    m.stock_nuevo,
                    m.id_responsable,
                    CONCAT(
                        r.nombres,
                        ' ',
                        r.apellidos
                    ) AS responsable,
                    m.observaciones,
                    m.fecha_movimiento

                FROM movimientos m

                INNER JOIN insumos i
                    ON m.id_insumo = i.id_insumo

                INNER JOIN tipos_movimientos tm
                    ON m.id_tipo_movimiento =
                       tm.id_tipo_movimiento

                LEFT JOIN responsables r
                    ON m.id_responsable =
                       r.id_responsable

                ORDER BY
                    m.id_movimiento DESC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        finally:

            cursor.close()
            conexion.close()


    # =====================================================
    # BUSCAR MOVIMIENTOS
    # =====================================================

    def buscar(self, texto):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            texto_busqueda = f"%{texto}%"

            sql = """
                SELECT
                    m.id_movimiento,
                    m.id_insumo,
                    i.codigo,
                    i.nombre AS insumo,
                    m.id_tipo_movimiento,
                    tm.nombre AS tipo_movimiento,
                    m.cantidad,
                    m.stock_anterior,
                    m.stock_nuevo,
                    m.id_responsable,
                    CONCAT(
                        r.nombres,
                        ' ',
                        r.apellidos
                    ) AS responsable,
                    m.observaciones,
                    m.fecha_movimiento

                FROM movimientos m

                INNER JOIN insumos i
                    ON m.id_insumo = i.id_insumo

                INNER JOIN tipos_movimientos tm
                    ON m.id_tipo_movimiento =
                       tm.id_tipo_movimiento

                LEFT JOIN responsables r
                    ON m.id_responsable =
                       r.id_responsable

                WHERE
                    i.codigo LIKE %s
                    OR i.nombre LIKE %s
                    OR tm.nombre LIKE %s
                    OR CONCAT(
                        r.nombres,
                        ' ',
                        r.apellidos
                    ) LIKE %s
                    OR m.observaciones LIKE %s

                ORDER BY
                    m.id_movimiento DESC
            """

            parametros = (
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
    # LISTAR TIPOS DE MOVIMIENTO
    # =====================================================

    def listar_tipos_movimiento(self):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
                SELECT
                    id_tipo_movimiento,
                    nombre,
                    descripcion

                FROM tipos_movimientos

                WHERE activo = 1

                ORDER BY
                    id_tipo_movimiento ASC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        finally:

            cursor.close()
            conexion.close()


    # =====================================================
    # LISTAR INSUMOS
    # =====================================================

    def listar_insumos(self):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
                SELECT
                    id_insumo,
                    codigo,
                    nombre,
                    stock

                FROM insumos

                WHERE activo = 1

                ORDER BY
                    id_insumo ASC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        finally:

            cursor.close()
            conexion.close()


    # =====================================================
    # LISTAR RESPONSABLES
    # =====================================================

    def listar_responsables(self):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
                SELECT
                    id_responsable,
                    CONCAT(
                        nombres,
                        ' ',
                        apellidos
                    ) AS responsable

                FROM responsables

                ORDER BY
                    id_responsable ASC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        finally:

            cursor.close()
            conexion.close()


    # =====================================================
    # OBTENER UN INSUMO
    # =====================================================

    def obtener_insumo(self, id_insumo):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
                SELECT
                    id_insumo,
                    codigo,
                    nombre,
                    stock

                FROM insumos

                WHERE id_insumo = %s
            """

            cursor.execute(
                sql,
                (id_insumo,)
            )

            return cursor.fetchone()

        finally:

            cursor.close()
            conexion.close()


    # =====================================================
    # REGISTRAR MOVIMIENTO
    # =====================================================

    def registrar(
        self,
        id_insumo,
        id_tipo_movimiento,
        cantidad,
        id_responsable,
        observaciones
    ):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            # =================================================
            # VALIDAR CANTIDAD
            # =================================================

            if cantidad is None:

                raise Exception(
                    "La cantidad es obligatoria."
                )

            try:

                cantidad = int(cantidad)

            except (ValueError, TypeError):

                raise Exception(
                    "La cantidad debe ser un número entero."
                )

            if cantidad <= 0:

                raise Exception(
                    "La cantidad debe ser mayor que cero."
                )


            # =================================================
            # OBTENER STOCK ACTUAL
            # =================================================

            sql_insumo = """
                SELECT
                    stock

                FROM insumos

                WHERE id_insumo = %s

                FOR UPDATE
            """

            cursor.execute(
                sql_insumo,
                (id_insumo,)
            )

            insumo = cursor.fetchone()

            if insumo is None:

                raise Exception(
                    "El insumo seleccionado no existe."
                )

            stock_anterior = insumo[0]

            if stock_anterior is None:

                stock_anterior = 0


            # =================================================
            # OBTENER TIPO DE MOVIMIENTO
            # =================================================

            sql_tipo = """
                SELECT
                    nombre

                FROM tipos_movimientos

                WHERE id_tipo_movimiento = %s
                AND activo = 1
            """

            cursor.execute(
                sql_tipo,
                (id_tipo_movimiento,)
            )

            tipo = cursor.fetchone()

            if tipo is None:

                raise Exception(
                    "El tipo de movimiento seleccionado "
                    "no existe."
                )

            tipo_movimiento = str(
                tipo[0]
            ).upper().strip()


            # =================================================
            # CALCULAR NUEVO STOCK
            # =================================================

            if tipo_movimiento == "ENTRADA":

                stock_nuevo = (
                    stock_anterior + cantidad
                )

            elif tipo_movimiento == "SALIDA":

                if cantidad > stock_anterior:

                    raise Exception(
                        "No hay suficiente stock disponible "
                        "para realizar esta salida.\n\n"
                        f"Stock actual: {stock_anterior}\n"
                        f"Cantidad solicitada: {cantidad}"
                    )

                stock_nuevo = (
                    stock_anterior - cantidad
                )

            elif tipo_movimiento == "AJUSTE":

                stock_nuevo = cantidad

            else:

                raise Exception(
                    "Tipo de movimiento no válido."
                )


            # =================================================
            # ACTUALIZAR STOCK DEL INSUMO
            # =================================================

            sql_actualizar_stock = """
                UPDATE insumos

                SET
                    stock = %s

                WHERE id_insumo = %s
            """

            cursor.execute(
                sql_actualizar_stock,
                (
                    stock_nuevo,
                    id_insumo
                )
            )


            # =================================================
            # REGISTRAR MOVIMIENTO
            # =================================================

            sql_movimiento = """
                INSERT INTO movimientos (
                    id_insumo,
                    id_tipo_movimiento,
                    cantidad,
                    stock_anterior,
                    stock_nuevo,
                    id_responsable,
                    observaciones
                )

                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """

            valores = (
                id_insumo,
                id_tipo_movimiento,
                cantidad,
                stock_anterior,
                stock_nuevo,
                id_responsable,
                observaciones
            )

            cursor.execute(
                sql_movimiento,
                valores
            )


            # =================================================
            # CONFIRMAR TRANSACCIÓN
            # =================================================

            conexion.commit()

        except Exception:

            conexion.rollback()

            raise

        finally:

            cursor.close()
            conexion.close()


    # =====================================================
    # OBTENER UN MOVIMIENTO
    # =====================================================

    def obtener(self, id_movimiento):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
                SELECT
                    id_movimiento,
                    id_insumo,
                    id_tipo_movimiento,
                    cantidad,
                    stock_anterior,
                    stock_nuevo,
                    id_responsable,
                    observaciones,
                    fecha_movimiento

                FROM movimientos

                WHERE id_movimiento = %s
            """

            cursor.execute(
                sql,
                (id_movimiento,)
            )

            return cursor.fetchone()

        finally:

            cursor.close()
            conexion.close()


    # =====================================================
    # ELIMINAR MOVIMIENTO
    # =====================================================

    def eliminar(self, id_movimiento):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            # =================================================
            # OBTENER MOVIMIENTO
            # =================================================

            sql_movimiento = """
                SELECT
                    id_movimiento,
                    id_insumo,
                    stock_anterior,
                    stock_nuevo

                FROM movimientos

                WHERE id_movimiento = %s

                FOR UPDATE
            """

            cursor.execute(
                sql_movimiento,
                (id_movimiento,)
            )

            movimiento = cursor.fetchone()

            if movimiento is None:

                raise Exception(
                    "El movimiento seleccionado "
                    "no existe."
                )

            id_movimiento_db = movimiento[0]
            id_insumo = movimiento[1]
            stock_anterior = movimiento[2]
            stock_nuevo = movimiento[3]


            # =================================================
            # VERIFICAR QUE SEA EL ÚLTIMO MOVIMIENTO
            # DEL MISMO INSUMO
            # =================================================

            sql_ultimo = """
                SELECT
                    id_movimiento

                FROM movimientos

                WHERE id_insumo = %s

                ORDER BY
                    id_movimiento DESC

                LIMIT 1

                FOR UPDATE
            """

            cursor.execute(
                sql_ultimo,
                (id_insumo,)
            )

            ultimo = cursor.fetchone()

            if ultimo is None:

                raise Exception(
                    "No se pudo verificar "
                    "el último movimiento."
                )

            if ultimo[0] != id_movimiento_db:

                raise Exception(
                    "No se puede eliminar este movimiento "
                    "porque existen movimientos posteriores "
                    "para el mismo insumo.\n\n"
                    "Para mantener el stock y el historial "
                    "correctos, primero debe eliminar "
                    "el movimiento más reciente."
                )


            # =================================================
            # OBTENER STOCK ACTUAL
            # =================================================

            sql_stock_actual = """
                SELECT
                    stock

                FROM insumos

                WHERE id_insumo = %s

                FOR UPDATE
            """

            cursor.execute(
                sql_stock_actual,
                (id_insumo,)
            )

            stock = cursor.fetchone()

            if stock is None:

                raise Exception(
                    "El insumo asociado al movimiento "
                    "no existe."
                )


            # =================================================
            # RESTAURAR STOCK ANTERIOR
            # =================================================

            sql_restaurar_stock = """
                UPDATE insumos

                SET
                    stock = %s

                WHERE id_insumo = %s
            """

            cursor.execute(
                sql_restaurar_stock,
                (
                    stock_anterior,
                    id_insumo
                )
            )


            # =================================================
            # ELIMINAR MOVIMIENTO
            # =================================================

            sql_delete = """
                DELETE FROM movimientos

                WHERE id_movimiento = %s
            """

            cursor.execute(
                sql_delete,
                (id_movimiento_db,)
            )

            if cursor.rowcount == 0:

                raise Exception(
                    "No se pudo eliminar "
                    "el movimiento."
                )


            # =================================================
            # CONFIRMAR TRANSACCIÓN
            # =================================================

            conexion.commit()

        except Exception:

            conexion.rollback()

            raise

        finally:

            cursor.close()
            conexion.close()