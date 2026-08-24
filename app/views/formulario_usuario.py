import customtkinter as ctk
from tkinter import messagebox

from app.models.usuario_model import UsuarioModel


class FormularioUsuario(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        usuario=None,
        callback=None
    ):

        super().__init__(parent)

        self.parent = parent
        self.usuario = usuario
        self.callback = callback

        # =====================================================
        # CONFIGURACIÓN
        # =====================================================

        if usuario:
            self.title("Editar Usuario")
        else:
            self.title("Nuevo Usuario")

        self.geometry("650x700")
        self.minsize(600, 650)

        self.transient(parent)

        self.grab_set()

        # =====================================================
        # VARIABLES
        # =====================================================

        self.roles = []

        # =====================================================
        # CREAR INTERFAZ
        # =====================================================

        self.crear_interfaz()

        # =====================================================
        # CARGAR ROLES
        # =====================================================

        self.cargar_roles()

        # =====================================================
        # CARGAR DATOS
        # =====================================================

        if self.usuario:
            self.cargar_datos()

    # =====================================================
    # CREAR INTERFAZ
    # =====================================================

    def crear_interfaz(self):

        titulo = ctk.CTkLabel(
            self,
            text=(
                "EDITAR USUARIO"
                if self.usuario
                else "NUEVO USUARIO"
            ),
            font=("Arial", 24, "bold")
        )

        titulo.pack(
            pady=(25, 20)
        )

        frame = ctk.CTkFrame(
            self
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )

        # =====================================================
        # NOMBRES
        # =====================================================

        lbl_nombres = ctk.CTkLabel(
            frame,
            text="Nombres *",
            font=("Arial", 14, "bold")
        )

        lbl_nombres.pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )

        self.entry_nombres = ctk.CTkEntry(
            frame,
            placeholder_text="Ingrese los nombres",
            width=500,
            height=40
        )

        self.entry_nombres.pack(
            padx=25,
            pady=(0, 10)
        )

        # =====================================================
        # APELLIDOS
        # =====================================================

        lbl_apellidos = ctk.CTkLabel(
            frame,
            text="Apellidos *",
            font=("Arial", 14, "bold")
        )

        lbl_apellidos.pack(
            anchor="w",
            padx=25,
            pady=(5, 5)
        )

        self.entry_apellidos = ctk.CTkEntry(
            frame,
            placeholder_text="Ingrese los apellidos",
            width=500,
            height=40
        )

        self.entry_apellidos.pack(
            padx=25,
            pady=(0, 10)
        )

        # =====================================================
        # USUARIO
        # =====================================================

        lbl_usuario = ctk.CTkLabel(
            frame,
            text="Usuario *",
            font=("Arial", 14, "bold")
        )

        lbl_usuario.pack(
            anchor="w",
            padx=25,
            pady=(5, 5)
        )

        self.entry_usuario = ctk.CTkEntry(
            frame,
            placeholder_text="Nombre de usuario",
            width=500,
            height=40
        )

        self.entry_usuario.pack(
            padx=25,
            pady=(0, 10)
        )

        # =====================================================
        # CLAVE
        # =====================================================

        lbl_clave = ctk.CTkLabel(
            frame,
            text=(
                "Clave *"
                if not self.usuario
                else "Nueva clave (opcional)"
            ),
            font=("Arial", 14, "bold")
        )

        lbl_clave.pack(
            anchor="w",
            padx=25,
            pady=(5, 5)
        )

        self.entry_clave = ctk.CTkEntry(
            frame,
            placeholder_text=(
                "Ingrese la clave"
                if not self.usuario
                else "Dejar vacío para conservar la actual"
            ),
            width=500,
            height=40,
            show="*"
        )

        self.entry_clave.pack(
            padx=25,
            pady=(0, 10)
        )

        # =====================================================
        # CORREO
        # =====================================================

        lbl_correo = ctk.CTkLabel(
            frame,
            text="Correo",
            font=("Arial", 14, "bold")
        )

        lbl_correo.pack(
            anchor="w",
            padx=25,
            pady=(5, 5)
        )

        self.entry_correo = ctk.CTkEntry(
            frame,
            placeholder_text="correo@ejemplo.com",
            width=500,
            height=40
        )

        self.entry_correo.pack(
            padx=25,
            pady=(0, 10)
        )

        # =====================================================
        # ROL
        # =====================================================

        lbl_rol = ctk.CTkLabel(
            frame,
            text="Rol *",
            font=("Arial", 14, "bold")
        )

        lbl_rol.pack(
            anchor="w",
            padx=25,
            pady=(5, 5)
        )

        self.combo_rol = ctk.CTkComboBox(
            frame,
            values=["Cargando roles..."],
            width=500,
            height=40,
            state="readonly"
        )

        self.combo_rol.pack(
            padx=25,
            pady=(0, 20)
        )

        # =====================================================
        # BOTONES
        # =====================================================

        frame_botones = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        frame_botones.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        # =====================================================
        # GUARDAR
        # =====================================================

        btn_guardar = ctk.CTkButton(
            frame_botones,
            text=(
                "Actualizar"
                if self.usuario
                else "Guardar"
            ),
            width=180,
            height=45,
            font=("Arial", 14, "bold"),
            command=self.guardar
        )

        btn_guardar.pack(
            side="left",
            padx=5
        )

        # =====================================================
        # CANCELAR
        # =====================================================

        btn_cancelar = ctk.CTkButton(
            frame_botones,
            text="Cancelar",
            width=180,
            height=45,
            fg_color="gray",
            hover_color="#555555",
            command=self.cancelar
        )

        btn_cancelar.pack(
            side="right",
            padx=5
        )

    # =====================================================
    # CARGAR ROLES
    # =====================================================

    def cargar_roles(self):

        try:

            self.roles = UsuarioModel.listar_roles()

            if not self.roles:

                self.combo_rol.configure(
                    values=["No hay roles activos"]
                )

                self.combo_rol.set(
                    "No hay roles activos"
                )

                return

            nombres_roles = [
                rol["nombre"]
                for rol in self.roles
            ]

            self.combo_rol.configure(
                values=nombres_roles
            )

            self.combo_rol.set(
                "Seleccione un rol"
            )

        except Exception as e:

            print(
                f"Error al cargar roles: {e}"
            )

            self.combo_rol.configure(
                values=["Error al cargar roles"]
            )

            self.combo_rol.set(
                "Error al cargar roles"
            )

    # =====================================================
    # CARGAR DATOS
    # =====================================================

    def cargar_datos(self):

        self.entry_nombres.insert(
            0,
            self.usuario.get(
                "nombres",
                ""
            )
        )

        self.entry_apellidos.insert(
            0,
            self.usuario.get(
                "apellidos",
                ""
            )
        )

        self.entry_usuario.insert(
            0,
            self.usuario.get(
                "usuario",
                ""
            )
        )

        self.entry_correo.insert(
            0,
            self.usuario.get(
                "correo",
                ""
            ) or ""
        )

        # =================================================
        # SELECCIONAR ROL
        # =================================================

        id_rol = self.usuario.get(
            "id_rol"
        )

        for rol in self.roles:

            if rol["id_rol"] == id_rol:

                self.combo_rol.set(
                    rol["nombre"]
                )

                break

    # =====================================================
    # OBTENER ID DEL ROL
    # =====================================================

    def obtener_id_rol(self):

        rol_seleccionado = (
            self.combo_rol.get().strip()
        )

        if not rol_seleccionado:
            return None

        if rol_seleccionado in (
            "Seleccione un rol",
            "No hay roles activos",
            "Error al cargar roles",
            "Cargando roles..."
        ):
            return None

        for rol in self.roles:

            if rol["nombre"] == rol_seleccionado:

                return rol["id_rol"]

        return None

    # =====================================================
    # GUARDAR
    # =====================================================

    def guardar(self):

        # =================================================
        # OBTENER DATOS
        # =================================================

        nombres = (
            self.entry_nombres.get().strip()
        )

        apellidos = (
            self.entry_apellidos.get().strip()
        )

        usuario = (
            self.entry_usuario.get().strip()
        )

        clave = (
            self.entry_clave.get()
        )

        correo = (
            self.entry_correo.get().strip()
        )

        id_rol = self.obtener_id_rol()

        # =================================================
        # VALIDAR NOMBRES
        # =================================================

        if not nombres:

            messagebox.showwarning(
                "Campo obligatorio",
                "Ingrese los nombres.",
                parent=self
            )

            self.entry_nombres.focus()

            return

        # =================================================
        # VALIDAR APELLIDOS
        # =================================================

        if not apellidos:

            messagebox.showwarning(
                "Campo obligatorio",
                "Ingrese los apellidos.",
                parent=self
            )

            self.entry_apellidos.focus()

            return

        # =================================================
        # VALIDAR USUARIO
        # =================================================

        if not usuario:

            messagebox.showwarning(
                "Campo obligatorio",
                "Ingrese el nombre de usuario.",
                parent=self
            )

            self.entry_usuario.focus()

            return

        # =================================================
        # VALIDAR CLAVE AL CREAR
        # =================================================

        if not self.usuario and not clave:

            messagebox.showwarning(
                "Campo obligatorio",
                "Ingrese la clave del usuario.",
                parent=self
            )

            self.entry_clave.focus()

            return

        # =================================================
        # VALIDAR ROL
        # =================================================

        if id_rol is None:

            messagebox.showwarning(
                "Rol requerido",
                "Seleccione un rol para el usuario.",
                parent=self
            )

            self.combo_rol.focus()

            return

        # =================================================
        # CREAR USUARIO
        # =================================================

        if not self.usuario:

            resultado = (
                UsuarioModel.crear_usuario(
                    nombres,
                    apellidos,
                    usuario,
                    clave,
                    correo,
                    id_rol
                )
            )

            if resultado:

                messagebox.showinfo(
                    "Usuario creado",
                    (
                        f"El usuario '{usuario}' "
                        "fue creado correctamente."
                    ),
                    parent=self
                )

                if self.callback:
                    self.callback()

                self.destroy()

            else:

                messagebox.showerror(
                    "Error",
                    (
                        "No se pudo crear el usuario.\n\n"
                        "Verifique que el nombre de usuario "
                        "no esté registrado."
                    ),
                    parent=self
                )

        # =================================================
        # ACTUALIZAR USUARIO
        # =================================================

        else:

            id_usuario = self.usuario.get(
                "id_usuario"
            )

            resultado = (
                UsuarioModel.actualizar_usuario(
                    id_usuario,
                    nombres,
                    apellidos,
                    usuario,
                    clave,
                    correo,
                    id_rol
                )
            )

            if resultado:

                messagebox.showinfo(
                    "Usuario actualizado",
                    (
                        f"El usuario '{usuario}' "
                        "fue actualizado correctamente."
                    ),
                    parent=self
                )

                if self.callback:
                    self.callback()

                self.destroy()

            else:

                messagebox.showerror(
                    "Error",
                    (
                        "No se pudo actualizar el usuario.\n\n"
                        "Verifique que el nombre de usuario "
                        "no esté registrado."
                    ),
                    parent=self
                )

    # =====================================================
    # CANCELAR
    # =====================================================

    def cancelar(self):

        self.destroy()