import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from openpyxl import Workbook

from app.models.usuario_model import UsuarioModel
from app.views.formulario_usuario import FormularioUsuario


class VentanaUsuarios(ctk.CTkToplevel):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.parent = parent

        # =====================================================
        # CONFIGURACIÓN
        # =====================================================

        self.title("Gestión de Usuarios")
        self.geometry("1150x650")
        self.minsize(1000, 600)

        self.transient(parent)

        self.crear_interfaz()

        self.cargar_usuarios()

    # =====================================================
    # CREAR INTERFAZ
    # =====================================================

    def crear_interfaz(self):

        # =====================================================
        # TÍTULO
        # =====================================================

        titulo = ctk.CTkLabel(
            self,
            text="GESTIÓN DE USUARIOS",
            font=("Arial", 26, "bold")
        )

        titulo.pack(
            pady=(20, 10)
        )

        # =====================================================
        # FRAME DE BÚSQUEDA
        # =====================================================

        frame_busqueda = ctk.CTkFrame(
            self
        )

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
            placeholder_text="Nombre, usuario, correo o rol",
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
            self.buscar_usuarios
        )

        btn_buscar = ctk.CTkButton(
            frame_busqueda,
            text="Buscar",
            width=100,
            command=self.buscar_usuarios
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

        frame_botones = ctk.CTkFrame(
            self
        )

        frame_botones.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        # =====================================================
        # NUEVO USUARIO
        # =====================================================

        btn_nuevo = ctk.CTkButton(
            frame_botones,
            text="+ Nuevo Usuario",
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            command=self.nuevo_usuario
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
            command=self.editar_usuario
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
        # EXPORTAR EXCEL
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
            command=self.cargar_usuarios
        )

        btn_actualizar.pack(
            side="right",
            padx=10,
            pady=10
        )

        # =====================================================
        # TABLA
        # =====================================================

        frame_tabla = ctk.CTkFrame(
            self
        )

        frame_tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        columnas = (
            "id_usuario",
            "nombres",
            "apellidos",
            "usuario",
            "correo",
            "rol",
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
            "id_usuario",
            text="ID"
        )

        self.tabla.heading(
            "nombres",
            text="Nombres"
        )

        self.tabla.heading(
            "apellidos",
            text="Apellidos"
        )

        self.tabla.heading(
            "usuario",
            text="Usuario"
        )

        self.tabla.heading(
            "correo",
            text="Correo"
        )

        self.tabla.heading(
            "rol",
            text="Rol"
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
            "id_usuario",
            width=60,
            anchor="center"
        )

        self.tabla.column(
            "nombres",
            width=140,
            anchor="w"
        )

        self.tabla.column(
            "apellidos",
            width=140,
            anchor="w"
        )

        self.tabla.column(
            "usuario",
            width=120,
            anchor="w"
        )

        self.tabla.column(
            "correo",
            width=180,
            anchor="w"
        )

        self.tabla.column(
            "rol",
            width=120,
            anchor="center"
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

        # =====================================================
        # SCROLLBAR HORIZONTAL
        # =====================================================

        scrollbar_horizontal = ttk.Scrollbar(
            frame_tabla,
            orient="horizontal",
            command=self.tabla.xview
        )

        self.tabla.configure(
            xscrollcommand=scrollbar_horizontal.set
        )

        # =====================================================
        # POSICIONAR TABLA
        # =====================================================

        self.tabla.pack(
            side="top",
            fill="both",
            expand=True
        )

        scrollbar_horizontal.pack(
            side="bottom",
            fill="x"
        )

        scrollbar_vertical.pack(
            side="right",
            fill="y"
        )

        # =====================================================
        # DOBLE CLIC
        # =====================================================

        self.tabla.bind(
            "<Double-1>",
            lambda event: self.editar_usuario()
        )

    # =====================================================
    # CARGAR USUARIOS
    # =====================================================

    def cargar_usuarios(self):

        try:

            usuarios = (
                UsuarioModel.listar_usuarios()
            )

            self.mostrar_usuarios(
                usuarios
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                (
                    "No se pudieron cargar "
                    f"los usuarios.\n\n{e}"
                ),
                parent=self
            )

    # =====================================================
    # MOSTRAR USUARIOS
    # =====================================================

    def mostrar_usuarios(
        self,
        usuarios
    ):

        # -------------------------------------------------
        # LIMPIAR TABLA
        # -------------------------------------------------

        for item in self.tabla.get_children():

            self.tabla.delete(
                item
            )

        # -------------------------------------------------
        # INSERTAR REGISTROS
        # -------------------------------------------------

        for usuario in usuarios:

            estado = (
                "Activo"
                if usuario.get("activo") == 1
                else "Inactivo"
            )

            fecha = usuario.get(
                "fecha_creacion"
            )

            if fecha:

                fecha = str(
                    fecha
                )

            self.tabla.insert(
                "",
                "end",
                values=(
                    usuario.get(
                        "id_usuario"
                    ),
                    usuario.get(
                        "nombres"
                    ),
                    usuario.get(
                        "apellidos"
                    ),
                    usuario.get(
                        "usuario"
                    ),
                    usuario.get(
                        "correo"
                    ) or "",
                    usuario.get(
                        "rol"
                    ),
                    estado,
                    fecha
                )
            )

    # =====================================================
    # BUSCAR USUARIOS
    # =====================================================

    def buscar_usuarios(
        self,
        event=None
    ):

        texto = (
            self.entry_buscar
            .get()
            .strip()
        )

        if texto:

            usuarios = (
                UsuarioModel.buscar_usuarios(
                    texto
                )
            )

        else:

            usuarios = (
                UsuarioModel.listar_usuarios()
            )

        self.mostrar_usuarios(
            usuarios
        )

    # =====================================================
    # LIMPIAR BÚSQUEDA
    # =====================================================

    def limpiar_busqueda(self):

        self.entry_buscar.delete(
            0,
            "end"
        )

        self.cargar_usuarios()

    # =====================================================
    # OBTENER USUARIO SELECCIONADO
    # =====================================================

    def obtener_seleccionado(self):

        seleccion = (
            self.tabla.selection()
        )

        if not seleccion:

            messagebox.showwarning(
                "Selección requerida",
                "Seleccione un usuario de la tabla.",
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
            "id_usuario": valores[0],
            "nombres": valores[1],
            "apellidos": valores[2],
            "usuario": valores[3],
            "correo": valores[4],
            "rol": valores[5],
            "activo": (
                1
                if valores[6] == "Activo"
                else 0
            ),
            "fecha_creacion": valores[7]
        }

    # =====================================================
    # NUEVO USUARIO
    # =====================================================

    def nuevo_usuario(self):

        FormularioUsuario(
            self,
            usuario=None,
            callback=self.cargar_usuarios
        )

    # =====================================================
    # EDITAR USUARIO
    # =====================================================

    def editar_usuario(self):

        usuario = (
            self.obtener_seleccionado()
        )

        if not usuario:

            return

        # -------------------------------------------------
        # Recuperar nuevamente el registro desde BD
        # para obtener id_rol correctamente
        # -------------------------------------------------

        usuarios = (
            UsuarioModel.listar_usuarios()
        )

        usuario_completo = None

        for registro in usuarios:

            if str(
                registro.get("id_usuario")
            ) == str(
                usuario.get("id_usuario")
            ):

                usuario_completo = registro

                break

        if not usuario_completo:

            messagebox.showerror(
                "Error",
                "No se pudo obtener la información completa del usuario.",
                parent=self
            )

            return

        FormularioUsuario(
            self,
            usuario=usuario_completo,
            callback=self.cargar_usuarios
        )

    # =====================================================
    # CAMBIAR ESTADO
    # =====================================================

    def cambiar_estado(self):

        usuario = (
            self.obtener_seleccionado()
        )

        if not usuario:

            return

        id_usuario = (
            usuario["id_usuario"]
        )

        nombre_completo = (
            f"{usuario['nombres']} "
            f"{usuario['apellidos']}"
        )

        activo = usuario[
            "activo"
        ]

        # =================================================
        # DESACTIVAR
        # =================================================

        if activo == 1:

            confirmar = messagebox.askyesno(
                "Desactivar usuario",
                (
                    "¿Está seguro de desactivar "
                    "el usuario?\n\n"
                    f"'{nombre_completo}'"
                ),
                parent=self
            )

            if not confirmar:

                return

            resultado = (
                UsuarioModel.desactivar_usuario(
                    id_usuario
                )
            )

            if resultado:

                messagebox.showinfo(
                    "Usuario desactivado",
                    (
                        f"El usuario '{nombre_completo}' "
                        "fue desactivado correctamente."
                    ),
                    parent=self
                )

                self.cargar_usuarios()

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudo desactivar el usuario.",
                    parent=self
                )

        # =================================================
        # ACTIVAR
        # =================================================

        else:

            confirmar = messagebox.askyesno(
                "Activar usuario",
                (
                    "¿Está seguro de activar "
                    "nuevamente el usuario?\n\n"
                    f"'{nombre_completo}'"
                ),
                parent=self
            )

            if not confirmar:

                return

            resultado = (
                UsuarioModel.activar_usuario(
                    id_usuario
                )
            )

            if resultado:

                messagebox.showinfo(
                    "Usuario activado",
                    (
                        f"El usuario '{nombre_completo}' "
                        "fue activado correctamente."
                    ),
                    parent=self
                )

                self.cargar_usuarios()

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudo activar el usuario.",
                    parent=self
                )

    # =====================================================
    # EXPORTAR A EXCEL
    # =====================================================

    def exportar_a_excel(self):

        try:

            # -------------------------------------------------
            # Obtener TODOS los usuarios directamente
            # desde la base de datos
            # -------------------------------------------------

            usuarios = (
                UsuarioModel.listar_usuarios()
            )

            if not usuarios:

                messagebox.showwarning(
                    "Sin datos",
                    "No existen usuarios para exportar.",
                    parent=self
                )

                return

            # -------------------------------------------------
            # Seleccionar ubicación
            # -------------------------------------------------

            archivo = filedialog.asksaveasfilename(
                parent=self,
                title="Guardar usuarios en Excel",
                defaultextension=".xlsx",
                filetypes=[
                    (
                        "Archivo Excel",
                        "*.xlsx"
                    )
                ],
                initialfile="usuarios.xlsx"
            )

            if not archivo:

                return

            # -------------------------------------------------
            # Crear libro
            # -------------------------------------------------

            wb = Workbook()

            ws = wb.active

            ws.title = "Usuarios"

            # -------------------------------------------------
            # ENCABEZADOS
            # -------------------------------------------------

            encabezados = [
                "ID",
                "Nombres",
                "Apellidos",
                "Usuario",
                "Correo",
                "Rol",
                "Estado",
                "Fecha de creación"
            ]

            ws.append(
                encabezados
            )

            # -------------------------------------------------
            # DATOS
            # -------------------------------------------------

            for usuario in usuarios:

                estado = (
                    "Activo"
                    if usuario.get("activo") == 1
                    else "Inactivo"
                )

                fecha = usuario.get(
                    "fecha_creacion"
                )

                if fecha:

                    fecha = str(
                        fecha
                    )

                ws.append(
                    [
                        usuario.get(
                            "id_usuario"
                        ),
                        usuario.get(
                            "nombres"
                        ),
                        usuario.get(
                            "apellidos"
                        ),
                        usuario.get(
                            "usuario"
                        ),
                        usuario.get(
                            "correo"
                        ) or "",
                        usuario.get(
                            "rol"
                        ),
                        estado,
                        fecha
                    ]
                )

            # -------------------------------------------------
            # AJUSTAR ANCHOS
            # -------------------------------------------------

            anchos = {
                "A": 10,
                "B": 20,
                "C": 20,
                "D": 18,
                "E": 30,
                "F": 18,
                "G": 15,
                "H": 25
            }

            for columna, ancho in anchos.items():

                ws.column_dimensions[
                    columna
                ].width = ancho

            # -------------------------------------------------
            # GUARDAR
            # -------------------------------------------------

            wb.save(
                archivo
            )

            messagebox.showinfo(
                "Exportación completada",
                (
                    "Los usuarios fueron exportados "
                    "correctamente a Excel."
                ),
                parent=self
            )

        except Exception as e:

            messagebox.showerror(
                "Error al exportar",
                (
                    "No se pudo exportar "
                    f"el archivo.\n\n{e}"
                ),
                parent=self
            )