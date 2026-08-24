import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from openpyxl import Workbook

from app.models.modelo_model import ModeloModel
from app.views.formulario_modelo import FormularioModelo


class VentanaModelos(ctk.CTkToplevel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent

        # =====================================================
        # CONFIGURACIÓN DE LA VENTANA
        # =====================================================

        self.title("Gestión de Modelos")
        self.geometry("1000x600")
        self.minsize(900, 500)

        self.transient(parent)

        self.crear_interfaz()
        self.cargar_modelos()

    # =====================================================
    # CREAR INTERFAZ
    # =====================================================

    def crear_interfaz(self):

        # =====================================================
        # TÍTULO
        # =====================================================

        titulo = ctk.CTkLabel(
            self,
            text="GESTIÓN DE MODELOS",
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
            placeholder_text="Modelo o marca",
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
            self.buscar_modelos
        )

        btn_buscar = ctk.CTkButton(
            frame_busqueda,
            text="Buscar",
            width=100,
            command=self.buscar_modelos
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
        # NUEVO MODELO
        # -----------------------------------------------------

        btn_nuevo = ctk.CTkButton(
            frame_botones,
            text="+ Nuevo Modelo",
            width=140,
            height=40,
            font=("Arial", 14, "bold"),
            command=self.nuevo_modelo
        )

        btn_nuevo.pack(
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
            command=self.editar_modelo
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
            command=self.cargar_modelos
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
            "id_modelo",
            "nombre",
            "marca",
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
            "id_modelo",
            text="ID"
        )

        self.tabla.heading(
            "nombre",
            text="Modelo"
        )

        self.tabla.heading(
            "marca",
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
            "id_modelo",
            width=70,
            anchor="center"
        )

        self.tabla.column(
            "nombre",
            width=250,
            anchor="w"
        )

        self.tabla.column(
            "marca",
            width=220,
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
            lambda event: self.editar_modelo()
        )

    # =====================================================
    # CARGAR MODELOS
    # =====================================================

    def cargar_modelos(self):

        try:

            modelos = ModeloModel.listar_modelos()

            self.mostrar_modelos(modelos)

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los modelos.\n\n{e}",
                parent=self
            )

    # =====================================================
    # MOSTRAR MODELOS
    # =====================================================

    def mostrar_modelos(self, modelos):

        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Insertar registros
        for modelo in modelos:

            estado = (
                "Activo"
                if modelo.get("activo") == 1
                else "Inactivo"
            )

            fecha = modelo.get("fecha_creacion")

            if fecha:
                fecha = str(fecha)

            self.tabla.insert(
                "",
                "end",
                values=(
                    modelo.get("id_modelo"),
                    modelo.get("nombre"),
                    modelo.get("marca"),
                    estado,
                    fecha
                )
            )

    # =====================================================
    # BUSCAR MODELOS
    # =====================================================

    def buscar_modelos(self, event=None):

        texto = self.entry_buscar.get().strip()

        try:

            if texto:

                modelos = ModeloModel.buscar_modelos(texto)

            else:

                modelos = ModeloModel.listar_modelos()

            self.mostrar_modelos(modelos)

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudieron buscar los modelos.\n\n{e}",
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

        self.cargar_modelos()

    # =====================================================
    # OBTENER MODELO SELECCIONADO
    # =====================================================

    def obtener_seleccionado(self):

        seleccion = self.tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Selección requerida",
                "Seleccione un modelo de la tabla.",
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
            "id_modelo": valores[0],
            "nombre": valores[1],
            "marca": valores[2],
            "activo": 1 if valores[3] == "Activo" else 0,
            "fecha_creacion": valores[4]
        }

    # =====================================================
    # NUEVO MODELO
    # =====================================================

    def nuevo_modelo(self):

        FormularioModelo(
            self,
            modelo=None,
            callback=self.cargar_modelos
        )

    # =====================================================
    # EDITAR MODELO
    # =====================================================

    def editar_modelo(self):

        modelo = self.obtener_seleccionado()

        if not modelo:
            return

        FormularioModelo(
            self,
            modelo=modelo,
            callback=self.cargar_modelos
        )

    # =====================================================
    # CAMBIAR ESTADO
    # =====================================================

    def cambiar_estado(self):

        modelo = self.obtener_seleccionado()

        if not modelo:
            return

        id_modelo = modelo["id_modelo"]
        nombre = modelo["nombre"]
        activo = modelo["activo"]

        # -------------------------------------------------
        # DESACTIVAR
        # -------------------------------------------------

        if activo == 1:

            confirmar = messagebox.askyesno(
                "Desactivar modelo",
                f"¿Está seguro de desactivar el modelo\n\n"
                f"'{nombre}'?",
                parent=self
            )

            if not confirmar:
                return

            resultado = ModeloModel.desactivar_modelo(
                id_modelo
            )

            if resultado:

                messagebox.showinfo(
                    "Modelo desactivado",
                    f"El modelo '{nombre}' fue desactivado correctamente.",
                    parent=self
                )

                self.cargar_modelos()

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudo desactivar el modelo.",
                    parent=self
                )

        # -------------------------------------------------
        # ACTIVAR
        # -------------------------------------------------

        else:

            confirmar = messagebox.askyesno(
                "Activar modelo",
                f"¿Está seguro de activar nuevamente el modelo\n\n"
                f"'{nombre}'?",
                parent=self
            )

            if not confirmar:
                return

            resultado = ModeloModel.activar_modelo(
                id_modelo
            )

            if resultado:

                messagebox.showinfo(
                    "Modelo activado",
                    f"El modelo '{nombre}' fue activado correctamente.",
                    parent=self
                )

                self.cargar_modelos()

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudo activar el modelo.",
                    parent=self
                )

    # =====================================================
    # EXPORTAR A EXCEL
    # =====================================================

    def exportar_a_excel(self):

        try:

            # Obtener todos los modelos directamente
            # desde la base de datos
            modelos = ModeloModel.listar_modelos()

            if not modelos:

                messagebox.showwarning(
                    "Sin datos",
                    "No existen modelos para exportar.",
                    parent=self
                )

                return

            # =================================================
            # SELECCIONAR UBICACIÓN
            # =================================================

            archivo = filedialog.asksaveasfilename(
                parent=self,
                title="Guardar modelos en Excel",
                defaultextension=".xlsx",
                filetypes=[
                    ("Archivos de Excel", "*.xlsx"),
                    ("Todos los archivos", "*.*")
                ],
                initialfile="modelos.xlsx"
            )

            if not archivo:
                return

            # =================================================
            # CREAR LIBRO
            # =================================================

            wb = Workbook()

            ws = wb.active
            ws.title = "Modelos"

            # =================================================
            # ENCABEZADOS
            # =================================================

            encabezados = [
                "ID",
                "Modelo",
                "Marca",
                "Estado",
                "Fecha de creación"
            ]

            ws.append(encabezados)

            # =================================================
            # DATOS
            # =================================================

            for modelo in modelos:

                estado = (
                    "Activo"
                    if modelo.get("activo") == 1
                    else "Inactivo"
                )

                fecha = modelo.get("fecha_creacion")

                if fecha:
                    fecha = str(fecha)

                ws.append([
                    modelo.get("id_modelo"),
                    modelo.get("nombre"),
                    modelo.get("marca"),
                    estado,
                    fecha
                ])

            # =================================================
            # ANCHO DE COLUMNAS
            # =================================================

            ws.column_dimensions["A"].width = 12
            ws.column_dimensions["B"].width = 35
            ws.column_dimensions["C"].width = 30
            ws.column_dimensions["D"].width = 18
            ws.column_dimensions["E"].width = 25

            # =================================================
            # ENCABEZADOS EN NEGRITA
            # =================================================

            for celda in ws[1]:
                celda.font = celda.font.copy(bold=True)

            # =================================================
            # GUARDAR
            # =================================================

            wb.save(archivo)

            # =================================================
            # CONFIRMACIÓN
            # =================================================

            messagebox.showinfo(
                "Exportación completada",
                f"Los modelos fueron exportados correctamente.\n\n"
                f"Registros exportados: {len(modelos)}\n\n"
                f"Archivo:\n{archivo}",
                parent=self
            )

        except Exception as e:

            messagebox.showerror(
                "Error al exportar",
                f"No se pudieron exportar los modelos a Excel.\n\n"
                f"{e}",
                parent=self
            )