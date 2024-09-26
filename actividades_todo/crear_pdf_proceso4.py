import datetime
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors  # Importar colors para poder usar colores en las tablas
from conversion_megaohms import convertir_a_megaohms
from settings.__init__ import proceso_4_pdf
from common.__init__ import *
import time
# Zona horaria de Guadalajara, Jalisco, México
import pytz
tz = pytz.timezone('America/Mexico_City')

def pdf_proceso4(registros):
    try:
        print(f'Registros llegados en pdf4: {registros}, registros')
        time.sleep(1)
        # Lista para almacenar los registros con la conversión a Megaohms
        registros_con_megohms = []

        # Obtener la fecha y hora actual en la zona horaria correcta
        ahora = datetime.now(tz)  # Corrección aquí: quitar 'datetime.datetime'
        fecha_hora = ahora.strftime('%Y-%m-%d_%H-%M-%S')
        año_actual = ahora.strftime('%Y')

        # Crear la carpeta del año actual si no existe (ruta almacenada en: proceso_2_pdf)
        ruta_pdf_esd = os.path.join(proceso_4_pdf, año_actual)
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

        # Contador para controlar las tablas por página
        contador_tablas = 0

        # Procesar cada registro
        for item in registros:
            try:
                # Convertir la medición a Megaohms
                megaohms = convertir_a_megaohms(item['medicion'])

                # Agregar el valor convertido al diccionario del registro
                item_con_megohms = item.copy()  # Hacer una copia del registro original
                item_con_megohms['megaohms'] = megaohms  # Añadir la conversión a Megaohms
                registros_con_megohms.append(item_con_megohms)  # Añadir el registro modificado a la nueva lista

                # Crear tabla de datos para cada registro
                data = [
                    ['Número de Serie', item['numero_registro']],
                    ['Elemento ESD', item['elemento_esd']],
                    ['Medición (Ω)', item['medicion']],
                    ['Medición (MegaΩ)', megaohms],
                    ['Color LED', item['color_led']],
                    ['Usuario Windows', item['usuario_windows']],
                    ['Comentarios', item['comentarios'] if item['comentarios'] else 'N/A'],
                    ['Fecha de Registro', item['fecha_registro']],
                ]

                # Crear la tabla con los datos
                table = Table(data)
                table_style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ])
                table.setStyle(table_style)

                # Añadir la tabla al PDF
                elements.append(table)
                elements.append(Spacer(1, 12))

                # Incrementar el contador de tablas
                contador_tablas += 1

                # Insertar salto de página cada 3 tablas
                if contador_tablas % 3 == 0:
                    elements.append(PageBreak())

            except Exception as e:
                # Mostrar el error en la consola pero continuar con el proceso
                print(f"Error al procesar el registro {item}: {e}")

        # Generar el PDF con todos los registros
        document.build(elements)

        # Crear una copia temporal del archivo PDF en el directorio temporal de Windows
        temp_dir = os.getenv('TEMP')
        temp_pdf_filepath = os.path.join(temp_dir, f"Temp_{pdf_filename}")
        shutil.copy(pdf_filepath, temp_pdf_filepath)

        # Abrir el archivo PDF directamente
        subprocess.Popen([temp_pdf_filepath], shell=True)

        print(f"PDF generado con éxito: {pdf_filepath}")

        # Llamar a la función para generar el gráfico
        pdf_filename = f"Grafico_ESD_BEA_{fecha_hora}.pdf"
        generar_grafico(registros_con_megohms, ruta_pdf_esd, pdf_filename)

    except Exception as e:
        print(f"Error al generar el PDF: {e}")


from fpdf import FPDF

import shutil  # Importar shutil para copiar archivos

def generar_grafico(registros, ruta_pdf_esd, pdf_filename):
    try:
        print(registros)
        time.sleep(1)
        # Filtrar los registros con color_led 'red'
        registros_red = [r for r in registros if r['color_led'] == 'red']

        if not registros_red:
            print("No hay registros con color LED rojo.")
            return

        # Crear el PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Título del reporte
        pdf.add_page()
        pdf.set_font("Arial", 'B', size=16)  # Negrita y tamaño grande
        pdf.cell(0, 10, txt=f"Reporte de Medición ESD {datetime.now().year}", ln=True, align='C')  # Centrado
        pdf.cell(0, 10, txt="", ln=True)  # Espacio adicional

        for idx, registro in enumerate(registros_red):
            # Convertir el valor de megaohms a un número real
            megaohms = float(registro['megaohms'].replace('E', 'e'))

            # Normalizar la medición
            medicion_normalizada = megaohms / max([float(r['megaohms'].replace('E', 'e')) for r in registros_red])

            # Crear la gráfica
            plt.figure(figsize=(4, 3))  # Tamaño más grande para mejor visualización
            plt.bar([registro['elemento_esd']], [medicion_normalizada], color='red')
            plt.xlabel('Elemento ESD', fontsize=12)  # Tamaño de fuente mayor
            plt.ylabel('Medición Normalizada', fontsize=12)  # Tamaño de fuente mayor
            plt.title(f'Registro {registro["numero_registro"]}', fontsize=14)  # Tamaño de fuente mayor
            plt.xticks(rotation=45, ha='right', fontsize=10)  # Mayor legibilidad

            # Guardar la gráfica como imagen temporal
            grafico_filename = f"MiniGrafico_{idx + 1}.png"
            plt.tight_layout()  # Ajusta el diseño para evitar superposición
            plt.savefig(grafico_filename, format='png')
            plt.close()

            # Añadir una nueva página al PDF
            pdf.add_page()

            # Añadir información del registro con mejor formato
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, txt=f"Registro: {registro['numero_registro']}", ln=True)
            pdf.cell(0, 10, txt=f"Elemento ESD: {registro['elemento_esd']}", ln=True)
            pdf.cell(0, 10, txt=f"Medición: {registro['medicion']}", ln=True)
            pdf.cell(0, 10, txt=f"Fecha: {registro['fecha_registro']}", ln=True)
            pdf.cell(0, 10, txt=f"Usuario: {registro['usuario_windows']}", ln=True)
            pdf.cell(0, 10, txt=f"Comentarios: {registro['comentarios']}", ln=True)
            pdf.cell(0, 10, txt="", ln=True)  # Espacio adicional

            # Añadir la gráfica al PDF
            pdf.image(grafico_filename, x=10, y=pdf.get_y(), w=100)  # Aumentar el ancho de la imagen

            # Eliminar la imagen temporal
            os.remove(grafico_filename)

        # Guardar el PDF
        grafico_filepath = os.path.join(ruta_pdf_esd, pdf_filename)
        pdf.output(grafico_filepath)

        # Crear una copia temporal del archivo PDF en el directorio temporal de Windows
        temp_dir = os.getenv('TEMP')
        temp_grafico_filepath = os.path.join(temp_dir, f"Temp_{pdf_filename}")
        shutil.copy(grafico_filepath, temp_grafico_filepath)

        # Abrir el archivo PDF temporalmente
        subprocess.Popen([temp_grafico_filepath], shell=True)

        print(f"PDF generado con éxito: {grafico_filepath}")

    except Exception as e:
        print(f"Error al generar el gráfico: {e}")
