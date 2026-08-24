import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from openpyxl import Workbook

from app.models.proveedor_model import ProveedorModel
from app.views.formulario_proveedor import FormularioProveedor


class VentanaProveedores(ctk.CTkToplevel):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.parent = parent

        # =====================================================
        # CONFIGURACIÓN DE LA VENTANA
        # =====================================================

        self.title("Gestión de Proveedores")
        self.geometry("1200x650")
        self.minsize(1000, 600)

        self.transient(parent)

        self.crear_interfaz()
        self.cargar_proveedores()

    # =====================================================
    # CREAR INTERFAZ
    # =====================================================

    def crear_interfaz(self):

        # =====================================================
        # TÍTULO
        # =====================================================

        titulo = ctk.CTkLabel(
            self,
            text="GESTIÓN DE PROVEEDORES",
            font=("Arial", 26, "bold")
        )

        titulo.pack(
            pady=(20, 10)
        )

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
            placeholder_text="Empresa, contacto, teléfono o correo",
            width=350,
            height=35
        )

        self.entry_buscar.pack(
            side="left",
            padx=5,
            pady=15
        )

        self.entry_buscar.bind(
            "<KeyRelease>",
            self.buscar_proveedores
        )

        btn_buscar = ctk.CTkButton(
            frame_busqueda,
            text="Buscar",
            width=100,
            command=self.buscar_proveedores
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

        # =====================================================
        # NUEVO
        # =====================================================

        btn_nuevo = ctk.CTkButton(
            frame_botones,
            text="+ Nuevo Proveedor",
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            command=self.nuevo_proveedor
        )

        btn_nuevo.pack(
            side="left",
            padx=10,
            pady=10
        )

        # =====================================================
        # EDITAR
        # =====================================================

        btn_editar = ctk.CTkButton(
            frame_botones,
            text="Editar",
            width=120,
            height=40,
            command=self.editar_proveedor
        )

        btn_editar.pack(
            side="left",
            padx=5,
            pady=10
        )

        # =====================================================
        # CAMBIAR ESTADO
        # =====================================================

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

        # =====================================================
        # EXPORTAR A EXCEL
        # =====================================================

        btn_exportar = ctk.CTkButton(
            frame_botones,
            text="Exportar a Excel",
            width=150,
            height=40,
            command=self.exportar_a_excel
        )

        btn_exportar.pack(
            side="left",
            padx=5,
            pady=10
        )

        # =====================================================
        # ACTUALIZAR
        # =====================================================

        btn_actualizar = ctk.CTkButton(
            frame_botones,
            text="Actualizar",
            width=120,
            height=40,
            command=self.cargar_proveedores
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
            "id_proveedor",
            "empresa",
            "contacto",
            "telefono",
            "correo",
            "direccion",
            "activo",
            "fecha_creacion"
        )

        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        # =====================================================
        # ENCABEZADOS
        # =====================================================

        self.tabla.heading(
            "id_proveedor",
            text="ID"
        )

        self.tabla.heading(
            "empresa",
            text="Empresa"
        )

        self.tabla.heading(
            "contacto",
            text="Contacto"
        )

        self.tabla.heading(
            "telefono",
            text="Teléfono"
        )

        self.tabla.heading(
            "correo",
            text="Correo"
        )

        self.tabla.heading(
            "direccion",
            text="Dirección"
        )

        self.tabla.heading(
            "activo",
            text="Estado"
        )

        self.tabla.heading(
            "fecha_creacion",
            text="Fecha de creación"
        )

        # =====================================================
        # ANCHOS
        # =====================================================

        self.tabla.column(
            "id_proveedor",
            width=60,
            anchor="center"
        )

        self.tabla.column(
            "empresa",
            width=180,
            anchor="w"
        )

        self.tabla.column(
            "contacto",
            width=150,
            anchor="w"
        )

        self.tabla.column(
            "telefono",
            width=110,
            anchor="center"
        )

        self.tabla.column(
            "correo",
            width=180,
            anchor="w"
        )

        self.tabla.column(
            "direccion",
            width=220,
            anchor="w"
        )

        self.tabla.column(
            "activo",
            width=100,
            anchor="center"
        )

        self.tabla.column(
            "fecha_creacion",
            width=160,
            anchor="center"
        )

        # =====================================================
        # SCROLLBAR VERTICAL
        # =====================================================

        scrollbar_vertical = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(
            yscrollcommand=scrollbar_vertical.set
        )

        self.tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar_vertical.pack(
            side="right",
            fill="y"
        )

        # =====================================================
        # DOBLE CLIC PARA EDITAR
        # =====================================================

        self.tabla.bind(
            "<Double-1>",
            lambda event: self.editar_proveedor()
        )

    # =====================================================
    # CARGAR PROVEEDORES
    # =====================================================

    def cargar_proveedores(self):

        try:

            proveedores = ProveedorModel.listar_proveedores()

            self.mostrar_proveedores(proveedores)

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los proveedores.\n\n{e}",
                parent=self
            )

    # =====================================================
    # MOSTRAR PROVEEDORES
    # =====================================================

    def mostrar_proveedores(self, proveedores):

        # Limpiar tabla

        for item in self.tabla.get_children():

            self.tabla.delete(item)

        # Insertar registros

        for proveedor in proveedores:

            estado = (
                "Activo"
                if proveedor.get("activo") == 1
                else "Inactivo"
            )

            fecha = proveedor.get(
                "fecha_creacion"
            )

            if fecha:

                fecha = str(fecha)

            self.tabla.insert(
                "",
                "end",
                values=(
                    proveedor.get("id_proveedor"),
                    proveedor.get("empresa"),
                    proveedor.get("contacto") or "",
                    proveedor.get("telefono") or "",
                    proveedor.get("correo") or "",
                    proveedor.get("direccion") or "",
                    estado,
                    fecha or ""
                )
            )

    # =====================================================
    # BUSCAR PROVEEDORES
    # =====================================================

    def buscar_proveedores(self, event=None):

        texto = self.entry_buscar.get().strip()

        if texto:

            proveedores = (
                ProveedorModel.buscar_proveedores(
                    texto
                )
            )

        else:

            proveedores = (
                ProveedorModel.listar_proveedores()
            )

        self.mostrar_proveedores(
            proveedores
        )

    # =====================================================
    # LIMPIAR BÚSQUEDA
    # =====================================================

    def limpiar_busqueda(self):

        self.entry_buscar.delete(
            0,
            "end"
        )

        self.cargar_proveedores()

    # =====================================================
    # OBTENER PROVEEDOR SELECCIONADO
    # =====================================================

    def obtener_seleccionado(self):

        seleccion = self.tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Selección requerida",
                "Seleccione un proveedor de la tabla.",
                parent=self
            )

            return None

        item = self.tabla.item(
            seleccion[0]
        )

        valores = item.get(
            "values"
        )

        if not valores:

            return None

        return {
            "id_proveedor": valores[0],
            "empresa": valores[1],
            "contacto": valores[2],
            "telefono": valores[3],
            "correo": valores[4],
            "direccion": valores[5],
            "activo": (
                1
                if valores[6] == "Activo"
                else 0
            ),
            "fecha_creacion": valores[7]
        }

    # =====================================================
    # NUEVO PROVEEDOR
    # =====================================================

    def nuevo_proveedor(self):

        FormularioProveedor(
            self,
            proveedor=None,
            callback=self.cargar_proveedores
        )

    # =====================================================
    # EDITAR PROVEEDOR
    # =====================================================

    def editar_proveedor(self):

        proveedor = self.obtener_seleccionado()

        if not proveedor:

            return

        FormularioProveedor(
            self,
            proveedor=proveedor,
            callback=self.cargar_proveedores
        )

    # =====================================================
    # CAMBIAR ESTADO
    # =====================================================

    def cambiar_estado(self):

        proveedor = self.obtener_seleccionado()

        if not proveedor:

            return

        id_proveedor = proveedor[
            "id_proveedor"
        ]

        empresa = proveedor[
            "empresa"
        ]

        activo = proveedor[
            "activo"
        ]

        # =================================================
        # DESACTIVAR
        # =================================================

        if activo == 1:

            confirmar = messagebox.askyesno(
                "Desactivar proveedor",
                (
                    "¿Está seguro de desactivar el proveedor?\n\n"
                    f"'{empresa}'?"
                ),
                parent=self
            )

            if not confirmar:

                return

            resultado = (
                ProveedorModel.desactivar_proveedor(
                    id_proveedor
                )
            )

            if resultado:

                messagebox.showinfo(
                    "Proveedor desactivado",
                    (
                        f"El proveedor '{empresa}' "
                        "fue desactivado correctamente."
                    ),
                    parent=self
                )

                self.cargar_proveedores()

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudo desactivar el proveedor.",
                    parent=self
                )

        # =================================================
        # ACTIVAR
        # =================================================

        else:

            confirmar = messagebox.askyesno(
                "Activar proveedor",
                (
                    "¿Está seguro de activar nuevamente "
                    "el proveedor?\n\n"
                    f"'{empresa}'?"
                ),
                parent=self
            )

            if not confirmar:

                return

            resultado = (
                ProveedorModel.activar_proveedor(
                    id_proveedor
                )
            )

            if resultado:

                messagebox.showinfo(
                    "Proveedor activado",
                    (
                        f"El proveedor '{empresa}' "
                        "fue activado correctamente."
                    ),
                    parent=self
                )

                self.cargar_proveedores()

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudo activar el proveedor.",
                    parent=self
                )

    # =====================================================
    # EXPORTAR A EXCEL
    # =====================================================

    def exportar_a_excel(self):

        try:

            # =================================================
            # OBTENER DATOS DIRECTAMENTE DE LA BASE
            # =================================================

            proveedores = (
                ProveedorModel.listar_proveedores()
            )

            if not proveedores:

                messagebox.showwarning(
                    "Sin datos",
                    "No existen proveedores para exportar.",
                    parent=self
                )

                return

            # =================================================
            # SELECCIONAR UBICACIÓN
            # =================================================

            archivo = filedialog.asksaveasfilename(
                parent=self,
                title="Guardar archivo Excel",
                defaultextension=".xlsx",
                filetypes=[
                    (
                        "Archivos Excel",
                        "*.xlsx"
                    )
                ],
                initialfile="proveedores.xlsx"
            )

            if not archivo:

                return

            # =================================================
            # CREAR LIBRO
            # =================================================

            wb = Workbook()

            ws = wb.active

            ws.title = "Proveedores"

            # =================================================
            # ENCABEZADOS
            # =================================================

            encabezados = [
                "ID",
                "Empresa",
                "Contacto",
                "Teléfono",
                "Correo",
                "Dirección",
                "Estado",
                "Fecha de creación"
            ]

            ws.append(
                encabezados
            )

            # =================================================
            # DATOS
            # =================================================

            for proveedor in proveedores:

                estado = (
                    "Activo"
                    if proveedor.get("activo") == 1
                    else "Inactivo"
                )

                fecha = proveedor.get(
                    "fecha_creacion"
                )

                if fecha:

                    fecha = str(fecha)

                ws.append(
                    [
                        proveedor.get(
                            "id_proveedor"
                        ),
                        proveedor.get(
                            "empresa"
                        ),
                        proveedor.get(
                            "contacto"
                        ) or "",
                        proveedor.get(
                            "telefono"
                        ) or "",
                        proveedor.get(
                            "correo"
                        ) or "",
                        proveedor.get(
                            "direccion"
                        ) or "",
                        estado,
                        fecha or ""
                    ]
                )

            # =================================================
            # AJUSTAR ANCHO DE COLUMNAS
            # =================================================

            anchos = {
                "A": 10,
                "B": 25,
                "C": 25,
                "D": 18,
                "E": 30,
                "F": 35,
                "G": 15,
                "H": 22
            }

            for columna, ancho in anchos.items():

                ws.column_dimensions[
                    columna
                ].width = ancho

            # =================================================
            # GUARDAR ARCHIVO
            # =================================================

            wb.save(
                archivo
            )

            messagebox.showinfo(
                "Exportación completada",
                (
                    "Los proveedores fueron "
                    "exportados correctamente a Excel.\n\n"
                    f"Archivo:\n{archivo}"
                ),
                parent=self
            )

        except Exception as e:

            messagebox.showerror(
                "Error al exportar",
                (
                    "No se pudo exportar la información "
                    "a Excel.\n\n"
                    f"{e}"
                ),
                parent=self
            )