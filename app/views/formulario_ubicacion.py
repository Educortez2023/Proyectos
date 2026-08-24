import customtkinter as ctk
from tkinter import messagebox

from app.models.ubicacion_model import UbicacionModel


class FormularioUbicacion(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        ubicacion=None,
        callback=None
    ):

        super().__init__(parent)

        # =====================================================
        # CONFIGURACIÓN
        # =====================================================

        self.parent = parent

        self.ubicacion = ubicacion

        self.callback = callback

        self.model = UbicacionModel()

        # =====================================================
        # DETERMINAR MODO
        # =====================================================

        self.modo_edicion = (
            ubicacion is not None
        )

        # =====================================================
        # CONFIGURACIÓN DE VENTANA
        # =====================================================

        if self.modo_edicion:

            self.title(
                "Editar Ubicación"
            )

        else:

            self.title(
                "Nueva Ubicación"
            )

        self.geometry(
            "600x450"
        )

        self.minsize(
            550,
            400
        )

        self.transient(
            parent
        )

        # =====================================================
        # CREAR INTERFAZ
        # =====================================================

        self.crear_interfaz()

        # =====================================================
        # CARGAR DATOS SI ES EDICIÓN
        # =====================================================

        if self.modo_edicion:

            self.cargar_datos()

        # =====================================================
        # MOSTRAR DELANTE
        # =====================================================

        self.after(
            100,
            self.mostrar_delante
        )


    # =====================================================
    # MOSTRAR VENTANA DELANTE
    # =====================================================

    def mostrar_delante(self):

        try:

            self.lift()

            self.focus_force()

        except Exception:

            pass


    # =====================================================
    # CREAR INTERFAZ
    # =====================================================

    def crear_interfaz(self):

        # =================================================
        # TÍTULO
        # =================================================

        titulo = ctk.CTkLabel(
            self,
            text=(
                "Editar Ubicación"
                if self.modo_edicion
                else "Nueva Ubicación"
            ),
            font=(
                "Arial",
                24,
                "bold"
            )
        )

        titulo.pack(
            pady=(
                25,
                20
            )
        )


        # =================================================
        # FRAME PRINCIPAL
        # =================================================

        frame_formulario = ctk.CTkFrame(
            self
        )

        frame_formulario.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )


        # =================================================
        # CAMPO NOMBRE
        # =================================================

        label_nombre = ctk.CTkLabel(
            frame_formulario,
            text="Nombre de la ubicación:",
            font=(
                "Arial",
                14,
                "bold"
            )
        )

        label_nombre.pack(
            anchor="w",
            padx=30,
            pady=(
                20,
                5
            )
        )


        self.entry_nombre = ctk.CTkEntry(
            frame_formulario,
            placeholder_text=(
                "Ejemplo: Laboratorio de Computación"
            ),
            height=40
        )

        self.entry_nombre.pack(
            fill="x",
            padx=30,
            pady=(
                0,
                15
            )
        )


        # =================================================
        # CAMPO DESCRIPCIÓN
        # =================================================

        label_descripcion = ctk.CTkLabel(
            frame_formulario,
            text="Descripción:",
            font=(
                "Arial",
                14,
                "bold"
            )
        )

        label_descripcion.pack(
            anchor="w",
            padx=30,
            pady=(
                5,
                5
            )
        )


        self.entry_descripcion = ctk.CTkEntry(
            frame_formulario,
            placeholder_text=(
                "Descripción de la ubicación"
            ),
            height=40
        )

        self.entry_descripcion.pack(
            fill="x",
            padx=30,
            pady=(
                0,
                15
            )
        )


        # =================================================
        # ESTADO
        # =================================================

        label_estado = ctk.CTkLabel(
            frame_formulario,
            text="Estado:",
            font=(
                "Arial",
                14,
                "bold"
            )
        )

        label_estado.pack(
            anchor="w",
            padx=30,
            pady=(
                5,
                5
            )
        )


        self.combo_estado = ctk.CTkComboBox(
            frame_formulario,
            values=[
                "Activo",
                "Inactivo"
            ],
            height=40
        )

        self.combo_estado.pack(
            fill="x",
            padx=30,
            pady=(
                0,
                20
            )
        )

        self.combo_estado.set(
            "Activo"
        )


        # =================================================
        # FRAME DE BOTONES
        # =================================================

        frame_botones = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        frame_botones.pack(
            fill="x",
            padx=30,
            pady=20
        )


        # =================================================
        # BOTÓN GUARDAR
        # =================================================

        boton_guardar = ctk.CTkButton(
            frame_botones,
            text="💾 Guardar",
            width=150,
            height=40,
            command=self.guardar
        )

        boton_guardar.pack(
            side="left",
            padx=10
        )


        # =================================================
        # BOTÓN CANCELAR
        # =================================================

        boton_cancelar = ctk.CTkButton(
            frame_botones,
            text="❌ Cancelar",
            width=150,
            height=40,
            fg_color="gray",
            hover_color="#555555",
            command=self.cerrar
        )

        boton_cancelar.pack(
            side="right",
            padx=10
        )


    # =====================================================
    # CARGAR DATOS PARA EDITAR
    # =====================================================

    def cargar_datos(self):

        try:

            # =================================================
            # DATOS RECIBIDOS DESDE LA TABLA
            #
            # 0 = ID
            # 1 = Nombre
            # 2 = Descripción
            # 3 = Estado
            # =================================================

            self.entry_nombre.delete(
                0,
                "end"
            )

            self.entry_nombre.insert(
                0,
                self.ubicacion[1]
            )


            self.entry_descripcion.delete(
                0,
                "end"
            )

            self.entry_descripcion.insert(
                0,
                self.ubicacion[2]
            )


            self.combo_estado.set(
                self.ubicacion[3]
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                (
                    "No se pudieron cargar "
                    "los datos de la ubicación:\n\n"
                    f"{e}"
                ),
                parent=self
            )


    # =====================================================
    # GUARDAR UBICACIÓN
    # =====================================================

    def guardar(self):

        # =================================================
        # OBTENER DATOS
        # =================================================

        nombre = (
            self.entry_nombre
            .get()
            .strip()
        )

        descripcion = (
            self.entry_descripcion
            .get()
            .strip()
        )

        estado_texto = (
            self.combo_estado
            .get()
        )


        # =================================================
        # VALIDAR NOMBRE
        # =================================================

        if not nombre:

            messagebox.showwarning(
                "Campo obligatorio",
                (
                    "Ingrese el nombre "
                    "de la ubicación."
                ),
                parent=self
            )

            self.entry_nombre.focus()

            return


        # =================================================
        # CONVERTIR ESTADO
        # =================================================

        activo = (
            1
            if estado_texto == "Activo"
            else 0
        )


        # =================================================
        # GUARDAR
        # =================================================

        try:

            # =================================================
            # MODO CREAR
            # =================================================

            if not self.modo_edicion:

                self.model.crear(
                    nombre,
                    descripcion
                )


                messagebox.showinfo(
                    "Éxito",
                    (
                        "La ubicación se creó "
                        "correctamente."
                    ),
                    parent=self
                )


            # =================================================
            # MODO EDITAR
            # =================================================

            else:

                id_ubicacion = (
                    self.ubicacion[0]
                )

                self.model.actualizar(
                    id_ubicacion,
                    nombre,
                    descripcion,
                    activo
                )


                messagebox.showinfo(
                    "Éxito",
                    (
                        "La ubicación se actualizó "
                        "correctamente."
                    ),
                    parent=self
                )


            # =================================================
            # ACTUALIZAR TABLA
            # =================================================

            if self.callback:

                self.callback()


            # =================================================
            # CERRAR FORMULARIO
            # =================================================

            self.cerrar()


        except Exception as e:

            messagebox.showerror(
                "Error",
                (
                    "No se pudo guardar "
                    "la ubicación:\n\n"
                    f"{e}"
                ),
                parent=self
            )


    # =====================================================
    # CERRAR FORMULARIO
    # =====================================================

    def cerrar(self):

        try:

            if self.grab_current():

                self.grab_release()

        except Exception:

            pass


        self.destroy()