import customtkinter as ctk
from tkinter import messagebox

from app.models.usuario_model import UsuarioModel
from app.views.dashboard import Dashboard


class Login(ctk.CTk):

    def __init__(self):
        super().__init__()

        # =====================================================
        # CONFIGURACIÓN
        # =====================================================

        self.title(
            "Sistema de Inventario Tecnológico"
        )

        self.geometry(
            "500x420"
        )

        self.resizable(
            False,
            False
        )

        ctk.set_appearance_mode(
            "light"
        )

        ctk.set_default_color_theme(
            "blue"
        )

        # =====================================================
        # VARIABLE PARA GUARDAR LOS DATOS DEL USUARIO
        # =====================================================

        self.datos_usuario = None

        # =====================================================
        # CREAR LOGIN
        # =====================================================

        self.crear_componentes()

    # =========================================================
    # COMPONENTES
    # =========================================================

    def crear_componentes(self):

        titulo = ctk.CTkLabel(
            self,
            text="Unidad Educativa Jacarandá",
            font=("Segoe UI", 24, "bold")
        )

        titulo.pack(
            pady=(30, 10)
        )

        subtitulo = ctk.CTkLabel(
            self,
            text="Sistema de Inventario Tecnológico",
            font=("Segoe UI", 16)
        )

        subtitulo.pack(
            pady=(0, 30)
        )

        self.txt_usuario = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Usuario"
        )

        self.txt_usuario.pack(
            pady=10
        )

        self.txt_password = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Contraseña",
            show="*"
        )

        self.txt_password.pack(
            pady=10
        )

        boton = ctk.CTkButton(
            self,
            text="Iniciar Sesión",
            width=300,
            command=self.validar_login
        )

        boton.pack(
            pady=25
        )

        self.bind(
            "<Return>",
            lambda event: self.validar_login()
        )

    # =========================================================
    # VALIDAR LOGIN
    # =========================================================

    def validar_login(self):

        usuario = self.txt_usuario.get().strip()

        clave = self.txt_password.get().strip()

        # -----------------------------------------------------
        # VALIDAR CAMPOS
        # -----------------------------------------------------

        if usuario == "" or clave == "":

            messagebox.showwarning(
                "Aviso",
                "Ingrese usuario y contraseña.",
                parent=self
            )

            return

        # -----------------------------------------------------
        # VALIDAR EN BASE DE DATOS
        # -----------------------------------------------------

        try:

            modelo = UsuarioModel()

            datos = modelo.validar_usuario(
                usuario,
                clave
            )

        except Exception as e:

            print(
                "Error al validar usuario:",
                e
            )

            messagebox.showerror(
                "Error",
                (
                    "No se pudo validar el usuario.\n\n"
                    f"Detalle:\n{e}"
                ),
                parent=self
            )

            return

        # =====================================================
        # LOGIN CORRECTO
        # =====================================================

        if datos:

            print(
                "LOGIN CORRECTO"
            )

            print(
                "Datos usuario:",
                datos
            )

            self.datos_usuario = datos

            self.mostrar_dashboard()

        # =====================================================
        # LOGIN INCORRECTO
        # =====================================================

        else:

            messagebox.showerror(
                "Error",
                "Usuario o contraseña incorrectos.",
                parent=self
            )

    # =========================================================
    # MOSTRAR DASHBOARD
    # =========================================================

    def mostrar_dashboard(self):

        try:

            # -------------------------------------------------
            # OCULTAR LOGIN
            # -------------------------------------------------

            self.withdraw()

            # -------------------------------------------------
            # CREAR DASHBOARD
            # -------------------------------------------------

            self.dashboard = Dashboard(
                self.datos_usuario,
                login=self
            )

            # -------------------------------------------------
            # CUANDO SE CIERRE EL DASHBOARD
            # -------------------------------------------------

            self.dashboard.protocol(
                "WM_DELETE_WINDOW",
                self.cerrar_desde_dashboard
            )

            # -------------------------------------------------
            # MOSTRAR DASHBOARD
            # -------------------------------------------------

            self.dashboard.deiconify()

            self.dashboard.lift()

            self.dashboard.focus_force()

            # -------------------------------------------------
            # MAXIMIZAR
            # -------------------------------------------------

            self.after(
                100,
                self.maximizar_dashboard
            )

        except Exception as e:

            print(
                "Error al abrir Dashboard:",
                e
            )

            self.deiconify()

            messagebox.showerror(
                "Error",
                (
                    "No se pudo abrir el Dashboard.\n\n"
                    f"Detalle:\n{e}"
                ),
                parent=self
            )

    # =========================================================
    # MAXIMIZAR DASHBOARD
    # =========================================================

    def maximizar_dashboard(self):

        try:

            if (
                hasattr(self, "dashboard")
                and self.dashboard.winfo_exists()
            ):

                self.dashboard.state(
                    "zoomed"
                )

        except Exception as e:

            print(
                "No se pudo maximizar Dashboard:",
                e
            )

    # =========================================================
    # CERRAR DESDE DASHBOARD
    # =========================================================

    def cerrar_desde_dashboard(self):

        try:

            if (
                hasattr(self, "dashboard")
                and self.dashboard.winfo_exists()
            ):

                self.dashboard.destroy()

        except Exception:
            pass

        self.destroy()

    # =========================================================
    # CERRAR APLICACIÓN
    # =========================================================

    def cerrar_aplicacion(self):

        try:

            if (
                hasattr(self, "dashboard")
                and self.dashboard.winfo_exists()
            ):

                self.dashboard.destroy()

        except Exception:
            pass

        self.destroy()


# =============================================================
# EJECUCIÓN DIRECTA
# =============================================================

if __name__ == "__main__":

    app = Login()

    app.mainloop()