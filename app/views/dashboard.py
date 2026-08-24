import customtkinter as ctk
from tkinter import messagebox

from app.views.equipos import VentanaEquipos
from app.views.insumos import VentanaInsumos
from app.views.prestamos import VentanaPrestamos
from app.views.responsables import VentanaResponsables
from app.views.ubicaciones import VentanaUbicaciones

# =====================================================
# NUEVOS MÓDULOS
# =====================================================

from app.views.departamentos import VentanaDepartamentos
from app.views.marcas import VentanaMarcas
from app.views.modelos import VentanaModelos
from app.views.proveedores import VentanaProveedores
from app.views.usuarios import VentanaUsuarios
from app.views.reporte import VentanaReportes

from app.models.equipo_model import EquipoModel
from app.models.insumo_model import InsumoModel


class Dashboard(ctk.CTk):

    def __init__(self, usuario, login=None):

        super().__init__()

        # =====================================================
        # DATOS DEL USUARIO
        # =====================================================

        self.usuario = usuario
        self.login = login

        # =====================================================
        # CONFIGURACIÓN
        # =====================================================

        self.title(
            "Sistema de Inventario Tecnológico"
        )

        self.geometry(
            "1366x768"
        )

        self.minsize(
            1200,
            700
        )

        # =====================================================
        # APARIENCIA
        # =====================================================

        ctk.set_appearance_mode(
            "light"
        )

        ctk.set_default_color_theme(
            "blue"
        )

        # =====================================================
        # MODELOS
        # =====================================================

        self.modelo_equipo = EquipoModel()
        self.modelo_insumo = InsumoModel()

        # =====================================================
        # REFERENCIAS DE VENTANAS
        # =====================================================

        self.ventana_equipos = None
        self.ventana_insumos = None
        self.ventana_prestamos = None
        self.ventana_responsables = None
        self.ventana_ubicaciones = None

        # =====================================================
        # NUEVAS REFERENCIAS
        # =====================================================

        self.ventana_departamentos = None
        self.ventana_marcas = None
        self.ventana_modelos = None
        self.ventana_proveedores = None
        self.ventana_usuarios = None
        self.ventana_reportes = None

        # =====================================================
        # CREAR INTERFAZ
        # =====================================================

        self.crear_interfaz()

        # =====================================================
        # ACTUALIZAR CONTADORES
        # =====================================================

        self.after(
            300,
            self.actualizar_contadores
        )

    # =========================================================
    # CREAR INTERFAZ
    # =========================================================

    def crear_interfaz(self):

        # =====================================================
        # MENÚ LATERAL
        # =====================================================

        self.menu = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0
        )

        self.menu.pack(
            side="left",
            fill="y"
        )

        self.menu.pack_propagate(
            False
        )

        # =====================================================
        # TÍTULO
        # =====================================================

        titulo = ctk.CTkLabel(
            self.menu,
            text="JACARANDÁ",
            font=(
                "Segoe UI",
                24,
                "bold"
            )
        )

        titulo.pack(
            pady=(
                30,
                10
            )
        )

        # =====================================================
        # OBTENER NOMBRE DEL USUARIO
        # =====================================================

        nombres = self.obtener_dato_usuario(
            "nombres"
        )

        apellidos = self.obtener_dato_usuario(
            "apellidos"
        )

        nombre_completo = (
            f"{nombres} {apellidos}"
        ).strip()

        if not nombre_completo:

            nombre_completo = "Usuario"

        # =====================================================
        # USUARIO
        # =====================================================

        usuario_label = ctk.CTkLabel(
            self.menu,
            text=nombre_completo,
            font=(
                "Segoe UI",
                15
            )
        )

        usuario_label.pack(
            pady=(
                0,
                20
            )
        )

        # =====================================================
        # BOTÓN DASHBOARD
        # =====================================================

        boton_dashboard = ctk.CTkButton(
            self.menu,
            text="🏠 Dashboard",
            width=190,
            height=40,
            command=self.ir_dashboard
        )

        boton_dashboard.pack(
            pady=5,
            padx=15
        )

        # =====================================================
        # BOTÓN EQUIPOS
        # =====================================================

        boton_equipos = ctk.CTkButton(
            self.menu,
            text="💻 Equipos",
            width=190,
            height=40,
            command=self.abrir_equipos
        )

        boton_equipos.pack(
            pady=5,
            padx=15
        )

        # =====================================================
        # BOTÓN INSUMOS
        # =====================================================

        boton_insumos = ctk.CTkButton(
            self.menu,
            text="🖱 Insumos",
            width=190,
            height=40,
            command=self.abrir_insumos
        )

        boton_insumos.pack(
            pady=5,
            padx=15
        )

        # =====================================================
        # BOTÓN PRÉSTAMOS
        # =====================================================

        boton_prestamos = ctk.CTkButton(
            self.menu,
            text="📋 Préstamos y Asignaciones",
            width=190,
            height=40,
            command=self.abrir_prestamos
        )

        boton_prestamos.pack(
            pady=5,
            padx=15
        )

        # =====================================================
        # BOTÓN RESPONSABLES
        # =====================================================

        boton_responsables = ctk.CTkButton(
            self.menu,
            text="👤 Responsables",
            width=190,
            height=40,
            command=self.abrir_responsables
        )

        boton_responsables.pack(
            pady=5,
            padx=15
        )

        # =====================================================
        # BOTÓN UBICACIONES
        # =====================================================

        boton_ubicaciones = ctk.CTkButton(
            self.menu,
            text="📍 Ubicaciones",
            width=190,
            height=40,
            command=self.abrir_ubicaciones
        )

        boton_ubicaciones.pack(
            pady=5,
            padx=15
        )

        # =====================================================
        # BOTÓN DEPARTAMENTOS
        # =====================================================

        boton_departamentos = ctk.CTkButton(
            self.menu,
            text="🏢 Departamentos",
            width=190,
            height=40,
            command=self.abrir_departamentos
        )

        boton_departamentos.pack(
            pady=5,
            padx=15
        )

        # =====================================================
        # BOTÓN MARCAS
        # =====================================================

        boton_marcas = ctk.CTkButton(
            self.menu,
            text="🏷 Marcas",
            width=190,
            height=40,
            command=self.abrir_marcas
        )

        boton_marcas.pack(
            pady=5,
            padx=15
        )

        # =====================================================
        # BOTÓN MODELOS
        # =====================================================

        boton_modelos = ctk.CTkButton(
            self.menu,
            text="📦 Modelos",
            width=190,
            height=40,
            command=self.abrir_modelos
        )

        boton_modelos.pack(
            pady=5,
            padx=15
        )

        # =====================================================
        # BOTÓN PROVEEDORES
        # =====================================================

        boton_proveedores = ctk.CTkButton(
            self.menu,
            text="🚚 Proveedores",
            width=190,
            height=40,
            command=self.abrir_proveedores
        )

        boton_proveedores.pack(
            pady=5,
            padx=15
        )

        # =====================================================
        # BOTÓN USUARIOS
        # =====================================================

        boton_usuarios = ctk.CTkButton(
            self.menu,
            text="👥 Usuarios",
            width=190,
            height=40,
            command=self.abrir_usuarios
        )

        boton_usuarios.pack(
            pady=5,
            padx=15
        )

        # =====================================================
        # BOTÓN REPORTES
        # =====================================================

        boton_reportes = ctk.CTkButton(
            self.menu,
            text="📄 Reportes",
            width=190,
            height=40,
            command=self.abrir_reportes
        )

        boton_reportes.pack(
            pady=5,
            padx=15
        )

        # =====================================================
        # CERRAR SESIÓN
        # =====================================================

        boton_salir = ctk.CTkButton(
            self.menu,
            text="🔒  CERRAR SESION",
            width=190,
            height=42,
            corner_radius=10,
            fg_color="#C0392B",
            hover_color="922b21",
            font=("Segoe UI", 14, "bold"),
            command=self.cerrar_sesion
        )

        boton_salir.pack(
            side="bottom",
            pady=12,
            padx=15
        )

        # =====================================================
        # ÁREA PRINCIPAL
        # =====================================================

        self.principal = ctk.CTkFrame(
            self,
            fg_color="#F5F5F5",
            corner_radius=0
        )

        self.principal.pack(
            side="left",
            fill="both",
            expand=True
        )

        # =====================================================
        # ENCABEZADO
        # =====================================================

        encabezado = ctk.CTkLabel(
            self.principal,
            text="Sistema de Inventario Tecnológico",
            font=(
                "Segoe UI",
                28,
                "bold"
            )
        )

        encabezado.pack(
            pady=(
                30,
                10
            )
        )

        # =====================================================
        # BIENVENIDA
        # =====================================================

        bienvenida = ctk.CTkLabel(
            self.principal,
            text=f"Bienvenido {nombre_completo}",
            font=(
                "Segoe UI",
                18
            )
        )

        bienvenida.pack(
            pady=10
        )

        # =====================================================
        # DESCRIPCIÓN
        # =====================================================

        descripcion = ctk.CTkLabel(
            self.principal,
            text="Resumen general del inventario tecnológico",
            font=(
                "Segoe UI",
                14
            ),
            text_color="#666666"
        )

        descripcion.pack(
            pady=(
                0,
                20
            )
        )

        # =====================================================
        # CONTENEDOR DE TARJETAS
        # =====================================================

        frame_tarjetas = ctk.CTkFrame(
            self.principal,
            fg_color="transparent"
        )

        frame_tarjetas.pack(
            pady=30
        )

        # =====================================================
        # TARJETA EQUIPOS
        # =====================================================

        tarjeta_equipos = ctk.CTkFrame(
            frame_tarjetas,
            width=280,
            height=160,
            corner_radius=15
        )

        tarjeta_equipos.grid(
            row=0,
            column=0,
            padx=20
        )

        tarjeta_equipos.grid_propagate(
            False
        )

        titulo_equipos = ctk.CTkLabel(
            tarjeta_equipos,
            text="💻 Equipos registrados",
            font=(
                "Segoe UI",
                18,
                "bold"
            )
        )

        titulo_equipos.pack(
            pady=(
                25,
                5
            )
        )

        self.cantidad_equipos = ctk.CTkLabel(
            tarjeta_equipos,
            text="0",
            font=(
                "Segoe UI",
                32,
                "bold"
            )
        )

        self.cantidad_equipos.pack()

        # =====================================================
        # TARJETA INSUMOS
        # =====================================================

        tarjeta_insumos = ctk.CTkFrame(
            frame_tarjetas,
            width=280,
            height=160,
            corner_radius=15
        )

        tarjeta_insumos.grid(
            row=0,
            column=1,
            padx=20
        )

        tarjeta_insumos.grid_propagate(
            False
        )

        titulo_insumos = ctk.CTkLabel(
            tarjeta_insumos,
            text="🖱 Insumos registrados",
            font=(
                "Segoe UI",
                18,
                "bold"
            )
        )

        titulo_insumos.pack(
            pady=(
                25,
                5
            )
        )

        self.cantidad_insumos = ctk.CTkLabel(
            tarjeta_insumos,
            text="0",
            font=(
                "Segoe UI",
                32,
                "bold"
            )
        )

        self.cantidad_insumos.pack()

    # =========================================================
    # OBTENER DATO DEL USUARIO
    # =========================================================

    def obtener_dato_usuario(self, clave):

        try:

            if isinstance(
                self.usuario,
                dict
            ):

                return self.usuario.get(
                    clave,
                    ""
                )

            return ""

        except Exception:

            return ""

    # =========================================================
    # DASHBOARD
    # =========================================================

    def ir_dashboard(self):

        try:

            self.actualizar_contadores()

            self.lift()

            self.focus_force()

        except Exception as e:

            print(
                "Error al actualizar Dashboard:",
                e
            )

    # =========================================================
    # ACTUALIZAR CONTADORES
    # =========================================================

    def actualizar_contadores(self):

        # =====================================================
        # EQUIPOS
        # =====================================================

        try:

            datos_equipos = (
                self.modelo_equipo.listar()
            )

            if datos_equipos is None:

                datos_equipos = []

            cantidad = len(
                datos_equipos
            )

            self.cantidad_equipos.configure(
                text=str(cantidad)
            )

            print(
                f"Equipos cargados: {cantidad}"
            )

        except Exception as e:

            print(
                "Error al cargar equipos:",
                e
            )

            self.cantidad_equipos.configure(
                text="0"
            )

        # =====================================================
        # INSUMOS
        # =====================================================

        try:

            datos_insumos = (
                self.modelo_insumo.listar()
            )

            if datos_insumos is None:

                datos_insumos = []

            cantidad = len(
                datos_insumos
            )

            self.cantidad_insumos.configure(
                text=str(cantidad)
            )

            print(
                f"Insumos cargados: {cantidad}"
            )

        except Exception as e:

            print(
                "Error al cargar insumos:",
                e
            )

            self.cantidad_insumos.configure(
                text="0"
            )

    # =========================================================
    # ABRIR EQUIPOS
    # =========================================================

    def abrir_equipos(self):

        try:

            if (
                self.ventana_equipos is None
                or not self.ventana_equipos.winfo_exists()
            ):

                self.ventana_equipos = VentanaEquipos(
                    self
                )

            else:

                self.ventana_equipos.lift()
                self.ventana_equipos.focus_force()

        except Exception as e:

            print(
                "Error al abrir Equipos:",
                e
            )

            messagebox.showerror(
                "Error",
                f"No se pudo abrir Equipos.\n\n{e}",
                parent=self
            )

    # =========================================================
    # ABRIR INSUMOS
    # =========================================================

    def abrir_insumos(self):

        try:

            if (
                self.ventana_insumos is None
                or not self.ventana_insumos.winfo_exists()
            ):

                self.ventana_insumos = VentanaInsumos(
                    self
                )

            else:

                self.ventana_insumos.lift()
                self.ventana_insumos.focus_force()

        except Exception as e:

            print(
                "Error al abrir Insumos:",
                e
            )

            messagebox.showerror(
                "Error",
                f"No se pudo abrir Insumos.\n\n{e}",
                parent=self
            )

    # =========================================================
    # ABRIR PRÉSTAMOS
    # =========================================================

    def abrir_prestamos(self):

        try:

            if (
                self.ventana_prestamos is None
                or not self.ventana_prestamos.winfo_exists()
            ):

                self.ventana_prestamos = VentanaPrestamos(
                    self
                )

            else:

                self.ventana_prestamos.lift()
                self.ventana_prestamos.focus_force()

        except Exception as e:

            print(
                "Error al abrir Préstamos:",
                e
            )

            messagebox.showerror(
                "Error",
                f"No se pudo abrir Préstamos.\n\n{e}",
                parent=self
            )

    # =========================================================
    # ABRIR RESPONSABLES
    # =========================================================

    def abrir_responsables(self):

        try:

            if (
                self.ventana_responsables is None
                or not self.ventana_responsables.winfo_exists()
            ):

                self.ventana_responsables = VentanaResponsables(
                    self
                )

            else:

                self.ventana_responsables.lift()
                self.ventana_responsables.focus_force()

        except Exception as e:

            print(
                "Error al abrir Responsables:",
                e
            )

            messagebox.showerror(
                "Error",
                f"No se pudo abrir Responsables.\n\n{e}",
                parent=self
            )

    # =========================================================
    # ABRIR UBICACIONES
    # =========================================================

    def abrir_ubicaciones(self):

        try:

            if (
                self.ventana_ubicaciones is None
                or not self.ventana_ubicaciones.winfo_exists()
            ):

                self.ventana_ubicaciones = VentanaUbicaciones(
                    self
                )

            else:

                self.ventana_ubicaciones.lift()
                self.ventana_ubicaciones.focus_force()

        except Exception as e:

            print(
                "Error al abrir Ubicaciones:",
                e
            )

            messagebox.showerror(
                "Error",
                f"No se pudo abrir Ubicaciones.\n\n{e}",
                parent=self
            )

    # =========================================================
    # ABRIR DEPARTAMENTOS
    # =========================================================

    def abrir_departamentos(self):

        try:

            if (
                self.ventana_departamentos is None
                or not self.ventana_departamentos.winfo_exists()
            ):

                self.ventana_departamentos = VentanaDepartamentos(
                    self
                )

            else:

                self.ventana_departamentos.lift()
                self.ventana_departamentos.focus_force()

        except Exception as e:

            print(
                "Error al abrir Departamentos:",
                e
            )

            messagebox.showerror(
                "Error",
                f"No se pudo abrir Departamentos.\n\n{e}",
                parent=self
            )

    # =========================================================
    # ABRIR MARCAS
    # =========================================================

    def abrir_marcas(self):

        try:

            if (
                self.ventana_marcas is None
                or not self.ventana_marcas.winfo_exists()
            ):

                self.ventana_marcas = VentanaMarcas(
                    self
                )

            else:

                self.ventana_marcas.lift()
                self.ventana_marcas.focus_force()

        except Exception as e:

            print(
                "Error al abrir Marcas:",
                e
            )

            messagebox.showerror(
                "Error",
                f"No se pudo abrir Marcas.\n\n{e}",
                parent=self
            )

    # =========================================================
    # ABRIR MODELOS
    # =========================================================

    def abrir_modelos(self):

        try:

            if (
                self.ventana_modelos is None
                or not self.ventana_modelos.winfo_exists()
            ):

                self.ventana_modelos = VentanaModelos(
                    self
                )

            else:

                self.ventana_modelos.lift()
                self.ventana_modelos.focus_force()

        except Exception as e:

            print(
                "Error al abrir Modelos:",
                e
            )

            messagebox.showerror(
                "Error",
                f"No se pudo abrir Modelos.\n\n{e}",
                parent=self
            )

    # =========================================================
    # ABRIR PROVEEDORES
    # =========================================================

    def abrir_proveedores(self):

        try:

            if (
                self.ventana_proveedores is None
                or not self.ventana_proveedores.winfo_exists()
            ):

                self.ventana_proveedores = VentanaProveedores(
                    self
                )

            else:

                self.ventana_proveedores.lift()
                self.ventana_proveedores.focus_force()

        except Exception as e:

            print(
                "Error al abrir Proveedores:",
                e
            )

            messagebox.showerror(
                "Error",
                f"No se pudo abrir Proveedores.\n\n{e}",
                parent=self
            )

    # =========================================================
    # ABRIR USUARIOS
    # =========================================================

    def abrir_usuarios(self):

        try:

            if (
                self.ventana_usuarios is None
                or not self.ventana_usuarios.winfo_exists()
            ):

                self.ventana_usuarios = VentanaUsuarios(
                    self
                )

            else:

                self.ventana_usuarios.lift()
                self.ventana_usuarios.focus_force()

        except Exception as e:

            print(
                "Error al abrir Usuarios:",
                e
            )

            messagebox.showerror(
                "Error",
                f"No se pudo abrir Usuarios.\n\n{e}",
                parent=self
            )

    # =========================================================
    # ABRIR REPORTES
    # =========================================================

    def abrir_reportes(self):

        try:

            if (
                self.ventana_reportes is None
                or not self.ventana_reportes.winfo_exists()
            ):

                self.ventana_reportes = VentanaReportes(
                    self
                )

            else:

                self.ventana_reportes.lift()
                self.ventana_reportes.focus_force()

        except Exception as e:

            print(
                "Error al abrir Reportes:",
                e
            )

            messagebox.showerror(
                "Error",
                f"No se pudo abrir Reportes.\n\n{e}",
                parent=self
            )

    # =========================================================
    # CERRAR SESIÓN
    # =========================================================

    def cerrar_sesion(self):

        respuesta = messagebox.askyesno(
            "Cerrar sesión",
            "¿Está seguro de que desea cerrar la sesión?",
            parent=self
        )

        if not respuesta:

            return

        try:

            # =================================================
            # CERRAR VENTANAS HIJAS
            # =================================================

            ventanas = [
                self.ventana_equipos,
                self.ventana_insumos,
                self.ventana_prestamos,
                self.ventana_responsables,
                self.ventana_ubicaciones,

                # Nuevas ventanas
                self.ventana_departamentos,
                self.ventana_marcas,
                self.ventana_modelos,
                self.ventana_proveedores,
                self.ventana_usuarios,
                self.ventana_reportes
            ]

            for ventana in ventanas:

                try:

                    if (
                        ventana is not None
                        and ventana.winfo_exists()
                    ):

                        ventana.destroy()

                except Exception:

                    pass

            # =================================================
            # CERRAR DASHBOARD
            # =================================================

            self.destroy()

            # =================================================
            # MOSTRAR NUEVAMENTE LOGIN
            # =================================================

            if (
                self.login is not None
                and self.login.winfo_exists()
            ):

                self.login.deiconify()

                self.login.lift()

                self.login.focus_force()

                # =================================================
                # LIMPIAR CAMPOS
                # =================================================

                try:

                    self.login.txt_usuario.delete(
                        0,
                        "end"
                    )

                    self.login.txt_password.delete(
                        0,
                        "end"
                    )

                    self.login.txt_usuario.focus()

                except Exception:

                    pass

        except Exception as e:

            print(
                "Error al cerrar sesión:",
                e
            )