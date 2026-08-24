from app.database.conexion import Conexion


class EquipoModel:

    # =====================================================
    # LISTAR EQUIPOS
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
                e.id_equipo,
                e.codigo,
                e.nombre,
                e.numero_serie,
                c.nombre AS categoria,
                m.nombre AS marca,
                es.nombre AS estado,
                e.fecha_compra,
                e.precio

            FROM equipos e

            LEFT JOIN categorias c
            ON e.id_categoria = c.id_categoria

            LEFT JOIN marcas m
            ON e.id_marca = m.id_marca

            LEFT JOIN estados es
            ON e.id_estado = es.id_estado

            ORDER BY e.id_equipo ASC
            """

            cursor.execute(sql)

            datos = cursor.fetchall()
            print("orden de equipos desde la bd:")
            for equipo in datos:
                print(equipo[0], equipo[1])

            return datos

        finally:

            cursor.close()
            conexion.close()


    # =====================================================
    # INSERTAR EQUIPO
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
            INSERT INTO equipos
            (
                codigo,
                nombre,
                numero_serie,
                id_categoria,
                id_marca,
                id_modelo,
                id_proveedor,
                id_estado,
                id_responsable,
                id_ubicacion,
                fecha_compra,
                garantia_meses,
                precio,
                observaciones
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
                %s,
                %s,
                %s,
                %s
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
    # OBTENER EQUIPO POR ID
    # =====================================================

    def obtener_por_id(self, id_equipo):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
            SELECT
                id_equipo,
                codigo,
                nombre,
                numero_serie,
                id_categoria,
                id_marca,
                id_modelo,
                id_proveedor,
                id_estado,
                id_responsable,
                id_ubicacion,
                fecha_compra,
                garantia_meses,
                precio,
                observaciones

            FROM equipos

            WHERE id_equipo = %s
            """

            cursor.execute(
                sql,
                (id_equipo,)
            )

            return cursor.fetchone()

        finally:

            cursor.close()
            conexion.close()

    # =====================================================
    # ACTUALIZAR EQUIPO
    # =====================================================

    def actualizar(self, id_equipo, datos):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
            UPDATE equipos

            SET
                codigo = %s,
                nombre = %s,
                numero_serie = %s,
                id_categoria = %s,
                id_marca = %s,
                id_modelo = %s,
                id_proveedor = %s,
                id_estado = %s,
                id_responsable = %s,
                id_ubicacion = %s,
                fecha_compra = %s,
                garantia_meses = %s,
                precio = %s,
                observaciones = %s

            WHERE id_equipo = %s
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
                datos[10],
                datos[11],
                datos[12],
                datos[13],
                id_equipo

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
    # BUSCAR EQUIPOS
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
                e.id_equipo,
                e.codigo,
                e.nombre,
                e.numero_serie,
                c.nombre AS categoria,
                m.nombre AS marca,
                es.nombre AS estado,
                e.fecha_compra,
                e.precio

            FROM equipos e

            LEFT JOIN categorias c
            ON e.id_categoria = c.id_categoria

            LEFT JOIN marcas m
            ON e.id_marca = m.id_marca

            LEFT JOIN estados es
            ON e.id_estado = es.id_estado

            WHERE
                e.codigo LIKE %s
                OR e.nombre LIKE %s
                OR e.numero_serie LIKE %s

            ORDER BY e.id_equipo ASC
            """

            valor = "%" + texto + "%"

            cursor.execute(
                sql,
                (
                    valor,
                    valor,
                    valor
                )
            )

            datos = cursor.fetchall()

            return datos

        finally:

            cursor.close()
            conexion.close()


    # =====================================================
    # ELIMINAR EQUIPO
    # =====================================================

    def eliminar(self, id_equipo):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
            DELETE FROM equipos
            WHERE id_equipo = %s
            """

            cursor.execute(
                sql,
                (id_equipo,)
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
    # LISTAR MODELOS POR MARCA
    # =====================================================

    def listar_modelos_por_marca(self, id_marca):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            cursor.execute("""
                SELECT
                    id_modelo,
                    nombre

                FROM modelos

                WHERE id_marca = %s
                AND activo = 1

                ORDER BY nombre
            """,
            (id_marca,))

            return cursor.fetchall()

        finally:

            cursor.close()
            conexion.close()


    # =====================================================
    # LISTAR ESTADOS
    # =====================================================

    def listar_estados(self):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            cursor.execute("""
                SELECT
                    id_estado,
                    nombre

                FROM estados

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

            cursor.execute("""
                SELECT
                    id_responsable,
                    CONCAT(
                        nombres,
                        ' ',
                        apellidos
                    ) AS responsable

                FROM responsables

                WHERE activo = 1

                ORDER BY nombres, apellidos
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