def convertir_a_megaohms(medicion):
    try:
        conversiones = {
            "10E3": 0.001,
            "10E4": 0.01,
            "10E5": 0.1,
            "10E6": 1,
            "10E7": 10,
            "10E8": 100,
            "10E9": 1000,
            "10E10": 10000,
            "10E11": 100000,
            "10E12": 1000000,
            "10E13": 10000000,
        }
        # Intentar la conversión normal
        resultado = conversiones.get(medicion, "N/A")

        if resultado == "N/A":
            # Si no se encuentra la medición, intentar con la conversión inversa
            return convertir_desde_megaohms(medicion)

        return resultado
    except Exception as e:
        print(f"Error al convertir a Megaohms: {e}")
        return "N/A"


def convertir_desde_megaohms(medicion):
    try:
        # Diccionario inverso para realizar la conversión
        conversiones_inversas = {
            0.001: "10E3",
            0.01: "10E4",
            0.1: "10E5",
            1: "10E6",
            10: "10E7",
            100: "10E8",
            1000: "10E9",
            10000: "10E10",
            100000: "10E11",
            1000000: "10E12",
            10000000: "10E13",
        }

        # Intentar convertir desde la medición dada
        return conversiones_inversas.get(float(medicion), "N/A")  # Convertir medición a float si es posible
    except Exception as e:
        print(f"Error al convertir desde Megaohms: {e}")
        return "N/A"
