import customtkinter as ctk
from tkinter import messagebox
from datetime import date

from app.models.prestamo_model import PrestamoModel
from app.database.conexion import Conexion


class FormularioPrestamo(ctk.CTkToplevel):

    def __init__(self, parent, prestamo=None, callback=None):

        super().__init__(parent)

        # =====================================================
        # CONFIGURACIÓN DE LA VENTANA
        # =====================================================

        self.parent = parent
        self.prestamo = prestamo
        self.callback = callback

        self.title(
            "Editar Préstamo"
            if prestamo
            else "Nuevo Préstamo"
        )

        self.geometry("600x650")
        self.minsize(550, 600)

        self.transient(parent)

        # =====================================================
        # MODELO
        # =====================================================

        self.model = PrestamoModel()

        # =====================================================
        # LISTAS INTERNAS
        # =====================================================

        self.equipos = []
        self.responsables = []

        # Diccionarios para relacionar lo que muestra
        # el ComboBox con los IDs reales de la base de datos.
        self.equipos_por_texto = {}
        self.responsables_por_texto = {}

        # =====================================================
        # CREAR INTERFAZ
        # =====================================================

        self.crear_interfaz()

        # =====================================================
        # CARGAR INFORMACIÓN
        # =====================================================

        self.cargar_equipos()
        self.cargar_responsables()

        # =====================================================
        # CARGAR DATOS SI ES EDICIÓN
        # =====================================================

        if self.prestamo:

            self.cargar_datos()

        else:

            # =================================================
            # NUEVO PRÉSTAMO
            # =================================================

            # Fecha actual como valor inicial
            self.entry_fecha_prestamo.delete(
                0,
                "end"
            )

            self.entry_fecha_prestamo.insert(
                0,
                str(date.today())
            )

            # Fecha de devolución vacía
            self.entry_fecha_devolucion.delete(
                0,
                "end"
            )

            # Equipo vacío
            self.combo_equipo.set("")

            # Responsable vacío
            self.combo_responsable.set("")

            # Estado vacío
            self.combo_estado.set("")

            # Observaciones vacías
            self.text_observaciones.delete(
                "1.0",
                "end"
            )

        # =====================================================
        # MOSTRAR DELANTE
        # =====================================================

        self.after(
            100,
            self.mostrar_delante
        )

    # =========================================================
    # MOSTRAR VENTANA DELANTE
    # =========================================================

    def mostrar_delante(self):

        try:

            self.lift()
            self.focus_force()

        except Exception:

            pass

    # =========================================================
    # CREAR INTERFAZ
    # =========================================================

    def crear_interfaz(self):

        titulo = ctk.CTkLabel(
            self,
            text=(
                "Editar Préstamo"
                if self.prestamo
                else "Nuevo Préstamo"
            ),
            font=(
                "Arial",
                24,
                "bold"
            )
        )

        titulo.pack(
            pady=(25, 20)
        )

        # =====================================================
        # EQUIPO
        # =====================================================

        ctk.CTkLabel(
            self,
            text="Equipo:"
        ).pack(
            anchor="w",
            padx=40
        )

        self.combo_equipo = ctk.CTkComboBox(
            self,
            width=500,
            values=[""]
        )

        self.combo_equipo.pack(
            padx=40,
            pady=(5, 15)
        )

        # =====================================================
        # RESPONSABLE
        # =====================================================

        ctk.CTkLabel(
            self,
            text="Responsable:"
        ).pack(
            anchor="w",
            padx=40
        )

        self.combo_responsable = ctk.CTkComboBox(
            self,
            width=500,
            values=[""]
        )

        self.combo_responsable.pack(
            padx=40,
            pady=(5, 15)
        )

        # =====================================================
        # FECHA DE PRÉSTAMO
        # =====================================================

        ctk.CTkLabel(
            self,
            text="Fecha de préstamo:"
        ).pack(
            anchor="w",
            padx=40
        )

        self.entry_fecha_prestamo = ctk.CTkEntry(
            self,
            width=500,
            placeholder_text="AAAA-MM-DD"
        )

        self.entry_fecha_prestamo.pack(
            padx=40,
            pady=(5, 15)
        )

        # Fecha actual como valor inicial
        self.entry_fecha_prestamo.insert(
            0,
            str(date.today())
        )

        # =====================================================
        # FECHA DE DEVOLUCIÓN
        # =====================================================

        ctk.CTkLabel(
            self,
            text="Fecha de devolución:"
        ).pack(
            anchor="w",
            padx=40
        )

        self.entry_fecha_devolucion = ctk.CTkEntry(
            self,
            width=500,
            placeholder_text="AAAA-MM-DD"
        )

        self.entry_fecha_devolucion.pack(
            padx=40,
            pady=(5, 15)
        )

        # No colocamos fecha para nuevos préstamos.

        # =====================================================
        # ESTADO
        # =====================================================

        ctk.CTkLabel(
            self,
            text="Estado:"
        ).pack(
            anchor="w",
            padx=40
        )

        self.combo_estado = ctk.CTkComboBox(
            self,
            width=500,
            values=[
                "PENDIENTE",
                "ENTREGADO",
                "DEVUELTO"
            ]
        )

        self.combo_estado.pack(
            padx=40,
            pady=(5, 15)
        )

        # IMPORTANTE:
        # No seleccionamos ningún estado automáticamente.
        self.combo_estado.set("")

        # =====================================================
        # OBSERVACIONES
        # =====================================================

        ctk.CTkLabel(
            self,
            text="Observaciones:"
        ).pack(
            anchor="w",
            padx=40
        )

        self.text_observaciones = ctk.CTkTextbox(
            self,
            width=500,
            height=80
        )

        self.text_observaciones.pack(
            padx=40,
            pady=(5, 20)
        )

        # =====================================================
        # FRAME BOTONES
        # =====================================================

        frame_botones = ctk.CTkFrame(
            self
        )

        frame_botones.pack(
            fill="x",
            padx=40,
            pady=10
        )

        # =====================================================
        # GUARDAR
        # =====================================================

        btn_guardar = ctk.CTkButton(
            frame_botones,
            text="💾 Guardar",
            width=150,
            command=self.guardar
        )

        btn_guardar.pack(
            side="left",
            padx=10,
            pady=10
        )

        # =====================================================
        # CANCELAR
        # =====================================================

        btn_cancelar = ctk.CTkButton(
            frame_botones,
            text="❌ Cancelar",
            width=150,
            command=self.cerrar
        )

        btn_cancelar.pack(
            side="right",
            padx=10,
            pady=10
        )

    # =========================================================
    # CARGAR EQUIPOS
    # =========================================================

    def cargar_equipos(self):

        conexion = Conexion.obtener_conexion()

        if conexion is None:

            messagebox.showerror(
                "Error",
                "No se pudo conectar con la base de datos.",
                parent=self
            )

            return

        cursor = conexion.cursor()

        try:

            id_prestamo_actual = None

            if self.prestamo:

                try:

                    id_prestamo_actual = int(
                        self.prestamo[0]
                    )

                except Exception:

                    id_prestamo_actual = None

            # =================================================
            # NUEVO PRÉSTAMO
            # =================================================

            if id_prestamo_actual is None:

                sql = """
                    SELECT
                        e.id_equipo,
                        e.codigo,
                        e.nombre

                    FROM equipos e

                    WHERE e.activo = 1

                    AND NOT EXISTS (

                        SELECT 1

                        FROM prestamos p

                        WHERE p.id_equipo = e.id_equipo

                        AND p.estado IN (
                            'PENDIENTE',
                            'ENTREGADO'
                        )
                    )

                    ORDER BY e.nombre
                """

                cursor.execute(
                    sql
                )

            # =================================================
            # EDITAR PRÉSTAMO
            # =================================================

            else:

                sql = """
                    SELECT
                        e.id_equipo,
                        e.codigo,
                        e.nombre

                    FROM equipos e

                    WHERE e.activo = 1

                    AND (

                        e.id_equipo = (

                            SELECT
                                id_equipo

                            FROM prestamos

                            WHERE id_prestamo = %s
                        )

                        OR NOT EXISTS (

                            SELECT 1

                            FROM prestamos p

                            WHERE p.id_equipo = e.id_equipo

                            AND p.estado IN (
                                'PENDIENTE',
                                'ENTREGADO'
                            )

                            AND p.id_prestamo <> %s
                        )
                    )

                    ORDER BY e.nombre
                """

                cursor.execute(
                    sql,
                    (
                        id_prestamo_actual,
                        id_prestamo_actual
                    )
                )

            self.equipos = cursor.fetchall()

            valores = []

            self.equipos_por_texto = {}

            # =================================================
            # CREAR VALORES DEL COMBO
            # =================================================

            for equipo in self.equipos:

                id_equipo = equipo[0]
                codigo = equipo[1]
                nombre = equipo[2]

                texto = (
                    f"{codigo} | {nombre}"
                )

                valores.append(
                    texto
                )

                self.equipos_por_texto[
                    texto
                ] = id_equipo

            # =================================================
            # EQUIPOS DISPONIBLES
            # =================================================

            if valores:

                self.combo_equipo.configure(
                    values=valores
                )

                # =================================================
                # IMPORTANTE
                # =================================================
                # Para NUEVO préstamo dejamos el ComboBox vacío.
                # Para EDITAR, cargar_datos() seleccionará
                # posteriormente el equipo correspondiente.
                # =================================================

                if not self.prestamo:

                    self.combo_equipo.set("")

            # =================================================
            # NO HAY EQUIPOS
            # =================================================

            else:

                mensaje = (
                    "No hay equipos disponibles"
                )

                self.combo_equipo.configure(
                    values=[
                        mensaje
                    ]
                )

                self.combo_equipo.set(
                    ""
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                (
                    "No se pudieron cargar "
                    f"los equipos:\n\n{e}"
                ),
                parent=self
            )

        finally:

            cursor.close()
            conexion.close()

    # =========================================================
    # CARGAR RESPONSABLES
    # =========================================================

    def cargar_responsables(self):

        conexion = Conexion.obtener_conexion()

        if conexion is None:

            messagebox.showerror(
                "Error",
                "No se pudo conectar con la base de datos.",
                parent=self
            )

            return

        cursor = conexion.cursor()

        try:

            sql = """
                SELECT
                    id_responsable,
                    nombres,
                    apellidos

                FROM responsables

                ORDER BY
                    nombres,
                    apellidos
            """

            cursor.execute(
                sql
            )

            self.responsables = cursor.fetchall()

            valores = []

            self.responsables_por_texto = {}

            # =================================================
            # CREAR VALORES
            # =================================================

            for responsable in self.responsables:

                id_responsable = responsable[0]
                nombres = responsable[1] or ""
                apellidos = responsable[2] or ""

                texto = (
                    f"{nombres} {apellidos}"
                ).strip()

                valores.append(
                    texto
                )

                self.responsables_por_texto[
                    texto
                ] = id_responsable

            # =================================================
            # RESPONSABLES DISPONIBLES
            # =================================================

            if valores:

                self.combo_responsable.configure(
                    values=valores
                )

                # =================================================
                # IMPORTANTE
                # =================================================
                # Para NUEVO préstamo dejamos vacío.
                # Para EDITAR, cargar_datos() seleccionará
                # posteriormente el responsable correspondiente.
                # =================================================

                if not self.prestamo:

                    self.combo_responsable.set("")

            # =================================================
            # NO HAY RESPONSABLES
            # =================================================

            else:

                mensaje = (
                    "No hay responsables disponibles"
                )

                self.combo_responsable.configure(
                    values=[
                        mensaje
                    ]
                )

                self.combo_responsable.set(
                    ""
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                (
                    "No se pudieron cargar "
                    f"los responsables:\n\n{e}"
                ),
                parent=self
            )

        finally:

            cursor.close()
            conexion.close()

    # =========================================================
    # CARGAR DATOS DEL PRÉSTAMO PARA EDITAR
    # =========================================================

    def cargar_datos(self):

        conexion = Conexion.obtener_conexion()

        if conexion is None:

            return

        cursor = conexion.cursor()

        try:

            id_prestamo = int(
                self.prestamo[0]
            )

            # =================================================
            # OBTENER REGISTRO REAL DE LA BASE
            # =================================================

            sql = """
                SELECT
                    p.id_prestamo,
                    p.id_equipo,
                    p.id_responsable,
                    p.fecha_prestamo,
                    p.fecha_devolucion,
                    p.estado,
                    p.observaciones,
                    e.codigo,
                    e.nombre,
                    r.nombres,
                    r.apellidos

                FROM prestamos p

                INNER JOIN equipos e
                    ON e.id_equipo = p.id_equipo

                INNER JOIN responsables r
                    ON r.id_responsable = p.id_responsable

                WHERE p.id_prestamo = %s
            """

            cursor.execute(
                sql,
                (
                    id_prestamo,
                )
            )

            registro = cursor.fetchone()

            if not registro:

                messagebox.showerror(
                    "Error",
                    "No se encontró el préstamo seleccionado.",
                    parent=self
                )

                return

            # =================================================
            # DATOS OBTENIDOS
            # =================================================

            id_equipo = registro[1]
            id_responsable = registro[2]

            fecha_prestamo = registro[3]
            fecha_devolucion = registro[4]

            estado = registro[5]
            observaciones = registro[6]

            codigo_equipo = registro[7]
            nombre_equipo = registro[8]

            nombres = registro[9] or ""
            apellidos = registro[10] or ""

            # =================================================
            # SELECCIONAR EQUIPO
            # =================================================

            texto_equipo = (
                f"{codigo_equipo} | "
                f"{nombre_equipo}"
            )

            # Si todavía no existe en el diccionario,
            # lo agregamos.
            self.equipos_por_texto[
                texto_equipo
            ] = id_equipo

            valores_equipos = list(
                self.equipos_por_texto.keys()
            )

            self.combo_equipo.configure(
                values=valores_equipos
            )

            self.combo_equipo.set(
                texto_equipo
            )

            # =================================================
            # SELECCIONAR RESPONSABLE
            # =================================================

            texto_responsable = (
                f"{nombres} {apellidos}"
            ).strip()

            self.responsables_por_texto[
                texto_responsable
            ] = id_responsable

            valores_responsables = list(
                self.responsables_por_texto.keys()
            )

            self.combo_responsable.configure(
                values=valores_responsables
            )

            self.combo_responsable.set(
                texto_responsable
            )

            # =================================================
            # FECHA DE PRÉSTAMO
            # =================================================

            self.entry_fecha_prestamo.delete(
                0,
                "end"
            )

            if fecha_prestamo:

                self.entry_fecha_prestamo.insert(
                    0,
                    str(fecha_prestamo)
                )

            # =================================================
            # FECHA DE DEVOLUCIÓN
            # =================================================

            self.entry_fecha_devolucion.delete(
                0,
                "end"
            )

            if fecha_devolucion:

                self.entry_fecha_devolucion.insert(
                    0,
                    str(fecha_devolucion)
                )

            # =================================================
            # ESTADO
            # =================================================

            if estado:

                self.combo_estado.set(
                    str(estado)
                )

            else:

                self.combo_estado.set(
                    ""
                )

            # =================================================
            # OBSERVACIONES
            # =================================================

            self.text_observaciones.delete(
                "1.0",
                "end"
            )

            if observaciones:

                self.text_observaciones.insert(
                    "1.0",
                    str(observaciones)
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                (
                    "No se pudieron cargar "
                    f"los datos del préstamo:\n\n{e}"
                ),
                parent=self
            )

        finally:

            cursor.close()
            conexion.close()

    # =========================================================
    # GUARDAR
    # =========================================================

    def guardar(self):

        # =====================================================
        # OBTENER VALORES
        # =====================================================

        equipo_seleccionado = (
            self.combo_equipo.get().strip()
        )

        responsable_seleccionado = (
            self.combo_responsable.get().strip()
        )

        fecha_prestamo = (
            self.entry_fecha_prestamo
            .get()
            .strip()
        )

        fecha_devolucion = (
            self.entry_fecha_devolucion
            .get()
            .strip()
        )

        estado = (
            self.combo_estado.get().strip()
        )

        observaciones = (
            self.text_observaciones
            .get(
                "1.0",
                "end"
            )
            .strip()
        )

        # =====================================================
        # VALIDAR EQUIPO
        # =====================================================

        if (
            not equipo_seleccionado
            or equipo_seleccionado
            == "Cargando..."
            or "No hay equipos"
            in equipo_seleccionado
        ):

            messagebox.showwarning(
                "Advertencia",
                "Seleccione un equipo.",
                parent=self
            )

            return

        # =====================================================
        # VALIDAR RESPONSABLE
        # =====================================================

        if (
            not responsable_seleccionado
            or responsable_seleccionado
            == "Cargando..."
            or "No hay responsables"
            in responsable_seleccionado
        ):

            messagebox.showwarning(
                "Advertencia",
                "Seleccione un responsable.",
                parent=self
            )

            return

        # =====================================================
        # VALIDAR FECHA DE PRÉSTAMO
        # =====================================================

        if not fecha_prestamo:

            messagebox.showwarning(
                "Advertencia",
                "Ingrese la fecha de préstamo.",
                parent=self
            )

            return

        # =====================================================
        # VALIDAR ESTADO
        # =====================================================

        if not estado:

            messagebox.showwarning(
                "Advertencia",
                "Seleccione un estado.",
                parent=self
            )

            return

        try:

            # =================================================
            # OBTENER ID REAL DEL EQUIPO
            # =================================================

            id_equipo = (
                self.equipos_por_texto.get(
                    equipo_seleccionado
                )
            )

            # =================================================
            # COMPATIBILIDAD ADICIONAL
            # =================================================

            if id_equipo is None:

                conexion = Conexion.obtener_conexion()

                if conexion is None:

                    raise Exception(
                        "No se pudo conectar con "
                        "la base de datos."
                    )

                cursor = conexion.cursor()

                try:

                    codigo = (
                        equipo_seleccionado
                        .split("|")[0]
                        .strip()
                    )

                    sql = """
                        SELECT id_equipo
                        FROM equipos
                        WHERE codigo = %s
                    """

                    cursor.execute(
                        sql,
                        (
                            codigo,
                        )
                    )

                    resultado = cursor.fetchone()

                    if resultado:

                        id_equipo = resultado[0]

                finally:

                    cursor.close()
                    conexion.close()

            # =================================================
            # VALIDAR ID EQUIPO
            # =================================================

            if id_equipo is None:

                raise Exception(
                    "No se pudo identificar "
                    "el equipo seleccionado."
                )

            # =================================================
            # ASEGURAR QUE SEA ENTERO
            # =================================================

            id_equipo = int(
                id_equipo
            )

            # =================================================
            # OBTENER ID RESPONSABLE
            # =================================================

            id_responsable = (
                self.responsables_por_texto.get(
                    responsable_seleccionado
                )
            )

            # =================================================
            # COMPATIBILIDAD CON FORMATO ANTIGUO
            # =================================================

            if id_responsable is None:

                conexion = Conexion.obtener_conexion()

                if conexion is None:

                    raise Exception(
                        "No se pudo conectar con "
                        "la base de datos."
                    )

                cursor = conexion.cursor()

                try:

                    nombre = (
                        responsable_seleccionado
                        .split("|")[-1]
                        .strip()
                    )

                    partes = nombre.split(
                        " ",
                        1
                    )

                    nombres = partes[0]

                    apellidos = (
                        partes[1]
                        if len(partes) > 1
                        else ""
                    )

                    sql = """
                        SELECT id_responsable

                        FROM responsables

                        WHERE nombres = %s

                        AND apellidos = %s

                        LIMIT 1
                    """

                    cursor.execute(
                        sql,
                        (
                            nombres,
                            apellidos
                        )
                    )

                    resultado = cursor.fetchone()

                    if resultado:

                        id_responsable = resultado[0]

                finally:

                    cursor.close()
                    conexion.close()

            # =================================================
            # VALIDAR RESPONSABLE
            # =================================================

            if id_responsable is None:

                raise Exception(
                    "No se pudo identificar "
                    "el responsable seleccionado."
                )

            # =================================================
            # ASEGURAR QUE SEA ENTERO
            # =================================================

            id_responsable = int(
                id_responsable
            )

            # =================================================
            # FECHA DEVOLUCIÓN
            # =================================================

            if not fecha_devolucion:

                fecha_devolucion = None

            # =================================================
            # EDITAR PRÉSTAMO
            # =================================================

            if self.prestamo:

                id_prestamo = int(
                    self.prestamo[0]
                )

                self.model.actualizar(
                    id_prestamo,
                    id_equipo,
                    id_responsable,
                    fecha_prestamo,
                    fecha_devolucion,
                    estado,
                    observaciones
                )

                mensaje = (
                    "Préstamo actualizado "
                    "correctamente."
                )

            # =================================================
            # NUEVO PRÉSTAMO
            # =================================================

            else:

                self.model.guardar(
                    id_equipo,
                    id_responsable,
                    fecha_prestamo,
                    fecha_devolucion,
                    estado,
                    observaciones
                )

                mensaje = (
                    "Préstamo registrado "
                    "correctamente."
                )

            # =================================================
            # MENSAJE DE ÉXITO
            # =================================================

            messagebox.showinfo(
                "Éxito",
                mensaje,
                parent=self
            )

            # =================================================
            # ACTUALIZAR TABLA PRINCIPAL
            # =================================================

            if self.callback:

                self.callback()

            # =================================================
            # CERRAR
            # =================================================

            self.cerrar()

        except Exception as e:

            messagebox.showerror(
                "Error",
                (
                    "No se pudo guardar "
                    f"el préstamo:\n\n{e}"
                ),
                parent=self
            )

    # =========================================================
    # CERRAR FORMULARIO
    # =========================================================

    def cerrar(self):

        try:

            self.grab_release()

        except Exception:

            pass

        self.destroy()