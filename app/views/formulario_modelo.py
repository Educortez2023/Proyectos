import customtkinter as ctk
from tkinter import messagebox

from app.models.modelo_model import ModeloModel
from app.models.marca_model import MarcaModel


class FormularioModelo(ctk.CTkToplevel):

    def __init__(self, parent, modelo=None, callback=None):
        super().__init__(parent)

        self.parent = parent
        self.modelo = modelo
        self.callback = callback

        # =====================================================
        # CONFIGURACIÓN DE LA VENTANA
        # =====================================================

        if modelo:
            self.title("Editar Modelo")
        else:
            self.title("Nuevo Modelo")

        self.geometry("550x400")
        self.minsize(500, 350)

        self.transient(parent)
        self.grab_set()

        self.crear_interfaz()
        self.cargar_marcas()

        if self.modelo:
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
                "EDITAR MODELO"
                if self.modelo
                else "NUEVO MODELO"
            ),
            font=("Arial", 24, "bold")
        )

        titulo.pack(pady=(25, 20))

        # =====================================================
        # FRAME DEL FORMULARIO
        # =====================================================

        frame_formulario = ctk.CTkFrame(self)

        frame_formulario.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        # =====================================================
        # NOMBRE
        # =====================================================

        lbl_nombre = ctk.CTkLabel(
            frame_formulario,
            text="Nombre del modelo:",
            font=("Arial", 14)
        )

        lbl_nombre.pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        self.entry_nombre = ctk.CTkEntry(
            frame_formulario,
            width=420,
            height=40,
            placeholder_text="Ingrese el nombre del modelo"
        )

        self.entry_nombre.pack(
            padx=25,
            pady=(0, 15)
        )

        # =====================================================
        # MARCA
        # =====================================================

        lbl_marca = ctk.CTkLabel(
            frame_formulario,
            text="Marca:",
            font=("Arial", 14)
        )

        lbl_marca.pack(
            anchor="w",
            padx=25,
            pady=(5, 5)
        )

        self.combo_marca = ctk.CTkComboBox(
            frame_formulario,
            width=420,
            height=40,
            state="readonly",
            values=["Cargando..."]
        )

        self.combo_marca.pack(
            padx=25,
            pady=(0, 20)
        )

        # =====================================================
        # FRAME DE BOTONES
        # =====================================================

        frame_botones = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        frame_botones.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        # =====================================================
        # GUARDAR
        # =====================================================

        btn_guardar = ctk.CTkButton(
            frame_botones,
            text="Guardar",
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            command=self.guardar
        )

        btn_guardar.pack(
            side="left",
            padx=10
        )

        # =====================================================
        # CANCELAR
        # =====================================================

        btn_cancelar = ctk.CTkButton(
            frame_botones,
            text="Cancelar",
            width=150,
            height=40,
            fg_color="gray",
            hover_color="#555555",
            command=self.destroy
        )

        btn_cancelar.pack(
            side="right",
            padx=10
        )

    # =====================================================
    # CARGAR MARCAS
    # =====================================================

    def cargar_marcas(self):

        try:

            marcas = MarcaModel.listar_marcas()

            self.marcas = marcas

            if not marcas:

                self.combo_marca.configure(
                    values=["No hay marcas disponibles"]
                )

                self.combo_marca.set(
                    "No hay marcas disponibles"
                )

                return

            # Crear lista de nombres
            nombres = [
                marca.get("nombre")
                for marca in marcas
            ]

            self.combo_marca.configure(
                values=nombres
            )

            # Seleccionar la primera marca
            self.combo_marca.set(
                nombres[0]
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar las marcas.\n\n{e}",
                parent=self
            )

    # =====================================================
    # CARGAR DATOS PARA EDITAR
    # =====================================================

    def cargar_datos(self):

        if not self.modelo:
            return

        # Nombre
        self.entry_nombre.insert(
            0,
            self.modelo.get("nombre", "")
        )

        # Marca
        nombre_marca = self.modelo.get("marca")

        if nombre_marca:

            self.combo_marca.set(
                nombre_marca
            )

    # =====================================================
    # OBTENER ID DE LA MARCA
    # =====================================================

    def obtener_id_marca(self):

        nombre_marca = self.combo_marca.get().strip()

        if not nombre_marca:
            return None

        for marca in self.marcas:

            if marca.get("nombre") == nombre_marca:

                return marca.get("id_marca")

        return None

    # =====================================================
    # GUARDAR
    # =====================================================

    def guardar(self):

        nombre = self.entry_nombre.get().strip()

        # =================================================
        # VALIDAR NOMBRE
        # =================================================

        if not nombre:

            messagebox.showwarning(
                "Campo requerido",
                "Ingrese el nombre del modelo.",
                parent=self
            )

            self.entry_nombre.focus()
            return

        # =================================================
        # VALIDAR MARCA
        # =================================================

        id_marca = self.obtener_id_marca()

        if not id_marca:

            messagebox.showwarning(
                "Marca requerida",
                "Seleccione una marca para el modelo.",
                parent=self
            )

            self.combo_marca.focus()
            return

        try:

            # =================================================
            # CREAR
            # =================================================

            if not self.modelo:

                resultado = ModeloModel.crear_modelo(
                    nombre,
                    id_marca
                )

                if resultado:

                    messagebox.showinfo(
                        "Modelo creado",
                        f"El modelo '{nombre}' fue creado correctamente.",
                        parent=self
                    )

                    if self.callback:
                        self.callback()

                    self.destroy()

                else:

                    messagebox.showerror(
                        "Error",
                        "No se pudo crear el modelo.",
                        parent=self
                    )

            # =================================================
            # ACTUALIZAR
            # =================================================

            else:

                id_modelo = self.modelo.get(
                    "id_modelo"
                )

                resultado = ModeloModel.actualizar_modelo(
                    id_modelo,
                    nombre,
                    id_marca
                )

                if resultado:

                    messagebox.showinfo(
                        "Modelo actualizado",
                        f"El modelo '{nombre}' fue actualizado correctamente.",
                        parent=self
                    )

                    if self.callback:
                        self.callback()

                    self.destroy()

                else:

                    messagebox.showerror(
                        "Error",
                        "No se pudo actualizar el modelo.",
                        parent=self
                    )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Ocurrió un error al guardar el modelo.\n\n{e}",
                parent=self
            )