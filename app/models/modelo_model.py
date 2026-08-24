from app.database.conexion import Conexion


class ModeloModel:

    # =====================================================
    # LISTAR MODELOS
    # =====================================================

    @staticmethod
    def listar_modelos():

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                print("No se pudo obtener la conexión a la base de datos.")
                return []

            cursor = conexion.cursor(dictionary=True)

            sql = """
                SELECT
                    mo.id_modelo,
                    mo.nombre,
                    mo.id_marca,
                    ma.nombre AS marca,
                    mo.activo,
                    mo.fecha_creacion
                FROM modelos mo
                INNER JOIN marcas ma
                    ON mo.id_marca = ma.id_marca
                ORDER BY mo.id_modelo ASC
            """

            cursor.execute(sql)

            modelos = cursor.fetchall()

            print(
                f"Modelos cargados: {len(modelos)}"
            )

            return modelos

        except Exception as e:

            print(
                f"Error al listar modelos: {e}"
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # BUSCAR MODELOS
    # =====================================================

    @staticmethod
    def buscar_modelos(texto):

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                print("No se pudo obtener la conexión a la base de datos.")
                return []

            cursor = conexion.cursor(dictionary=True)

            sql = """
                SELECT
                    mo.id_modelo,
                    mo.nombre,
                    mo.id_marca,
                    ma.nombre AS marca,
                    mo.activo,
                    mo.fecha_creacion
                FROM modelos mo
                INNER JOIN marcas ma
                    ON mo.id_marca = ma.id_marca
                WHERE
                    mo.nombre LIKE ?
                    OR ma.nombre LIKE ?
                ORDER BY mo.id_modelo ASC
            """

            parametro = f"%{texto}%"

            cursor.execute(
                sql,
                (
                    parametro,
                    parametro
                )
            )

            return cursor.fetchall()

        except Exception as e:

            print(
                f"Error al buscar modelos: {e}"
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # CREAR MODELO
    # =====================================================

    @staticmethod
    def crear_modelo(nombre, id_marca):

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                print("No se pudo obtener la conexión a la base de datos.")
                return False

            cursor = conexion.cursor()

            sql = """
                INSERT INTO modelos
                (
                    nombre,
                    id_marca,
                    activo
                )
                VALUES
                (
                    ?,
                    ?,
                    1
                )
            """

            cursor.execute(
                sql,
                (
                    nombre,
                    id_marca
                )
            )

            conexion.commit()

            print(
                f"Modelo creado correctamente: {nombre}"
            )

            return True

        except Exception as e:

            print(
                f"Error al crear modelo: {e}"
            )

            if conexion:
                conexion.rollback()

            return False

        finally:

            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # ACTUALIZAR MODELO
    # =====================================================

    @staticmethod
    def actualizar_modelo(
        id_modelo,
        nombre,
        id_marca
    ):

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                print("No se pudo obtener la conexión a la base de datos.")
                return False

            cursor = conexion.cursor()

            sql = """
                UPDATE modelos
                SET
                    nombre = ?,
                    id_marca = ?
                WHERE
                    id_modelo = ?
            """

            cursor.execute(
                sql,
                (
                    nombre,
                    id_marca,
                    id_modelo
                )
            )

            conexion.commit()

            print(
                f"Modelo actualizado correctamente: {id_modelo}"
            )

            return True

        except Exception as e:

            print(
                f"Error al actualizar modelo: {e}"
            )

            if conexion:
                conexion.rollback()

            return False

        finally:

            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # DESACTIVAR MODELO
    # =====================================================

    @staticmethod
    def desactivar_modelo(id_modelo):

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                print("No se pudo obtener la conexión a la base de datos.")
                return False

            cursor = conexion.cursor()

            sql = """
                UPDATE modelos
                SET
                    activo = 0
                WHERE
                    id_modelo = ?
            """

            cursor.execute(
                sql,
                (
                    id_modelo,
                )
            )

            conexion.commit()

            print(
                f"Modelo desactivado correctamente: {id_modelo}"
            )

            return True

        except Exception as e:

            print(
                f"Error al desactivar modelo: {e}"
            )

            if conexion:
                conexion.rollback()

            return False

        finally:

            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # ACTIVAR MODELO
    # =====================================================

    @staticmethod
    def activar_modelo(id_modelo):

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                print("No se pudo obtener la conexión a la base de datos.")
                return False

            cursor = conexion.cursor()

            sql = """
                UPDATE modelos
                SET
                    activo = 1
                WHERE
                    id_modelo = ?
            """

            cursor.execute(
                sql,
                (
                    id_modelo,
                )
            )

            conexion.commit()

            print(
                f"Modelo activado correctamente: {id_modelo}"
            )

            return True

        except Exception as e:

            print(
                f"Error al activar modelo: {e}"
            )

            if conexion:
                conexion.rollback()

            return False

        finally:

            if cursor:
                cursor.close()

            if conexion:
                conexion.close()