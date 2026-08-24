import customtkinter as ctk
from tkinter import messagebox

from app.models.responsable_model import ResponsableModel


class FormularioResponsable(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        responsable=None,
        callback=None
    ):

        super().__init__(parent)

        # =====================================================
        # CONFIGURACIÓN DE LA VENTANA
        # =====================================================

        self.parent = parent

        self.responsable = responsable

        self.callback = callback

        self.model = ResponsableModel()

        self.title(
            "Nuevo Responsable"
            if responsable is None
            else "Editar Responsable"
        )

        self.geometry(
            "650x650"
        )

        self.minsize(
            600,
            600
        )

        self.transient(parent)

        # =====================================================
        # VARIABLES
        # =====================================================

        self.departamentos = []

        self.cargos = []

        # =====================================================
        # CREAR INTERFAZ
        # =====================================================

        self.crear_interfaz()

        # =====================================================
        # CARGAR COMBOS
        # =====================================================

        self.cargar_departamentos()

        self.cargar_cargos()

        # =====================================================
        # CARGAR DATOS SI ES EDICIÓN
        # =====================================================

        if self.responsable is not None:

            self.cargar_datos()

        # =====================================================
        # POSICIONAR VENTANA
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

        # =====================================================
        # TÍTULO
        # =====================================================

        titulo = ctk.CTkLabel(
            self,
            text=(
                "Nuevo Responsable"
                if self.responsable is None
                else "Editar Responsable"
            ),
            font=(
                "Arial",
                24,
                "bold"
            )
        )

        titulo.pack(
            pady=(
                20,
                15
            )
        )


        # =====================================================
        # FRAME PRINCIPAL
        # =====================================================

        frame = ctk.CTkFrame(
            self
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )


        # =====================================================
        # NOMBRES
        # =====================================================

        label_nombres = ctk.CTkLabel(
            frame,
            text="Nombres:"
        )

        label_nombres.grid(
            row=0,
            column=0,
            padx=15,
            pady=10,
            sticky="e"
        )


        self.entry_nombres = ctk.CTkEntry(
            frame,
            width=350,
            placeholder_text="Ingrese los nombres"
        )

        self.entry_nombres.grid(
            row=0,
            column=1,
            padx=15,
            pady=10,
            sticky="w"
        )


        # =====================================================
        # APELLIDOS
        # =====================================================

        label_apellidos = ctk.CTkLabel(
            frame,
            text="Apellidos:"
        )

        label_apellidos.grid(
            row=1,
            column=0,
            padx=15,
            pady=10,
            sticky="e"
        )


        self.entry_apellidos = ctk.CTkEntry(
            frame,
            width=350,
            placeholder_text="Ingrese los apellidos"
        )

        self.entry_apellidos.grid(
            row=1,
            column=1,
            padx=15,
            pady=10,
            sticky="w"
        )


        # =====================================================
        # CÉDULA
        # =====================================================

        label_cedula = ctk.CTkLabel(
            frame,
            text="Documento / Cédula:"
        )

        label_cedula.grid(
            row=2,
            column=0,
            padx=15,
            pady=10,
            sticky="e"
        )


        self.entry_cedula = ctk.CTkEntry(
            frame,
            width=350,
            placeholder_text="Ingrese el documento"
        )

        self.entry_cedula.grid(
            row=2,
            column=1,
            padx=15,
            pady=10,
            sticky="w"
        )


        # =====================================================
        # CORREO
        # =====================================================

        label_correo = ctk.CTkLabel(
            frame,
            text="Correo:"
        )

        label_correo.grid(
            row=3,
            column=0,
            padx=15,
            pady=10,
            sticky="e"
        )


        self.entry_correo = ctk.CTkEntry(
            frame,
            width=350,
            placeholder_text="Ingrese el correo electrónico"
        )

        self.entry_correo.grid(
            row=3,
            column=1,
            padx=15,
            pady=10,
            sticky="w"
        )


        # =====================================================
        # TELÉFONO
        # =====================================================

        label_telefono = ctk.CTkLabel(
            frame,
            text="Teléfono:"
        )

        label_telefono.grid(
            row=4,
            column=0,
            padx=15,
            pady=10,
            sticky="e"
        )


        self.entry_telefono = ctk.CTkEntry(
            frame,
            width=350,
            placeholder_text="Ingrese el teléfono"
        )

        self.entry_telefono.grid(
            row=4,
            column=1,
            padx=15,
            pady=10,
            sticky="w"
        )


        # =====================================================
        # DEPARTAMENTO
        # =====================================================

        label_departamento = ctk.CTkLabel(
            frame,
            text="Departamento:"
        )

        label_departamento.grid(
            row=5,
            column=0,
            padx=15,
            pady=10,
            sticky="e"
        )


        self.combo_departamento = ctk.CTkComboBox(
            frame,
            width=350,
            state="readonly"
        )

        self.combo_departamento.grid(
            row=5,
            column=1,
            padx=15,
            pady=10,
            sticky="w"
        )


        # =====================================================
        # CARGO
        # =====================================================

        label_cargo = ctk.CTkLabel(
            frame,
            text="Cargo:"
        )

        label_cargo.grid(
            row=6,
            column=0,
            padx=15,
            pady=10,
            sticky="e"
        )


        self.combo_cargo = ctk.CTkComboBox(
            frame,
            width=350,
            state="readonly"
        )

        self.combo_cargo.grid(
            row=6,
            column=1,
            padx=15,
            pady=10,
            sticky="w"
        )


        # =====================================================
        # FRAME DE BOTONES
        # =====================================================

        frame_botones = ctk.CTkFrame(
            self
        )

        frame_botones.pack(
            fill="x",
            padx=30,
            pady=20
        )


        # =====================================================
        # BOTÓN GUARDAR
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
        # BOTÓN CANCELAR
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


        # =====================================================
        # ENTER PARA GUARDAR
        # =====================================================

        self.bind(
            "<Return>",
            lambda event: self.guardar()
        )


        # =====================================================
        # ESC PARA CERRAR
        # =====================================================

        self.bind(
            "<Escape>",
            lambda event: self.cerrar()
        )


        # =====================================================
        # CIERRE DE VENTANA
        # =====================================================

        self.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar
        )


    # =====================================================
    # CARGAR DEPARTAMENTOS
    # =====================================================

    def cargar_departamentos(self):

        try:

            self.departamentos = (
                self.model.listar_departamentos()
            )

            nombres = []

            for departamento in self.departamentos:

                nombres.append(
                    str(
                        departamento[1]
                    )
                )

            self.combo_departamento.configure(
                values=nombres
            )

            if nombres:

                self.combo_departamento.set(
                    "Seleccione un departamento"
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                (
                    "No se pudieron cargar "
                    "los departamentos:\n\n"
                    f"{e}"
                ),
                parent=self
            )


    # =====================================================
    # CARGAR CARGOS
    # =====================================================

    def cargar_cargos(self):

        try:

            self.cargos = (
                self.model.listar_cargos()
            )

            nombres = []

            for cargo in self.cargos:

                nombres.append(
                    str(
                        cargo[1]
                    )
                )

            self.combo_cargo.configure(
                values=nombres
            )

            if nombres:

                self.combo_cargo.set(
                    "Seleccione un cargo"
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                (
                    "No se pudieron cargar "
                    "los cargos:\n\n"
                    f"{e}"
                ),
                parent=self
            )


    # =====================================================
    # CARGAR DATOS PARA EDITAR
    # =====================================================

    def cargar_datos(self):

        try:

            # =================================================
            # ESTRUCTURA ESPERADA DE RESPONSABLE
            #
            # 0  = id_responsable
            # 1  = nombres
            # 2  = apellidos
            # 3  = cedula
            # 4  = correo
            # 5  = telefono
            # 6  = departamento
            # 7  = cargo
            # 8  = id_departamento
            # 9  = id_cargo
            # 10 = activo
            # 11 = fecha_creacion
            # =================================================

            self.entry_nombres.insert(
                0,
                str(
                    self.responsable[1]
                )
            )

            self.entry_apellidos.insert(
                0,
                str(
                    self.responsable[2]
                )
            )

            if self.responsable[3] is not None:

                self.entry_cedula.insert(
                    0,
                    str(
                        self.responsable[3]
                    )
                )


            if self.responsable[4] is not None:

                self.entry_correo.insert(
                    0,
                    str(
                        self.responsable[4]
                    )
                )


            if self.responsable[5] is not None:

                self.entry_telefono.insert(
                    0,
                    str(
                        self.responsable[5]
                    )
                )


            # =================================================
            # SELECCIONAR DEPARTAMENTO
            # =================================================

            id_departamento = (
                self.responsable[8]
            )

            for departamento in self.departamentos:

                if departamento[0] == id_departamento:

                    self.combo_departamento.set(
                        str(
                            departamento[1]
                        )
                    )

                    break


            # =================================================
            # SELECCIONAR CARGO
            # =================================================

            id_cargo = (
                self.responsable[9]
            )

            for cargo in self.cargos:

                if cargo[0] == id_cargo:

                    self.combo_cargo.set(
                        str(
                            cargo[1]
                        )
                    )

                    break


        except Exception as e:

            messagebox.showerror(
                "Error",
                (
                    "No se pudieron cargar "
                    "los datos del responsable:\n\n"
                    f"{e}"
                ),
                parent=self
            )


    # =====================================================
    # OBTENER ID DEL DEPARTAMENTO
    # =====================================================

    def obtener_id_departamento(self):

        seleccionado = (
            self.combo_departamento.get()
        )

        for departamento in self.departamentos:

            if str(
                departamento[1]
            ) == seleccionado:

                return departamento[0]

        return None


    # =====================================================
    # OBTENER ID DEL CARGO
    # =====================================================

    def obtener_id_cargo(self):

        seleccionado = (
            self.combo_cargo.get()
        )

        for cargo in self.cargos:

            if str(
                cargo[1]
            ) == seleccionado:

                return cargo[0]

        return None


    # =====================================================
    # GUARDAR RESPONSABLE
    # =====================================================

    def guardar(self):

        # =====================================================
        # OBTENER DATOS
        # =====================================================

        nombres = (
            self.entry_nombres.get().strip()
        )

        apellidos = (
            self.entry_apellidos.get().strip()
        )

        cedula = (
            self.entry_cedula.get().strip()
        )

        correo = (
            self.entry_correo.get().strip()
        )

        telefono = (
            self.entry_telefono.get().strip()
        )

        id_departamento = (
            self.obtener_id_departamento()
        )

        id_cargo = (
            self.obtener_id_cargo()
        )


        # =====================================================
        # VALIDAR NOMBRES
        # =====================================================

        if not nombres:

            messagebox.showwarning(
                "Advertencia",
                "Ingrese los nombres del responsable.",
                parent=self
            )

            self.entry_nombres.focus()

            return


        # =====================================================
        # VALIDAR APELLIDOS
        # =====================================================

        if not apellidos:

            messagebox.showwarning(
                "Advertencia",
                "Ingrese los apellidos del responsable.",
                parent=self
            )

            self.entry_apellidos.focus()

            return


        # =====================================================
        # VALIDAR CÉDULA
        # =====================================================

        if not cedula:

            messagebox.showwarning(
                "Advertencia",
                "Ingrese el documento o cédula.",
                parent=self
            )

            self.entry_cedula.focus()

            return


        # =====================================================
        # VALIDAR DEPARTAMENTO
        # =====================================================

        if id_departamento is None:

            messagebox.showwarning(
                "Advertencia",
                "Seleccione un departamento.",
                parent=self
            )

            self.combo_departamento.focus()

            return


        # =====================================================
        # VALIDAR CARGO
        # =====================================================

        if id_cargo is None:

            messagebox.showwarning(
                "Advertencia",
                "Seleccione un cargo.",
                parent=self
            )

            self.combo_cargo.focus()

            return


        # =====================================================
        # GUARDAR NUEVO RESPONSABLE
        # =====================================================

        try:

            if self.responsable is None:

                self.model.crear(
                    nombres,
                    apellidos,
                    cedula,
                    correo,
                    telefono,
                    id_departamento,
                    id_cargo
                )

                mensaje = (
                    "Responsable creado "
                    "correctamente."
                )


            # =================================================
            # ACTUALIZAR RESPONSABLE
            # =================================================

            else:

                id_responsable = (
                    self.responsable[0]
                )

                self.model.actualizar(
                    id_responsable,
                    nombres,
                    apellidos,
                    cedula,
                    correo,
                    telefono,
                    id_departamento,
                    id_cargo
                )

                mensaje = (
                    "Responsable actualizado "
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
            # ACTUALIZAR VENTANA PRINCIPAL
            # =================================================

            if self.callback is not None:

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
                    "el responsable:\n\n"
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