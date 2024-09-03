from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
import datetime
import os
import shutil
import subprocess
import matplotlib.pyplot as plt
import numpy as np
from settings.__init__ import ruta_base_pdf_esd
from conversion_megaohms import convertir_a_megaohms
from actividades_todo.proceso1_db_actividades import guardar_db_actividad1_terminada
from actividades_todo.proceso1_db_actividades import confirmacion_proceso1_db




def pdf_proceso1(registros, proceso_1, ventana_procedimiento_actividad):
    try:
        registros_con_megohms = []  # Lista para almacenar los registros con la conversión a Megaohms

        # Obtener la fecha y hora actual
        now = datetime.datetime.now()
        fecha_hora = now.strftime("%d-%m-%Y_%H-%M-%S")
        año_actual = now.strftime("%Y")

        # Crear la carpeta del año actual si no existe
        ruta_pdf_esd = os.path.join(ruta_base_pdf_esd, año_actual)
        if not os.path.exists(ruta_pdf_esd):
            os.makedirs(ruta_pdf_esd)

        # Crear el archivo PDF en la ruta especificada con fecha y hora en el nombre
        pdf_filename = f"Reporte_ESD_BEA_{fecha_hora}.pdf"
        pdf_filepath = os.path.join(ruta_pdf_esd, pdf_filename)
        document = SimpleDocTemplate(pdf_filepath, pagesize=letter)

        # Estilos
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        title_style.alignment = TA_CENTER
        subtitle_style = styles['Heading2']
        subtitle_style.alignment = TA_CENTER
        body_style = styles['BodyText']
        body_style.spaceAfter = 12

        # Título del PDF
        title = Paragraph(f"Reporte de Medición ESD {año_actual}", title_style)
        elements = [title, Spacer(1, 20)]

        for item in registros:
            try:
                # Agregar subtítulo para cada registro
                subtitle = Paragraph(f"Usuario: {item['Usuario']} - Elemento ESD: {item['Elemento ESD']}", subtitle_style)
                elements.append(KeepTogether([subtitle, Spacer(1, 12)]))

                # Convertir la medición a Megaohms
                megaohms = convertir_a_megaohms(item['Medición'])

                # Agregar el valor convertido al diccionario del registro
                item_con_megohms = item.copy()  # Hacer una copia del registro original
                item_con_megohms['Megaohms'] = megaohms  # Añadir la conversión a Megaohms
                registros_con_megohms.append(item_con_megohms)  # Añadir el registro modificado a la nueva lista

                # Crear tabla de datos para cada registro
                data = [
                    ['Campo', 'Valor'],
                    ['ID Usuario', item['usuario_id']],
                    ['ID Elemento ESD', item['esd_item_id']],
                    ['Número de Serie', item['N. Serie']],
                    ['Área', item['Área']],
                    ['Línea', item['Línea']],
                    ['Medición ESD', item['Medición']],
                    ['Magnitud en Megaohms', f"{megaohms} MΩ"],  # Nueva fila con la magnitud en Megaohms
                    ['Comentarios', item['Comentarios']],
                    ['Color LED', item['Color LED']]
                ]

                # Estilo de la tabla
                table_style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#D9EAD3")),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('TOPPADDING', (0, 1), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ])

                table = Table(data)
                table.setStyle(table_style)

                # Agrupar subtítulo y tabla para mantenerlos juntos
                elements.append(KeepTogether([table, Spacer(1, 20)]))

            except Exception as e:
                print(f"Error al procesar el registro {item}: {e}")


        # Generar el PDF con todos los registros
        document.build(elements)

        # Crear una copia temporal del archivo PDF en el directorio temporal de Windows
        temp_dir = os.getenv('TEMP')
        temp_pdf_filepath = os.path.join(temp_dir, f"Temp_{pdf_filename}")
        shutil.copy(pdf_filepath, temp_pdf_filepath)

        # Usa esto para abrir el archivo PDF directamente:
        subprocess.Popen([temp_pdf_filepath], shell=True)

        # Guardar los registros en la base de datos solo una vez al final del proceso
        guardar_db_actividad1_terminada(registros)

        print(f"PDF generado con éxito: {pdf_filepath}")
        generar_grafico(registros, ruta_pdf_esd, pdf_filename)

        print('..............................................')
        if confirmacion_proceso1_db():
            print('Se escribio correctamente los datos en la db')
            proceso_1.withdraw()
            ventana_procedimiento_actividad.deiconify()
        else:
            print('Error critico al escribir los datos en la db')
        print('..............................................')

    except Exception as e:
        print(f"Error al generar el PDF: {e}")



def generar_grafico(registros, ruta_pdf_esd, pdf_filename):
    try:
        # Filtrar los registros con mediciones que no pasaron la prueba
        registros_no_pasan = [r for r in registros if r['Medición'] in ["10E12", "10E13"]]

        if not registros_no_pasan:
            print("No hay registros que no pasen la prueba.")
            return

        # Preparar los datos para la gráfica
        nombres = [f"Nombre: {r['Usuario']} - Área: {r['Área']} - Línea: {r['Línea']} - Elemento ESD: {r['Elemento ESD']}" for r in registros_no_pasan]
        mediciones = [convertir_a_megaohms(r['Medición']) for r in registros_no_pasan]

        # Normalizar los datos
        mediciones_normalizadas = np.array(mediciones) / max(mediciones)

        # Crear la gráfica
        plt.figure(figsize=(12, 8))
        bars = plt.barh(nombres, mediciones_normalizadas, color='red')
        plt.axvline(1, color='gray', linestyle='--', linewidth=0.7)  # Línea de referencia en 1
        plt.title('Mediciones ESD que no pasaron la prueba')
        plt.xlabel('Mediciones Normalizadas (MΩ)')
        plt.ylabel('Usuarios')
        plt.tight_layout()

        # Añadir etiquetas en las barras
        for bar, value in zip(bars, mediciones_normalizadas):
            plt.text(value, bar.get_y() + bar.get_height() / 2,
                     f'{value:.2f}', ha='left', va='center')

        # Guardar la gráfica como PDF
        grafico_filename = f"Grafico_ESD_BEA_{pdf_filename.split('.')[0]}.pdf"
        grafico_filepath = os.path.join(ruta_pdf_esd, grafico_filename)
        plt.savefig(grafico_filepath)

        # Crear una copia temporal del gráfico en el directorio temporal de Windows
        temp_dir = os.getenv('TEMP')
        temp_grafico_filepath = os.path.join(temp_dir, f"Temp_{grafico_filename}")
        shutil.copy(grafico_filepath, temp_grafico_filepath)

        # Abrir el gráfico directamente
        subprocess.Popen([temp_grafico_filepath], shell=True)

        print(f"Gráfico generado con éxito: {grafico_filepath}")

    except Exception as e:
        print(f"Error al generar el gráfico: {e}")

