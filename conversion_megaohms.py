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
        return conversiones.get(medicion, "N/A")  # Devuelve "N/A" si la medición no está en el diccionario
    except Exception as e:
        print(f"Error al convertir a Megaohms: {e}")
        return "N/A"