import customtkinter as ctk
from tkinter import messagebox


class FormularioDepartamento(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        departamento=None,
        callback=None
    ):

        super().__init__(
            parent
        )

        # =====================================================
        # CONFIGURACIÓN
        # =====================================================

        self.parent = parent

        self.departamento = departamento

        self.callback = callback

        self.title(
            "Nuevo Departamento"
            if departamento is None
            else "Editar Departamento"
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
        # MODELO
        # =====================================================

        from app.models.departamento_model import DepartamentoModel

        self.model = DepartamentoModel()

        # =====================================================
        # CREAR INTERFAZ
        # =====================================================

        self.crear_interfaz()

        # =====================================================
        # CARGAR DATOS SI ES EDICIÓN
        # =====================================================

        if self.departamento is not None:

            self.cargar_datos()

        # =====================================================
        # POSICIONAR DELANTE
        # =====================================================

        self.after(
            100,
            self.mostrar_delante
        )


    # =====================================================
    # MOSTRAR VENTANA DELANTE
    # =====================================================

    def mostrar_delante(
        self
    ):

        try:

            self.lift()

            self.focus_force()

        except Exception:

            pass


    # =====================================================
    # CREAR INTERFAZ
    # =====================================================

    def crear_interfaz(
        self
    ):

        # =================================================
        # TÍTULO
        # =================================================

        titulo = ctk.CTkLabel(
            self,
            text=(
                "Nuevo Departamento"
                if self.departamento is None
                else "Editar Departamento"
            ),
            font=(
                "Segoe UI",
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
        # FRAME DEL FORMULARIO
        # =================================================

        frame_formulario = ctk.CTkFrame(
            self
        )

        frame_formulario.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=10
        )


        # =================================================
        # CAMPO NOMBRE
        # =================================================

        label_nombre = ctk.CTkLabel(
            frame_formulario,
            text="Nombre del departamento:"
        )

        label_nombre.pack(
            anchor="w",
            padx=30,
            pady=(
                25,
                5
            )
        )


        self.entry_nombre = ctk.CTkEntry(
            frame_formulario,
            width=450,
            placeholder_text="Ingrese el nombre del departamento"
        )

        self.entry_nombre.pack(
            padx=30,
            pady=5
        )


        # =================================================
        # CAMPO DESCRIPCIÓN
        # =================================================

        label_descripcion = ctk.CTkLabel(
            frame_formulario,
            text="Descripción:"
        )

        label_descripcion.pack(
            anchor="w",
            padx=30,
            pady=(
                20,
                5
            )
        )


        self.entry_descripcion = ctk.CTkEntry(
            frame_formulario,
            width=450,
            placeholder_text="Ingrese una descripción"
        )

        self.entry_descripcion.pack(
            padx=30,
            pady=5
        )


        # =================================================
        # FRAME DE BOTONES
        # =================================================

        frame_botones = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        frame_botones.pack(
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
            command=self.destroy
        )

        boton_cancelar.pack(
            side="left",
            padx=10
        )


    # =====================================================
    # CARGAR DATOS PARA EDITAR
    # =====================================================

    def cargar_datos(
        self
    ):

        try:

            # =================================================
            # ESTRUCTURA ESPERADA
            #
            # 0 = id_departamento
            # 1 = nombre
            # 2 = descripcion
            # 3 = activo
            # 4 = fecha_creacion
            # =================================================

            self.entry_nombre.insert(
                0,
                self.departamento[1]
                if self.departamento[1] is not None
                else ""
            )

            self.entry_descripcion.insert(
                0,
                self.departamento[2]
                if self.departamento[2] is not None
                else ""
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los datos del departamento:\n\n{e}",
                parent=self
            )


    # =====================================================
    # GUARDAR DEPARTAMENTO
    # =====================================================

    def guardar(
        self
    ):

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


        # =================================================
        # VALIDAR NOMBRE
        # =================================================

        if not nombre:

            messagebox.showwarning(
                "Advertencia",
                "Ingrese el nombre del departamento.",
                parent=self
            )

            self.entry_nombre.focus()

            return


        # =================================================
        # GUARDAR NUEVO
        # =================================================

        try:

            if self.departamento is None:

                self.model.crear(
                    nombre,
                    descripcion
                )

                mensaje = (
                    "Departamento creado correctamente."
                )


            # =================================================
            # ACTUALIZAR EXISTENTE
            # =================================================

            else:

                id_departamento = (
                    self.departamento[0]
                )

                self.model.actualizar(
                    id_departamento,
                    nombre,
                    descripcion
                )

                mensaje = (
                    "Departamento actualizado correctamente."
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
            # ACTUALIZAR LISTA PRINCIPAL
            # =================================================

            if self.callback is not None:

                self.callback()


            # =================================================
            # CERRAR FORMULARIO
            # =================================================

            self.destroy()


        except Exception as e:

            mensaje_error = str(
                e
            )

            # =================================================
            # ERROR POR NOMBRE DUPLICADO
            # =================================================

            if (
                "Duplicate entry"
                in mensaje_error
            ):

                messagebox.showwarning(
                    "Departamento duplicado",
                    "Ya existe un departamento con ese nombre.",
                    parent=self
                )

                return


            # =================================================
            # OTROS ERRORES
            # =================================================

            messagebox.showerror(
                "Error",
                (
                    "No se pudo guardar el departamento:"
                    f"\n\n{mensaje_error}"
                ),
                parent=self
            )