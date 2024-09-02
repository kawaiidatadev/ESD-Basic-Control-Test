from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def pdf_proceso1(usuario_id, esd_item_id, medicion_esd, n_serie, usuario, elemento_esd, area, linea,
                 comentarios, color_led):

    print(f"pdf_proceso1(usuario_id={usuario_id}, esd_item_id={esd_item_id}, medicion_esd={medicion_esd}, "
          f"n_serie={n_serie}, usuario={usuario}, elemento_esd={elemento_esd}, area={area}, "
          f"linea={linea}, comentarios={comentarios}, color_led={color_led})")

    # Crear el archivo PDF
    pdf_filename = f"Reporte_{usuario_id}_{esd_item_id}.pdf"
    document = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title_style.alignment = TA_CENTER
    subtitle_style = styles['Heading2']
    subtitle_style.alignment = TA_CENTER
    body_style = styles['BodyText']
    body_style.spaceAfter = 12

    # Título del PDF
    title = Paragraph("Reporte de Medición ESD", title_style)
    subtitle = Paragraph(f"Usuario: {usuario} - Elemento ESD: {elemento_esd}", subtitle_style)

    # Crear tabla de datos
    data = [
        ['Campo', 'Valor'],
        ['ID Usuario', usuario_id],
        ['ID Elemento ESD', esd_item_id],
        ['Número de Serie', n_serie],
        ['Área', area],
        ['Línea', linea],
        ['Medición ESD', medicion_esd],
        ['Comentarios', comentarios],
        ['Color LED', color_led]
    ]

    # Estilo de la tabla
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    table = Table(data)
    table.setStyle(table_style)

    # Crear una lista de elementos para el documento PDF
    elements = []
    elements.append(title)
    elements.append(Spacer(1, 12))
    elements.append(subtitle)
    elements.append(Spacer(1, 12))
    elements.append(table)

    # Generar el PDF
    document.build(elements)

    print(f"PDF generado con éxito: {pdf_filename}")


# Ejemplo de llamada a la función
pdf_proceso1(
    usuario_id=1,
    esd_item_id=2,
    medicion_esd='10E11',
    n_serie=1018,
    usuario='Andrea Vargas',
    elemento_esd='Bata ESD',
    area='Producción',
    linea='Línea 2',
    comentarios='En buen estado',
    color_led='yellow'
)



