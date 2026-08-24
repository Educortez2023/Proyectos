from app.database.conexion import Conexion


class InsumoModel:

    # =====================================================
    # LISTAR INSUMOS
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
                i.id_insumo,
                i.codigo,
                i.nombre,
                c.nombre AS categoria,
                m.nombre AS marca,
                p.empresa AS proveedor,
                i.stock,
                i.stock_minimo,
                i.precio,
                u.nombre AS ubicacion,
                i.observaciones

            FROM insumos i

            LEFT JOIN categorias c
                ON i.id_categoria = c.id_categoria

            LEFT JOIN marcas m
                ON i.id_marca = m.id_marca

            LEFT JOIN proveedores p
                ON i.id_proveedor = p.id_proveedor

            LEFT JOIN ubicaciones u
                ON i.id_ubicacion = u.id_ubicacion

            WHERE i.activo = 1

            ORDER BY i.id_insumo ASC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        finally:

            cursor.close()
            conexion.close()


    # =====================================================
    # INSERTAR INSUMO
    # =====================================================

    def insertar(self, datos):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
            INSERT INTO insumos
            (
                codigo,
                nombre,
                id_categoria,
                id_marca,
                id_proveedor,
                stock,
                stock_minimo,
                precio,
                id_ubicacion,
                observaciones,
                activo
            )

            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                1
            )
            """

            cursor.execute(
                sql,
                datos
            )

            conexion.commit()

        except Exception:

            conexion.rollback()

            raise

        finally:

            cursor.close()
            conexion.close()


    # =====================================================
    # OBTENER INSUMO POR ID
    # =====================================================

    def obtener_por_id(self, id_insumo):

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
                id_categoria,
                id_marca,
                id_proveedor,
                stock,
                stock_minimo,
                precio,
                id_ubicacion,
                observaciones

            FROM insumos

            WHERE id_insumo = %s
            AND activo = 1
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
    # ACTUALIZAR INSUMO
    # =====================================================

    def actualizar(self, id_insumo, datos):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
            UPDATE insumos

            SET
                codigo = %s,
                nombre = %s,
                id_categoria = %s,
                id_marca = %s,
                id_proveedor = %s,
                stock = %s,
                stock_minimo = %s,
                precio = %s,
                id_ubicacion = %s,
                observaciones = %s

            WHERE id_insumo = %s
            """

            valores = (
                datos[0],
                datos[1],
                datos[2],
                datos[3],
                datos[4],
                datos[5],
                datos[6],
                datos[7],
                datos[8],
                datos[9],
                id_insumo
            )

            cursor.execute(
                sql,
                valores
            )

            conexion.commit()

        except Exception:

            conexion.rollback()

            raise

        finally:

            cursor.close()
            conexion.close()


    # =====================================================
    # BUSCAR INSUMOS
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
                i.id_insumo,
                i.codigo,
                i.nombre,
                c.nombre AS categoria,
                m.nombre AS marca,
                p.empresa AS proveedor,
                i.stock,
                i.stock_minimo,
                i.precio,
                u.nombre AS ubicacion,
                i.observaciones

            FROM insumos i

            LEFT JOIN categorias c
                ON i.id_categoria = c.id_categoria

            LEFT JOIN marcas m
                ON i.id_marca = m.id_marca

            LEFT JOIN proveedores p
                ON i.id_proveedor = p.id_proveedor

            LEFT JOIN ubicaciones u
                ON i.id_ubicacion = u.id_ubicacion

            WHERE i.activo = 1

            AND (
                i.codigo LIKE %s
                OR i.nombre LIKE %s
            )

            ORDER BY i.id_insumo ASC
            """

            valor = "%" + texto + "%"

            cursor.execute(
                sql,
                (
                    valor,
                    valor
                )
            )

            return cursor.fetchall()

        finally:

            cursor.close()
            conexion.close()


    # =====================================================
    # ELIMINAR / DESACTIVAR INSUMO
    # =====================================================

    def eliminar(self, id_insumo):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
            UPDATE insumos

            SET activo = 0

            WHERE id_insumo = %s
            """

            cursor.execute(
                sql,
                (id_insumo,)
            )

            conexion.commit()

        except Exception:

            conexion.rollback()

            raise

        finally:

            cursor.close()
            conexion.close()


    # =====================================================
    # LISTAR CATEGORÍAS
    # =====================================================

    def listar_categorias(self):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            cursor.execute("""
                SELECT
                    id_categoria,
                    nombre

                FROM categorias

                WHERE activo = 1

                ORDER BY nombre
            """)

            return cursor.fetchall()

        finally:

            cursor.close()
            conexion.close()


    # =====================================================
    # LISTAR MARCAS
    # =====================================================

    def listar_marcas(self):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            cursor.execute("""
                SELECT
                    id_marca,
                    nombre

                FROM marcas

                WHERE activo = 1

                ORDER BY nombre
            """)

            return cursor.fetchall()

        finally:

            cursor.close()
            conexion.close()


    # =====================================================
    # LISTAR PROVEEDORES
    # =====================================================

    def listar_proveedores(self):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            cursor.execute("""
                SELECT
                    id_proveedor,
                    empresa

                FROM proveedores

                WHERE activo = 1

                ORDER BY empresa
            """)

            return cursor.fetchall()

        finally:

            cursor.close()
            conexion.close()


    # =====================================================
    # LISTAR UBICACIONES
    # =====================================================

    def listar_ubicaciones(self):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            cursor.execute("""
                SELECT
                    id_ubicacion,
                    nombre

                FROM ubicaciones

                WHERE activo = 1

                ORDER BY nombre
            """)

            return cursor.fetchall()

        finally:

            cursor.close()
            conexion.close()