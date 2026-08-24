import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog

from app.models.movimiento_model import MovimientoModel


# =========================================================
# VENTANA DE REPORTE DE MOVIMIENTOS
# =========================================================

class VentanaReporteMovimientos(ctk.CTkToplevel):

    def __init__(self, master=None):

        super().__init__(master)

        # =================================================
        # MODELO
        # =================================================

        self.modelo = MovimientoModel()

        # =================================================
        # DATOS ACTUALES DEL REPORTE
        # =================================================

        self.datos_actuales = []

        # =================================================
        # CONFIGURACIÓN DE VENTANA
        # =================================================

        self.title(
            "Reporte de Movimientos de Insumos"
        )

        self.geometry(
            "1350x700"
        )

        self.minsize(
            1100,
            600
        )

        self.transient(
            master
        )

        # =================================================
        # CREAR INTERFAZ
        # =================================================

        self.crear_interfaz()

        # =================================================
        # CARGAR MOVIMIENTOS
        # =================================================

        self.cargar_movimientos()


    # =====================================================
    # CREAR INTERFAZ
    # =====================================================

    def crear_interfaz(self):

        # =================================================
        # TÍTULO
        # =================================================

        titulo = ctk.CTkLabel(
            self,
            text="Reporte de Movimientos de Insumos",
            font=("Arial", 24, "bold")
        )

        titulo.pack(
            pady=15
        )


        # =================================================
        # FRAME DE FILTROS
        # =================================================

        frame_filtros = ctk.CTkFrame(
            self
        )

        frame_filtros.pack(
            fill="x",
            padx=15,
            pady=5
        )


        # =================================================
        # BUSCADOR
        # =================================================

        label_buscar = ctk.CTkLabel(
            frame_filtros,
            text="Buscar:"
        )

        label_buscar.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )


        self.txt_buscar = ctk.CTkEntry(
            frame_filtros,
            width=220,
            placeholder_text="Código o nombre"
        )

        self.txt_buscar.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )


        # =================================================
        # TIPO DE MOVIMIENTO
        # =================================================

        label_tipo = ctk.CTkLabel(
            frame_filtros,
            text="Tipo:"
        )

        label_tipo.grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )


        self.cmb_tipo = ctk.CTkComboBox(
            frame_filtros,
            values=[
                "TODOS",
                "ENTRADA",
                "SALIDA",
                "AJUSTE"
            ],
            width=150
        )

        self.cmb_tipo.grid(
            row=0,
            column=3,
            padx=10,
            pady=10
        )

        self.cmb_tipo.set(
            "TODOS"
        )


        # =================================================
        # BOTÓN BUSCAR
        # =================================================

        btn_buscar = ctk.CTkButton(
            frame_filtros,
            text="🔎 Buscar",
            width=120,
            height=35,
            command=self.filtrar
        )

        btn_buscar.grid(
            row=0,
            column=4,
            padx=10,
            pady=10
        )


        # =================================================
        # BOTÓN ACTUALIZAR
        # =================================================

        btn_actualizar = ctk.CTkButton(
            frame_filtros,
            text="🔄 Actualizar",
            width=120,
            height=35,
            command=self.cargar_movimientos
        )

        btn_actualizar.grid(
            row=0,
            column=5,
            padx=10,
            pady=10
        )


        # =================================================
        # BOTÓN EXPORTAR EXCEL
        # =================================================

        btn_exportar = ctk.CTkButton(
            frame_filtros,
            text="📥 Exportar a Excel",
            width=160,
            height=35,
            command=self.exportar_excel
        )

        btn_exportar.grid(
            row=0,
            column=6,
            padx=10,
            pady=10
        )


        # =================================================
        # RESUMEN
        # =================================================

        self.lbl_resumen = ctk.CTkLabel(
            self,
            text="Entradas: 0 | Salidas: 0 | Ajustes: 0",
            font=("Arial", 16, "bold")
        )

        self.lbl_resumen.pack(
            pady=10
        )


        # =================================================
        # FRAME TABLA
        # =================================================

        frame_tabla = ctk.CTkFrame(
            self
        )

        frame_tabla.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )


        # =================================================
        # COLUMNAS
        # =================================================

        columnas = (

            "ID",

            "Código",

            "Insumo",

            "Movimiento",

            "Cantidad",

            "Stock anterior",

            "Stock nuevo",

            "Responsable",

            "Observaciones",

            "Fecha"

        )


        # =================================================
        # CREAR TABLA
        # =================================================

        self.tabla = ttk.Treeview(

            frame_tabla,

            columns=columnas,

            show="headings"

        )


        # =================================================
        # ANCHOS
        # =================================================

        anchos = {

            "ID": 60,

            "Código": 100,

            "Insumo": 180,

            "Movimiento": 120,

            "Cantidad": 90,

            "Stock anterior": 110,

            "Stock nuevo": 100,

            "Responsable": 180,

            "Observaciones": 200,

            "Fecha": 150

        }


        # =================================================
        # CONFIGURAR COLUMNAS
        # =================================================

        for columna in columnas:

            self.tabla.heading(

                columna,

                text=columna

            )

            self.tabla.column(

                columna,

                width=anchos[columna],

                anchor="center",

                stretch=True

            )


        # =================================================
        # SCROLLBAR VERTICAL
        # =================================================

        scrollbar_vertical = ttk.Scrollbar(

            frame_tabla,

            orient="vertical",

            command=self.tabla.yview

        )


        # =================================================
        # SCROLLBAR HORIZONTAL
        # =================================================

        scrollbar_horizontal = ttk.Scrollbar(

            frame_tabla,

            orient="horizontal",

            command=self.tabla.xview

        )


        # =================================================
        # CONFIGURAR SCROLLBAR
        # =================================================

        self.tabla.configure(

            yscrollcommand=scrollbar_vertical.set,

            xscrollcommand=scrollbar_horizontal.set

        )


        # =================================================
        # COLOCAR TABLA
        # =================================================

        self.tabla.grid(

            row=0,

            column=0,

            sticky="nsew"

        )


        scrollbar_vertical.grid(

            row=0,

            column=1,

            sticky="ns"

        )


        scrollbar_horizontal.grid(

            row=1,

            column=0,

            sticky="ew"

        )


        # =================================================
        # CONFIGURAR GRID
        # =================================================

        frame_tabla.grid_rowconfigure(

            0,

            weight=1

        )


        frame_tabla.grid_columnconfigure(

            0,

            weight=1

        )


    # =====================================================
    # CARGAR TODOS LOS MOVIMIENTOS
    # =====================================================

    def cargar_movimientos(self):

        try:

            datos = self.modelo.listar()

            self.mostrar_datos(
                datos
            )

        except Exception as e:

            print(
                "Error al cargar movimientos:",
                e
            )

            messagebox.showerror(

                "Error",

                f"No se pudo generar el reporte:\n\n{e}",

                parent=self

            )


    # =====================================================
    # MOSTRAR DATOS EN TABLA
    # =====================================================

    def mostrar_datos(
        self,
        datos
    ):

        # =================================================
        # GUARDAR DATOS ACTUALES
        # =================================================

        self.datos_actuales = list(
            datos
        )


        # =================================================
        # LIMPIAR TABLA
        # =================================================

        for fila in self.tabla.get_children():

            self.tabla.delete(
                fila
            )


        # =================================================
        # CONTADORES
        # =================================================

        entradas = 0

        salidas = 0

        ajustes = 0


        # =================================================
        # INSERTAR DATOS
        # =================================================

        for movimiento in datos:

            self.tabla.insert(

                "",

                "end",

                values=movimiento

            )


            # =================================================
            # OBTENER TIPO
            # =================================================

            if len(movimiento) > 3:

                tipo = str(

                    movimiento[3]

                ).strip().upper()

            else:

                tipo = ""


            # =================================================
            # OBTENER CANTIDAD
            # =================================================

            try:

                cantidad = int(

                    movimiento[4]

                )

            except (
                ValueError,
                TypeError,
                IndexError
            ):

                cantidad = 0


            # =================================================
            # SUMAR ENTRADAS
            # =================================================

            if tipo == "ENTRADA":

                entradas += cantidad


            # =================================================
            # SUMAR SALIDAS
            # =================================================

            elif tipo == "SALIDA":

                salidas += cantidad


            # =================================================
            # SUMAR AJUSTES
            # =================================================

            elif tipo == "AJUSTE":

                ajustes += cantidad


        # =================================================
        # ACTUALIZAR RESUMEN
        # =================================================

        self.lbl_resumen.configure(

            text=(

                f"Entradas: {entradas} | "

                f"Salidas: {salidas} | "

                f"Ajustes: {ajustes}"

            )

        )


    # =====================================================
    # FILTRAR MOVIMIENTOS
    # =====================================================

    def filtrar(self):

        try:

            # =================================================
            # TEXTO DE BÚSQUEDA
            # =================================================

            texto = (

                self.txt_buscar.get()

                .strip()

                .lower()

            )


            # =================================================
            # TIPO SELECCIONADO
            # =================================================

            tipo_seleccionado = (

                self.cmb_tipo.get()

                .strip()

                .upper()

            )


            # =================================================
            # OBTENER TODOS LOS MOVIMIENTOS
            # =================================================

            datos = self.modelo.listar()


            # =================================================
            # LISTA DE RESULTADOS
            # =================================================

            resultados = []


            # =================================================
            # RECORRER DATOS
            # =================================================

            for movimiento in datos:

                # =============================================
                # CÓDIGO
                # =============================================

                try:

                    codigo = str(

                        movimiento[1]

                    ).lower()

                except IndexError:

                    codigo = ""


                # =============================================
                # NOMBRE DEL INSUMO
                # =============================================

                try:

                    insumo = str(

                        movimiento[2]

                    ).lower()

                except IndexError:

                    insumo = ""


                # =============================================
                # TIPO DE MOVIMIENTO
                # =============================================

                try:

                    tipo = str(

                        movimiento[3]

                    ).strip().upper()

                except IndexError:

                    tipo = ""


                # =============================================
                # COMPROBAR TEXTO
                # =============================================

                coincide_texto = (

                    not texto

                    or texto in codigo

                    or texto in insumo

                )


                # =============================================
                # COMPROBAR TIPO
                # =============================================

                coincide_tipo = (

                    tipo_seleccionado == "TODOS"

                    or tipo == tipo_seleccionado

                )


                # =============================================
                # AGREGAR RESULTADO
                # =============================================

                if (

                    coincide_texto

                    and coincide_tipo

                ):

                    resultados.append(

                        movimiento

                    )


            # =================================================
            # MOSTRAR RESULTADOS
            # =================================================

            self.mostrar_datos(

                resultados

            )


            print(

                "Resultados encontrados:",

                len(resultados)

            )


        except Exception as e:

            print(

                "Error al filtrar:",

                e

            )

            messagebox.showerror(

                "Error",

                f"No se pudo filtrar el reporte:\n\n{e}",

                parent=self

            )


    # =====================================================
    # EXPORTAR A EXCEL
    # =====================================================

    def exportar_excel(self):

        try:

            # =================================================
            # COMPROBAR DATOS
            # =================================================

            if not self.datos_actuales:

                messagebox.showwarning(

                    "Sin datos",

                    "No hay movimientos para exportar.",

                    parent=self

                )

                return


            # =================================================
            # IMPORTAR OPENPYXL
            # =================================================

            try:

                from openpyxl import Workbook

            except ImportError:

                messagebox.showerror(

                    "Librería no instalada",

                    "No se encontró la librería openpyxl.\n\n"

                    "Instálala ejecutando:\n\n"

                    "pip install openpyxl",

                    parent=self

                )

                return


            # =================================================
            # SELECCIONAR ARCHIVO
            # =================================================

            ruta = filedialog.asksaveasfilename(

                parent=self,

                title="Guardar reporte de movimientos",

                defaultextension=".xlsx",

                filetypes=[

                    (

                        "Archivos de Excel",

                        "*.xlsx"

                    )

                ],

                initialfile=(

                    "reporte_movimientos.xlsx"

                )

            )


            # =================================================
            # SI CANCELA
            # =================================================

            if not ruta:

                return


            # =================================================
            # CREAR LIBRO
            # =================================================

            libro = Workbook()


            hoja = libro.active


            hoja.title = (

                "Movimientos"

            )


            # =================================================
            # ENCABEZADOS
            # =================================================

            encabezados = [

                "ID",

                "Código",

                "Insumo",

                "Movimiento",

                "Cantidad",

                "Stock anterior",

                "Stock nuevo",

                "Responsable",

                "Observaciones",

                "Fecha"

            ]


            hoja.append(

                encabezados

            )


            # =================================================
            # INSERTAR DATOS
            # =================================================

            for movimiento in self.datos_actuales:

                hoja.append(

                    list(

                        movimiento

                    )

                )


            # =================================================
            # AJUSTAR ANCHOS
            # =================================================

            anchos = {

                "A": 10,

                "B": 15,

                "C": 30,

                "D": 18,

                "E": 12,

                "F": 18,

                "G": 15,

                "H": 30,

                "I": 40,

                "J": 22

            }


            for columna, ancho in anchos.items():

                hoja.column_dimensions[

                    columna

                ].width = ancho


            # =================================================
            # CONGELAR ENCABEZADOS
            # =================================================

            hoja.freeze_panes = (

                "A2"

            )


            # =================================================
            # GUARDAR
            # =================================================

            libro.save(

                ruta

            )


            # =================================================
            # MENSAJE
            # =================================================

            messagebox.showinfo(

                "Exportación completada",

                "El reporte fue exportado correctamente.\n\n"

                f"Archivo guardado en:\n{ruta}",

                parent=self

            )


            print(

                "Reporte exportado:",

                ruta

            )


        except Exception as e:

            print(

                "Error al exportar a Excel:",

                e

            )

            messagebox.showerror(

                "Error",

                "No se pudo exportar el reporte a Excel:\n\n"

                f"{e}",

                parent=self

            )