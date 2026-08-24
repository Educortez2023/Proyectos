import customtkinter as ctk
from tkinter import messagebox

from app.models.marca_model import MarcaModel


class FormularioMarca(ctk.CTkToplevel):

    def __init__(self, parent, marca=None, callback=None):
        super().__init__(parent)

        self.parent = parent
        self.marca = marca
        self.callback = callback

        # =====================================================
        # CONFIGURACIÓN DE LA VENTANA
        # =====================================================

        if self.marca:
            self.title("Editar Marca")
        else:
            self.title("Nueva Marca")

        self.geometry("500x300")
        self.resizable(False, False)

        # Mantener la ventana al frente
        self.transient(parent)
        self.grab_set()

        self.crear_interfaz()

        # Si estamos editando, cargar los datos
        if self.marca:
            self.cargar_datos()

    # =====================================================
    # CREAR INTERFAZ
    # =====================================================

    def crear_interfaz(self):

        # -------------------------------------------------
        # TÍTULO
        # -------------------------------------------------

        titulo = ctk.CTkLabel(
            self,
            text="EDITAR MARCA" if self.marca else "NUEVA MARCA",
            font=("Arial", 24, "bold")
        )

        titulo.pack(pady=(25, 20))

        # -------------------------------------------------
        # CONTENEDOR
        # -------------------------------------------------

        frame = ctk.CTkFrame(self)

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )

        # -------------------------------------------------
        # NOMBRE
        # -------------------------------------------------

        lbl_nombre = ctk.CTkLabel(
            frame,
            text="Nombre de la marca:",
            font=("Arial", 14)
        )

        lbl_nombre.pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        self.entry_nombre = ctk.CTkEntry(
            frame,
            placeholder_text="Ingrese el nombre de la marca",
            height=40,
            font=("Arial", 14)
        )

        self.entry_nombre.pack(
            fill="x",
            padx=25
        )

        # -------------------------------------------------
        # BOTONES
        # -------------------------------------------------

        frame_botones = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        frame_botones.pack(
            fill="x",
            padx=25,
            pady=30
        )

        btn_guardar = ctk.CTkButton(
            frame_botones,
            text="Guardar",
            width=140,
            height=40,
            font=("Arial", 14, "bold"),
            command=self.guardar
        )

        btn_guardar.pack(
            side="left",
            expand=True,
            padx=(0, 10)
        )

        btn_cancelar = ctk.CTkButton(
            frame_botones,
            text="Cancelar",
            width=140,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="gray",
            hover_color="#555555",
            command=self.destroy
        )

        btn_cancelar.pack(
            side="right",
            expand=True,
            padx=(10, 0)
        )

    # =====================================================
    # CARGAR DATOS PARA EDITAR
    # =====================================================

    def cargar_datos(self):

        try:
            nombre = self.marca.get("nombre", "")

            self.entry_nombre.delete(0, "end")
            self.entry_nombre.insert(0, nombre)

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los datos de la marca.\n\n{e}",
                parent=self
            )

    # =====================================================
    # GUARDAR
    # =====================================================

    def guardar(self):

        nombre = self.entry_nombre.get().strip()

        # -------------------------------------------------
        # VALIDAR NOMBRE
        # -------------------------------------------------

        if not nombre:

            messagebox.showwarning(
                "Campo obligatorio",
                "Debe ingresar el nombre de la marca.",
                parent=self
            )

            self.entry_nombre.focus()
            return

        # -------------------------------------------------
        # VALIDAR LONGITUD
        # -------------------------------------------------

        if len(nombre) > 100:

            messagebox.showwarning(
                "Nombre demasiado largo",
                "El nombre de la marca no puede superar los 100 caracteres.",
                parent=self
            )

            self.entry_nombre.focus()
            return

        # -------------------------------------------------
        # OBTENER ID SI ESTAMOS EDITANDO
        # -------------------------------------------------

        id_marca = None

        if self.marca:

            id_marca = self.marca.get("id_marca")

        # -------------------------------------------------
        # VERIFICAR DUPLICADOS
        # -------------------------------------------------

        if MarcaModel.existe_nombre(nombre, id_marca):

            messagebox.showwarning(
                "Marca existente",
                f"La marca '{nombre}' ya existe.",
                parent=self
            )

            self.entry_nombre.focus()
            return

        # -------------------------------------------------
        # CREAR MARCA
        # -------------------------------------------------

        if not self.marca:

            resultado = MarcaModel.crear_marca(nombre)

            if resultado:

                messagebox.showinfo(
                    "Marca registrada",
                    "La marca se registró correctamente.",
                    parent=self
                )

                if self.callback:
                    self.callback()

                self.destroy()

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudo registrar la marca.",
                    parent=self
                )

        # -------------------------------------------------
        # ACTUALIZAR MARCA
        # -------------------------------------------------

        else:

            resultado = MarcaModel.actualizar_marca(
                id_marca,
                nombre
            )

            if resultado:

                messagebox.showinfo(
                    "Marca actualizada",
                    "La marca se actualizó correctamente.",
                    parent=self
                )

                if self.callback:
                    self.callback()

                self.destroy()

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudo actualizar la marca.",
                    parent=self
                )