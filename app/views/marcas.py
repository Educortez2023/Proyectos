import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from openpyxl import Workbook

from app.models.marca_model import MarcaModel
from app.views.formulario_marca import FormularioMarca


class VentanaMarcas(ctk.CTkToplevel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent

        # =====================================================
        # CONFIGURACIÓN DE LA VENTANA
        # =====================================================

        self.title("Gestión de Marcas")
        self.geometry("900x600")
        self.minsize(800, 500)

        self.transient(parent)

        self.crear_interfaz()
        self.cargar_marcas()

    # =====================================================
    # CREAR INTERFAZ
    # =====================================================

    def crear_interfaz(self):

        # =====================================================
        # TÍTULO
        # =====================================================

        titulo = ctk.CTkLabel(
            self,
            text="GESTIÓN DE MARCAS",
            font=("Arial", 26, "bold")
        )

        titulo.pack(pady=(20, 10))

        # =====================================================
        # FRAME DE BÚSQUEDA
        # =====================================================

        frame_busqueda = ctk.CTkFrame(self)

        frame_busqueda.pack(
            fill="x",
            padx=20,
            pady=10
        )

        lbl_buscar = ctk.CTkLabel(
            frame_busqueda,
            text="Buscar:",
            font=("Arial", 14)
        )

        lbl_buscar.pack(
            side="left",
            padx=(15, 5),
            pady=15
        )

        self.entry_buscar = ctk.CTkEntry(
            frame_busqueda,
            placeholder_text="Ingrese el nombre de la marca",
            width=300,
            height=35
        )

        self.entry_buscar.pack(
            side="left",
            padx=5,
            pady=15
        )

        self.entry_buscar.bind(
            "<KeyRelease>",
            self.buscar_marcas
        )

        btn_buscar = ctk.CTkButton(
            frame_busqueda,
            text="Buscar",
            width=100,
            command=self.buscar_marcas
        )

        btn_buscar.pack(
            side="left",
            padx=5
        )

        btn_limpiar = ctk.CTkButton(
            frame_busqueda,
            text="Limpiar",
            width=100,
            fg_color="gray",
            hover_color="#555555",
            command=self.limpiar_busqueda
        )

        btn_limpiar.pack(
            side="left",
            padx=5
        )

        # =====================================================
        # FRAME DE BOTONES
        # =====================================================

        frame_botones = ctk.CTkFrame(self)

        frame_botones.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        # -----------------------------------------------------
        # NUEVA MARCA
        # -----------------------------------------------------

        btn_nueva = ctk.CTkButton(
            frame_botones,
            text="+ Nueva Marca",
            width=140,
            height=40,
            font=("Arial", 14, "bold"),
            command=self.nueva_marca
        )

        btn_nueva.pack(
            side="left",
            padx=10,
            pady=10
        )

        # -----------------------------------------------------
        # EDITAR
        # -----------------------------------------------------

        btn_editar = ctk.CTkButton(
            frame_botones,
            text="Editar",
            width=120,
            height=40,
            command=self.editar_marca
        )

        btn_editar.pack(
            side="left",
            padx=5,
            pady=10
        )

        # -----------------------------------------------------
        # CAMBIAR ESTADO
        # -----------------------------------------------------

        btn_estado = ctk.CTkButton(
            frame_botones,
            text="Cambiar Estado",
            width=140,
            height=40,
            command=self.cambiar_estado
        )

        btn_estado.pack(
            side="left",
            padx=5,
            pady=10
        )

        # -----------------------------------------------------
        # EXPORTAR A EXCEL
        # -----------------------------------------------------

        btn_exportar = ctk.CTkButton(
            frame_botones,
            text="Exportar a Excel",
            width=150,
            height=40,
            fg_color="#217346",
            hover_color="#185C37",
            command=self.exportar_a_excel
        )

        btn_exportar.pack(
            side="left",
            padx=5,
            pady=10
        )

        # -----------------------------------------------------
        # ACTUALIZAR
        # -----------------------------------------------------

        btn_actualizar = ctk.CTkButton(
            frame_botones,
            text="Actualizar",
            width=120,
            height=40,
            command=self.cargar_marcas
        )

        btn_actualizar.pack(
            side="right",
            padx=10,
            pady=10
        )

        # =====================================================
        # TABLA
        # =====================================================

        frame_tabla = ctk.CTkFrame(self)

        frame_tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        columnas = (
            "id_marca",
            "nombre",
            "activo",
            "fecha_creacion"
        )

        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        # -----------------------------------------------------
        # ENCABEZADOS
        # -----------------------------------------------------

        self.tabla.heading(
            "id_marca",
            text="ID"
        )

        self.tabla.heading(
            "nombre",
            text="Marca"
        )

        self.tabla.heading(
            "activo",
            text="Estado"
        )

        self.tabla.heading(
            "fecha_creacion",
            text="Fecha de creación"
        )

        # -----------------------------------------------------
        # ANCHOS
        # -----------------------------------------------------

        self.tabla.column(
            "id_marca",
            width=70,
            anchor="center"
        )

        self.tabla.column(
            "nombre",
            width=300,
            anchor="w"
        )

        self.tabla.column(
            "activo",
            width=120,
            anchor="center"
        )

        self.tabla.column(
            "fecha_creacion",
            width=180,
            anchor="center"
        )

        # -----------------------------------------------------
        # SCROLLBAR
        # -----------------------------------------------------

        scrollbar = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(
            yscrollcommand=scrollbar.set
        )

        self.tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # -----------------------------------------------------
        # DOBLE CLIC PARA EDITAR
        # -----------------------------------------------------

        self.tabla.bind(
            "<Double-1>",
            lambda event: self.editar_marca()
        )

    # =====================================================
    # CARGAR MARCAS
    # =====================================================

    def cargar_marcas(self):

        try:

            marcas = MarcaModel.listar_marcas()

            self.mostrar_marcas(marcas)

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar las marcas.\n\n{e}",
                parent=self
            )

    # =====================================================
    # MOSTRAR MARCAS
    # =====================================================

    def mostrar_marcas(self, marcas):

        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Insertar registros
        for marca in marcas:

            estado = (
                "Activa"
                if marca.get("activo") == 1
                else "Inactiva"
            )

            fecha = marca.get("fecha_creacion")

            if fecha:
                fecha = str(fecha)

            self.tabla.insert(
                "",
                "end",
                values=(
                    marca.get("id_marca"),
                    marca.get("nombre"),
                    estado,
                    fecha
                )
            )

    # =====================================================
    # BUSCAR MARCAS
    # =====================================================

    def buscar_marcas(self, event=None):

        texto = self.entry_buscar.get().strip()

        try:

            if texto:

                marcas = MarcaModel.buscar_marcas(texto)

            else:

                marcas = MarcaModel.listar_marcas()

            self.mostrar_marcas(marcas)

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudieron buscar las marcas.\n\n{e}",
                parent=self
            )

    # =====================================================
    # LIMPIAR BÚSQUEDA
    # =====================================================

    def limpiar_busqueda(self):

        self.entry_buscar.delete(
            0,
            "end"
        )

        self.cargar_marcas()

    # =====================================================
    # OBTENER MARCA SELECCIONADA
    # =====================================================

    def obtener_seleccionada(self):

        seleccion = self.tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Selección requerida",
                "Seleccione una marca de la tabla.",
                parent=self
            )

            return None

        item = self.tabla.item(
            seleccion[0]
        )

        valores = item.get("values")

        if not valores:
            return None

        return {
            "id_marca": valores[0],
            "nombre": valores[1],
            "activo": 1 if valores[2] == "Activa" else 0,
            "fecha_creacion": valores[3]
        }

    # =====================================================
    # NUEVA MARCA
    # =====================================================

    def nueva_marca(self):

        FormularioMarca(
            self,
            marca=None,
            callback=self.cargar_marcas
        )

    # =====================================================
    # EDITAR MARCA
    # =====================================================

    def editar_marca(self):

        marca = self.obtener_seleccionada()

        if not marca:
            return

        FormularioMarca(
            self,
            marca=marca,
            callback=self.cargar_marcas
        )

    # =====================================================
    # CAMBIAR ESTADO
    # =====================================================

    def cambiar_estado(self):

        marca = self.obtener_seleccionada()

        if not marca:
            return

        id_marca = marca["id_marca"]
        nombre = marca["nombre"]
        activo = marca["activo"]

        # -------------------------------------------------
        # DESACTIVAR
        # -------------------------------------------------

        if activo == 1:

            confirmar = messagebox.askyesno(
                "Desactivar marca",
                f"¿Está seguro de desactivar la marca\n\n"
                f"'{nombre}'?",
                parent=self
            )

            if not confirmar:
                return

            resultado = MarcaModel.desactivar_marca(
                id_marca
            )

            if resultado:

                messagebox.showinfo(
                    "Marca desactivada",
                    f"La marca '{nombre}' fue desactivada correctamente.",
                    parent=self
                )

                self.cargar_marcas()

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudo desactivar la marca.",
                    parent=self
                )

        # -------------------------------------------------
        # ACTIVAR
        # -------------------------------------------------

        else:

            confirmar = messagebox.askyesno(
                "Activar marca",
                f"¿Está seguro de activar nuevamente la marca\n\n"
                f"'{nombre}'?",
                parent=self
            )

            if not confirmar:
                return

            resultado = MarcaModel.activar_marca(
                id_marca
            )

            if resultado:

                messagebox.showinfo(
                    "Marca activada",
                    f"La marca '{nombre}' fue activada correctamente.",
                    parent=self
                )

                self.cargar_marcas()

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudo activar la marca.",
                    parent=self
                )

    # =====================================================
    # EXPORTAR A EXCEL
    # =====================================================

    def exportar_a_excel(self):

        try:

            # =================================================
            # OBTENER TODOS LOS REGISTROS DIRECTAMENTE
            # DESDE LA BASE DE DATOS
            # =================================================

            marcas = MarcaModel.listar_marcas()

            if not marcas:

                messagebox.showwarning(
                    "Sin datos",
                    "No existen marcas para exportar.",
                    parent=self
                )

                return

            # =================================================
            # SELECCIONAR UBICACIÓN DEL ARCHIVO
            # =================================================

            archivo = filedialog.asksaveasfilename(
                parent=self,
                title="Guardar marcas en Excel",
                defaultextension=".xlsx",
                filetypes=[
                    ("Archivos de Excel", "*.xlsx"),
                    ("Todos los archivos", "*.*")
                ],
                initialfile="marcas.xlsx"
            )

            if not archivo:
                return

            # =================================================
            # CREAR LIBRO DE EXCEL
            # =================================================

            wb = Workbook()

            ws = wb.active
            ws.title = "Marcas"

            # =================================================
            # ENCABEZADOS
            # =================================================

            encabezados = [
                "ID",
                "Marca",
                "Estado",
                "Fecha de creación"
            ]

            ws.append(encabezados)

            # =================================================
            # AGREGAR DATOS
            # =================================================

            for marca in marcas:

                estado = (
                    "Activa"
                    if marca.get("activo") == 1
                    else "Inactiva"
                )

                fecha = marca.get("fecha_creacion")

                if fecha:
                    fecha = str(fecha)

                ws.append([
                    marca.get("id_marca"),
                    marca.get("nombre"),
                    estado,
                    fecha
                ])

            # =================================================
            # AJUSTAR ANCHO DE COLUMNAS
            # =================================================

            ws.column_dimensions["A"].width = 12
            ws.column_dimensions["B"].width = 35
            ws.column_dimensions["C"].width = 18
            ws.column_dimensions["D"].width = 25

            # =================================================
            # NEGRITA EN ENCABEZADOS
            # =================================================

            for celda in ws[1]:
                celda.font = celda.font.copy(bold=True)

            # =================================================
            # GUARDAR ARCHIVO
            # =================================================

            wb.save(archivo)

            # =================================================
            # MENSAJE DE CONFIRMACIÓN
            # =================================================

            messagebox.showinfo(
                "Exportación completada",
                f"Las marcas fueron exportadas correctamente.\n\n"
                f"Registros exportados: {len(marcas)}\n\n"
                f"Archivo:\n{archivo}",
                parent=self
            )

        except Exception as e:

            messagebox.showerror(
                "Error al exportar",
                f"No se pudieron exportar las marcas a Excel.\n\n"
                f"{e}",
                parent=self
            )