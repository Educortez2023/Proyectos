from app.database.conexion import Conexion


class DepartamentoModel:

    # =====================================================
    # LISTAR DEPARTAMENTOS
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
                    id_departamento,
                    nombre,
                    descripcion,
                    activo,
                    fecha_creacion

                FROM departamentos

                ORDER BY
                    id_departamento
            """

            cursor.execute(sql)

            return cursor.fetchall()

        finally:

            cursor.close()
            conexion.close()

    # =====================================================
    # BUSCAR DEPARTAMENTOS
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
                    id_departamento,
                    nombre,
                    descripcion,
                    activo,
                    fecha_creacion

                FROM departamentos

                WHERE
                    nombre LIKE %s
                    OR descripcion LIKE %s

                ORDER BY
                    id_departamento
            """

            parametros = (
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
    # OBTENER DEPARTAMENTO
    # =====================================================

    def obtener(self, id_departamento):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
                SELECT
                    id_departamento,
                    nombre,
                    descripcion,
                    activo,
                    fecha_creacion

                FROM departamentos

                WHERE id_departamento = %s
            """

            cursor.execute(
                sql,
                (id_departamento,)
            )

            return cursor.fetchone()

        finally:

            cursor.close()
            conexion.close()

    # =====================================================
    # CREAR DEPARTAMENTO
    # =====================================================

    def crear(self, nombre, descripcion):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            # =================================================
            # VALIDAR NOMBRE
            # =================================================

            if nombre is None:
                raise Exception(
                    "El nombre del departamento es obligatorio."
                )

            nombre = str(nombre).strip()

            if not nombre:
                raise Exception(
                    "El nombre del departamento es obligatorio."
                )

            # =================================================
            # LIMPIAR DESCRIPCIÓN
            # =================================================

            if descripcion is not None:

                descripcion = str(
                    descripcion
                ).strip()

            else:

                descripcion = None

            # =================================================
            # VERIFICAR DUPLICADO
            # =================================================

            sql_verificar = """
                SELECT
                    id_departamento

                FROM departamentos

                WHERE nombre = %s

                LIMIT 1
            """

            cursor.execute(
                sql_verificar,
                (nombre,)
            )

            existe = cursor.fetchone()

            if existe is not None:

                raise Exception(
                    "Ya existe un departamento con "
                    f"el nombre '{nombre}'."
                )

            # =================================================
            # INSERTAR
            # =================================================

            sql = """
                INSERT INTO departamentos (
                    nombre,
                    descripcion,
                    activo
                )

                VALUES (
                    %s,
                    %s,
                    1
                )
            """

            valores = (
                nombre,
                descripcion
            )

            cursor.execute(
                sql,
                valores
            )

            # =================================================
            # CONFIRMAR
            # =================================================

            conexion.commit()

            return cursor.lastrowid

        except Exception:

            conexion.rollback()

            raise

        finally:

            cursor.close()
            conexion.close()

    # =====================================================
    # ACTUALIZAR DEPARTAMENTO
    # =====================================================

    def actualizar(
        self,
        id_departamento,
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

            # =================================================
            # VALIDAR NOMBRE
            # =================================================

            if nombre is None:
                raise Exception(
                    "El nombre del departamento es obligatorio."
                )

            nombre = str(nombre).strip()

            if not nombre:
                raise Exception(
                    "El nombre del departamento es obligatorio."
                )

            # =================================================
            # LIMPIAR DESCRIPCIÓN
            # =================================================

            if descripcion is not None:

                descripcion = str(
                    descripcion
                ).strip()

            else:

                descripcion = None

            # =================================================
            # VERIFICAR QUE EXISTA
            # =================================================

            sql_existe = """
                SELECT
                    id_departamento

                FROM departamentos

                WHERE id_departamento = %s
            """

            cursor.execute(
                sql_existe,
                (id_departamento,)
            )

            departamento = cursor.fetchone()

            if departamento is None:

                raise Exception(
                    "El departamento seleccionado "
                    "no existe."
                )

            # =================================================
            # VERIFICAR NOMBRE DUPLICADO
            # =================================================

            sql_verificar = """
                SELECT
                    id_departamento

                FROM departamentos

                WHERE
                    nombre = %s
                    AND id_departamento <> %s

                LIMIT 1
            """

            cursor.execute(
                sql_verificar,
                (
                    nombre,
                    id_departamento
                )
            )

            existe = cursor.fetchone()

            if existe is not None:

                raise Exception(
                    "Ya existe otro departamento "
                    f"con el nombre '{nombre}'."
                )

            # =================================================
            # ACTUALIZAR
            # =================================================

            sql = """
                UPDATE departamentos

                SET
                    nombre = %s,
                    descripcion = %s

                WHERE id_departamento = %s
            """

            valores = (
                nombre,
                descripcion,
                id_departamento
            )

            cursor.execute(
                sql,
                valores
            )

            # =================================================
            # CONFIRMAR
            # =================================================

            conexion.commit()

        except Exception:

            conexion.rollback()

            raise

        finally:

            cursor.close()
            conexion.close()

    # =====================================================
    # CAMBIAR ESTADO
    # =====================================================

    def cambiar_estado(
        self,
        id_departamento,
        nuevo_estado
    ):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            # =================================================
            # VALIDAR ESTADO
            # =================================================

            if nuevo_estado not in (0, 1):

                raise Exception(
                    "El estado indicado no es válido."
                )

            # =================================================
            # VERIFICAR QUE EXISTA
            # =================================================

            sql_existe = """
                SELECT
                    id_departamento

                FROM departamentos

                WHERE id_departamento = %s
            """

            cursor.execute(
                sql_existe,
                (id_departamento,)
            )

            departamento = cursor.fetchone()

            if departamento is None:

                raise Exception(
                    "El departamento seleccionado "
                    "no existe."
                )

            # =================================================
            # ACTUALIZAR ESTADO
            # =================================================

            sql = """
                UPDATE departamentos

                SET
                    activo = %s

                WHERE id_departamento = %s
            """

            cursor.execute(
                sql,
                (
                    nuevo_estado,
                    id_departamento
                )
            )

            # =================================================
            # CONFIRMAR
            # =================================================

            conexion.commit()

        except Exception:

            conexion.rollback()

            raise

        finally:

            cursor.close()
            conexion.close()

    # =====================================================
    # ELIMINAR DEPARTAMENTO
    # =====================================================

    def eliminar(self, id_departamento):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            # =================================================
            # VERIFICAR QUE EXISTA
            # =================================================

            sql_existe = """
                SELECT
                    id_departamento

                FROM departamentos

                WHERE id_departamento = %s
            """

            cursor.execute(
                sql_existe,
                (id_departamento,)
            )

            departamento = cursor.fetchone()

            if departamento is None:

                raise Exception(
                    "El departamento seleccionado "
                    "no existe."
                )

            # =================================================
            # ELIMINAR
            # =================================================

            sql = """
                DELETE FROM departamentos

                WHERE id_departamento = %s
            """

            cursor.execute(
                sql,
                (id_departamento,)
            )

            # =================================================
            # CONFIRMAR
            # =================================================

            conexion.commit()

        except Exception as e:

            conexion.rollback()

            # =================================================
            # ERROR DE CLAVE FORÁNEA
            # =================================================

            mensaje = str(e)

            if "1451" in mensaje:

                raise Exception(
                    "No se puede eliminar este departamento "
                    "porque está siendo utilizado por otros "
                    "registros del sistema.\n\n"
                    "Puede utilizar la opción "
                    "'Activar / Desactivar' en su lugar."
                )

            raise

        finally:

            cursor.close()
            conexion.close()