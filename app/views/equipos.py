import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from openpyxl import Workbook

from app.models.equipo_model import EquipoModel
from app.utils.ventana import configurar_ventana


class VentanaEquipos(ctk.CTkToplevel):

    def __init__(self, master=None):

        super().__init__(master)

        # =====================================================
        # CONFIGURACIÓN
        # =====================================================

        self.modelo = EquipoModel()

        self.title(
            "Gestión de Equipos"
        )

        self.transient(
            master
        )

        # =====================================================
        # CONFIGURAR VENTANA AUTOMÁTICAMENTE
        # =====================================================

        configurar_ventana(
            self,
            ancho=950,
            alto=550,
            maximizada=True
        )

        # =====================================================
        # CREAR INTERFAZ
        # =====================================================

        self.crear_interfaz()

        # =====================================================
        # CARGAR EQUIPOS
        # =====================================================

        self.cargar_equipos()

        # =====================================================
        # ASEGURAR VENTANA AL FRENTE
        # =====================================================

        self.lift()

        self.focus_force()

    # =====================================================
    # CREAR INTERFAZ
    # =====================================================

    def crear_interfaz(self):

        # =================================================
        # TÍTULO
        # =================================================

        titulo = ctk.CTkLabel(
            self,
            text="Inventario de Equipos Tecnológicos",
            font=("Arial", 22, "bold")
        )

        titulo.pack(
            pady=(10, 5)
        )

        # =================================================
        # FRAME DE ACCIONES
        # =================================================

        frame_acciones = ctk.CTkFrame(
            self
        )

        frame_acciones.pack(
            fill="x",
            padx=15,
            pady=8
        )

        # =================================================
        # BOTÓN NUEVO
        # =================================================

        btn_nuevo = ctk.CTkButton(
            frame_acciones,
            text="➕ Nuevo",
            width=120,
            height=35,
            command=self.abrir_nuevo
        )

        btn_nuevo.pack(
            side="left",
            padx=5,
            pady=8
        )

        # =================================================
        # BOTÓN EDITAR
        # =================================================

        btn_editar = ctk.CTkButton(
            frame_acciones,
            text="✏ Editar",
            width=120,
            height=35,
            command=self.editar_equipo
        )

        btn_editar.pack(
            side="left",
            padx=5,
            pady=8
        )

        # =================================================
        # BOTÓN ELIMINAR
        # =================================================

        btn_eliminar = ctk.CTkButton(
            frame_acciones,
            text="🗑 Eliminar",
            width=120,
            height=35,
            command=self.eliminar_equipo
        )

        btn_eliminar.pack(
            side="left",
            padx=5,
            pady=8
        )

        # =================================================
        # BOTÓN EXPORTAR
        # =================================================

        btn_exportar = ctk.CTkButton(
            frame_acciones,
            text="📊 Exportar a Excel",
            width=150,
            height=35,
            command=self.exportar_a_excel
        )

        btn_exportar.pack(
            side="left",
            padx=5,
            pady=8
        )

        # =================================================
        # BUSCADOR
        # =================================================

        self.buscar = ctk.CTkEntry(
            frame_acciones,
            width=280,
            height=35,
            placeholder_text="Código, equipo o serie..."
        )

        self.buscar.pack(
            side="right",
            padx=5,
            pady=8
        )

        # =================================================
        # BOTÓN BUSCAR
        # =================================================

        btn_buscar = ctk.CTkButton(
            frame_acciones,
            text="🔍 Buscar",
            width=110,
            height=35,
            command=self.buscar_equipo
        )

        btn_buscar.pack(
            side="right",
            padx=5,
            pady=8
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
            pady=(5, 10)
        )

        # =================================================
        # COLUMNAS
        # =================================================

        columnas = (
            "ID",
            "Código",
            "Equipo",
            "Serie",
            "Categoría",
            "Marca",
            "Estado",
            "Fecha Compra",
            "Precio"
        )

        # =================================================
        # TABLA
        # =================================================

        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        # =================================================
        # ANCHOS
        # =================================================

        anchos = {
            "ID": 60,
            "Código": 110,
            "Equipo": 220,
            "Serie": 160,
            "Categoría": 140,
            "Marca": 130,
            "Estado": 110,
            "Fecha Compra": 120,
            "Precio": 100
        }

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

        # =================================================
        # SCROLLBAR VERTICAL
        # =================================================

        scrollbar_vertical.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        # =================================================
        # SCROLLBAR HORIZONTAL
        # =================================================

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

        # =================================================
        # DOBLE CLIC PARA EDITAR
        # =================================================

        self.tabla.bind(
            "<Double-1>",
            lambda event: self.editar_equipo()
        )

        # =================================================
        # ENTER PARA BUSCAR
        # =================================================

        self.buscar.bind(
            "<Return>",
            lambda event: self.buscar_equipo()
        )

    # =====================================================
    # CARGAR EQUIPOS
    # =====================================================

    def cargar_equipos(self):

        try:

            # -------------------------------------------------
            # LIMPIAR TABLA
            # -------------------------------------------------

            for fila in self.tabla.get_children():

                self.tabla.delete(
                    fila
                )

            # -------------------------------------------------
            # CONSULTAR BASE DE DATOS
            # -------------------------------------------------

            datos = self.modelo.listar()

            # -------------------------------------------------
            # INSERTAR DATOS
            # -------------------------------------------------

            for equipo in datos:

                self.tabla.insert(
                    "",
                    "end",
                    values=equipo
                )

            print(
                "Equipos cargados:",
                len(datos)
            )

        except Exception as e:

            print(
                "Error al cargar equipos:",
                e
            )

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los equipos:\n\n{e}",
                parent=self
            )

    # =====================================================
    # NUEVO EQUIPO
    # =====================================================

    def abrir_nuevo(self):

        try:

            from app.views.formulario_equipo import FormularioEquipo

            ventana = FormularioEquipo(
                self
            )

            self.wait_window(
                ventana
            )

            self.cargar_equipos()

        except Exception as e:

            print(
                "Error al abrir formulario de equipo:",
                e
            )

            messagebox.showerror(
                "Error",
                f"No se pudo abrir el formulario:\n\n{e}",
                parent=self
            )

    # =====================================================
    # EDITAR EQUIPO
    # =====================================================

    def editar_equipo(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:

            messagebox.showwarning(
                "Aviso",
                "Seleccione un equipo para editar.",
                parent=self
            )

            return

        item = self.tabla.item(
            seleccionado[0]
        )

        valores = item.get(
            "values"
        )

        if not valores:

            messagebox.showerror(
                "Error",
                "No se pudo obtener el equipo seleccionado.",
                parent=self
            )

            return

        id_equipo = valores[0]

        try:

            from app.views.formulario_equipo import FormularioEquipo

            ventana = FormularioEquipo(
                self,
                id_equipo=id_equipo
            )

            self.wait_window(
                ventana
            )

            self.cargar_equipos()

        except Exception as e:

            print(
                "Error al editar equipo:",
                e
            )

            messagebox.showerror(
                "Error",
                f"No se pudo abrir el formulario de edición:\n\n{e}",
                parent=self
            )

    # =====================================================
    # BUSCAR EQUIPO
    # =====================================================

    def buscar_equipo(self):

        texto = self.buscar.get().strip()

        try:

            # -------------------------------------------------
            # SI ESTÁ VACÍO, MOSTRAR TODOS
            # -------------------------------------------------

            if not texto:

                self.cargar_equipos()

                return

            # -------------------------------------------------
            # LIMPIAR TABLA
            # -------------------------------------------------

            for fila in self.tabla.get_children():

                self.tabla.delete(
                    fila
                )

            # -------------------------------------------------
            # BUSCAR EN BASE DE DATOS
            # -------------------------------------------------

            datos = self.modelo.buscar(
                texto
            )

            # -------------------------------------------------
            # MOSTRAR RESULTADOS
            # -------------------------------------------------

            for equipo in datos:

                self.tabla.insert(
                    "",
                    "end",
                    values=equipo
                )

            print(
                "Resultados encontrados:",
                len(datos)
            )

            # -------------------------------------------------
            # SIN RESULTADOS
            # -------------------------------------------------

            if not datos:

                messagebox.showinfo(
                    "Búsqueda",
                    f"No se encontraron equipos para:\n\n{texto}",
                    parent=self
                )

        except Exception as e:

            print(
                "Error en búsqueda:",
                e
            )

            messagebox.showerror(
                "Error",
                f"No se pudo realizar la búsqueda:\n\n{e}",
                parent=self
            )

    # =====================================================
    # EXPORTAR A EXCEL
    # =====================================================

    def exportar_a_excel(self):

        try:

            # -------------------------------------------------
            # OBTENER DATOS DIRECTAMENTE DE LA BASE
            # -------------------------------------------------

            datos = self.modelo.listar()

            if not datos:

                messagebox.showwarning(
                    "Sin datos",
                    "No existen equipos registrados para exportar.",
                    parent=self
                )

                return

            # -------------------------------------------------
            # SELECCIONAR UBICACIÓN
            # -------------------------------------------------

            archivo = filedialog.asksaveasfilename(
                parent=self,
                title="Guardar archivo Excel",
                defaultextension=".xlsx",
                initialfile="equipos.xlsx",
                filetypes=[
                    ("Archivos Excel", "*.xlsx")
                ]
            )

            if not archivo:

                return

            # -------------------------------------------------
            # CREAR LIBRO
            # -------------------------------------------------

            wb = Workbook()

            ws = wb.active

            ws.title = "Equipos"

            # -------------------------------------------------
            # ENCABEZADOS
            # -------------------------------------------------

            encabezados = [
                "ID",
                "Código",
                "Equipo",
                "Serie",
                "Categoría",
                "Marca",
                "Estado",
                "Fecha Compra",
                "Precio"
            ]

            ws.append(
                encabezados
            )

            # -------------------------------------------------
            # DATOS
            # -------------------------------------------------

            for equipo in datos:

                ws.append(
                    list(equipo)
                )

            # -------------------------------------------------
            # ANCHOS
            # -------------------------------------------------

            anchos = {
                "A": 10,
                "B": 18,
                "C": 35,
                "D": 25,
                "E": 20,
                "F": 20,
                "G": 18,
                "H": 18,
                "I": 15
            }

            for columna, ancho in anchos.items():

                ws.column_dimensions[
                    columna
                ].width = ancho

            # -------------------------------------------------
            # ENCABEZADOS EN NEGRITA
            # -------------------------------------------------

            for celda in ws[1]:

                celda.font = celda.font.copy(
                    bold=True
                )

            # -------------------------------------------------
            # CONGELAR ENCABEZADO
            # -------------------------------------------------

            ws.freeze_panes = "A2"

            # -------------------------------------------------
            # FILTRO
            # -------------------------------------------------

            ws.auto_filter.ref = ws.dimensions

            # -------------------------------------------------
            # GUARDAR
            # -------------------------------------------------

            wb.save(
                archivo
            )

            # -------------------------------------------------
            # CONFIRMACIÓN
            # -------------------------------------------------

            messagebox.showinfo(
                "Exportación completada",
                f"Los equipos fueron exportados correctamente.\n\n"
                f"Registros exportados: {len(datos)}\n\n"
                f"Archivo:\n{archivo}",
                parent=self
            )

            print(
                "Excel exportado correctamente:",
                archivo
            )

        except Exception as e:

            print(
                "Error al exportar a Excel:",
                e
            )

            messagebox.showerror(
                "Error",
                f"No se pudo exportar a Excel:\n\n{e}",
                parent=self
            )

    # =====================================================
    # ELIMINAR EQUIPO
    # =====================================================

    def eliminar_equipo(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:

            messagebox.showwarning(
                "Aviso",
                "Seleccione un equipo para eliminar.",
                parent=self
            )

            return

        item = self.tabla.item(
            seleccionado[0]
        )

        valores = item.get(
            "values"
        )

        if not valores:

            messagebox.showerror(
                "Error",
                "No se pudo obtener el equipo seleccionado.",
                parent=self
            )

            return

        id_equipo = valores[0]

        nombre_equipo = valores[2]

        # =================================================
        # CONFIRMAR
        # =================================================

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Desea eliminar este equipo?\n\n"
            f"ID: {id_equipo}\n"
            f"Equipo: {nombre_equipo}",
            parent=self
        )

        if not confirmar:

            return

        try:

            # -------------------------------------------------
            # ELIMINAR DE LA BASE DE DATOS
            # -------------------------------------------------

            self.modelo.eliminar(
                id_equipo
            )

            # -------------------------------------------------
            # RECARGAR TABLA
            # -------------------------------------------------

            self.cargar_equipos()

            messagebox.showinfo(
                "Correcto",
                "Equipo eliminado correctamente.",
                parent=self
            )

        except Exception as e:

            print(
                "Error al eliminar:",
                e
            )

            messagebox.showerror(
                "Error",
                f"No se pudo eliminar el equipo:\n\n{e}",
                parent=self
            )