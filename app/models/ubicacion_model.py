from app.database.conexion import Conexion


class UbicacionModel:

    # =====================================================
    # LISTAR UBICACIONES
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
                id_ubicacion,
                nombre,
                descripcion,
                activo

            FROM ubicaciones

            ORDER BY
                nombre ASC
            """

            cursor.execute(
                sql
            )

            resultados = cursor.fetchall()

            return resultados

        finally:

            cursor.close()

            conexion.close()


    # =====================================================
    # BUSCAR UBICACIONES
    # =====================================================

    def buscar(
        self,
        texto
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
                id_ubicacion,
                nombre,
                descripcion,
                activo

            FROM ubicaciones

            WHERE
                nombre LIKE ?
                OR descripcion LIKE ?

            ORDER BY
                nombre ASC
            """

            parametro = (
                f"%{texto}%"
            )

            cursor.execute(
                sql,
                (
                    parametro,
                    parametro
                )
            )

            resultados = cursor.fetchall()

            return resultados

        finally:

            cursor.close()

            conexion.close()


    # =====================================================
    # CREAR UBICACIÓN
    # =====================================================

    def crear(
        self,
        nombre,
        descripcion
    ):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
            INSERT INTO ubicaciones (
                nombre,
                descripcion,
                activo
            )

            VALUES (
                ?,
                ?,
                1
            )
            """

            cursor.execute(
                sql,
                (
                    nombre,
                    descripcion
                )
            )

            conexion.commit()

        except Exception:

            conexion.rollback()

            raise

        finally:

            cursor.close()

            conexion.close()


    # =====================================================
    # ACTUALIZAR UBICACIÓN
    # =====================================================

    def actualizar(
        self,
        id_ubicacion,
        nombre,
        descripcion,
        activo
    ):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
            UPDATE ubicaciones

            SET
                nombre = ?,
                descripcion = ?,
                activo = ?

            WHERE
                id_ubicacion = ?
            """

            cursor.execute(
                sql,
                (
                    nombre,
                    descripcion,
                    activo,
                    id_ubicacion
                )
            )

            conexion.commit()

        except Exception:

            conexion.rollback()

            raise

        finally:

            cursor.close()

            conexion.close()


    # =====================================================
    # ELIMINAR UBICACIÓN
    # =====================================================

    def eliminar(
        self,
        id_ubicacion
    ):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
            DELETE FROM ubicaciones

            WHERE
                id_ubicacion = ?
            """

            cursor.execute(
                sql,
                (
                    id_ubicacion,
                )
            )

            conexion.commit()

        except Exception:

            conexion.rollback()

            raise

        finally:

            cursor.close()

            conexion.close()