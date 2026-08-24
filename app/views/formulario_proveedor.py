import customtkinter as ctk
from tkinter import messagebox

from app.models.proveedor_model import ProveedorModel


class FormularioProveedor(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        proveedor=None,
        callback=None
    ):

        super().__init__(parent)

        self.parent = parent
        self.proveedor = proveedor
        self.callback = callback

        # =====================================================
        # CONFIGURACIÓN
        # =====================================================

        if proveedor:

            self.title("Editar Proveedor")

        else:

            self.title("Nuevo Proveedor")

        self.geometry("650x600")
        self.minsize(600, 550)

        self.transient(parent)

        self.grab_set()

        self.crear_interfaz()

        # =====================================================
        # CARGAR DATOS SI ES EDICIÓN
        # =====================================================

        if self.proveedor:

            self.cargar_datos()

    # =====================================================
    # CREAR INTERFAZ
    # =====================================================

    def crear_interfaz(self):

        # =====================================================
        # TÍTULO
        # =====================================================

        titulo = ctk.CTkLabel(
            self,
            text=(
                "EDITAR PROVEEDOR"
                if self.proveedor
                else "NUEVO PROVEEDOR"
            ),
            font=("Arial", 24, "bold")
        )

        titulo.pack(
            pady=(25, 20)
        )

        # =====================================================
        # CONTENEDOR PRINCIPAL
        # =====================================================

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
        # EMPRESA
        # =====================================================

        lbl_empresa = ctk.CTkLabel(
            frame,
            text="Empresa *",
            font=("Arial", 14, "bold")
        )

        lbl_empresa.pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        self.entry_empresa = ctk.CTkEntry(
            frame,
            placeholder_text="Nombre de la empresa",
            width=500,
            height=40
        )

        self.entry_empresa.pack(
            padx=25,
            pady=(0, 10)
        )

        # =====================================================
        # CONTACTO
        # =====================================================

        lbl_contacto = ctk.CTkLabel(
            frame,
            text="Contacto",
            font=("Arial", 14, "bold")
        )

        lbl_contacto.pack(
            anchor="w",
            padx=25,
            pady=(5, 5)
        )

        self.entry_contacto = ctk.CTkEntry(
            frame,
            placeholder_text="Nombre de la persona de contacto",
            width=500,
            height=40
        )

        self.entry_contacto.pack(
            padx=25,
            pady=(0, 10)
        )

        # =====================================================
        # TELÉFONO
        # =====================================================

        lbl_telefono = ctk.CTkLabel(
            frame,
            text="Teléfono",
            font=("Arial", 14, "bold")
        )

        lbl_telefono.pack(
            anchor="w",
            padx=25,
            pady=(5, 5)
        )

        self.entry_telefono = ctk.CTkEntry(
            frame,
            placeholder_text="Número de teléfono",
            width=500,
            height=40
        )

        self.entry_telefono.pack(
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
            placeholder_text="correo@empresa.com",
            width=500,
            height=40
        )

        self.entry_correo.pack(
            padx=25,
            pady=(0, 10)
        )

        # =====================================================
        # DIRECCIÓN
        # =====================================================

        lbl_direccion = ctk.CTkLabel(
            frame,
            text="Dirección",
            font=("Arial", 14, "bold")
        )

        lbl_direccion.pack(
            anchor="w",
            padx=25,
            pady=(5, 5)
        )

        self.entry_direccion = ctk.CTkEntry(
            frame,
            placeholder_text="Dirección del proveedor",
            width=500,
            height=40
        )

        self.entry_direccion.pack(
            padx=25,
            pady=(0, 20)
        )

        # =====================================================
        # FRAME BOTONES
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
                if self.proveedor
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
    # CARGAR DATOS
    # =====================================================

    def cargar_datos(self):

        self.entry_empresa.insert(
            0,
            self.proveedor.get(
                "empresa",
                ""
            )
        )

        self.entry_contacto.insert(
            0,
            self.proveedor.get(
                "contacto",
                ""
            )
        )

        self.entry_telefono.insert(
            0,
            self.proveedor.get(
                "telefono",
                ""
            )
        )

        self.entry_correo.insert(
            0,
            self.proveedor.get(
                "correo",
                ""
            )
        )

        self.entry_direccion.insert(
            0,
            self.proveedor.get(
                "direccion",
                ""
            )
        )

    # =====================================================
    # GUARDAR
    # =====================================================

    def guardar(self):

        # =================================================
        # OBTENER DATOS
        # =================================================

        empresa = self.entry_empresa.get().strip()

        contacto = self.entry_contacto.get().strip()

        telefono = self.entry_telefono.get().strip()

        correo = self.entry_correo.get().strip()

        direccion = self.entry_direccion.get().strip()

        # =================================================
        # VALIDAR EMPRESA
        # =================================================

        if not empresa:

            messagebox.showwarning(
                "Campo obligatorio",
                "Ingrese el nombre de la empresa.",
                parent=self
            )

            self.entry_empresa.focus()

            return

        # =================================================
        # CREAR
        # =================================================

        if not self.proveedor:

            resultado = (
                ProveedorModel.crear_proveedor(
                    empresa,
                    contacto,
                    telefono,
                    correo,
                    direccion
                )
            )

            if resultado:

                messagebox.showinfo(
                    "Proveedor creado",
                    (
                        f"El proveedor '{empresa}' "
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
                    "No se pudo crear el proveedor.",
                    parent=self
                )

        # =================================================
        # ACTUALIZAR
        # =================================================

        else:

            id_proveedor = self.proveedor.get(
                "id_proveedor"
            )

            resultado = (
                ProveedorModel.actualizar_proveedor(
                    id_proveedor,
                    empresa,
                    contacto,
                    telefono,
                    correo,
                    direccion
                )
            )

            if resultado:

                messagebox.showinfo(
                    "Proveedor actualizado",
                    (
                        f"El proveedor '{empresa}' "
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
                    "No se pudo actualizar el proveedor.",
                    parent=self
                )

    # =====================================================
    # CANCELAR
    # =====================================================

    def cancelar(self):

        self.destroy()