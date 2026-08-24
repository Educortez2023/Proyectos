# insumos.py

import customtkinter as ctk
from tkinter import ttk, messagebox

from app.models.insumo_model import InsumoModel
from app.views.formulario_insumo import FormularioInsumo
from app.views.movimientos import VentanaMovimientos
from app.views.reporte_movimientos import VentanaReporteMovimientos


class VentanaInsumos(ctk.CTkToplevel):

    def __init__(self, master=None):

        super().__init__(master)

        # =================================================
        # OCULTAR VENTANA DURANTE LA CONFIGURACIÓN
        # =================================================

        self.withdraw()

        self.master = master
        self.modelo = InsumoModel()

        # =================================================
        # CONFIGURACIÓN DE VENTANA
        # =================================================

        self.title(
            "Gestión de Insumos Tecnológicos"
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
        # CARGAR DATOS
        # =================================================

        self.cargar_insumos()

        # =================================================
        # MOSTRAR MAXIMIZADA
        # =================================================

        self.after(
            50,
            self.mostrar_maximizada
        )

    # =====================================================
    # MOSTRAR VENTANA MAXIMIZADA
    # =====================================================

    def mostrar_maximizada(self):

        try:

            # -------------------------------------------------
            # MAXIMIZAR ANTES DE MOSTRAR
            # -------------------------------------------------

            self.state(
                "zoomed"
            )

        except Exception as e:

            print(
                "No se pudo maximizar con state:",
                e
            )

            # -------------------------------------------------
            # RESPALDO
            # -------------------------------------------------

            try:

                ancho = self.winfo_screenwidth()
                alto = self.winfo_screenheight()

                self.geometry(
                    f"{ancho}x{alto}+0+0"
                )

            except Exception as error:

                print(
                    "No se pudo ajustar la ventana:",
                    error
                )

        # -------------------------------------------------
        # MOSTRAR VENTANA YA AJUSTADA
        # -------------------------------------------------

        self.deiconify()

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
            text="Gestión de Insumos Tecnológicos",
            font=("Arial", 24, "bold")
        )

        titulo.pack(
            pady=(15, 10)
        )

        # =================================================
        # FRAME DE BOTONES
        # =================================================

        frame_botones = ctk.CTkFrame(
            self
        )

        frame_botones.pack(
            fill="x",
            padx=15,
            pady=5
        )

        # =================================================
        # BOTÓN NUEVO
        # =================================================

        btn_nuevo = ctk.CTkButton(
            frame_botones,
            text="➕ Nuevo Insumo",
            width=150,
            height=35,
            command=self.nuevo_insumo
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
            frame_botones,
            text="✏️ Editar",
            width=120,
            height=35,
            command=self.editar_insumo
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
            frame_botones,
            text="🗑️ Eliminar",
            width=120,
            height=35,
            command=self.eliminar_insumo
        )

        btn_eliminar.pack(
            side="left",
            padx=5,
            pady=8
        )

        # =================================================
        # BOTÓN MOVIMIENTOS
        # =================================================

        btn_movimientos = ctk.CTkButton(
            frame_botones,
            text="📋 Movimientos",
            width=150,
            height=35,
            command=self.abrir_movimientos
        )

        btn_movimientos.pack(
            side="left",
            padx=5,
            pady=8
        )

        # =================================================
        # BOTÓN REPORTES
        # =================================================

        btn_reportes = ctk.CTkButton(
            frame_botones,
            text="📊 Reportes",
            width=150,
            height=35,
            command=self.abrir_reporte_movimientos
        )

        btn_reportes.pack(
            side="left",
            padx=5,
            pady=8
        )

        # =================================================
        # BUSCADOR
        # =================================================

        self.txt_buscar = ctk.CTkEntry(
            frame_botones,
            width=250,
            height=35,
            placeholder_text="Buscar por código o nombre..."
        )

        self.txt_buscar.pack(
            side="right",
            padx=5,
            pady=8
        )

        # =================================================
        # BOTÓN BUSCAR
        # =================================================

        btn_buscar = ctk.CTkButton(
            frame_botones,
            text="🔎 Buscar",
            width=100,
            height=35,
            command=self.buscar_insumos
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
            pady=10
        )

        # =================================================
        # COLUMNAS
        # =================================================

        columnas = (
            "ID",
            "Código",
            "Nombre",
            "Categoría",
            "Marca",
            "Proveedor",
            "Stock",
            "Stock mínimo",
            "Precio",
            "Ubicación",
            "Observaciones"
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
            "Código": 100,
            "Nombre": 180,
            "Categoría": 120,
            "Marca": 120,
            "Proveedor": 180,
            "Stock": 80,
            "Stock mínimo": 100,
            "Precio": 100,
            "Ubicación": 150,
            "Observaciones": 200

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

        self.tabla.configure(
            yscrollcommand=scrollbar_vertical.set,
            xscrollcommand=scrollbar_horizontal.set
        )

        # =================================================
        # GRID TABLA
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
        # DOBLE CLICK PARA EDITAR
        # =================================================

        self.tabla.bind(
            "<Double-1>",
            lambda event: self.editar_insumo()
        )

        # =================================================
        # ENTER PARA BUSCAR
        # =================================================

        self.txt_buscar.bind(
            "<Return>",
            lambda event: self.buscar_insumos()
        )

    # =====================================================
    # CARGAR INSUMOS
    # =====================================================

    def cargar_insumos(self):

        try:

            # -------------------------------------------------
            # LIMPIAR TABLA
            # -------------------------------------------------

            for fila in self.tabla.get_children():

                self.tabla.delete(
                    fila
                )

            # -------------------------------------------------
            # OBTENER DATOS
            # -------------------------------------------------

            datos = self.modelo.listar()

            # -------------------------------------------------
            # INSERTAR DATOS
            # -------------------------------------------------

            for insumo in datos:

                self.tabla.insert(
                    "",
                    "end",
                    values=insumo
                )

            print(
                "Insumos cargados:",
                len(datos)
            )

        except Exception as e:

            print(
                "Error al cargar insumos:",
                e
            )

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los insumos:\n\n{e}",
                parent=self
            )

    # =====================================================
    # BUSCAR INSUMOS
    # =====================================================

    def buscar_insumos(self):

        try:

            texto = (
                self.txt_buscar.get()
                .strip()
            )

            # -------------------------------------------------
            # SI ESTÁ VACÍO
            # -------------------------------------------------

            if not texto:

                self.cargar_insumos()

                return

            # -------------------------------------------------
            # BUSCAR
            # -------------------------------------------------

            datos = self.modelo.buscar(
                texto
            )

            # -------------------------------------------------
            # LIMPIAR TABLA
            # -------------------------------------------------

            for fila in self.tabla.get_children():

                self.tabla.delete(
                    fila
                )

            # -------------------------------------------------
            # MOSTRAR RESULTADOS
            # -------------------------------------------------

            for insumo in datos:

                self.tabla.insert(
                    "",
                    "end",
                    values=insumo
                )

            print(
                "Resultados encontrados:",
                len(datos)
            )

            if not datos:

                messagebox.showinfo(
                    "Búsqueda",
                    f"No se encontraron insumos para:\n\n{texto}",
                    parent=self
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudo realizar la búsqueda:\n\n{e}",
                parent=self
            )

    # =====================================================
    # OBTENER ID SELECCIONADO
    # =====================================================

    def obtener_id_seleccionado(self):

        seleccion = self.tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Seleccionar insumo",
                "Debe seleccionar un insumo.",
                parent=self
            )

            return None

        fila = self.tabla.item(
            seleccion[0]
        )

        valores = fila.get(
            "values"
        )

        if not valores:

            return None

        return valores[0]

    # =====================================================
    # NUEVO INSUMO
    # =====================================================

    def nuevo_insumo(self):

        try:

            ventana = FormularioInsumo(
                self
            )

            self.wait_window(
                ventana
            )

            self.cargar_insumos()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudo abrir el formulario:\n\n{e}",
                parent=self
            )

    # =====================================================
    # EDITAR INSUMO
    # =====================================================

    def editar_insumo(self):

        id_insumo = (
            self.obtener_id_seleccionado()
        )

        if id_insumo is None:

            return

        try:

            ventana = FormularioInsumo(
                self,
                id_insumo
            )

            self.wait_window(
                ventana
            )

            self.cargar_insumos()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudo abrir el formulario de edición:\n\n{e}",
                parent=self
            )

    # =====================================================
    # ELIMINAR INSUMO
    # =====================================================

    def eliminar_insumo(self):

        id_insumo = (
            self.obtener_id_seleccionado()
        )

        if id_insumo is None:

            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro de desactivar este insumo?",
            parent=self
        )

        if not confirmar:

            return

        try:

            self.modelo.eliminar(
                id_insumo
            )

            messagebox.showinfo(
                "Correcto",
                "El insumo fue desactivado correctamente.",
                parent=self
            )

            self.cargar_insumos()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudo eliminar el insumo:\n\n{e}",
                parent=self
            )

    # =====================================================
    # ABRIR MOVIMIENTOS
    # =====================================================

    def abrir_movimientos(self):

        try:

            ventana = VentanaMovimientos(
                self
            )

            self.wait_window(
                ventana
            )

            self.cargar_insumos()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudo abrir la ventana de movimientos:\n\n{e}",
                parent=self
            )

    # =====================================================
    # ABRIR REPORTE DE MOVIMIENTOS
    # =====================================================

    def abrir_reporte_movimientos(self):

        try:

            ventana = VentanaReporteMovimientos(
                self
            )

            self.wait_window(
                ventana
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudo abrir el reporte de movimientos:\n\n{e}",
                parent=self
            )