import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

from app.models.reporte_model import ReporteModel


class VentanaReportes(ctk.CTkToplevel):

    def __init__(self, parent=None):

        super().__init__(parent)

        # =====================================================
        # CONFIGURACIÓN DE LA VENTANA
        # =====================================================

        self.parent = parent

        self.title("Reportes de Inventario")

        # Tamaño inicial
        self.geometry("1250x700")

        # Tamaño mínimo razonable
        self.minsize(950, 600)

        self.transient(parent)

        # =====================================================
        # VARIABLES
        # =====================================================

        self.categorias = []
        self.marcas = []
        self.modelos = []
        self.proveedores = []
        self.estados = []
        self.responsables = []
        self.ubicaciones = []

        self.datos_reporte = []

        # =====================================================
        # CREAR INTERFAZ
        # =====================================================

        self.crear_interfaz()

        # =====================================================
        # CARGAR FILTROS
        # =====================================================

        self.cargar_filtros()

        # =====================================================
        # GENERAR REPORTE INICIAL
        # =====================================================

        self.generar_reporte()

        # =====================================================
        # AJUSTAR COLUMNAS AL CAMBIAR TAMAÑO
        # =====================================================

        self.bind(
            "<Configure>",
            self._evento_redimensionar
        )

    # =====================================================
    # EVENTO DE REDIMENSIONAMIENTO
    # =====================================================

    def _evento_redimensionar(self, event=None):

        try:

            if not hasattr(self, "tabla"):
                return

            if event is not None:

                if event.widget != self:
                    return

            self.ajustar_columnas()

        except Exception:
            pass

    # =====================================================
    # CREAR INTERFAZ
    # =====================================================

    def crear_interfaz(self):

        # =================================================
        # CONFIGURACIÓN PRINCIPAL
        # =================================================

        self.grid_rowconfigure(
            2,
            weight=1
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        # =================================================
        # TÍTULO
        # =================================================

        titulo = ctk.CTkLabel(
            self,
            text="REPORTES DE INVENTARIO",
            font=("Arial", 24, "bold")
        )

        titulo.grid(
            row=0,
            column=0,
            padx=20,
            pady=(15, 10),
            sticky="w"
        )

        # =================================================
        # FRAME DE FILTROS
        # =================================================

        self.frame_filtros = ctk.CTkFrame(
            self
        )

        self.frame_filtros.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 10),
            sticky="ew"
        )

        self.frame_filtros.grid_columnconfigure(
            0,
            weight=1
        )

        # =================================================
        # FILA 1
        # =================================================

        fila1 = ctk.CTkFrame(
            self.frame_filtros,
            fg_color="transparent"
        )

        fila1.grid(
            row=0,
            column=0,
            padx=10,
            pady=(10, 5),
            sticky="ew"
        )

        # Código

        ctk.CTkLabel(
            fila1,
            text="Código:"
        ).pack(
            side="left",
            padx=(0, 5)
        )

        self.entry_codigo = ctk.CTkEntry(
            fila1,
            width=130,
            placeholder_text="Código"
        )

        self.entry_codigo.pack(
            side="left",
            padx=(0, 12)
        )

        # Equipo

        ctk.CTkLabel(
            fila1,
            text="Equipo:"
        ).pack(
            side="left",
            padx=(0, 5)
        )

        self.entry_nombre = ctk.CTkEntry(
            fila1,
            width=180,
            placeholder_text="Nombre del equipo"
        )

        self.entry_nombre.pack(
            side="left",
            padx=(0, 12)
        )

        # Serie

        ctk.CTkLabel(
            fila1,
            text="Serie:"
        ).pack(
            side="left",
            padx=(0, 5)
        )

        self.entry_serie = ctk.CTkEntry(
            fila1,
            width=170,
            placeholder_text="Número de serie"
        )

        self.entry_serie.pack(
            side="left",
            padx=(0, 12)
        )

        # Categoría

        ctk.CTkLabel(
            fila1,
            text="Categoría:"
        ).pack(
            side="left",
            padx=(0, 5)
        )

        self.combo_categoria = ctk.CTkComboBox(
            fila1,
            width=170,
            values=["Todas"]
        )

        self.combo_categoria.pack(
            side="left",
            padx=(0, 5)
        )

        # =================================================
        # FILA 2
        # =================================================

        fila2 = ctk.CTkFrame(
            self.frame_filtros,
            fg_color="transparent"
        )

        fila2.grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky="ew"
        )

        # Marca

        ctk.CTkLabel(
            fila2,
            text="Marca:"
        ).pack(
            side="left",
            padx=(0, 5)
        )

        self.combo_marca = ctk.CTkComboBox(
            fila2,
            width=160,
            values=["Todas"],
            command=self.cargar_modelos_por_marca
        )

        self.combo_marca.pack(
            side="left",
            padx=(0, 12)
        )

        # Modelo

        ctk.CTkLabel(
            fila2,
            text="Modelo:"
        ).pack(
            side="left",
            padx=(0, 5)
        )

        self.combo_modelo = ctk.CTkComboBox(
            fila2,
            width=170,
            values=["Todos"]
        )

        self.combo_modelo.pack(
            side="left",
            padx=(0, 12)
        )

        # Proveedor

        ctk.CTkLabel(
            fila2,
            text="Proveedor:"
        ).pack(
            side="left",
            padx=(0, 5)
        )

        self.combo_proveedor = ctk.CTkComboBox(
            fila2,
            width=190,
            values=["Todos"]
        )

        self.combo_proveedor.pack(
            side="left",
            padx=(0, 12)
        )

        # Estado

        ctk.CTkLabel(
            fila2,
            text="Estado:"
        ).pack(
            side="left",
            padx=(0, 5)
        )

        self.combo_estado = ctk.CTkComboBox(
            fila2,
            width=150,
            values=["Todos"]
        )

        self.combo_estado.pack(
            side="left",
            padx=(0, 5)
        )

        # =================================================
        # FILA 3
        # =================================================

        fila3 = ctk.CTkFrame(
            self.frame_filtros,
            fg_color="transparent"
        )

        fila3.grid(
            row=2,
            column=0,
            padx=10,
            pady=(5, 10),
            sticky="ew"
        )

        # Responsable

        ctk.CTkLabel(
            fila3,
            text="Responsable:"
        ).pack(
            side="left",
            padx=(0, 5)
        )

        self.combo_responsable = ctk.CTkComboBox(
            fila3,
            width=210,
            values=["Todos"]
        )

        self.combo_responsable.pack(
            side="left",
            padx=(0, 12)
        )

        # Ubicación

        ctk.CTkLabel(
            fila3,
            text="Ubicación:"
        ).pack(
            side="left",
            padx=(0, 5)
        )

        self.combo_ubicacion = ctk.CTkComboBox(
            fila3,
            width=180,
            values=["Todas"]
        )

        self.combo_ubicacion.pack(
            side="left",
            padx=(0, 12)
        )

        # Registro

        ctk.CTkLabel(
            fila3,
            text="Registro:"
        ).pack(
            side="left",
            padx=(0, 5)
        )

        self.combo_activo = ctk.CTkComboBox(
            fila3,
            width=130,
            values=[
                "Todos",
                "Activos",
                "Inactivos"
            ]
        )

        self.combo_activo.pack(
            side="left",
            padx=(0, 15)
        )

        self.combo_activo.set(
            "Todos"
        )

        # =================================================
        # BOTÓN GENERAR
        # =================================================

        self.btn_generar = ctk.CTkButton(
            fila3,
            text="🔍 Generar reporte",
            width=145,
            height=34,
            command=self.generar_reporte
        )

        self.btn_generar.pack(
            side="left",
            padx=4
        )

        # =================================================
        # BOTÓN LIMPIAR
        # =================================================

        self.btn_limpiar = ctk.CTkButton(
            fila3,
            text="🧹 Limpiar",
            width=105,
            height=34,
            fg_color="gray",
            hover_color="#555555",
            command=self.limpiar_filtros
        )

        self.btn_limpiar.pack(
            side="left",
            padx=4
        )

        # =================================================
        # BOTÓN EXPORTAR
        # =================================================

        self.btn_exportar = ctk.CTkButton(
            fila3,
            text="📊 Exportar Excel",
            width=140,
            height=34,
            command=self.exportar_a_excel
        )

        self.btn_exportar.pack(
            side="left",
            padx=4
        )

        # =================================================
        # CONTADOR
        # =================================================

        self.lbl_resultados = ctk.CTkLabel(
            self,
            text="Registros encontrados: 0",
            font=("Arial", 14, "bold")
        )

        self.lbl_resultados.grid(
            row=2,
            column=0,
            padx=20,
            pady=(0, 5),
            sticky="nw"
        )

        # =================================================
        # FRAME DE TABLA
        # =================================================

        self.frame_tabla = ctk.CTkFrame(
            self
        )

        self.frame_tabla.grid(
            row=3,
            column=0,
            padx=15,
            pady=(0, 15),
            sticky="nsew"
        )

        self.grid_rowconfigure(
            3,
            weight=1
        )

        self.frame_tabla.grid_rowconfigure(
            0,
            weight=1
        )

        self.frame_tabla.grid_columnconfigure(
            0,
            weight=1
        )

        # =================================================
        # COLUMNAS
        # =================================================

        columnas = (
            "codigo",
            "nombre",
            "serie",
            "categoria",
            "marca",
            "modelo",
            "proveedor",
            "estado",
            "responsable",
            "ubicacion",
            "fecha_compra",
            "garantia",
            "precio",
            "activo"
        )

        self.columnas = columnas

        # =================================================
        # TABLA
        # =================================================

        self.tabla = ttk.Treeview(
            self.frame_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        # =================================================
        # ENCABEZADOS
        # =================================================

        encabezados = {
            "codigo": "Código",
            "nombre": "Equipo",
            "serie": "Número de serie",
            "categoria": "Categoría",
            "marca": "Marca",
            "modelo": "Modelo",
            "proveedor": "Proveedor",
            "estado": "Estado",
            "responsable": "Responsable",
            "ubicacion": "Ubicación",
            "fecha_compra": "Fecha compra",
            "garantia": "Garantía",
            "precio": "Precio",
            "activo": "Registro"
        }

        for columna in columnas:

            self.tabla.heading(
                columna,
                text=encabezados[columna]
            )

        # =================================================
        # ANCHOS MÍNIMOS
        # =================================================

        configuracion_columnas = {

            "codigo": (95, 75),
            "nombre": (170, 120),
            "serie": (150, 110),
            "categoria": (130, 100),
            "marca": (120, 90),
            "modelo": (140, 100),
            "proveedor": (170, 120),
            "estado": (110, 90),
            "responsable": (180, 120),
            "ubicacion": (140, 100),
            "fecha_compra": (115, 100),
            "garantia": (105, 90),
            "precio": (100, 85),
            "activo": (95, 80)
        }

        for columna, valores in configuracion_columnas.items():

            ancho = valores[0]
            minimo = valores[1]

            self.tabla.column(
                columna,
                width=ancho,
                minwidth=minimo,
                anchor="center",
                stretch=True
            )

        # =================================================
        # SCROLLBAR VERTICAL
        # =================================================

        self.scrollbar_vertical = ttk.Scrollbar(
            self.frame_tabla,
            orient="vertical",
            command=self.tabla.yview
        )

        # =================================================
        # SCROLLBAR HORIZONTAL
        # =================================================

        self.scrollbar_horizontal = ttk.Scrollbar(
            self.frame_tabla,
            orient="horizontal",
            command=self.tabla.xview
        )

        # =================================================
        # CONECTAR TABLA
        # =================================================

        self.tabla.configure(
            yscrollcommand=self.scrollbar_vertical.set,
            xscrollcommand=self.scrollbar_horizontal.set
        )

        # =================================================
        # POSICIONAR TABLA
        # =================================================

        self.tabla.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.scrollbar_vertical.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.scrollbar_horizontal.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        # =================================================
        # ENTER EN CAMPOS DE TEXTO
        # =================================================

        self.entry_codigo.bind(
            "<Return>",
            lambda event: self.generar_reporte()
        )

        self.entry_nombre.bind(
            "<Return>",
            lambda event: self.generar_reporte()
        )

        self.entry_serie.bind(
            "<Return>",
            lambda event: self.generar_reporte()
        )

    # =====================================================
    # AJUSTAR COLUMNAS
    # =====================================================

    def ajustar_columnas(self):

        try:

            if not hasattr(self, "tabla"):
                return

            ancho_disponible = self.tabla.winfo_width()

            if ancho_disponible <= 10:
                return

            # Ancho aproximado de las columnas.
            # Se utiliza únicamente cuando existe
            # suficiente espacio.

            pesos = {
                "codigo": 0.07,
                "nombre": 0.12,
                "serie": 0.10,
                "categoria": 0.09,
                "marca": 0.08,
                "modelo": 0.09,
                "proveedor": 0.11,
                "estado": 0.07,
                "responsable": 0.11,
                "ubicacion": 0.08,
                "fecha_compra": 0.08,
                "garantia": 0.07,
                "precio": 0.07,
                "activo": 0.07
            }

            suma_pesos = sum(
                pesos.values()
            )

            ancho_real = max(
                1,
                ancho_disponible
            )

            # No dejamos que la tabla genere
            # una ventana o frame gigante.

            for columna in self.columnas:

                nuevo_ancho = int(
                    ancho_real
                    * (
                        pesos[columna]
                        / suma_pesos
                    )
                )

                minimo = int(
                    self.tabla.column(
                        columna,
                        "minwidth"
                    )
                )

                if nuevo_ancho < minimo:

                    nuevo_ancho = minimo

                self.tabla.column(
                    columna,
                    width=nuevo_ancho
                )

        except Exception:
            pass

    # =====================================================
    # CARGAR FILTROS
    # =====================================================

    def cargar_filtros(self):

        try:

            # =================================================
            # CATEGORÍAS
            # =================================================

            self.categorias = (
                ReporteModel.listar_categorias()
            )

            valores = ["Todas"]

            for categoria in self.categorias:

                valores.append(
                    categoria["nombre"]
                )

            self.combo_categoria.configure(
                values=valores
            )

            self.combo_categoria.set(
                "Todas"
            )

            # =================================================
            # MARCAS
            # =================================================

            self.marcas = (
                ReporteModel.listar_marcas()
            )

            valores = ["Todas"]

            for marca in self.marcas:

                valores.append(
                    marca["nombre"]
                )

            self.combo_marca.configure(
                values=valores
            )

            self.combo_marca.set(
                "Todas"
            )

            # =================================================
            # MODELOS
            # =================================================

            self.modelos = (
                ReporteModel.listar_modelos()
            )

            valores = ["Todos"]

            for modelo in self.modelos:

                valores.append(
                    modelo["nombre"]
                )

            self.combo_modelo.configure(
                values=valores
            )

            self.combo_modelo.set(
                "Todos"
            )

            # =================================================
            # PROVEEDORES
            # =================================================

            self.proveedores = (
                ReporteModel.listar_proveedores()
            )

            valores = ["Todos"]

            for proveedor in self.proveedores:

                valores.append(
                    proveedor["empresa"]
                )

            self.combo_proveedor.configure(
                values=valores
            )

            self.combo_proveedor.set(
                "Todos"
            )

            # =================================================
            # ESTADOS
            # =================================================

            self.estados = (
                ReporteModel.listar_estados()
            )

            valores = ["Todos"]

            for estado in self.estados:

                valores.append(
                    estado["nombre"]
                )

            self.combo_estado.configure(
                values=valores
            )

            self.combo_estado.set(
                "Todos"
            )

            # =================================================
            # RESPONSABLES
            # =================================================

            self.responsables = (
                ReporteModel.listar_responsables()
            )

            valores = ["Todos"]

            for responsable in self.responsables:

                valores.append(
                    responsable["nombre_completo"]
                )

            self.combo_responsable.configure(
                values=valores
            )

            self.combo_responsable.set(
                "Todos"
            )

            # =================================================
            # UBICACIONES
            # =================================================

            self.ubicaciones = (
                ReporteModel.listar_ubicaciones()
            )

            valores = ["Todas"]

            for ubicacion in self.ubicaciones:

                valores.append(
                    ubicacion["nombre"]
                )

            self.combo_ubicacion.configure(
                values=valores
            )

            self.combo_ubicacion.set(
                "Todas"
            )

        except Exception as e:

            print(
                "Error al cargar filtros:",
                e
            )

            messagebox.showerror(
                "Error",
                (
                    "No se pudieron cargar "
                    "los filtros.\n\n"
                    f"{e}"
                ),
                parent=self
            )

    # =====================================================
    # CARGAR MODELOS SEGÚN MARCA
    # =====================================================

    def cargar_modelos_por_marca(self, valor):

        try:

            if valor == "Todas":

                modelos = self.modelos

            else:

                id_marca = None

                for marca in self.marcas:

                    if marca["nombre"] == valor:

                        id_marca = marca["id_marca"]

                        break

                if id_marca is None:

                    modelos = []

                else:

                    modelos = [
                        modelo
                        for modelo in self.modelos
                        if modelo["id_marca"] == id_marca
                    ]

            valores = ["Todos"]

            for modelo in modelos:

                valores.append(
                    modelo["nombre"]
                )

            self.combo_modelo.configure(
                values=valores
            )

            self.combo_modelo.set(
                "Todos"
            )

        except Exception as e:

            print(
                "Error al cargar modelos:",
                e
            )

    # =====================================================
    # OBTENER ID POR NOMBRE
    # =====================================================

    def obtener_id_por_nombre(
        self,
        registros,
        campo_nombre,
        campo_id,
        valor
    ):

        if valor in (
            "Todas",
            "Todos",
            ""
        ):

            return None

        for registro in registros:

            if registro.get(
                campo_nombre
            ) == valor:

                return registro.get(
                    campo_id
                )

        return None

    # =====================================================
    # GENERAR REPORTE
    # =====================================================

    def generar_reporte(self):

        try:

            codigo = (
                self.entry_codigo
                .get()
                .strip()
            )

            nombre = (
                self.entry_nombre
                .get()
                .strip()
            )

            numero_serie = (
                self.entry_serie
                .get()
                .strip()
            )

            # =================================================
            # OBTENER IDS
            # =================================================

            id_categoria = (
                self.obtener_id_por_nombre(
                    self.categorias,
                    "nombre",
                    "id_categoria",
                    self.combo_categoria.get()
                )
            )

            id_marca = (
                self.obtener_id_por_nombre(
                    self.marcas,
                    "nombre",
                    "id_marca",
                    self.combo_marca.get()
                )
            )

            id_modelo = (
                self.obtener_id_por_nombre(
                    self.modelos,
                    "nombre",
                    "id_modelo",
                    self.combo_modelo.get()
                )
            )

            id_proveedor = (
                self.obtener_id_por_nombre(
                    self.proveedores,
                    "empresa",
                    "id_proveedor",
                    self.combo_proveedor.get()
                )
            )

            id_estado = (
                self.obtener_id_por_nombre(
                    self.estados,
                    "nombre",
                    "id_estado",
                    self.combo_estado.get()
                )
            )

            id_responsable = (
                self.obtener_id_por_nombre(
                    self.responsables,
                    "nombre_completo",
                    "id_responsable",
                    self.combo_responsable.get()
                )
            )

            id_ubicacion = (
                self.obtener_id_por_nombre(
                    self.ubicaciones,
                    "nombre",
                    "id_ubicacion",
                    self.combo_ubicacion.get()
                )
            )

            # =================================================
            # ACTIVO
            # =================================================

            valor_activo = (
                self.combo_activo.get()
            )

            if valor_activo == "Activos":

                activo = 1

            elif valor_activo == "Inactivos":

                activo = 0

            else:

                activo = None

            # =================================================
            # CONSULTAR BASE DE DATOS
            # =================================================

            self.datos_reporte = (
                ReporteModel.listar_equipos(
                    codigo=codigo,
                    nombre=nombre,
                    numero_serie=numero_serie,
                    id_categoria=id_categoria,
                    id_marca=id_marca,
                    id_modelo=id_modelo,
                    id_proveedor=id_proveedor,
                    id_estado=id_estado,
                    id_responsable=id_responsable,
                    id_ubicacion=id_ubicacion,
                    activo=activo
                )
            )

            # =================================================
            # MOSTRAR
            # =================================================

            self.mostrar_reporte(
                self.datos_reporte
            )

        except Exception as e:

            print(
                "Error al generar reporte:",
                e
            )

            messagebox.showerror(
                "Error",
                (
                    "No se pudo generar "
                    "el reporte.\n\n"
                    f"{e}"
                ),
                parent=self
            )

    # =====================================================
    # MOSTRAR REPORTE
    # =====================================================

    def mostrar_reporte(self, datos):

        try:

            # =================================================
            # LIMPIAR TABLA
            # =================================================

            for item in self.tabla.get_children():

                self.tabla.delete(
                    item
                )

            # =================================================
            # INSERTAR DATOS
            # =================================================

            for equipo in datos:

                fecha_compra = (
                    equipo.get(
                        "fecha_compra"
                    )
                    or ""
                )

                precio = equipo.get(
                    "precio"
                )

                if precio is not None:

                    try:

                        precio = (
                            f"{float(precio):.2f}"
                        )

                    except Exception:

                        precio = str(
                            precio
                        )

                else:

                    precio = ""

                garantia = (
                    equipo.get(
                        "garantia_meses"
                    )
                    or 0
                )

                activo = (
                    "Activo"
                    if equipo.get(
                        "activo"
                    ) == 1
                    else "Inactivo"
                )

                self.tabla.insert(
                    "",
                    "end",
                    values=(
                        equipo.get(
                            "codigo"
                        ) or "",

                        equipo.get(
                            "nombre"
                        ) or "",

                        equipo.get(
                            "numero_serie"
                        ) or "",

                        equipo.get(
                            "categoria"
                        ) or "",

                        equipo.get(
                            "marca"
                        ) or "",

                        equipo.get(
                            "modelo"
                        ) or "",

                        equipo.get(
                            "proveedor"
                        ) or "",

                        equipo.get(
                            "estado"
                        ) or "",

                        equipo.get(
                            "responsable"
                        ) or "",

                        equipo.get(
                            "ubicacion"
                        ) or "",

                        str(
                            fecha_compra
                        ),

                        garantia,

                        precio,

                        activo
                    )
                )

            # =================================================
            # ACTUALIZAR CONTADOR
            # =================================================

            self.lbl_resultados.configure(
                text=(
                    "Registros encontrados: "
                    f"{len(datos)}"
                )
            )

            # =================================================
            # AJUSTAR COLUMNAS
            # =================================================

            self.after_idle(
                self.ajustar_columnas
            )

        except Exception as e:

            print(
                "Error al mostrar reporte:",
                e
            )

    # =====================================================
    # LIMPIAR FILTROS
    # =====================================================

    def limpiar_filtros(self):

        try:

            self.entry_codigo.delete(
                0,
                "end"
            )

            self.entry_nombre.delete(
                0,
                "end"
            )

            self.entry_serie.delete(
                0,
                "end"
            )

            self.combo_categoria.set(
                "Todas"
            )

            self.combo_marca.set(
                "Todas"
            )

            valores_modelos = ["Todos"]

            for modelo in self.modelos:

                valores_modelos.append(
                    modelo["nombre"]
                )

            self.combo_modelo.configure(
                values=valores_modelos
            )

            self.combo_modelo.set(
                "Todos"
            )

            self.combo_proveedor.set(
                "Todos"
            )

            self.combo_estado.set(
                "Todos"
            )

            self.combo_responsable.set(
                "Todos"
            )

            self.combo_ubicacion.set(
                "Todas"
            )

            self.combo_activo.set(
                "Todos"
            )

            # =================================================
            # GENERAR DE NUEVO
            # =================================================

            self.generar_reporte()

        except Exception as e:

            print(
                "Error al limpiar filtros:",
                e
            )

    # =====================================================
    # EXPORTAR A EXCEL
    # =====================================================

    def exportar_a_excel(self):

        try:

            if not self.datos_reporte:

                messagebox.showwarning(
                    "Sin datos",
                    (
                        "No existen registros "
                        "para exportar."
                    ),
                    parent=self
                )

                return

            # =================================================
            # SELECCIONAR ARCHIVO
            # =================================================

            archivo = (
                filedialog.asksaveasfilename(
                    parent=self,
                    title="Guardar reporte en Excel",
                    defaultextension=".xlsx",
                    filetypes=[
                        (
                            "Archivo Excel",
                            "*.xlsx"
                        ),
                        (
                            "Todos los archivos",
                            "*.*"
                        )
                    ],
                    initialfile=(
                        "Reporte_Equipos.xlsx"
                    )
                )
            )

            if not archivo:

                return

            # =================================================
            # CREAR LIBRO
            # =================================================

            wb = Workbook()

            ws = wb.active

            ws.title = "Reporte Equipos"

            # =================================================
            # ENCABEZADOS
            # =================================================

            encabezados = [
                "Código",
                "Equipo",
                "Número de serie",
                "Categoría",
                "Marca",
                "Modelo",
                "Proveedor",
                "Estado",
                "Responsable",
                "Ubicación",
                "Fecha compra",
                "Garantía meses",
                "Precio",
                "Registro"
            ]

            ws.append(
                encabezados
            )

            # =================================================
            # FORMATO ENCABEZADOS
            # =================================================

            for celda in ws[1]:

                celda.font = Font(
                    bold=True
                )

                celda.alignment = Alignment(
                    horizontal="center",
                    vertical="center"
                )

            # =================================================
            # DATOS
            # =================================================

            for equipo in self.datos_reporte:

                fecha_compra = (
                    equipo.get(
                        "fecha_compra"
                    )
                    or ""
                )

                precio = equipo.get(
                    "precio"
                )

                if precio is not None:

                    try:

                        precio = float(
                            precio
                        )

                    except Exception:

                        pass

                activo = (
                    "Activo"
                    if equipo.get(
                        "activo"
                    ) == 1
                    else "Inactivo"
                )

                ws.append(
                    [
                        equipo.get(
                            "codigo"
                        ) or "",

                        equipo.get(
                            "nombre"
                        ) or "",

                        equipo.get(
                            "numero_serie"
                        ) or "",

                        equipo.get(
                            "categoria"
                        ) or "",

                        equipo.get(
                            "marca"
                        ) or "",

                        equipo.get(
                            "modelo"
                        ) or "",

                        equipo.get(
                            "proveedor"
                        ) or "",

                        equipo.get(
                            "estado"
                        ) or "",

                        equipo.get(
                            "responsable"
                        ) or "",

                        equipo.get(
                            "ubicacion"
                        ) or "",

                        str(
                            fecha_compra
                        ),

                        equipo.get(
                            "garantia_meses"
                        ) or 0,

                        precio,

                        activo
                    ]
                )

            # =================================================
            # FILTRO
            # =================================================

            ws.auto_filter.ref = (
                ws.dimensions
            )

            # =================================================
            # CONGELAR ENCABEZADO
            # =================================================

            ws.freeze_panes = "A2"

            # =================================================
            # ANCHOS
            # =================================================

            anchos = {
                "A": 15,
                "B": 28,
                "C": 25,
                "D": 20,
                "E": 20,
                "F": 22,
                "G": 30,
                "H": 18,
                "I": 30,
                "J": 22,
                "K": 18,
                "L": 18,
                "M": 15,
                "N": 15
            }

            for columna, ancho in anchos.items():

                ws.column_dimensions[
                    columna
                ].width = ancho

            # =================================================
            # GUARDAR
            # =================================================

            wb.save(
                archivo
            )

            # =================================================
            # CONFIRMACIÓN
            # =================================================

            messagebox.showinfo(
                "Exportación completada",
                (
                    "El reporte fue exportado "
                    "correctamente a Excel.\n\n"
                    f"Registros exportados: "
                    f"{len(self.datos_reporte)}"
                ),
                parent=self
            )

            print(
                "Reporte exportado:",
                archivo
            )

        except Exception as e:

            print(
                "Error al exportar reporte:",
                e
            )

            messagebox.showerror(
                "Error al exportar",
                (
                    "No se pudo exportar "
                    "el reporte.\n\n"
                    f"{e}"
                ),
                parent=self
            )