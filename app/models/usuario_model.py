from app.database.conexion import Conexion


class UsuarioModel:

    # =====================================================
    # LISTAR USUARIOS
    # =====================================================

    @staticmethod
    def listar_usuarios():

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return []

            cursor = conexion.cursor(dictionary=True)

            sql = """
                SELECT
                    u.id_usuario,
                    u.nombres,
                    u.apellidos,
                    u.usuario,
                    u.correo,
                    u.id_rol,
                    r.nombre AS rol,
                    u.activo,
                    u.fecha_creacion
                FROM usuarios u
                INNER JOIN roles r
                    ON u.id_rol = r.id_rol
                ORDER BY u.id_usuario ASC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Exception as e:

            print(
                f"Error al listar usuarios: {e}"
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # BUSCAR USUARIOS
    # =====================================================

    @staticmethod
    def buscar_usuarios(texto):

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return []

            cursor = conexion.cursor(dictionary=True)

            sql = """
                SELECT
                    u.id_usuario,
                    u.nombres,
                    u.apellidos,
                    u.usuario,
                    u.correo,
                    u.id_rol,
                    r.nombre AS rol,
                    u.activo,
                    u.fecha_creacion
                FROM usuarios u
                INNER JOIN roles r
                    ON u.id_rol = r.id_rol
                WHERE
                    u.nombres LIKE ?
                    OR u.apellidos LIKE ?
                    OR u.usuario LIKE ?
                    OR u.correo LIKE ?
                    OR r.nombre LIKE ?
                ORDER BY u.id_usuario ASC
            """

            parametro = f"%{texto}%"

            cursor.execute(
                sql,
                (
                    parametro,
                    parametro,
                    parametro,
                    parametro,
                    parametro
                )
            )

            return cursor.fetchall()

        except Exception as e:

            print(
                f"Error al buscar usuarios: {e}"
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # LISTAR ROLES ACTIVOS
    # =====================================================

    @staticmethod
    def listar_roles():

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return []

            cursor = conexion.cursor(dictionary=True)

            sql = """
                SELECT
                    id_rol,
                    nombre,
                    descripcion
                FROM roles
                WHERE activo = 1
                ORDER BY nombre ASC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Exception as e:

            print(
                f"Error al listar roles: {e}"
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # CREAR USUARIO
    # =====================================================

    @staticmethod
    def crear_usuario(
        nombres,
        apellidos,
        usuario,
        clave,
        correo,
        id_rol
    ):

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return False

            cursor = conexion.cursor()

            sql = """
                INSERT INTO usuarios (
                    nombres,
                    apellidos,
                    usuario,
                    clave,
                    correo,
                    id_rol,
                    activo
                )
                VALUES (?, ?, ?, ?, ?, ?, 1)
            """

            cursor.execute(
                sql,
                (
                    nombres,
                    apellidos,
                    usuario,
                    clave,
                    correo if correo else None,
                    id_rol
                )
            )

            conexion.commit()

            print(
                f"Usuario '{usuario}' creado correctamente."
            )

            return True

        except Exception as e:

            print(
                f"Error al crear usuario: {e}"
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
    # ACTUALIZAR USUARIO
    # =====================================================

    @staticmethod
    def actualizar_usuario(
        id_usuario,
        nombres,
        apellidos,
        usuario,
        clave,
        correo,
        id_rol
    ):

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return False

            cursor = conexion.cursor()

            # -------------------------------------------------
            # Si se escribió una nueva clave
            # -------------------------------------------------

            if clave:

                sql = """
                    UPDATE usuarios
                    SET
                        nombres = ?,
                        apellidos = ?,
                        usuario = ?,
                        clave = ?,
                        correo = ?,
                        id_rol = ?
                    WHERE id_usuario = ?
                """

                parametros = (
                    nombres,
                    apellidos,
                    usuario,
                    clave,
                    correo if correo else None,
                    id_rol,
                    id_usuario
                )

            # -------------------------------------------------
            # Si la clave está vacía,
            # conservar la clave actual
            # -------------------------------------------------

            else:

                sql = """
                    UPDATE usuarios
                    SET
                        nombres = ?,
                        apellidos = ?,
                        usuario = ?,
                        correo = ?,
                        id_rol = ?
                    WHERE id_usuario = ?
                """

                parametros = (
                    nombres,
                    apellidos,
                    usuario,
                    correo if correo else None,
                    id_rol,
                    id_usuario
                )

            cursor.execute(
                sql,
                parametros
            )

            conexion.commit()

            print(
                f"Usuario {id_usuario} actualizado correctamente."
            )

            return True

        except Exception as e:

            print(
                f"Error al actualizar usuario: {e}"
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
    # DESACTIVAR USUARIO
    # =====================================================

    @staticmethod
    def desactivar_usuario(id_usuario):

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:

                print(
                    "Error: no se pudo obtener conexión con la base de datos."
                )

                return False

            cursor = conexion.cursor()

            # -------------------------------------------------
            # Verificar que el usuario exista
            # -------------------------------------------------

            sql_verificar = """
                SELECT
                    id_usuario,
                    activo
                FROM usuarios
                WHERE id_usuario = ?
            """

            cursor.execute(
                sql_verificar,
                (id_usuario,)
            )

            usuario = cursor.fetchone()

            if not usuario:

                print(
                    f"No existe el usuario con ID: {id_usuario}"
                )

                return False

            # -------------------------------------------------
            # Desactivar usuario
            # -------------------------------------------------

            sql = """
                UPDATE usuarios
                SET activo = 0
                WHERE id_usuario = ?
            """

            cursor.execute(
                sql,
                (id_usuario,)
            )

            conexion.commit()

            # -------------------------------------------------
            # Verificar resultado
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT activo
                FROM usuarios
                WHERE id_usuario = ?
                """,
                (id_usuario,)
            )

            resultado = cursor.fetchone()

            if resultado and int(resultado[0]) == 0:

                print(
                    f"Usuario {id_usuario} desactivado correctamente."
                )

                return True

            print(
                f"No se pudo verificar la desactivación "
                f"del usuario {id_usuario}."
            )

            return False

        except Exception as e:

            print(
                f"ERROR REAL AL DESACTIVAR USUARIO: {e}"
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
    # ACTIVAR USUARIO
    # =====================================================

    @staticmethod
    def activar_usuario(id_usuario):

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:

                print(
                    "Error: no se pudo obtener conexión con la base de datos."
                )

                return False

            cursor = conexion.cursor()

            # -------------------------------------------------
            # Verificar que el usuario exista
            # -------------------------------------------------

            sql_verificar = """
                SELECT
                    id_usuario,
                    activo
                FROM usuarios
                WHERE id_usuario = ?
            """

            cursor.execute(
                sql_verificar,
                (id_usuario,)
            )

            usuario = cursor.fetchone()

            if not usuario:

                print(
                    f"No existe el usuario con ID: {id_usuario}"
                )

                return False

            # -------------------------------------------------
            # Activar usuario
            # -------------------------------------------------

            sql = """
                UPDATE usuarios
                SET activo = 1
                WHERE id_usuario = ?
            """

            cursor.execute(
                sql,
                (id_usuario,)
            )

            conexion.commit()

            # -------------------------------------------------
            # Verificar resultado
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT activo
                FROM usuarios
                WHERE id_usuario = ?
                """,
                (id_usuario,)
            )

            resultado = cursor.fetchone()

            if resultado and int(resultado[0]) == 1:

                print(
                    f"Usuario {id_usuario} activado correctamente."
                )

                return True

            print(
                f"No se pudo verificar la activación "
                f"del usuario {id_usuario}."
            )

            return False

        except Exception as e:

            print(
                f"ERROR REAL AL ACTIVAR USUARIO: {e}"
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
    # VALIDAR LOGIN
    # =====================================================

    @staticmethod
    def validar_usuario(usuario, clave):

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return None

            cursor = conexion.cursor(dictionary=True)

            sql = """
                SELECT
                    u.id_usuario,
                    u.nombres,
                    u.apellidos,
                    u.usuario,
                    u.correo,
                    u.id_rol,
                    r.nombre AS rol,
                    u.activo
                FROM usuarios u
                INNER JOIN roles r
                    ON u.id_rol = r.id_rol
                WHERE
                    u.usuario = ?
                    AND u.clave = ?
                    AND u.activo = 1
                    AND r.activo = 1
                LIMIT 1
            """

            cursor.execute(
                sql,
                (
                    usuario,
                    clave
                )
            )

            resultado = cursor.fetchone()

            return resultado

        except Exception as e:

            print(
                f"Error al validar usuario: {e}"
            )

            return None

        finally:

            if cursor:
                cursor.close()

            if conexion:
                conexion.close()