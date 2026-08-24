from app.database.conexion import Conexion


class ResponsableModel:

    # =====================================================
    # LISTAR RESPONSABLES
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
                r.id_responsable,
                r.nombres,
                r.apellidos,
                r.cedula,
                r.correo,
                r.telefono,
                d.nombre AS departamento,
                c.nombre AS cargo,
                r.id_departamento,
                r.id_cargo,
                r.activo,
                r.fecha_creacion

            FROM responsables r

            INNER JOIN departamentos d
                ON r.id_departamento = d.id_departamento

            INNER JOIN cargos c
                ON r.id_cargo = c.id_cargo

            ORDER BY
                r.apellidos ASC,
                r.nombres ASC
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
    # BUSCAR RESPONSABLES
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
                r.id_responsable,
                r.nombres,
                r.apellidos,
                r.cedula,
                r.correo,
                r.telefono,
                d.nombre AS departamento,
                c.nombre AS cargo,
                r.id_departamento,
                r.id_cargo,
                r.activo,
                r.fecha_creacion

            FROM responsables r

            INNER JOIN departamentos d
                ON r.id_departamento = d.id_departamento

            INNER JOIN cargos c
                ON r.id_cargo = c.id_cargo

            WHERE
                r.nombres LIKE ?
                OR r.apellidos LIKE ?
                OR r.cedula LIKE ?
                OR r.correo LIKE ?
                OR r.telefono LIKE ?
                OR d.nombre LIKE ?
                OR c.nombre LIKE ?

            ORDER BY
                r.apellidos ASC,
                r.nombres ASC
            """

            parametro = f"%{texto}%"

            cursor.execute(
                sql,
                (
                    parametro,
                    parametro,
                    parametro,
                    parametro,
                    parametro,
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
    # OBTENER DEPARTAMENTOS
    # =====================================================

    def listar_departamentos(self):

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
                nombre

            FROM departamentos

            ORDER BY
                nombre ASC
            """

            cursor.execute(
                sql
            )

            return cursor.fetchall()

        finally:

            cursor.close()

            conexion.close()


    # =====================================================
    # OBTENER CARGOS
    # =====================================================

    def listar_cargos(self):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
            SELECT
                id_cargo,
                nombre

            FROM cargos

            ORDER BY
                nombre ASC
            """

            cursor.execute(
                sql
            )

            return cursor.fetchall()

        finally:

            cursor.close()

            conexion.close()


    # =====================================================
    # CREAR RESPONSABLE
    # =====================================================

    def crear(
        self,
        nombres,
        apellidos,
        cedula,
        correo,
        telefono,
        id_departamento,
        id_cargo
    ):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
            INSERT INTO responsables (
                nombres,
                apellidos,
                cedula,
                correo,
                telefono,
                id_departamento,
                id_cargo,
                activo
            )

            VALUES (
                ?,
                ?,
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
                    nombres,
                    apellidos,
                    cedula,
                    correo,
                    telefono,
                    id_departamento,
                    id_cargo
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
    # ACTUALIZAR RESPONSABLE
    # =====================================================

    def actualizar(
        self,
        id_responsable,
        nombres,
        apellidos,
        cedula,
        correo,
        telefono,
        id_departamento,
        id_cargo
    ):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
            UPDATE responsables

            SET
                nombres = ?,
                apellidos = ?,
                cedula = ?,
                correo = ?,
                telefono = ?,
                id_departamento = ?,
                id_cargo = ?

            WHERE
                id_responsable = ?
            """

            cursor.execute(
                sql,
                (
                    nombres,
                    apellidos,
                    cedula,
                    correo,
                    telefono,
                    id_departamento,
                    id_cargo,
                    id_responsable
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
    # ELIMINAR RESPONSABLE
    # =====================================================

    def eliminar(
        self,
        id_responsable
    ):

        conexion = Conexion.obtener_conexion()

        if conexion is None:
            raise Exception(
                "No se pudo conectar con la base de datos."
            )

        cursor = conexion.cursor()

        try:

            sql = """
            DELETE FROM responsables

            WHERE
                id_responsable = ?
            """

            cursor.execute(
                sql,
                (
                    id_responsable,
                )
            )

            conexion.commit()

        except Exception:

            conexion.rollback()

            raise

        finally:

            cursor.close()

            conexion.close()