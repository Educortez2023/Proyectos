from app.database.conexion import Conexion


class ReporteModel:

    # =====================================================
    # REPORTE GENERAL DE EQUIPOS
    # =====================================================

    @staticmethod
    def listar_equipos(
        codigo="",
        nombre="",
        numero_serie="",
        id_categoria=None,
        id_marca=None,
        id_modelo=None,
        id_proveedor=None,
        id_estado=None,
        id_responsable=None,
        id_ubicacion=None,
        activo=None
    ):

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return []

            cursor = conexion.cursor(dictionary=True)

            sql = """
                SELECT
                    e.id_equipo,
                    e.codigo,
                    e.nombre,
                    e.numero_serie,

                    e.id_categoria,
                    c.nombre AS categoria,

                    e.id_marca,
                    ma.nombre AS marca,

                    e.id_modelo,
                    mo.nombre AS modelo,

                    e.id_proveedor,
                    p.empresa AS proveedor,

                    e.id_estado,
                    es.nombre AS estado,

                    e.id_responsable,
                    CONCAT(
                        r.nombres,
                        ' ',
                        r.apellidos
                    ) AS responsable,

                    e.id_ubicacion,
                    u.nombre AS ubicacion,

                    e.fecha_compra,
                    e.garantia_meses,
                    e.precio,
                    e.observaciones,
                    e.activo,
                    e.fecha_creacion

                FROM equipos e

                INNER JOIN categorias c
                    ON e.id_categoria = c.id_categoria

                INNER JOIN marcas ma
                    ON e.id_marca = ma.id_marca

                LEFT JOIN modelos mo
                    ON e.id_modelo = mo.id_modelo

                LEFT JOIN proveedores p
                    ON e.id_proveedor = p.id_proveedor

                INNER JOIN estados es
                    ON e.id_estado = es.id_estado

                LEFT JOIN responsables r
                    ON e.id_responsable = r.id_responsable

                LEFT JOIN ubicaciones u
                    ON e.id_ubicacion = u.id_ubicacion

                WHERE 1 = 1
            """

            parametros = []

            # =================================================
            # FILTRO POR CÓDIGO
            # =================================================

            if codigo:

                sql += """
                    AND e.codigo LIKE ?
                """

                parametros.append(
                    f"%{codigo}%"
                )

            # =================================================
            # FILTRO POR NOMBRE
            # =================================================

            if nombre:

                sql += """
                    AND e.nombre LIKE ?
                """

                parametros.append(
                    f"%{nombre}%"
                )

            # =================================================
            # FILTRO POR NÚMERO DE SERIE
            # =================================================

            if numero_serie:

                sql += """
                    AND e.numero_serie LIKE ?
                """

                parametros.append(
                    f"%{numero_serie}%"
                )

            # =================================================
            # FILTRO POR CATEGORÍA
            # =================================================

            if id_categoria is not None:

                sql += """
                    AND e.id_categoria = ?
                """

                parametros.append(
                    id_categoria
                )

            # =================================================
            # FILTRO POR MARCA
            # =================================================

            if id_marca is not None:

                sql += """
                    AND e.id_marca = ?
                """

                parametros.append(
                    id_marca
                )

            # =================================================
            # FILTRO POR MODELO
            # =================================================

            if id_modelo is not None:

                sql += """
                    AND e.id_modelo = ?
                """

                parametros.append(
                    id_modelo
                )

            # =================================================
            # FILTRO POR PROVEEDOR
            # =================================================

            if id_proveedor is not None:

                sql += """
                    AND e.id_proveedor = ?
                """

                parametros.append(
                    id_proveedor
                )

            # =================================================
            # FILTRO POR ESTADO
            # =================================================

            if id_estado is not None:

                sql += """
                    AND e.id_estado = ?
                """

                parametros.append(
                    id_estado
                )

            # =================================================
            # FILTRO POR RESPONSABLE
            # =================================================

            if id_responsable is not None:

                sql += """
                    AND e.id_responsable = ?
                """

                parametros.append(
                    id_responsable
                )

            # =================================================
            # FILTRO POR UBICACIÓN
            # =================================================

            if id_ubicacion is not None:

                sql += """
                    AND e.id_ubicacion = ?
                """

                parametros.append(
                    id_ubicacion
                )

            # =================================================
            # FILTRO POR ESTADO ACTIVO
            # =================================================

            if activo is not None:

                sql += """
                    AND e.activo = ?
                """

                parametros.append(
                    activo
                )

            # =================================================
            # ORDEN
            # =================================================

            sql += """
                ORDER BY e.id_equipo ASC
            """

            cursor.execute(
                sql,
                tuple(parametros)
            )

            return cursor.fetchall()

        except Exception as e:

            print(
                f"Error al generar reporte de equipos: {e}"
            )

            return []

        finally:

            if cursor:

                cursor.close()

            if conexion:

                conexion.close()

    # =====================================================
    # LISTAR CATEGORÍAS
    # =====================================================

    @staticmethod
    def listar_categorias():

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return []

            cursor = conexion.cursor(
                dictionary=True
            )

            sql = """
                SELECT
                    id_categoria,
                    nombre
                FROM categorias
                WHERE activo = 1
                ORDER BY nombre ASC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Exception as e:

            print(
                f"Error al listar categorías: {e}"
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # LISTAR MARCAS
    # =====================================================

    @staticmethod
    def listar_marcas():

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return []

            cursor = conexion.cursor(
                dictionary=True
            )

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

            print(
                f"Error al listar marcas: {e}"
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

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
                return []

            cursor = conexion.cursor(
                dictionary=True
            )

            sql = """
                SELECT
                    mo.id_modelo,
                    mo.nombre,
                    mo.id_marca,
                    ma.nombre AS marca
                FROM modelos mo

                INNER JOIN marcas ma
                    ON mo.id_marca = ma.id_marca

                WHERE mo.activo = 1

                ORDER BY mo.nombre ASC
            """

            cursor.execute(sql)

            return cursor.fetchall()

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
    # LISTAR PROVEEDORES
    # =====================================================

    @staticmethod
    def listar_proveedores():

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return []

            cursor = conexion.cursor(
                dictionary=True
            )

            sql = """
                SELECT
                    id_proveedor,
                    empresa
                FROM proveedores
                WHERE activo = 1
                ORDER BY empresa ASC
            """

            cursor.execute(sql)

            return cursor.fetchall()

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
    # LISTAR ESTADOS
    # =====================================================

    @staticmethod
    def listar_estados():

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return []

            cursor = conexion.cursor(
                dictionary=True
            )

            sql = """
                SELECT
                    id_estado,
                    nombre
                FROM estados
                WHERE activo = 1
                ORDER BY nombre ASC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Exception as e:

            print(
                f"Error al listar estados: {e}"
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # LISTAR RESPONSABLES
    # =====================================================

    @staticmethod
    def listar_responsables():

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return []

            cursor = conexion.cursor(
                dictionary=True
            )

            sql = """
                SELECT
                    id_responsable,
                    nombres,
                    apellidos,
                    CONCAT(
                        nombres,
                        ' ',
                        apellidos
                    ) AS nombre_completo
                FROM responsables
                WHERE activo = 1
                ORDER BY nombres ASC, apellidos ASC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Exception as e:

            print(
                f"Error al listar responsables: {e}"
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    # =====================================================
    # LISTAR UBICACIONES
    # =====================================================

    @staticmethod
    def listar_ubicaciones():

        conexion = None
        cursor = None

        try:

            conexion = Conexion.obtener_conexion()

            if conexion is None:
                return []

            cursor = conexion.cursor(
                dictionary=True
            )

            sql = """
                SELECT
                    id_ubicacion,
                    nombre
                FROM ubicaciones
                WHERE activo = 1
                ORDER BY nombre ASC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Exception as e:

            print(
                f"Error al listar ubicaciones: {e}"
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if conexion:

                conexion.close()