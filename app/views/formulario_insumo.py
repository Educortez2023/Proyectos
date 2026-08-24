import customtkinter as ctk
from tkinter import messagebox

from app.models.insumo_model import InsumoModel


class FormularioInsumo(ctk.CTkToplevel):

    def __init__(
        self,
        master=None,
        id_insumo=None
    ):

        super().__init__(master)

        self.master = master
        self.modelo = InsumoModel()
        self.id_insumo = id_insumo

        # =================================================
        # CONFIGURACIÓN DE VENTANA
        # =================================================

        self.title(
            "Editar Insumo"
            if id_insumo
            else "Nuevo Insumo"
        )

        self.geometry(
            "650x750"
        )

        self.minsize(
            600,
            650
        )

        self.transient(
            master
        )

        # =================================================
        # CREAR INTERFAZ
        # =================================================

        self.crear_interfaz()

        # =================================================
        # CENTRAR VENTANA
        # =================================================

        self.centrar_ventana()

        # =================================================
        # CARGAR DATOS
        # =================================================

        self.cargar_datos()

        # =================================================
        # MOSTRAR DELANTE
        # =================================================

        self.after(
            100,
            self.mostrar_delante
        )


    # =====================================================
    # CENTRAR VENTANA
    # =====================================================

    def centrar_ventana(self):

        self.update_idletasks()

        ancho = 650
        alto = 750

        if self.master:

            padre_x = self.master.winfo_rootx()
            padre_y = self.master.winfo_rooty()

            padre_ancho = self.master.winfo_width()
            padre_alto = self.master.winfo_height()

            x = (
                padre_x
                + (padre_ancho - ancho) // 2
            )

            y = (
                padre_y
                + (padre_alto - alto) // 2
            )

        else:

            pantalla_ancho = self.winfo_screenwidth()
            pantalla_alto = self.winfo_screenheight()

            x = (
                pantalla_ancho - ancho
            ) // 2

            y = (
                pantalla_alto - alto
            ) // 2

        if x < 0:
            x = 0

        if y < 0:
            y = 0

        self.geometry(
            f"{ancho}x{alto}+{x}+{y}"
        )


    # =====================================================
    # MOSTRAR DELANTE
    # =====================================================

    def mostrar_delante(self):

        self.lift()

        self.focus_force()

        self.grab_set()


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
                "Editar Insumo"
                if self.id_insumo
                else "Nuevo Insumo"
            ),
            font=(
                "Arial",
                22,
                "bold"
            )
        )

        titulo.pack(
            pady=(15, 10)
        )


        # =================================================
        # CONTENEDOR PRINCIPAL
        # =================================================

        frame_principal = ctk.CTkFrame(
            self
        )

        frame_principal.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=5
        )


        # =================================================
        # ÁREA CON SCROLL
        # =================================================

        self.frame_scroll = ctk.CTkScrollableFrame(
            frame_principal
        )

        self.frame_scroll.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


        # =================================================
        # CÓDIGO
        # =================================================

        self.txt_codigo = self.crear_entry(
            "Código"
        )


        # =================================================
        # NOMBRE
        # =================================================

        self.txt_nombre = self.crear_entry(
            "Nombre"
        )


        # =================================================
        # CATEGORÍA
        # =================================================

        self.cmb_categoria = self.crear_combo(
            "Categoría"
        )


        # =================================================
        # MARCA
        # =================================================

        self.cmb_marca = self.crear_combo(
            "Marca"
        )


        # =================================================
        # PROVEEDOR
        # =================================================

        self.cmb_proveedor = self.crear_combo(
            "Proveedor"
        )


        # =================================================
        # STOCK
        # =================================================

        self.txt_stock = self.crear_entry(
            "Stock"
        )


        # =================================================
        # STOCK MÍNIMO
        # =================================================

        self.txt_stock_minimo = self.crear_entry(
            "Stock mínimo"
        )


        # =================================================
        # PRECIO
        # =================================================

        self.txt_precio = self.crear_entry(
            "Precio"
        )


        # =================================================
        # UBICACIÓN
        # =================================================

        self.cmb_ubicacion = self.crear_combo(
            "Ubicación"
        )


        # =================================================
        # OBSERVACIONES
        # =================================================

        label_observaciones = ctk.CTkLabel(
            self.frame_scroll,
            text="Observaciones",
            font=(
                "Arial",
                14,
                "bold"
            )
        )

        label_observaciones.pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )


        # =================================================
        # CAMPO OBSERVACIONES
        # =================================================

        self.txt_observaciones = ctk.CTkTextbox(
            self.frame_scroll,
            height=120,
            width=520
        )

        self.txt_observaciones.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )


        # =================================================
        # FRAME BOTONES
        # =================================================

        frame_botones = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        frame_botones.pack(
            fill="x",
            padx=30,
            pady=(5, 15)
        )


        # =================================================
        # BOTÓN GUARDAR
        # =================================================

        btn_guardar = ctk.CTkButton(
            frame_botones,
            text="💾 Guardar",
            width=200,
            height=45,
            command=self.guardar
        )

        btn_guardar.pack(
            side="left",
            padx=10
        )


        # =================================================
        # BOTÓN CANCELAR
        # =================================================

        btn_cancelar = ctk.CTkButton(
            frame_botones,
            text="❌ Cancelar",
            width=200,
            height=45,
            fg_color="#777777",
            hover_color="#555555",
            command=self.cancelar
        )

        btn_cancelar.pack(
            side="right",
            padx=10
        )


    # =====================================================
    # CREAR ENTRY
    # =====================================================

    def crear_entry(
        self,
        texto
    ):

        label = ctk.CTkLabel(
            self.frame_scroll,
            text=texto
        )

        label.pack(
            anchor="w",
            padx=20,
            pady=(5, 2)
        )


        entrada = ctk.CTkEntry(
            self.frame_scroll,
            width=520,
            height=35
        )

        entrada.pack(
            fill="x",
            padx=20,
            pady=(0, 8)
        )


        return entrada


    # =====================================================
    # CREAR COMBO
    # =====================================================

    def crear_combo(
        self,
        texto
    ):

        label = ctk.CTkLabel(
            self.frame_scroll,
            text=texto
        )

        label.pack(
            anchor="w",
            padx=20,
            pady=(5, 2)
        )


        combo = ctk.CTkComboBox(
            self.frame_scroll,
            values=[""],
            width=520,
            height=35
        )

        combo.pack(
            fill="x",
            padx=20,
            pady=(0, 8)
        )


        return combo


    # =====================================================
    # CANCELAR
    # =====================================================

    def cancelar(self):

        try:

            self.grab_release()

        except Exception:

            pass

        self.destroy()


    # =====================================================
    # CARGAR DATOS
    # =====================================================

    def cargar_datos(self):

        try:

            # =================================================
            # DICCIONARIOS
            # =================================================

            self.categorias = {}

            self.marcas = {}

            self.proveedores = {}

            self.ubicaciones = {}


            # =================================================
            # CATEGORÍAS
            # =================================================

            datos = (
                self.modelo.listar_categorias()
            )

            for id_categoria, nombre in datos:

                self.categorias[
                    nombre
                ] = id_categoria


            self.cmb_categoria.configure(
                values=list(
                    self.categorias.keys()
                )
            )


            # =================================================
            # MARCAS
            # =================================================

            datos = (
                self.modelo.listar_marcas()
            )

            for id_marca, nombre in datos:

                self.marcas[
                    nombre
                ] = id_marca


            self.cmb_marca.configure(
                values=list(
                    self.marcas.keys()
                )
            )


            # =================================================
            # PROVEEDORES
            # =================================================

            datos = (
                self.modelo.listar_proveedores()
            )

            for id_proveedor, empresa in datos:

                self.proveedores[
                    empresa
                ] = id_proveedor


            self.cmb_proveedor.configure(
                values=list(
                    self.proveedores.keys()
                )
            )


            # =================================================
            # UBICACIONES
            # =================================================

            datos = (
                self.modelo.listar_ubicaciones()
            )

            for id_ubicacion, nombre in datos:

                self.ubicaciones[
                    nombre
                ] = id_ubicacion


            self.cmb_ubicacion.configure(
                values=list(
                    self.ubicaciones.keys()
                )
            )


            # =================================================
            # CARGAR DATOS PARA EDITAR
            # =================================================

            if self.id_insumo:

                insumo = (
                    self.modelo.obtener_por_id(
                        self.id_insumo
                    )
                )


                if insumo:

                    # =================================================
                    # CÓDIGO
                    # =================================================

                    self.txt_codigo.insert(
                        0,
                        insumo[1]
                    )


                    # =================================================
                    # NOMBRE
                    # =================================================

                    self.txt_nombre.insert(
                        0,
                        insumo[2]
                    )


                    # =================================================
                    # STOCK
                    # =================================================

                    if insumo[6] is not None:

                        self.txt_stock.insert(
                            0,
                            str(
                                insumo[6]
                            )
                        )


                    # =================================================
                    # STOCK MÍNIMO
                    # =================================================

                    if insumo[7] is not None:

                        self.txt_stock_minimo.insert(
                            0,
                            str(
                                insumo[7]
                            )
                        )


                    # =================================================
                    # PRECIO
                    # =================================================

                    if insumo[8] is not None:

                        self.txt_precio.insert(
                            0,
                            str(
                                insumo[8]
                            )
                        )


                    # =================================================
                    # CATEGORÍA
                    # =================================================

                    if insumo[3] is not None:

                        for nombre, id_categoria in self.categorias.items():

                            if id_categoria == insumo[3]:

                                self.cmb_categoria.set(
                                    nombre
                                )

                                break


                    # =================================================
                    # MARCA
                    # =================================================

                    if insumo[4] is not None:

                        for nombre, id_marca in self.marcas.items():

                            if id_marca == insumo[4]:

                                self.cmb_marca.set(
                                    nombre
                                )

                                break


                    # =================================================
                    # PROVEEDOR
                    # =================================================

                    if insumo[5] is not None:

                        for empresa, id_proveedor in self.proveedores.items():

                            if id_proveedor == insumo[5]:

                                self.cmb_proveedor.set(
                                    empresa
                                )

                                break


                    # =================================================
                    # UBICACIÓN
                    # =================================================

                    if insumo[9] is not None:

                        for nombre, id_ubicacion in self.ubicaciones.items():

                            if id_ubicacion == insumo[9]:

                                self.cmb_ubicacion.set(
                                    nombre
                                )

                                break


                    # =================================================
                    # OBSERVACIONES
                    # =================================================

                    if insumo[10] is not None:

                        self.txt_observaciones.insert(
                            "1.0",
                            str(
                                insumo[10]
                            )
                        )


        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los datos:\n\n{e}",
                parent=self
            )


    # =====================================================
    # GUARDAR
    # =====================================================

    def guardar(self):

        try:

            # =================================================
            # CÓDIGO
            # =================================================

            codigo = (
                self.txt_codigo
                .get()
                .strip()
            )


            # =================================================
            # NOMBRE
            # =================================================

            nombre = (
                self.txt_nombre
                .get()
                .strip()
            )


            # =================================================
            # VALIDAR CÓDIGO
            # =================================================

            if not codigo:

                messagebox.showwarning(
                    "Validación",
                    "Debe ingresar el código.",
                    parent=self
                )

                self.txt_codigo.focus()

                return


            # =================================================
            # VALIDAR NOMBRE
            # =================================================

            if not nombre:

                messagebox.showwarning(
                    "Validación",
                    "Debe ingresar el nombre.",
                    parent=self
                )

                self.txt_nombre.focus()

                return


            # =================================================
            # OBTENER IDS
            # =================================================

            id_categoria = (
                self.categorias.get(
                    self.cmb_categoria.get()
                )
            )


            id_marca = (
                self.marcas.get(
                    self.cmb_marca.get()
                )
            )


            id_proveedor = (
                self.proveedores.get(
                    self.cmb_proveedor.get()
                )
            )


            id_ubicacion = (
                self.ubicaciones.get(
                    self.cmb_ubicacion.get()
                )
            )


            # =================================================
            # STOCK
            # =================================================

            stock_texto = (
                self.txt_stock
                .get()
                .strip()
            )

            if not stock_texto:

                stock = 0

            else:

                stock = int(
                    stock_texto
                )


            # =================================================
            # STOCK MÍNIMO
            # =================================================

            stock_minimo_texto = (
                self.txt_stock_minimo
                .get()
                .strip()
            )

            if not stock_minimo_texto:

                stock_minimo = 0

            else:

                stock_minimo = int(
                    stock_minimo_texto
                )


            # =================================================
            # PRECIO
            # =================================================

            precio_texto = (
                self.txt_precio
                .get()
                .strip()
            )

            if not precio_texto:

                precio = 0

            else:

                precio = float(
                    precio_texto
                )


            # =================================================
            # OBSERVACIONES
            # =================================================

            observaciones = (
                self.txt_observaciones
                .get(
                    "1.0",
                    "end-1c"
                )
                .strip()
            )


            # =================================================
            # DATOS
            # =================================================

            datos = (

                codigo,

                nombre,

                id_categoria,

                id_marca,

                id_proveedor,

                stock,

                stock_minimo,

                precio,

                id_ubicacion,

                observaciones

            )


            # =================================================
            # NUEVO INSUMO
            # =================================================

            if self.id_insumo is None:

                self.modelo.insertar(
                    datos
                )

                mensaje = (
                    "El insumo fue registrado correctamente."
                )


            # =================================================
            # EDITAR INSUMO
            # =================================================

            else:

                self.modelo.actualizar(
                    self.id_insumo,
                    datos
                )

                mensaje = (
                    "El insumo fue actualizado correctamente."
                )


            # =================================================
            # MENSAJE DE ÉXITO
            # =================================================

            messagebox.showinfo(
                "Correcto",
                mensaje,
                parent=self
            )


            # =================================================
            # CERRAR VENTANA
            # =================================================

            self.cancelar()


        except ValueError:

            messagebox.showwarning(
                "Validación",
                "Stock y stock mínimo deben ser números enteros y el precio debe ser un número válido.",
                parent=self
            )


        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudo guardar el insumo:\n\n{e}",
                parent=self
            )