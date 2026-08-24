import customtkinter as ctk
from tkinter import messagebox

from app.models.movimiento_model import MovimientoModel


class FormularioMovimiento(ctk.CTkToplevel):

    def __init__(self, parent, callback=None):

        super().__init__(parent)

        # =====================================================
        # CONFIGURACIÓN
        # =====================================================

        self.parent = parent
        self.callback = callback

        self.title("Registrar Movimiento")

        self.geometry("700x700")

        self.minsize(
            650,
            600
        )

        self.transient(parent)

        # =====================================================
        # MODELO
        # =====================================================

        self.model = MovimientoModel()

        # =====================================================
        # DATOS
        # =====================================================

        self.insumos = []
        self.tipos_movimiento = []
        self.responsables = []

        # =====================================================
        # CREAR INTERFAZ
        # =====================================================

        self.crear_interfaz()

        # =====================================================
        # CARGAR DATOS
        # =====================================================

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
            text="Registrar Movimiento",
            font=("Arial", 24, "bold")
        )

        titulo.pack(
            pady=(20, 10)
        )

        # =================================================
        # CONTENEDOR CON SCROLL
        # =================================================

        frame_scroll = ctk.CTkScrollableFrame(
            self,
            width=620,
            height=560
        )

        frame_scroll.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 20)
        )

        # =================================================
        # INSUMO
        # =================================================

        ctk.CTkLabel(
            frame_scroll,
            text="Insumo:",
            font=("Arial", 14)
        ).pack(
            anchor="w",
            padx=25,
            pady=(15, 5)
        )

        self.combo_insumo = ctk.CTkComboBox(
            frame_scroll,
            width=550,
            values=["Seleccione un insumo"]
        )

        self.combo_insumo.pack(
            padx=25,
            pady=(0, 10)
        )

        self.combo_insumo.set(
            "Seleccione un insumo"
        )

        self.combo_insumo.bind(
            "<<ComboboxSelected>>",
            self.actualizar_stock
        )

        # =================================================
        # STOCK ACTUAL
        # =================================================

        self.label_stock = ctk.CTkLabel(
            frame_scroll,
            text="Stock actual: --",
            font=("Arial", 16, "bold")
        )

        self.label_stock.pack(
            anchor="w",
            padx=25,
            pady=(5, 15)
        )

        # =================================================
        # TIPO DE MOVIMIENTO
        # =================================================

        ctk.CTkLabel(
            frame_scroll,
            text="Tipo de movimiento:",
            font=("Arial", 14)
        ).pack(
            anchor="w",
            padx=25,
            pady=(5, 5)
        )

        self.combo_tipo = ctk.CTkComboBox(
            frame_scroll,
            width=550,
            values=["Seleccione un tipo"]
        )

        self.combo_tipo.pack(
            padx=25,
            pady=(0, 15)
        )

        self.combo_tipo.set(
            "Seleccione un tipo"
        )

        # =================================================
        # CANTIDAD
        # =================================================

        ctk.CTkLabel(
            frame_scroll,
            text="Cantidad:",
            font=("Arial", 14)
        ).pack(
            anchor="w",
            padx=25,
            pady=(5, 5)
        )

        self.entry_cantidad = ctk.CTkEntry(
            frame_scroll,
            width=550,
            placeholder_text="Ingrese la cantidad"
        )

        self.entry_cantidad.pack(
            padx=25,
            pady=(0, 15)
        )

        # =================================================
        # RESPONSABLE
        # =================================================

        ctk.CTkLabel(
            frame_scroll,
            text="Responsable:",
            font=("Arial", 14)
        ).pack(
            anchor="w",
            padx=25,
            pady=(5, 5)
        )

        self.combo_responsable = ctk.CTkComboBox(
            frame_scroll,
            width=550,
            values=["Sin responsable"]
        )

        self.combo_responsable.pack(
            padx=25,
            pady=(0, 15)
        )

        self.combo_responsable.set(
            "Sin responsable"
        )

        # =================================================
        # OBSERVACIONES
        # =================================================

        ctk.CTkLabel(
            frame_scroll,
            text="Observaciones:",
            font=("Arial", 14)
        ).pack(
            anchor="w",
            padx=25,
            pady=(5, 5)
        )

        self.text_observaciones = ctk.CTkTextbox(
            frame_scroll,
            width=550,
            height=120
        )

        self.text_observaciones.pack(
            padx=25,
            pady=(0, 20)
        )

        # =================================================
        # SEPARADOR
        # =================================================

        separador = ctk.CTkFrame(
            frame_scroll,
            height=2,
            fg_color="gray"
        )

        separador.pack(
            fill="x",
            padx=25,
            pady=(0, 15)
        )

        # =================================================
        # FRAME BOTONES
        # =================================================

        frame_botones = ctk.CTkFrame(
            frame_scroll,
            fg_color="transparent"
        )

        frame_botones.pack(
            fill="x",
            padx=25,
            pady=(5, 25)
        )

        # =================================================
        # BOTÓN GUARDAR
        # =================================================

        btn_guardar = ctk.CTkButton(
            frame_botones,
            text="💾 Guardar Movimiento",
            width=220,
            height=40,
            command=self.guardar
        )

        btn_guardar.pack(
            side="left",
            padx=5
        )

        # =================================================
        # BOTÓN CANCELAR
        # =================================================

        btn_cancelar = ctk.CTkButton(
            frame_botones,
            text="❌ Cancelar",
            width=160,
            height=40,
            command=self.cerrar
        )

        btn_cancelar.pack(
            side="right",
            padx=5
        )

    # =====================================================
    # CARGAR DATOS
    # =====================================================

    def cargar_datos(self):

        try:

            # =================================================
            # INSUMOS
            # =================================================

            self.insumos = (
                self.model.listar_insumos()
            )

            # Orden ascendente por ID
            self.insumos.sort(
                key=lambda x: x[0]
            )

            valores_insumos = []

            for insumo in self.insumos:

                id_insumo = insumo[0]
                codigo = insumo[1]
                nombre = insumo[2]

                valores_insumos.append(
                    f"{id_insumo} - {codigo} - {nombre}"
                )

            if valores_insumos:

                self.combo_insumo.configure(
                    values=valores_insumos
                )

                # NO seleccionar automáticamente
                self.combo_insumo.set(
                    "Seleccione un insumo"
                )

                self.label_stock.configure(
                    text="Stock actual: --"
                )

            else:

                self.combo_insumo.configure(
                    values=["No existen insumos"]
                )

                self.combo_insumo.set(
                    "No existen insumos"
                )

                self.label_stock.configure(
                    text="Stock actual: --"
                )

            # =================================================
            # TIPOS DE MOVIMIENTO
            # =================================================

            self.tipos_movimiento = (
                self.model.listar_tipos_movimiento()
            )

            # Orden ascendente por ID
            self.tipos_movimiento.sort(
                key=lambda x: x[0]
            )

            valores_tipos = []

            for tipo in self.tipos_movimiento:

                id_tipo = tipo[0]
                nombre = tipo[1]

                valores_tipos.append(
                    f"{id_tipo} - {nombre}"
                )

            if valores_tipos:

                self.combo_tipo.configure(
                    values=valores_tipos
                )

                # NO seleccionar automáticamente
                self.combo_tipo.set(
                    "Seleccione un tipo"
                )

            else:

                self.combo_tipo.configure(
                    values=["No existen tipos"]
                )

                self.combo_tipo.set(
                    "No existen tipos"
                )

            # =================================================
            # RESPONSABLES
            # =================================================

            self.responsables = (
                self.model.listar_responsables()
            )

            # Orden ascendente por ID
            self.responsables.sort(
                key=lambda x: x[0]
            )

            valores_responsables = [
                "Sin responsable"
            ]

            for responsable in self.responsables:

                id_responsable = responsable[0]
                nombre = responsable[1]

                valores_responsables.append(
                    f"{id_responsable} - {nombre}"
                )

            self.combo_responsable.configure(
                values=valores_responsables
            )

            self.combo_responsable.set(
                "Sin responsable"
            )

        except Exception as e:

            print(
                "Error al cargar datos del formulario:",
                e
            )

            messagebox.showerror(
                "Error",
                (
                    "No se pudieron cargar los datos "
                    "del formulario:\n\n"
                    f"{e}"
                ),
                parent=self
            )

    # =====================================================
    # ACTUALIZAR STOCK
    # =====================================================

    def actualizar_stock(self, event=None):

        try:

            seleccion = (
                self.combo_insumo
                .get()
                .strip()
            )

            if (
                not seleccion
                or seleccion.startswith("No existen")
                or seleccion.startswith("Seleccione")
            ):

                self.label_stock.configure(
                    text="Stock actual: --"
                )

                return

            # =================================================
            # OBTENER ID
            # =================================================

            id_insumo = int(
                seleccion.split(" - ")[0]
            )

            insumo = (
                self.model.obtener_insumo(
                    id_insumo
                )
            )

            if insumo is None:

                self.label_stock.configure(
                    text="Stock actual: --"
                )

                return

            stock = (
                insumo[3]
                if insumo[3] is not None
                else 0
            )

            self.label_stock.configure(
                text=f"Stock actual: {stock}"
            )

        except Exception as e:

            print(
                "Error al actualizar stock:",
                e
            )

            self.label_stock.configure(
                text="Stock actual: --"
            )

    # =====================================================
    # GUARDAR MOVIMIENTO
    # =====================================================

    def guardar(self):

        try:

            # =================================================
            # VALIDAR INSUMO
            # =================================================

            seleccion_insumo = (
                self.combo_insumo
                .get()
                .strip()
            )

            if (
                not seleccion_insumo
                or seleccion_insumo.startswith("No existen")
                or seleccion_insumo.startswith("Seleccione")
            ):

                messagebox.showwarning(
                    "Advertencia",
                    "Seleccione un insumo.",
                    parent=self
                )

                return

            # =================================================
            # ID INSUMO
            # =================================================

            try:

                id_insumo = int(
                    seleccion_insumo.split(" - ")[0]
                )

            except Exception:

                messagebox.showerror(
                    "Error",
                    "No se pudo identificar el insumo seleccionado.",
                    parent=self
                )

                return

            # =================================================
            # VALIDAR TIPO
            # =================================================

            seleccion_tipo = (
                self.combo_tipo
                .get()
                .strip()
            )

            if (
                not seleccion_tipo
                or seleccion_tipo.startswith("No existen")
                or seleccion_tipo.startswith("Seleccione")
            ):

                messagebox.showwarning(
                    "Advertencia",
                    "Seleccione un tipo de movimiento.",
                    parent=self
                )

                return

            # =================================================
            # ID TIPO
            # =================================================

            try:

                id_tipo_movimiento = int(
                    seleccion_tipo.split(" - ")[0]
                )

            except Exception:

                messagebox.showerror(
                    "Error",
                    "No se pudo identificar el tipo de movimiento.",
                    parent=self
                )

                return

            # =================================================
            # CANTIDAD
            # =================================================

            cantidad_texto = (
                self.entry_cantidad
                .get()
                .strip()
            )

            if not cantidad_texto:

                messagebox.showwarning(
                    "Advertencia",
                    "Ingrese una cantidad.",
                    parent=self
                )

                self.entry_cantidad.focus()

                return

            try:

                cantidad = int(
                    cantidad_texto
                )

            except ValueError:

                messagebox.showwarning(
                    "Advertencia",
                    "La cantidad debe ser un número entero.",
                    parent=self
                )

                self.entry_cantidad.focus()

                return

            if cantidad <= 0:

                messagebox.showwarning(
                    "Advertencia",
                    "La cantidad debe ser mayor que cero.",
                    parent=self
                )

                self.entry_cantidad.focus()

                return

            # =================================================
            # RESPONSABLE
            # =================================================

            seleccion_responsable = (
                self.combo_responsable
                .get()
                .strip()
            )

            id_responsable = None

            if (
                seleccion_responsable
                and seleccion_responsable != "Sin responsable"
            ):

                try:

                    id_responsable = int(
                        seleccion_responsable.split(" - ")[0]
                    )

                except Exception:

                    id_responsable = None

            # =================================================
            # OBSERVACIONES
            # =================================================

            observaciones = (
                self.text_observaciones
                .get(
                    "1.0",
                    "end"
                )
                .strip()
            )

            # =================================================
            # CONFIRMAR
            # =================================================

            confirmar = messagebox.askyesno(
                "Confirmar movimiento",
                "¿Desea registrar este movimiento?",
                parent=self
            )

            if not confirmar:

                return

            # =================================================
            # GUARDAR EN BASE DE DATOS
            # =================================================

            self.model.registrar(
                id_insumo,
                id_tipo_movimiento,
                cantidad,
                id_responsable,
                observaciones
            )

            # =================================================
            # MENSAJE
            # =================================================

            messagebox.showinfo(
                "Éxito",
                "El movimiento se registró correctamente.",
                parent=self
            )

            # =================================================
            # CALLBACK
            # =================================================

            if self.callback:

                self.callback()

            # =================================================
            # CERRAR
            # =================================================

            self.cerrar()

        except Exception as e:

            print(
                "Error al guardar movimiento:",
                e
            )

            messagebox.showerror(
                "Error",
                (
                    "No se pudo registrar "
                    "el movimiento:\n\n"
                    f"{e}"
                ),
                parent=self
            )

    # =====================================================
    # CERRAR
    # =====================================================

    def cerrar(self):

        try:

            self.grab_release()

        except Exception:

            pass

        try:

            self.destroy()

        except Exception:

            pass