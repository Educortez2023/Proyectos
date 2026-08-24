from app.database.conexion import Conexion


class ProveedorModel:

    # =====================================================
    # LISTAR PROVEEDORES
    # =====================================================

    @staticmethod
    def listar_proveedores():

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                print(
                    "No se pudo obtener la conexión a la base de datos."
                )
                return []

            cursor = conexion.cursor(dictionary=True)

            sql = """
                SELECT
                    id_proveedor,
                    empresa,
                    contacto,
                    telefono,
                    correo,
                    direccion,
                    activo,
                    fecha_creacion
                FROM proveedores
                ORDER BY id_proveedor ASC
            """

            cursor.execute(sql)

            proveedores = cursor.fetchall()

            print(
                f"Proveedores cargados: {len(proveedores)}"
            )

            return proveedores

        except Exception as e:

            print(
                f"Error al listar proveedores: {e}"
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # BUSCAR PROVEEDORES
    # =====================================================

    @staticmethod
    def buscar_proveedores(texto):

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                print(
                    "No se pudo obtener la conexión a la base de datos."
                )
                return []

            cursor = conexion.cursor(dictionary=True)

            sql = """
                SELECT
                    id_proveedor,
                    empresa,
                    contacto,
                    telefono,
                    correo,
                    direccion,
                    activo,
                    fecha_creacion
                FROM proveedores
                WHERE
                    empresa LIKE ?
                    OR contacto LIKE ?
                    OR telefono LIKE ?
                    OR correo LIKE ?
                ORDER BY id_proveedor ASC
            """

            parametro = f"%{texto}%"

            cursor.execute(
                sql,
                (
                    parametro,
                    parametro,
                    parametro,
                    parametro
                )
            )

            return cursor.fetchall()

        except Exception as e:

            print(
                f"Error al buscar proveedores: {e}"
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # CREAR PROVEEDOR
    # =====================================================

    @staticmethod
    def crear_proveedor(
        empresa,
        contacto,
        telefono,
        correo,
        direccion
    ):

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                print(
                    "No se pudo obtener la conexión a la base de datos."
                )
                return False

            cursor = conexion.cursor()

            sql = """
                INSERT INTO proveedores
                (
                    empresa,
                    contacto,
                    telefono,
                    correo,
                    direccion,
                    activo
                )
                VALUES
                (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    1
                )
            """

            cursor.execute(
                sql,
                (
                    empresa,
                    contacto,
                    telefono,
                    correo,
                    direccion
                )
            )

            conexion.commit()

            print(
                f"Proveedor creado correctamente: {empresa}"
            )

            return True

        except Exception as e:

            print(
                f"Error al crear proveedor: {e}"
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
    # ACTUALIZAR PROVEEDOR
    # =====================================================

    @staticmethod
    def actualizar_proveedor(
        id_proveedor,
        empresa,
        contacto,
        telefono,
        correo,
        direccion
    ):

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                print(
                    "No se pudo obtener la conexión a la base de datos."
                )
                return False

            cursor = conexion.cursor()

            sql = """
                UPDATE proveedores
                SET
                    empresa = ?,
                    contacto = ?,
                    telefono = ?,
                    correo = ?,
                    direccion = ?
                WHERE
                    id_proveedor = ?
            """

            cursor.execute(
                sql,
                (
                    empresa,
                    contacto,
                    telefono,
                    correo,
                    direccion,
                    id_proveedor
                )
            )

            conexion.commit()

            print(
                f"Proveedor actualizado correctamente: {id_proveedor}"
            )

            return True

        except Exception as e:

            print(
                f"Error al actualizar proveedor: {e}"
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
    # DESACTIVAR PROVEEDOR
    # =====================================================

    @staticmethod
    def desactivar_proveedor(id_proveedor):

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                print(
                    "No se pudo obtener la conexión a la base de datos."
                )
                return False

            cursor = conexion.cursor()

            sql = """
                UPDATE proveedores
                SET
                    activo = 0
                WHERE
                    id_proveedor = ?
            """

            cursor.execute(
                sql,
                (
                    id_proveedor,
                )
            )

            conexion.commit()

            print(
                f"Proveedor desactivado correctamente: {id_proveedor}"
            )

            return True

        except Exception as e:

            print(
                f"Error al desactivar proveedor: {e}"
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
    # ACTIVAR PROVEEDOR
    # =====================================================

    @staticmethod
    def activar_proveedor(id_proveedor):

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                print(
                    "No se pudo obtener la conexión a la base de datos."
                )
                return False

            cursor = conexion.cursor()

            sql = """
                UPDATE proveedores
                SET
                    activo = 1
                WHERE
                    id_proveedor = ?
            """

            cursor.execute(
                sql,
                (
                    id_proveedor,
                )
            )

            conexion.commit()

            print(
                f"Proveedor activado correctamente: {id_proveedor}"
            )

            return True

        except Exception as e:

            print(
                f"Error al activar proveedor: {e}"
            )

            if conexion:
                conexion.rollback()

            return False

        finally:

            if cursor:
                cursor.close()

            if conexion:
                conexion.close()