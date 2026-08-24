from app.database.conexion import Conexion


class MarcaModel:

    # =====================================================
    # LISTAR MARCAS
    # =====================================================
    @staticmethod
    def listar_marcas():
        conexion = None
        cursor = None

        try:
            conexion = Conexion().conectar()
            cursor = conexion.cursor(dictionary=True)

            sql = """
                SELECT
                    id_marca,
                    nombre,
                    activo,
                    fecha_creacion
                FROM marcas
                ORDER BY nombre ASC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Exception as e:
            print(f"Error al listar marcas: {e}")
            return []

        finally:
            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # LISTAR SOLO MARCAS ACTIVAS
    # =====================================================
    @staticmethod
    def listar_marcas_activas():
        conexion = None
        cursor = None

        try:
            conexion = Conexion().conectar()
            cursor = conexion.cursor(dictionary=True)

            sql = """
                SELECT
                    id_marca,
                    nombre
                FROM marcas
                WHERE activo = 1
                ORDER BY nombre ASC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Exception as e:
            print(f"Error al listar marcas activas: {e}")
            return []

        finally:
            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # BUSCAR MARCAS
    # =====================================================
    @staticmethod
    def buscar_marcas(texto):
        conexion = None
        cursor = None

        try:
            conexion = Conexion().conectar()
            cursor = conexion.cursor(dictionary=True)

            sql = """
                SELECT
                    id_marca,
                    nombre,
                    activo,
                    fecha_creacion
                FROM marcas
                WHERE nombre LIKE ?
                ORDER BY nombre ASC
            """

            cursor.execute(
                sql,
                (f"%{texto}%",)
            )

            return cursor.fetchall()

        except Exception as e:
            print(f"Error al buscar marcas: {e}")
            return []

        finally:
            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # OBTENER MARCA POR ID
    # =====================================================
    @staticmethod
    def obtener_marca(id_marca):
        conexion = None
        cursor = None

        try:
            conexion = Conexion().conectar()
            cursor = conexion.cursor(dictionary=True)

            sql = """
                SELECT
                    id_marca,
                    nombre,
                    activo,
                    fecha_creacion
                FROM marcas
                WHERE id_marca = ?
            """

            cursor.execute(
                sql,
                (id_marca,)
            )

            return cursor.fetchone()

        except Exception as e:
            print(f"Error al obtener marca: {e}")
            return None

        finally:
            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # CREAR MARCA
    # =====================================================
    @staticmethod
    def crear_marca(nombre):
        conexion = None
        cursor = None

        try:
            conexion = Conexion().conectar()
            cursor = conexion.cursor()

            sql = """
                INSERT INTO marcas
                (
                    nombre,
                    activo
                )
                VALUES
                (
                    ?,
                    1
                )
            """

            cursor.execute(
                sql,
                (nombre.strip(),)
            )

            conexion.commit()

            return True

        except Exception as e:
            print(f"Error al crear marca: {e}")

            if conexion:
                conexion.rollback()

            return False

        finally:
            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # ACTUALIZAR MARCA
    # =====================================================
    @staticmethod
    def actualizar_marca(id_marca, nombre):
        conexion = None
        cursor = None

        try:
            conexion = Conexion().conectar()
            cursor = conexion.cursor()

            sql = """
                UPDATE marcas
                SET nombre = ?
                WHERE id_marca = ?
            """

            cursor.execute(
                sql,
                (
                    nombre.strip(),
                    id_marca
                )
            )

            conexion.commit()

            return True

        except Exception as e:
            print(f"Error al actualizar marca: {e}")

            if conexion:
                conexion.rollback()

            return False

        finally:
            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # DESACTIVAR MARCA
    # =====================================================
    @staticmethod
    def desactivar_marca(id_marca):
        conexion = None
        cursor = None

        try:
            conexion = Conexion().conectar()
            cursor = conexion.cursor()

            sql = """
                UPDATE marcas
                SET activo = 0
                WHERE id_marca = ?
            """

            cursor.execute(
                sql,
                (id_marca,)
            )

            conexion.commit()

            return True

        except Exception as e:
            print(f"Error al desactivar marca: {e}")

            if conexion:
                conexion.rollback()

            return False

        finally:
            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # ACTIVAR MARCA
    # =====================================================
    @staticmethod
    def activar_marca(id_marca):
        conexion = None
        cursor = None

        try:
            conexion = Conexion().conectar()
            cursor = conexion.cursor()

            sql = """
                UPDATE marcas
                SET activo = 1
                WHERE id_marca = ?
            """

            cursor.execute(
                sql,
                (id_marca,)
            )

            conexion.commit()

            return True

        except Exception as e:
            print(f"Error al activar marca: {e}")

            if conexion:
                conexion.rollback()

            return False

        finally:
            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # VERIFICAR SI EXISTE UNA MARCA
    # =====================================================
    @staticmethod
    def existe_nombre(nombre, id_marca=None):
        conexion = None
        cursor = None

        try:
            conexion = Conexion().conectar()
            cursor = conexion.cursor()

            if id_marca is None:

                sql = """
                    SELECT COUNT(*)
                    FROM marcas
                    WHERE nombre = ?
                """

                cursor.execute(
                    sql,
                    (nombre.strip(),)
                )

            else:

                sql = """
                    SELECT COUNT(*)
                    FROM marcas
                    WHERE nombre = ?
                    AND id_marca <> ?
                """

                cursor.execute(
                    sql,
                    (
                        nombre.strip(),
                        id_marca
                    )
                )

            resultado = cursor.fetchone()

            return resultado[0] > 0

        except Exception as e:
            print(
                f"Error al verificar nombre de marca: {e}"
            )

            return False

        finally:
            if cursor:
                cursor.close()

            if conexion:
                conexion.close()