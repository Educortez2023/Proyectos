import customtkinter as ctk
from tkinter import messagebox

from app.views.equipos import VentanaEquipos
from app.views.insumos import VentanaInsumos
from app.views.prestamos import VentanaPrestamos
from app.views.responsables import VentanaResponsables
from app.views.ubicaciones import VentanaUbicaciones
from app.views.departamentos import VentanaDepartamentos
from app.views.marcas import VentanaMarcas
from app.views.modelos import VentanaModelos
from app.views.proveedores import VentanaProveedores
from app.views.usuarios import VentanaUsuarios
from app.views.reporte import VentanaReportes

from app.models.equipo_model import EquipoModel
from app.models.insumo_model import InsumoModel


class Dashboard(ctk.CTk):
    """
    Ventana principal del sistema. El menú lateral, las ventanas hijas y
    las tarjetas de resumen se generan a partir de diccionarios de
    configuración (MENU_ITEMS, TARJETAS) en lugar de código repetido,
    así que agregar un módulo nuevo es una entrada más en la lista,
    no un método completo.
    """

    # =====================================================
    # CONFIGURACIÓN DE VENTANAS HIJAS
    # clave -> (clase, texto del botón, ícono)
    # =====================================================
    MENU_ITEMS = [
        ("equipos",        VentanaEquipos,        "💻 Equipos"),
        ("insumos",        VentanaInsumos,        "🖱 Insumos"),
        ("prestamos",      VentanaPrestamos,      "📋 Préstamos y Asignaciones"),
        ("responsables",   VentanaResponsables,   "👤 Responsables"),
        ("ubicaciones",    VentanaUbicaciones,    "📍 Ubicaciones"),
        ("departamentos",  VentanaDepartamentos,  "🏢 Departamentos"),
        ("marcas",         VentanaMarcas,         "🏷 Marcas"),
        ("modelos",        VentanaModelos,        "📦 Modelos"),
        ("proveedores",    VentanaProveedores,    "🚚 Proveedores"),
        ("usuarios",       VentanaUsuarios,       "👥 Usuarios"),
        ("reportes",       VentanaReportes,       "📄 Reportes"),
    ]

    # =====================================================
    # CONFIGURACIÓN DE TARJETAS DEL DASHBOARD
    # clave del modelo -> (ícono/título, atributo del modelo a llamar)
    # =====================================================
    TARJETAS = [
        ("equipos", "💻 Equipos registrados"),
        ("insumos", "🖱 Insumos registrados"),
    ]

    def __init__(self, usuario, login=None):
        super().__init__()

        self.usuario = usuario
        self.login = login

        self.title("Sistema de Inventario Tecnológico")
        self.geometry("1366x768")
        self.minsize(1200, 700)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Modelos usados para los contadores del dashboard
        self.modelos = {
            "equipos": EquipoModel(),
            "insumos": InsumoModel(),
        }

        # Referencias a ventanas hijas abiertas (una sola instancia c/u)
        self.ventanas_abiertas = {}

        # Labels de contadores, llenados en crear_tarjeta()
        self.labels_contadores = {}

        self.crear_interfaz()
        self.after(300, self.actualizar_contadores)

    # =========================================================
    # CREAR INTERFAZ
    # =========================================================
    def crear_interfaz(self):
        self._crear_menu_lateral()
        self._crear_area_principal()

    def _crear_menu_lateral(self):
        # Contenedor exterior de ancho fijo. Todo lo que va dentro se
        # organiza en 3 franjas verticales: cabecera fija (arriba),
        # lista de módulos con scroll (en medio) y botón de salir
        # fijo (abajo). Así, sin importar cuántos módulos haya o qué
        # tan chica sea la ventana, "Cerrar sesión" SIEMPRE es visible.
        self.menu = ctk.CTkFrame(self, width=230, corner_radius=0)
        self.menu.pack(side="left", fill="y")
        self.menu.pack_propagate(False)

        self._crear_cabecera_menu(self.menu)
        self._crear_pie_menu(self.menu)          # se empaqueta primero
        self._crear_lista_modulos(self.menu)      # ocupa el espacio restante

    def _crear_cabecera_menu(self, contenedor):
        cabecera = ctk.CTkFrame(contenedor, fg_color="transparent")
        cabecera.pack(side="top", fill="x")

        ctk.CTkLabel(
            cabecera, text="JACARANDÁ", font=("Segoe UI", 24, "bold")
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            cabecera, text=self._nombre_usuario(), font=("Segoe UI", 15)
        ).pack(pady=(0, 20))

        ctk.CTkButton(
            cabecera, text="🏠 Dashboard", width=190, height=40,
            command=self.ir_dashboard
        ).pack(pady=5, padx=15)

    def _crear_pie_menu(self, contenedor):
        # Se empaqueta con side="bottom" ANTES que la lista scrollable,
        # así reserva su espacio primero y nunca queda tapado.
        pie = ctk.CTkFrame(contenedor, fg_color="transparent")
        pie.pack(side="bottom", fill="x")

        ctk.CTkButton(
            pie, text="🔒  CERRAR SESION", width=190, height=42,
            corner_radius=10, fg_color="#C0392B", hover_color="#922B21",
            font=("Segoe UI", 14, "bold"), command=self.cerrar_sesion
        ).pack(pady=12, padx=15)

    def _crear_lista_modulos(self, contenedor):
        # Ocupa el espacio restante entre la cabecera y el pie.
        # Con scroll: si hay muchos módulos o la ventana es chica,
        # el usuario desliza en vez de que los botones se corten.
        lista = ctk.CTkScrollableFrame(
            contenedor, fg_color="transparent", corner_radius=0
        )
        lista.pack(side="top", fill="both", expand=True)

        # Un botón por cada entrada de MENU_ITEMS: sin repetir código.
        for clave, _clase, texto in self.MENU_ITEMS:
            ctk.CTkButton(
                lista, text=texto, width=190, height=40,
                command=lambda c=clave: self.abrir_ventana(c)
            ).pack(pady=5, padx=15)

    def _crear_area_principal(self):
        self.principal = ctk.CTkFrame(self, fg_color="#F5F5F5", corner_radius=0)
        self.principal.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            self.principal, text="Sistema de Inventario Tecnológico",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            self.principal, text=f"Bienvenido {self._nombre_usuario()}",
            font=("Segoe UI", 18)
        ).pack(pady=10)

        ctk.CTkLabel(
            self.principal, text="Resumen general del inventario tecnológico",
            font=("Segoe UI", 14), text_color="#666666"
        ).pack(pady=(0, 20))

        frame_tarjetas = ctk.CTkFrame(self.principal, fg_color="transparent")
        frame_tarjetas.pack(pady=30)

        # Una tarjeta por cada entrada de TARJETAS: agregar una nueva
        # tarjeta (p.ej. "Préstamos activos") es una sola línea en la lista.
        for columna, (clave, titulo) in enumerate(self.TARJETAS):
            self._crear_tarjeta(frame_tarjetas, columna, clave, titulo)

    def _crear_tarjeta(self, contenedor, columna, clave, titulo):
        tarjeta = ctk.CTkFrame(contenedor, width=280, height=160, corner_radius=15)
        tarjeta.grid(row=0, column=columna, padx=20)
        tarjeta.grid_propagate(False)

        ctk.CTkLabel(
            tarjeta, text=titulo, font=("Segoe UI", 18, "bold")
        ).pack(pady=(25, 5))

        label_cantidad = ctk.CTkLabel(tarjeta, text="0", font=("Segoe UI", 32, "bold"))
        label_cantidad.pack()

        self.labels_contadores[clave] = label_cantidad

    # =========================================================
    # DATOS DEL USUARIO
    # =========================================================
    def obtener_dato_usuario(self, clave):
        try:
            if isinstance(self.usuario, dict):
                return self.usuario.get(clave, "")
            return ""
        except Exception:
            return ""

    def _nombre_usuario(self):
        nombres = self.obtener_dato_usuario("nombres")
        apellidos = self.obtener_dato_usuario("apellidos")
        nombre_completo = f"{nombres} {apellidos}".strip()
        return nombre_completo or "Usuario"

    # =========================================================
    # DASHBOARD / CONTADORES
    # =========================================================
    def ir_dashboard(self):
        try:
            self.actualizar_contadores()
            self.lift()
            self.focus_force()
        except Exception as e:
            print("Error al actualizar Dashboard:", e)

    def actualizar_contadores(self):
        # Un solo bucle cubre todos los contadores actuales y futuros:
        # agregar un contador nuevo no requiere un try/except adicional.
        for clave, modelo in self.modelos.items():
            label = self.labels_contadores.get(clave)
            if label is None:
                continue
            try:
                datos = modelo.listar() or []
                cantidad = len(datos)
                label.configure(text=str(cantidad))
                print(f"{clave.capitalize()} cargados: {cantidad}")
            except Exception as e:
                print(f"Error al cargar {clave}:", e)
                label.configure(text="0")

    # =========================================================
    # ABRIR VENTANAS HIJAS (genérico para las 11 ventanas)
    # =========================================================
    def abrir_ventana(self, clave):
        clase = self._clase_por_clave(clave)
        if clase is None:
            print(f"Ventana desconocida: {clave}")
            return

        try:
            ventana = self.ventanas_abiertas.get(clave)

            if ventana is None or not ventana.winfo_exists():
                ventana = clase(self)
                self.ventanas_abiertas[clave] = ventana
            else:
                ventana.lift()
                ventana.focus_force()

        except Exception as e:
            titulo = clave.capitalize()
            print(f"Error al abrir {titulo}:", e)
            messagebox.showerror(
                "Error", f"No se pudo abrir {titulo}.\n\n{e}", parent=self
            )

    def _clase_por_clave(self, clave):
        for c, clase, _texto in self.MENU_ITEMS:
            if c == clave:
                return clase
        return None

    # =========================================================
    # CERRAR SESIÓN
    # =========================================================
    def cerrar_sesion(self):
        if not messagebox.askyesno(
            "Cerrar sesión", "¿Está seguro de que desea cerrar la sesión?",
            parent=self
        ):
            return

        try:
            for ventana in self.ventanas_abiertas.values():
                try:
                    if ventana is not None and ventana.winfo_exists():
                        ventana.destroy()
                except Exception:
                    pass

            self.destroy()
            self._restaurar_login()

        except Exception as e:
            print("Error al cerrar sesión:", e)

    def _restaurar_login(self):
        if self.login is None or not self.login.winfo_exists():
            return

        self.login.deiconify()
        self.login.lift()
        self.login.focus_force()

        try:
            self.login.txt_usuario.delete(0, "end")
            self.login.txt_password.delete(0, "end")
            self.login.txt_usuario.focus()
        except Exception:
            pass