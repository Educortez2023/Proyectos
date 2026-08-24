import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from openpyxl import Workbook

from app.models.departamento_model import DepartamentoModel


class VentanaDepartamentos(ctk.CTkToplevel):

    def __init__(self, master=None):

        super().__init__(master)

        # =====================================================
        # CONFIGURACIÓN
        # =====================================================

        self.title("Gestión de Departamentos")

        self.geometry("1000x650")

        self.minsize(
            900,
            600
        )

        self.transient(master)

        self.model = DepartamentoModel()

        # =====================================================
        # CREAR INTERFAZ
        # =====================================================

        self.crear_interfaz()

        # =====================================================
        # CARGAR DATOS
        # =====================================================

        self.cargar_departamentos()

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
            text="Gestión de Departamentos",
            font=("Arial", 24, "bold")
        )

        titulo.pack(
            pady=(20, 10)
        )

        # =================================================
        # FRAME SUPERIOR
        # =================================================

        frame_superior = ctk.CTkFrame(
            self
        )

        frame_superior.pack(
            fill="x",
            padx=25,
            pady=10
        )

        # =================================================
        # BUSCAR
        # =================================================

        self.entry_buscar = ctk.CTkEntry(
            frame_superior,
            width=350,
            placeholder_text="Buscar departamento..."
        )

        self.entry_buscar.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.entry_buscar.bind(
            "<KeyRelease>",
            self.buscar_departamentos
        )

        # =================================================
        # BOTÓN BUSCAR
        # =================================================

        btn_buscar = ctk.CTkButton(
            frame_superior,
            text="🔎 Buscar",
            width=120,
            command=self.buscar_departamentos
        )

        btn_buscar.pack(
            side="left",
            padx=5
        )

        # =================================================
        # BOTÓN NUEVO
        # =================================================

        btn_nuevo = ctk.CTkButton(
            frame_superior,
            text="➕ Nuevo",
            width=130,
            command=self.nuevo_departamento
        )

        btn_nuevo.pack(
            side="right",
            padx=5
        )

        # =================================================
        # TABLA
        # =================================================

        frame_tabla = ctk.CTkFrame(
            self
        )

        frame_tabla.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        columnas = (
            "id",
            "nombre",
            "descripcion",
            "estado",
            "fecha"
        )

        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings"
        )

        # =================================================
        # ENCABEZADOS
        # =================================================

        self.tabla.heading(
            "id",
            text="ID"
        )

        self.tabla.heading(
            "nombre",
            text="Departamento"
        )

        self.tabla.heading(
            "descripcion",
            text="Descripción"
        )

        self.tabla.heading(
            "estado",
            text="Estado"
        )

        self.tabla.heading(
            "fecha",
            text="Fecha creación"
        )

        # =================================================
        # ANCHOS
        # =================================================

        self.tabla.column(
            "id",
            width=70,
            anchor="center"
        )

        self.tabla.column(
            "nombre",
            width=220
        )

        self.tabla.column(
            "descripcion",
            width=330
        )

        self.tabla.column(
            "estado",
            width=100,
            anchor="center"
        )

        self.tabla.column(
            "fecha",
            width=150,
            anchor="center"
        )

        # =================================================
        # SCROLLBAR
        # =================================================

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

        # =================================================
        # DOBLE CLICK
        # =================================================

        self.tabla.bind(
            "<Double-1>",
            self.editar_departamento
        )

        # =================================================
        # BOTONES INFERIORES
        # =================================================

        frame_botones = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        frame_botones.pack(
            fill="x",
            padx=25,
            pady=(5, 20)
        )

        # =================================================
        # EDITAR
        # =================================================

        btn_editar = ctk.CTkButton(
            frame_botones,
            text="✏️ Editar",
            width=140,
            command=self.editar_departamento
        )

        btn_editar.pack(
            side="left",
            padx=5
        )

        # =================================================
        # CAMBIAR ESTADO
        # =================================================

        btn_estado = ctk.CTkButton(
            frame_botones,
            text="🔄 Activar / Desactivar",
            width=180,
            command=self.cambiar_estado
        )

        btn_estado.pack(
            side="left",
            padx=5
        )

        # =================================================
        # ELIMINAR
        # =================================================

        btn_eliminar = ctk.CTkButton(
            frame_botones,
            text="🗑️ Eliminar",
            width=140,
            command=self.eliminar_departamento
        )

        btn_eliminar.pack(
            side="left",
            padx=5
        )

        # =================================================
        # EXPORTAR
        # =================================================

        btn_exportar = ctk.CTkButton(
            frame_botones,
            text="📊 Exportar Excel",
            width=160,
            command=self.exportar_excel
        )

        btn_exportar.pack(
            side="right",
            padx=5
        )

    # =====================================================
    # CARGAR DEPARTAMENTOS
    # =====================================================

    def cargar_departamentos(self):

        try:

            registros = self.model.listar()

            self.mostrar_registros(
                registros
            )

        except Exception as e:

            print(
                "Error al cargar departamentos:",
                e
            )

            messagebox.showerror(
                "Error",
                (
                    "No se pudieron cargar "
                    "los departamentos.\n\n"
                    f"{e}"
                ),
                parent=self
            )

    # =====================================================
    # MOSTRAR REGISTROS
    # =====================================================

    def mostrar_registros(self, registros):

        # =================================================
        # LIMPIAR TABLA
        # =================================================

        for item in self.tabla.get_children():

            self.tabla.delete(item)

        # =================================================
        # INSERTAR REGISTROS
        # =================================================

        for departamento in registros:

            id_departamento = departamento[0]
            nombre = departamento[1]
            descripcion = departamento[2]

            activo = departamento[3]

            fecha = departamento[4]

            # =================================================
            # ESTADO
            # =================================================

            if activo == 1:

                estado = "ACTIVO"

            else:

                estado = "INACTIVO"

            # =================================================
            # FECHA
            # =================================================

            if fecha is not None:

                fecha_texto = str(fecha)

            else:

                fecha_texto = ""

            # =================================================
            # INSERTAR
            # =================================================

            self.tabla.insert(
                "",
                "end",
                values=(
                    id_departamento,
                    nombre,
                    descripcion or "",
                    estado,
                    fecha_texto
                )
            )

    # =====================================================
    # BUSCAR
    # =====================================================

    def buscar_departamentos(self, event=None):

        try:

            texto = (
                self.entry_buscar
                .get()
                .strip()
            )

            if texto:

                registros = self.model.buscar(
                    texto
                )

            else:

                registros = self.model.listar()

            self.mostrar_registros(
                registros
            )

        except Exception as e:

            print(
                "Error al buscar departamentos:",
                e
            )

            messagebox.showerror(
                "Error",
                (
                    "No se pudo realizar "
                    "la búsqueda.\n\n"
                    f"{e}"
                ),
                parent=self
            )

    # =====================================================
    # OBTENER SELECCIÓN
    # =====================================================

    def obtener_seleccion(self):

        seleccion = (
            self.tabla.selection()
        )

        if not seleccion:

            messagebox.showwarning(
                "Advertencia",
                "Seleccione un departamento.",
                parent=self
            )

            return None

        valores = (
            self.tabla.item(
                seleccion[0],
                "values"
            )
        )

        return valores

    # =====================================================
    # NUEVO DEPARTAMENTO
    # =====================================================

    def nuevo_departamento(self):

        ventana = ctk.CTkToplevel(
            self
        )

        ventana.title(
            "Nuevo Departamento"
        )

        ventana.geometry(
            "550x400"
        )

        ventana.minsize(
            500,
            350
        )

        ventana.transient(
            self
        )

        # =================================================
        # TÍTULO
        # =================================================

        ctk.CTkLabel(
            ventana,
            text="Nuevo Departamento",
            font=("Arial", 22, "bold")
        ).pack(
            pady=(25, 20)
        )

        # =================================================
        # NOMBRE
        # =================================================

        ctk.CTkLabel(
            ventana,
            text="Nombre:"
        ).pack(
            anchor="w",
            padx=40,
            pady=(5, 5)
        )

        entry_nombre = ctk.CTkEntry(
            ventana,
            width=470,
            placeholder_text="Ingrese el nombre"
        )

        entry_nombre.pack(
            padx=40,
            pady=(0, 15)
        )

        # =================================================
        # DESCRIPCIÓN
        # =================================================

        ctk.CTkLabel(
            ventana,
            text="Descripción:"
        ).pack(
            anchor="w",
            padx=40,
            pady=(5, 5)
        )

        entry_descripcion = ctk.CTkTextbox(
            ventana,
            width=470,
            height=100
        )

        entry_descripcion.pack(
            padx=40,
            pady=(0, 20)
        )

        # =================================================
        # GUARDAR
        # =================================================

        def guardar():

            try:

                nombre = (
                    entry_nombre
                    .get()
                    .strip()
                )

                descripcion = (
                    entry_descripcion
                    .get(
                        "1.0",
                        "end"
                    )
                    .strip()
                )

                if not nombre:

                    messagebox.showwarning(
                        "Advertencia",
                        "Ingrese el nombre del departamento.",
                        parent=ventana
                    )

                    entry_nombre.focus()

                    return

                confirmar = messagebox.askyesno(
                    "Confirmar",
                    "¿Desea guardar este departamento?",
                    parent=ventana
                )

                if not confirmar:

                    return

                self.model.crear(
                    nombre,
                    descripcion
                )

                messagebox.showinfo(
                    "Éxito",
                    "Departamento registrado correctamente.",
                    parent=ventana
                )

                ventana.destroy()

                self.cargar_departamentos()

            except Exception as e:

                print(
                    "Error al crear departamento:",
                    e
                )

                messagebox.showerror(
                    "Error",
                    (
                        "No se pudo registrar "
                        "el departamento.\n\n"
                        f"{e}"
                    ),
                    parent=ventana
                )

        # =================================================
        # BOTONES
        # =================================================

        frame_botones = ctk.CTkFrame(
            ventana,
            fg_color="transparent"
        )

        frame_botones.pack(
            fill="x",
            padx=40,
            pady=5
        )

        ctk.CTkButton(
            frame_botones,
            text="💾 Guardar",
            width=180,
            command=guardar
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            frame_botones,
            text="❌ Cancelar",
            width=150,
            command=ventana.destroy
        ).pack(
            side="right",
            padx=5
        )

        ventana.after(
            100,
            lambda: (
                ventana.lift(),
                ventana.focus_force()
            )
        )

    # =====================================================
    # EDITAR DEPARTAMENTO
    # =====================================================

    def editar_departamento(self, event=None):

        valores = self.obtener_seleccion()

        if valores is None:

            return

        id_departamento = valores[0]

        departamento = self.model.obtener(
            id_departamento
        )

        if departamento is None:

            messagebox.showerror(
                "Error",
                "No se encontró el departamento.",
                parent=self
            )

            return

        ventana = ctk.CTkToplevel(
            self
        )

        ventana.title(
            "Editar Departamento"
        )

        ventana.geometry(
            "550x400"
        )

        ventana.minsize(
            500,
            350
        )

        ventana.transient(
            self
        )

        # =================================================
        # TÍTULO
        # =================================================

        ctk.CTkLabel(
            ventana,
            text="Editar Departamento",
            font=("Arial", 22, "bold")
        ).pack(
            pady=(25, 20)
        )

        # =================================================
        # NOMBRE
        # =================================================

        ctk.CTkLabel(
            ventana,
            text="Nombre:"
        ).pack(
            anchor="w",
            padx=40,
            pady=(5, 5)
        )

        entry_nombre = ctk.CTkEntry(
            ventana,
            width=470
        )

        entry_nombre.pack(
            padx=40,
            pady=(0, 15)
        )

        entry_nombre.insert(
            0,
            departamento[1]
        )

        # =================================================
        # DESCRIPCIÓN
        # =================================================

        ctk.CTkLabel(
            ventana,
            text="Descripción:"
        ).pack(
            anchor="w",
            padx=40,
            pady=(5, 5)
        )

        entry_descripcion = ctk.CTkTextbox(
            ventana,
            width=470,
            height=100
        )

        entry_descripcion.pack(
            padx=40,
            pady=(0, 20)
        )

        if departamento[2]:

            entry_descripcion.insert(
                "1.0",
                departamento[2]
            )

        # =================================================
        # ACTUALIZAR
        # =================================================

        def actualizar():

            try:

                nombre = (
                    entry_nombre
                    .get()
                    .strip()
                )

                descripcion = (
                    entry_descripcion
                    .get(
                        "1.0",
                        "end"
                    )
                    .strip()
                )

                if not nombre:

                    messagebox.showwarning(
                        "Advertencia",
                        "Ingrese el nombre del departamento.",
                        parent=ventana
                    )

                    entry_nombre.focus()

                    return

                confirmar = messagebox.askyesno(
                    "Confirmar",
                    "¿Desea actualizar este departamento?",
                    parent=ventana
                )

                if not confirmar:

                    return

                self.model.actualizar(
                    id_departamento,
                    nombre,
                    descripcion
                )

                messagebox.showinfo(
                    "Éxito",
                    "Departamento actualizado correctamente.",
                    parent=ventana
                )

                ventana.destroy()

                self.cargar_departamentos()

            except Exception as e:

                print(
                    "Error al actualizar departamento:",
                    e
                )

                messagebox.showerror(
                    "Error",
                    (
                        "No se pudo actualizar "
                        "el departamento.\n\n"
                        f"{e}"
                    ),
                    parent=ventana
                )

        # =================================================
        # BOTONES
        # =================================================

        frame_botones = ctk.CTkFrame(
            ventana,
            fg_color="transparent"
        )

        frame_botones.pack(
            fill="x",
            padx=40,
            pady=5
        )

        ctk.CTkButton(
            frame_botones,
            text="💾 Actualizar",
            width=180,
            command=actualizar
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            frame_botones,
            text="❌ Cancelar",
            width=150,
            command=ventana.destroy
        ).pack(
            side="right",
            padx=5
        )

        ventana.after(
            100,
            lambda: (
                ventana.lift(),
                ventana.focus_force()
            )
        )

    # =====================================================
    # CAMBIAR ESTADO
    # =====================================================

    def cambiar_estado(self):

        valores = self.obtener_seleccion()

        if valores is None:

            return

        id_departamento = int(
            valores[0]
        )

        estado_actual = valores[3]

        if estado_actual == "ACTIVO":

            nuevo_estado = 0
            texto = "desactivar"

        else:

            nuevo_estado = 1
            texto = "activar"

        confirmar = messagebox.askyesno(
            "Confirmar",
            (
                f"¿Desea {texto} "
                "este departamento?"
            ),
            parent=self
        )

        if not confirmar:

            return

        try:

            self.model.cambiar_estado(
                id_departamento,
                nuevo_estado
            )

            messagebox.showinfo(
                "Éxito",
                "Estado actualizado correctamente.",
                parent=self
            )

            self.cargar_departamentos()

        except Exception as e:

            print(
                "Error al cambiar estado:",
                e
            )

            messagebox.showerror(
                "Error",
                (
                    "No se pudo cambiar "
                    "el estado.\n\n"
                    f"{e}"
                ),
                parent=self
            )

    # =====================================================
    # ELIMINAR
    # =====================================================

    def eliminar_departamento(self):

        valores = self.obtener_seleccion()

        if valores is None:

            return

        id_departamento = int(
            valores[0]
        )

        nombre = valores[1]

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            (
                "¿Está seguro de eliminar "
                f"el departamento '{nombre}'?\n\n"
                "Esta acción no se puede deshacer."
            ),
            parent=self
        )

        if not confirmar:

            return

        try:

            self.model.eliminar(
                id_departamento
            )

            messagebox.showinfo(
                "Éxito",
                "Departamento eliminado correctamente.",
                parent=self
            )

            self.cargar_departamentos()

        except Exception as e:

            print(
                "Error al eliminar departamento:",
                e
            )

            messagebox.showerror(
                "Error",
                (
                    "No se pudo eliminar "
                    "el departamento.\n\n"
                    f"{e}"
                ),
                parent=self
            )

    # =====================================================
    # EXPORTAR A EXCEL
    # =====================================================

    def exportar_excel(self):

        try:

            registros = self.model.listar()

            if not registros:

                messagebox.showwarning(
                    "Advertencia",
                    "No existen departamentos para exportar.",
                    parent=self
                )

                return

            archivo = filedialog.asksaveasfilename(
                parent=self,
                title="Guardar archivo Excel",
                defaultextension=".xlsx",
                filetypes=[
                    (
                        "Archivos Excel",
                        "*.xlsx"
                    )
                ]
            )

            if not archivo:

                return

            wb = Workbook()

            ws = wb.active

            ws.title = "Departamentos"

            # =================================================
            # ENCABEZADOS
            # =================================================

            encabezados = [
                "ID",
                "Departamento",
                "Descripción",
                "Estado",
                "Fecha creación"
            ]

            ws.append(
                encabezados
            )

            # =================================================
            # DATOS
            # =================================================

            for departamento in registros:

                activo = departamento[3]

                estado = (
                    "ACTIVO"
                    if activo == 1
                    else "INACTIVO"
                )

                ws.append(
                    [
                        departamento[0],
                        departamento[1],
                        departamento[2] or "",
                        estado,
                        str(
                            departamento[4]
                        )
                        if departamento[4]
                        else ""
                    ]
                )

            # =================================================
            # AJUSTAR COLUMNAS
            # =================================================

            anchos = {
                "A": 10,
                "B": 30,
                "C": 45,
                "D": 15,
                "E": 25
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

            messagebox.showinfo(
                "Éxito",
                (
                    "Los departamentos fueron "
                    "exportados correctamente."
                ),
                parent=self
            )

        except Exception as e:

            print(
                "Error al exportar departamentos:",
                e
            )

            messagebox.showerror(
                "Error",
                (
                    "No se pudo exportar "
                    "el archivo Excel.\n\n"
                    f"{e}"
                ),
                parent=self
            )