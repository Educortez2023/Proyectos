import mariadb


class Conexion:

    def __init__(self):

        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "inventario_tecnologia"
        self.port = 3306

    # ==========================================
    # OBTENER CONEXIÓN
    # ==========================================

    @staticmethod
    def obtener_conexion():

        try:

            conexion = mariadb.connect(
                host="localhost",
                user="root",
                password="",
                database="inventario_tecnologia",
                port=3306
            )

            return conexion

        except mariadb.Error as e:

            print("Error al conectar con MariaDB:", e)

            return None

    # ==========================================
    # MÉTODO COMPATIBLE
    # ==========================================

    def conectar(self):

        return Conexion.obtener_conexion()

    # ==========================================
    # CERRAR CONEXIÓN
    # ==========================================

    def cerrar(self, conexion):

        if conexion:
            conexion.close()


# ==========================================
# FUNCIÓN GLOBAL
# ==========================================

def conectar():

    return Conexion.obtener_conexion()