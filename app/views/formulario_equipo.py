import customtkinter as ctk
from tkinter import messagebox

from app.models.equipo_model import EquipoModel


class FormularioEquipo(ctk.CTkToplevel):

    def __init__(self, master=None, id_equipo=None):

        super().__init__(master)

        # =====================================================
        # CONFIGURACIÓN
        # =====================================================

        self.id_equipo = id_equipo
        self.modelo = EquipoModel()

        self.categorias = {}
        self.marcas = {}
        self.modelos = {}
        self.estados = {}
        self.proveedores = {}
        self.responsables = {}
        self.ubicaciones = {}

        # =====================================================
        # VENTANA
        # =====================================================

        if self.id_equipo:
            self.title("Editar Equipo")
        else:
            self.title("Nuevo Equipo")

        self.geometry("850x650")
        self.minsize(800, 600)

        self.transient(master)

        # =====================================================
        # CREAR INTERFAZ
        # =====================================================

        self.crear_interfaz()

        # =====================================================
        # CARGAR COMBOS
        # =====================================================

        self.cargar_combos()

        # =====================================================
        # CARGAR DATOS SI ES EDICIÓN
        # =====================================================

        if self.id_equipo:
            self.cargar_datos_equipo()


    # =========================================================
    # CREAR INTERFAZ
    # =========================================================

    def crear_interfaz(self):

        # =====================================================
        # TÍTULO
        # =====================================================

        titulo = ctk.CTkLabel(
            self,
            text="Formulario de Equipo",
            font=("Arial", 22, "bold")
        )

        titulo.pack(
            pady=(10, 5)
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
            padx=15,
            pady=5
        )


        # =====================================================
        # COLUMNAS
        # =====================================================

        frame.grid_columnconfigure(
            0,
            weight=1
        )

        frame.grid_columnconfigure(
            1,
            weight=1
        )


        # =====================================================
        # DATOS BÁSICOS
        # =====================================================

        self.txt_codigo = self.crear_entry(
            frame,
            "Código",
            0,
            0
        )


        self.txt_nombre = self.crear_entry(
            frame,
            "Nombre Equipo",
            0,
            1
        )


        self.txt_serie = self.crear_entry(
            frame,
            "Número Serie",
            2,
            0
        )


        self.txt_fecha = self.crear_entry(
            frame,
            "Fecha Compra",
            2,
            1
        )


        self.txt_garantia = self.crear_entry(
            frame,
            "Garantía (meses)",
            4,
            0
        )


        self.txt_precio = self.crear_entry(
            frame,
            "Precio",
            4,
            1
        )


        # =====================================================
        # CATEGORÍA
        # =====================================================

        self.cmb_categoria = self.crear_combo(
            frame,
            "Categoría",
            6,
            0
        )


        # =====================================================
        # MARCA
        # =====================================================

        self.cmb_marca = self.crear_combo(
            frame,
            "Marca",
            6,
            1
        )

        self.cmb_marca.configure(
            command=self.cargar_modelos
        )


        # =====================================================
        # MODELO
        # =====================================================

        self.cmb_modelo = self.crear_combo(
            frame,
            "Modelo",
            8,
            0
        )


        # =====================================================
        # ESTADO
        # =====================================================

        self.cmb_estado = self.crear_combo(
            frame,
            "Estado",
            8,
            1
        )


        # =====================================================
        # PROVEEDOR
        # =====================================================

        self.cmb_proveedor = self.crear_combo(
            frame,
            "Proveedor",
            10,
            0
        )


        # =====================================================
        # RESPONSABLE
        # =====================================================

        self.cmb_responsable = self.crear_combo(
            frame,
            "Responsable",
            10,
            1
        )


        # =====================================================
        # UBICACIÓN
        # =====================================================

        self.cmb_ubicacion = self.crear_combo(
            frame,
            "Ubicación",
            12,
            0
        )


        # =====================================================
        # OBSERVACIONES
        # =====================================================

        lbl_observaciones = ctk.CTkLabel(
            frame,
            text="Observaciones",
            font=("Arial", 12, "bold")
        )

        lbl_observaciones.grid(
            row=12,
            column=1,
            padx=10,
            pady=(8, 3),
            sticky="w"
        )


        self.txt_observaciones = ctk.CTkTextbox(
            frame,
            height=65
        )

        self.txt_observaciones.grid(
            row=13,
            column=1,
            padx=10,
            pady=(0, 5),
            sticky="nsew"
        )


        # =====================================================
        # BOTONES
        # =====================================================

        frame_botones = ctk.CTkFrame(
            self
        )

        frame_botones.pack(
            fill="x",
            padx=15,
            pady=(5, 10)
        )


        # =====================================================
        # TEXTO DEL BOTÓN
        # =====================================================

        if self.id_equipo:

            texto_boton = "💾 Actualizar Equipo"

        else:

            texto_boton = "💾 Guardar Equipo"


        # =====================================================
        # BOTÓN GUARDAR / ACTUALIZAR
        # =====================================================

        btn_guardar = ctk.CTkButton(
            frame_botones,
            text=texto_boton,
            width=180,
            height=38,
            font=("Arial", 13, "bold"),
            command=self.guardar
        )

        btn_guardar.pack(
            side="left",
            padx=10,
            pady=8
        )


        # =====================================================
        # BOTÓN CANCELAR
        # =====================================================

        btn_cancelar = ctk.CTkButton(
            frame_botones,
            text="Cancelar",
            width=130,
            height=38,
            font=("Arial", 13),
            command=self.destroy
        )

        btn_cancelar.pack(
            side="right",
            padx=10,
            pady=8
        )


    # =========================================================
    # CREAR ENTRY
    # =========================================================

    def crear_entry(
        self,
        padre,
        texto,
        fila,
        columna
    ):

        label = ctk.CTkLabel(
            padre,
            text=texto
        )

        label.grid(
            row=fila,
            column=columna,
            padx=10,
            pady=(5, 2),
            sticky="w"
        )


        entrada = ctk.CTkEntry(
            padre,
            height=32
        )

        entrada.grid(
            row=fila + 1,
            column=columna,
            padx=10,
            pady=(0, 3),
            sticky="ew"
        )


        return entrada


    # =========================================================
    # CREAR COMBOBOX
    # =========================================================

    def crear_combo(
        self,
        padre,
        texto,
        fila,
        columna
    ):

        label = ctk.CTkLabel(
            padre,
            text=texto
        )

        label.grid(
            row=fila,
            column=columna,
            padx=10,
            pady=(5, 2),
            sticky="w"
        )


        combo = ctk.CTkComboBox(
            padre,
            values=[""],
            height=32
        )

        combo.grid(
            row=fila + 1,
            column=columna,
            padx=10,
            pady=(0, 3),
            sticky="ew"
        )


        return combo


    # =========================================================
    # CARGAR COMBOS
    # =========================================================

    def cargar_combos(self):

        try:

            # =================================================
            # CATEGORÍAS
            # =================================================

            self.categorias = {}

            for id_categoria, nombre in self.modelo.listar_categorias():

                self.categorias[nombre] = id_categoria


            self.cmb_categoria.configure(
                values=list(
                    self.categorias.keys()
                )
            )


            # =================================================
            # MARCAS
            # =================================================

            self.marcas = {}

            for id_marca, nombre in self.modelo.listar_marcas():

                self.marcas[nombre] = id_marca


            self.cmb_marca.configure(
                values=list(
                    self.marcas.keys()
                )
            )


            # =================================================
            # ESTADOS
            # =================================================

            self.estados = {}

            for id_estado, nombre in self.modelo.listar_estados():

                self.estados[nombre] = id_estado


            self.cmb_estado.configure(
                values=list(
                    self.estados.keys()
                )
            )


            # =================================================
            # PROVEEDORES
            # =================================================

            self.proveedores = {}

            for id_proveedor, nombre in self.modelo.listar_proveedores():

                self.proveedores[nombre] = id_proveedor


            self.cmb_proveedor.configure(
                values=list(
                    self.proveedores.keys()
                )
            )


            # =================================================
            # RESPONSABLES
            # =================================================

            self.responsables = {}

            for id_responsable, nombre in self.modelo.listar_responsables():

                self.responsables[nombre] = id_responsable


            self.cmb_responsable.configure(
                values=list(
                    self.responsables.keys()
                )
            )


            # =================================================
            # UBICACIONES
            # =================================================

            self.ubicaciones = {}

            for id_ubicacion, nombre in self.modelo.listar_ubicaciones():

                self.ubicaciones[nombre] = id_ubicacion


            self.cmb_ubicacion.configure(
                values=list(
                    self.ubicaciones.keys()
                )
            )


        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los datos:\n\n{e}",
                parent=self
            )


    # =========================================================
    # CARGAR MODELOS SEGÚN MARCA
    # =========================================================

    def cargar_modelos(self, marca):

        self.modelos = {}

        self.cmb_modelo.set("")


        id_marca = self.marcas.get(
            marca
        )


        if not id_marca:

            self.cmb_modelo.configure(
                values=[""]
            )

            return


        try:

            datos = self.modelo.listar_modelos_por_marca(
                id_marca
            )


            lista = []


            for id_modelo, nombre in datos:

                self.modelos[nombre] = id_modelo

                lista.append(
                    nombre
                )


            if lista:

                self.cmb_modelo.configure(
                    values=lista
                )

            else:

                self.cmb_modelo.configure(
                    values=[""]
                )


        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los modelos:\n\n{e}",
                parent=self
            )


    # =========================================================
    # CARGAR DATOS PARA EDITAR
    # =========================================================

    def cargar_datos_equipo(self):

        try:

            equipo = self.modelo.obtener_por_id(
                self.id_equipo
            )


            if not equipo:

                messagebox.showerror(
                    "Error",
                    "No se encontró el equipo seleccionado.",
                    parent=self
                )

                self.destroy()

                return


            (
                id_equipo,
                codigo,
                nombre,
                numero_serie,
                id_categoria,
                id_marca,
                id_modelo,
                id_proveedor,
                id_estado,
                id_responsable,
                id_ubicacion,
                fecha_compra,
                garantia_meses,
                precio,
                observaciones
            ) = equipo


            # =================================================
            # CAMPOS DE TEXTO
            # =================================================

            self.txt_codigo.delete(
                0,
                "end"
            )

            self.txt_codigo.insert(
                0,
                codigo or ""
            )


            self.txt_nombre.delete(
                0,
                "end"
            )

            self.txt_nombre.insert(
                0,
                nombre or ""
            )


            self.txt_serie.delete(
                0,
                "end"
            )

            self.txt_serie.insert(
                0,
                numero_serie or ""
            )


            self.txt_fecha.delete(
                0,
                "end"
            )

            if fecha_compra:

                self.txt_fecha.insert(
                    0,
                    str(fecha_compra)
                )


            self.txt_garantia.delete(
                0,
                "end"
            )

            if garantia_meses is not None:

                self.txt_garantia.insert(
                    0,
                    str(garantia_meses)
                )


            self.txt_precio.delete(
                0,
                "end"
            )

            if precio is not None:

                self.txt_precio.insert(
                    0,
                    str(precio)
                )


            # =================================================
            # CATEGORÍA
            # =================================================

            for nombre_categoria, id_cat in self.categorias.items():

                if id_cat == id_categoria:

                    self.cmb_categoria.set(
                        nombre_categoria
                    )

                    break


            # =================================================
            # MARCA
            # =================================================

            nombre_marca = None


            for nombre_marca_actual, id_m in self.marcas.items():

                if id_m == id_marca:

                    nombre_marca = nombre_marca_actual

                    self.cmb_marca.set(
                        nombre_marca_actual
                    )

                    break


            # =================================================
            # MODELOS
            # =================================================

            if nombre_marca:

                self.cargar_modelos(
                    nombre_marca
                )


            for nombre_modelo, id_mod in self.modelos.items():

                if id_mod == id_modelo:

                    self.cmb_modelo.set(
                        nombre_modelo
                    )

                    break


            # =================================================
            # PROVEEDOR
            # =================================================

            for nombre_proveedor, id_prov in self.proveedores.items():

                if id_prov == id_proveedor:

                    self.cmb_proveedor.set(
                        nombre_proveedor
                    )

                    break


            # =================================================
            # ESTADO
            # =================================================

            for nombre_estado, id_est in self.estados.items():

                if id_est == id_estado:

                    self.cmb_estado.set(
                        nombre_estado
                    )

                    break


            # =================================================
            # RESPONSABLE
            # =================================================

            for nombre_responsable, id_resp in self.responsables.items():

                if id_resp == id_responsable:

                    self.cmb_responsable.set(
                        nombre_responsable
                    )

                    break


            # =================================================
            # UBICACIÓN
            # =================================================

            for nombre_ubicacion, id_ubi in self.ubicaciones.items():

                if id_ubi == id_ubicacion:

                    self.cmb_ubicacion.set(
                        nombre_ubicacion
                    )

                    break


            # =================================================
            # OBSERVACIONES
            # =================================================

            self.txt_observaciones.delete(
                "1.0",
                "end"
            )

            if observaciones:

                self.txt_observaciones.insert(
                    "1.0",
                    observaciones
                )


        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los datos del equipo:\n\n{e}",
                parent=self
            )


    # =========================================================
    # GUARDAR / ACTUALIZAR
    # =========================================================

    def guardar(self):

        try:

            # =================================================
            # CAMPOS BÁSICOS
            # =================================================

            codigo = self.txt_codigo.get().strip()

            nombre = self.txt_nombre.get().strip()

            serie = self.txt_serie.get().strip()


            # =================================================
            # VALIDAR CÓDIGO
            # =================================================

            if not codigo:

                messagebox.showwarning(
                    "Aviso",
                    "Ingrese el código del equipo.",
                    parent=self
                )

                self.txt_codigo.focus()

                return


            # =================================================
            # VALIDAR NOMBRE
            # =================================================

            if not nombre:

                messagebox.showwarning(
                    "Aviso",
                    "Ingrese el nombre del equipo.",
                    parent=self
                )

                self.txt_nombre.focus()

                return


            # =================================================
            # OBTENER IDS
            # =================================================

            id_categoria = self.categorias.get(
                self.cmb_categoria.get()
            )


            id_marca = self.marcas.get(
                self.cmb_marca.get()
            )


            id_modelo = self.modelos.get(
                self.cmb_modelo.get()
            )


            id_proveedor = self.proveedores.get(
                self.cmb_proveedor.get()
            )


            id_estado = self.estados.get(
                self.cmb_estado.get()
            )


            id_responsable = self.responsables.get(
                self.cmb_responsable.get()
            )


            id_ubicacion = self.ubicaciones.get(
                self.cmb_ubicacion.get()
            )


            # =================================================
            # FECHA
            # =================================================

            fecha = self.txt_fecha.get().strip()

            if not fecha:

                fecha = None


            # =================================================
            # GARANTÍA
            # =================================================

            garantia = self.txt_garantia.get().strip()

            if garantia:

                garantia = int(
                    garantia
                )

            else:

                garantia = 0


            # =================================================
            # PRECIO
            # =================================================

            precio = self.txt_precio.get().strip()

            if precio:

                precio = float(
                    precio
                )

            else:

                precio = None


            # =================================================
            # OBSERVACIONES
            # =================================================

            observaciones = self.txt_observaciones.get(
                "1.0",
                "end"
            ).strip()


            # =================================================
            # DATOS
            # =================================================

            datos = (

                codigo,
                nombre,
                serie,
                id_categoria,
                id_marca,
                id_modelo,
                id_proveedor,
                id_estado,
                id_responsable,
                id_ubicacion,
                fecha,
                garantia,
                precio,
                observaciones

            )


            # =================================================
            # INSERTAR / ACTUALIZAR
            # =================================================

            if self.id_equipo:

                self.modelo.actualizar(
                    self.id_equipo,
                    datos
                )

                mensaje = "Equipo actualizado correctamente."

            else:

                self.modelo.insertar(
                    datos
                )

                mensaje = "Equipo guardado correctamente."


            # =================================================
            # MENSAJE
            # =================================================

            messagebox.showinfo(
                "Correcto",
                mensaje,
                parent=self
            )


            # =================================================
            # CERRAR
            # =================================================

            self.destroy()


        except ValueError:

            messagebox.showerror(
                "Error",
                "La garantía debe ser un número entero y el precio debe ser numérico.",
                parent=self
            )


        except Exception as e:

            messagebox.showerror(
                "Error al guardar",
                f"No se pudo guardar el equipo:\n\n{e}",
                parent=self
            )