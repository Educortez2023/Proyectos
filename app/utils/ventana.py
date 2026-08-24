import customtkinter as ctk


# ============================================================
# CONFIGURACIÓN GENERAL DE VENTANAS
# ============================================================

class ConfigVentana:
    """
    Configuración centralizada para todas las ventanas
    del sistema de inventario.
    """

    @staticmethod
    def preparar(ventana, ancho=1100, alto=650, maximizada=True):
        """
        Configura una ventana antes de mostrarla.

        Parámetros:
            ventana   -> instancia de CTk o CTkToplevel
            ancho     -> ancho mínimo/base
            alto      -> alto mínimo/base
            maximizada -> True para abrir maximizada
        """

        try:
            # ------------------------------------------------
            # Evitar que la ventana se muestre mientras
            # se está configurando.
            # ------------------------------------------------
            ventana.withdraw()

            # ------------------------------------------------
            # Tamaño mínimo
            # ------------------------------------------------
            ventana.minsize(
                ancho,
                alto
            )

            # ------------------------------------------------
            # Intentar maximizar directamente
            # ------------------------------------------------
            if maximizada:

                try:
                    ventana.state("zoomed")

                except Exception:

                    try:
                        ancho_pantalla = ventana.winfo_screenwidth()
                        alto_pantalla = ventana.winfo_screenheight()

                        ventana.geometry(
                            f"{ancho_pantalla}x{alto_pantalla}+0+0"
                        )

                    except Exception:
                        ventana.geometry(
                            f"{ancho}x{alto}"
                        )

            else:

                # ------------------------------------------------
                # Si no se quiere maximizar, centrar ventana
                # ------------------------------------------------
                ConfigVentana.centrar(
                    ventana,
                    ancho,
                    alto
                )

            # ------------------------------------------------
            # Mostrar la ventana solamente después de haber
            # terminado toda la configuración.
            # ------------------------------------------------
            ventana.update_idletasks()

            ventana.deiconify()

            # ------------------------------------------------
            # Llevar al frente
            # ------------------------------------------------
            ventana.lift()

            ventana.focus_force()

        except Exception as e:

            print(
                "Error al preparar ventana:",
                e
            )

            try:
                ventana.deiconify()
            except Exception:
                pass


    # ========================================================
    # CENTRAR VENTANA
    # ========================================================

    @staticmethod
    def centrar(ventana, ancho, alto):

        try:

            ancho_pantalla = ventana.winfo_screenwidth()
            alto_pantalla = ventana.winfo_screenheight()

            posicion_x = (
                ancho_pantalla - ancho
            ) // 2

            posicion_y = (
                alto_pantalla - alto
            ) // 2

            ventana.geometry(
                f"{ancho}x{alto}+{posicion_x}+{posicion_y}"
            )

        except Exception as e:

            print(
                "Error al centrar ventana:",
                e
            )


# ============================================================
# FUNCIÓN GENERAL
# ============================================================

def configurar_ventana(
    ventana,
    ancho=1100,
    alto=650,
    maximizada=True
):
    """
    Función rápida para configurar cualquier ventana.

    Ejemplo:

        configurar_ventana(self)

    """

    ConfigVentana.preparar(
        ventana,
        ancho,
        alto,
        maximizada
    )
