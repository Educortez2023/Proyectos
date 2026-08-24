import customtkinter as ctk


def configurar_ventana(
    ventana,
    maximizar=True,
    margen=0
):
    """
    Configura una ventana CTk o CTkToplevel para que
    aparezca ajustada a la pantalla sin mostrar
    el cambio de tamaño al usuario.

    Parámetros:
        ventana:
            La ventana que se desea configurar.

        maximizar:
            True = ocupa toda la pantalla.
            False = utiliza el tamaño definido previamente.

        margen:
            Margen opcional alrededor de la pantalla.
    """

    try:

        # =================================================
        # OCULTAR LA VENTANA
        # =================================================

        ventana.withdraw()

        # =================================================
        # ACTUALIZAR INFORMACIÓN DE PANTALLA
        # =================================================

        ventana.update_idletasks()

        # =================================================
        # OBTENER RESOLUCIÓN
        # =================================================

        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()

        # =================================================
        # MAXIMIZAR
        # =================================================

        if maximizar:

            try:

                # -----------------------------------------
                # MÉTODO PRINCIPAL EN WINDOWS
                # -----------------------------------------

                ventana.state("zoomed")

            except Exception:

                try:

                    # -------------------------------------
                    # MÉTODO ALTERNATIVO
                    # -------------------------------------

                    ancho = ancho_pantalla - (
                        margen * 2
                    )

                    alto = alto_pantalla - (
                        margen * 2
                    )

                    ventana.geometry(
                        f"{ancho}x{alto}+{margen}+{margen}"
                    )

                except Exception as error:

                    print(
                        "Error al ajustar ventana:",
                        error
                    )

        else:

            # =================================================
            # SI NO SE DESEA MAXIMIZAR
            # =================================================

            try:

                ancho_actual = ventana.winfo_width()
                alto_actual = ventana.winfo_height()

                if ancho_actual <= 1:
                    ancho_actual = 950

                if alto_actual <= 1:
                    alto_actual = 600

                # -----------------------------------------
                # CENTRAR VENTANA
                # -----------------------------------------

                x = (
                    ancho_pantalla - ancho_actual
                ) // 2

                y = (
                    alto_pantalla - alto_actual
                ) // 2

                ventana.geometry(
                    f"{ancho_actual}x{alto_actual}+{x}+{y}"
                )

            except Exception as error:

                print(
                    "Error al centrar ventana:",
                    error
                )

        # =================================================
        # ACTUALIZAR ANTES DE MOSTRAR
        # =================================================

        ventana.update_idletasks()

        # =================================================
        # MOSTRAR VENTANA
        # =================================================

        ventana.deiconify()

        # =================================================
        # LLEVAR AL FRENTE
        # =================================================

        ventana.lift()

        ventana.focus_force()

    except Exception as error:

        print(
            "Error general al configurar ventana:",
            error
        )

        # =================================================
        # ASEGURAR QUE LA VENTANA SEA VISIBLE
        # =================================================

        try:

            ventana.deiconify()

        except Exception:

            pass