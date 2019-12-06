from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.shapes import Drawing
from datetime import date
from time import time as timestamp


def make_pdf(variables, preset, results, max_val, tab_d):
    now = timestamp()
    file = canvas.Canvas("reports/report-" + str(now) + ".pdf", pagesize=A4)
    preset_names = ['aTl', 'aTna', 'aTa', 'aM', 'aMna', 'aMa', 'yMna',
                    'yMa', 'uM', 'uMf', 'dMna', 'dMnaTl', 'dTlMna', 'dMa',
                    'dMaTl', 'dTlMa', 'dMnaf', 'dMnafTl', 'dMnafT', 'dTlMnaf',
                    'dTMnaf', 'dMaf', 'dMafTl', 'MafT', 'TlMaf', 'TMaf',
                    'dTl', 'dTna', 'dTa']
    B = preset[:len(preset) // 2]
    C = preset[len(preset) // 2:]
    table_data = [['MNA', 'MA', 'MNAF', 'MAF', 'TL', 'TNA', 'TA'], variables]
    t_pres1_data = [['aTl', 'aTna', 'aTa', 'aM', 'aMna', 'aMa', 'yMna',
                     'yMa', 'uM', 'uMf', 'dMna', 'dMnaTl', 'dTlMna', 'dMa'], B]
    t_pres2_data = [['dMaTl', 'dTlMa', 'dMnaf', 'dMnafTl', 'dMnafT', 'dTlMnaf',
                     'dTMnaf', 'dMaf', 'dMafTl', 'MafT', 'TlMaf', 'TMaf',
                     'dTl', 'dTna', 'dTa'], C]
    t_d = [['Mes', 'MNA', 'MA', 'MNAF', 'MAF', 'TL', 'TNA', 'TA']]
    for s in tab_d:
        t_d.append(s)
    today = date.today()
    table_info_data = [['MNA =', 'Macrofago no activado'],
                       ['MA =', 'Macrofago activado'],
                       ['MNAF =', 'Macrofago no activado que fagocito'],
                       ['MAF =', 'Macrofago activado que fagocito'],
                       ['TL =', 'Tuberculosis libre'],
                       ['TNA =', 'Tuberculosis en MNAF'],
                       ['TA =', 'Tuberculosis en MAF']]
    preset_info_data = make_desc_arr(preset_names)
    pres_info_a = preset_info_data[:len(preset_info_data) // 2]
    pres_info_b = preset_info_data[len(preset_info_data) // 2:]

    file.drawString(480, 780, str(today))
    file.setFont('Helvetica', 12)
    file.drawString(80, 460, 'Los parametros iniciales son los siguientes')
    file.drawString(80, 710, 'Las condiciones iniciales de los nodos de la ' +
                             'red fueron:')

    file.setFont('Helvetica', 10)
    file.drawString(80, 620, 'donde')
    file.drawString(80, 310, 'donde')

    file.setFont('Helvetica-Bold', 24)
    file.drawString(80, 750, 'Reporte de RESISTENCE')
    file.setAuthor('Alan Monreal - Daniela Zapata')

    file.setFont('Helvetica', 10)
    t_var = Table(table_data, style=[('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                     ('BACKGROUND', (0, 0), (-1, 0),
                                      colors.grey),
                                     ('INNERGRID', (0, 0), (-1, -1), 0.25,
                                      colors.black),
                                     ('BOX', (0, 0), (-1, -1), 0.25,
                                      colors.black)]
                  )
    t_var_info = Table(table_info_data, style=[('FONTSIZE', (0, 0), (-1, -1),
                                                8)])
    t_var.wrapOn(file, 150, 150)
    t_var.drawOn(file, 180, 650)
    t_var_info.wrapOn(file, 150, 150)
    t_var_info.drawOn(file, 100, 490)

    t_pres1 = Table(t_pres1_data, style=[('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                         ('BACKGROUND', (0, 0), (-1, 0),
                                          colors.grey),
                                         ('INNERGRID', (0, 0), (-1, -1), 0.25,
                                         colors.black),
                                         ('BOX', (0, 0), (-1, -1), 0.25,
                                          colors.black),
                                         ('FONTSIZE', (0, 0), (-1, -1), 8)])
    t_pres2 = Table(t_pres2_data, style=[('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                         ('BACKGROUND', (0, 0), (-1, 0),
                                          colors.grey),
                                         ('INNERGRID', (0, 0), (-1, -1), 0.25,
                                         colors.black),
                                         ('BOX', (0, 0), (-1, -1), 0.25,
                                          colors.black),
                                         ('FONTSIZE', (0, 0), (-1, -1), 8)])
    t_pres_info = Table(pres_info_a, style=[('FONTSIZE', (0, 0), (-1, -1),
                                             8)])
    t_pres1.wrapOn(file, 150, 150)
    t_pres2.wrapOn(file, 150, 150)
    t_pres1.drawOn(file, 100, 400)
    t_pres2.drawOn(file, 50, 340)
    t_pres_info.wrapOn(file, 150, 150)
    t_pres_info.drawOn(file, 100, 50)
    file.showPage()
    t_pres_info_b = Table(pres_info_b, style=[('FONTSIZE', (0, 0), (-1, -1),
                                              8)])
    t_pres_info_b.wrapOn(file, 150, 150)
    t_pres_info_b.drawOn(file, 100, 520)
    file.showPage()

    file.setFont('Helvetica-Bold', 18)
    file.drawString(80, 750, 'Resultados')
    file.setFont('Helvetica', 12)
    file.drawString(65, 710, 'Después de simular la evolución de la ' +
                    'enfermedad se obtuvieron los siguientes resultados')
    t_res = Table(t_d, style=[('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                              ('BACKGROUND', (0, 0), (-1, 0),
                               colors.grey),
                              ('INNERGRID', (0, 0), (-1, -1), 0.25,
                               colors.black),
                              ('BOX', (0, 0), (-1, -1), 0.25,
                               colors.black),
                              ('FONTSIZE', (0, 0), (-1, -1), 6)])
    t_res.wrapOn(file, 150, 150)
    t_res.drawOn(file, 65, 430)
    file.setFont('Helvetica', 8)
    file.drawString(90, 420, '**Los resultados se expresan en número de células individuales.')
    file.setFont('Helvetica-Bold', 14)
    file.drawString(65, 400, '¡Aviso!')
    file.setFont('Helvetica', 10)
    file.drawString(65, 380, 'Los resultados fueron obtenidos usando un modelo' +
                    ' en desarrollo. Estos no deberán interpretarse como')
    file.drawString(65, 365, 'resultados exactos ni ser usados como referencia bajo ninguna circunstancia.')
    file.showPage()

    drawing = create_chart(results, variables, max_val)
    drawing.wrapOn(file, 150, 150)
    drawing.drawOn(file, 80, 100)
    file.setFont('Helvetica', 8)
    file.drawString(90, 90, 'Eje x: tiempo en meses.    Eje y: numero de celulas')
    file.drawString(90, 80, 'Rojo: MNA.  Azul: MA.  Rosa: MNAF.  Gris: MAF')
    file.drawString(90, 70, 'Verde: TL.  Naranja: TNA.  Morado: TA.')
    file.showPage()
    file.save()


def make_desc_arr(data):
    output = []
    descriptions = ['Tasa de proliferacion de M. tuberculosis',
                    'Tasa de proliferacion de M. tuberculosis fagocitada por macrofago no activado',
                    'Tasa de proliferacion de M. tuberculosis fagocitada por macrofago activado',
                    'Entrada constante de macrofago', 
                    'Tasa de reclutamiento de monocitos circulantes al lugar de la infección por Macrófago no activado que fagocitó',
                    'Tasa de reclutamiento de monocitos circulantes al lugar de la infección por Macrófago activado que fagocitó',
                    'Capacidad fagocítica de Macrófago no activado',
                    'Capacidad fagocítica de Macrófago activado',
                    'Activación de macrófago que no ha fagocitado',
                    'Activación de macrófago que ha fagocitado',
                    'Vida media de macrofago no activado',
                    'Tasa de muerte de M. tuberculosis libre causado por Macrófago no activado',
                    'Tasa de muerte de Macrófago no activado causada por M. tuberculosis libre',
                    'Vida media de macrofago activado',
                    'Tasa de muerte de M. tuberculosis libre causado por Macrófago activado',
                    'Tasa de muerte de Macrófago activado causada por M. tuberculosis libre',
                    'Vida media de Macrófago no activado que ha fagocitado',
                    'Tasa de muerte de M. tuberculosis libre causado por Macrófago no activado',
                    'Tasa de muerte de M. tuberculosis fagocitada causado por Macrófago no activado',
                    'Tasa de muerte de Macrófago no activado que ha fagocitado causada por M. tuberculosis libre',
                    'Tasa de muerte de Macrófago no activado que ha fagocitado causada por M. tuberculosis fagocitada',
                    'Vida media de Macrófago activado que ha fagocitado',
                    'Tasa de muerte de M. tuberculosis libre causado por Macrófago activado que ha fagocitado',
                    'Tasa de muerte de M. tuberculosis fagocitada causado por Macrófago activado que ha fagocitado',
                    'Tasa de muerte de Macrófago activado que ha fagocitado causada por M. tuberculosis libre',
                    'Tasa de muerte de Macrófago activado que ha fagocitado causada por M. tuberculosis fagocitada',
                    'Vida media de M. tuberculosis libre',
                    'Vida media de M. tuberculosis fagocitada por macrófago no activado',
                    'Vida media de M. tuberculosis fagocitada por macrófago activado']

    for i, item in enumerate(data):
        descr = item + '= '
        li = [descr, descriptions[i]]
        output.append(li)
    return output


def create_chart(data, variables, max_val):
    drawing = Drawing(400, 200)
    lp = LinePlot()
    lp.x = 50
    lp.y = 50
    lp.height = 600
    lp.width = 400
    lp.data = data
    lp.joinedLines = 1
    color_list = [colors.red, colors.blue, colors.pink, colors.grey,
                  colors.green, colors.orange, colors.purple]
    for i in range(len(data)):
        lp.lines[i].strokeColor = color_list[i]
        lp.lines[i].symbol = makeMarker('FilledCircle')
    # lp.lineLabelFormat = '%2.0f'
    lp.strokeColor = colors.black
    lp.xValueAxis.valueMin = 0
    lp.xValueAxis.valueMax = 12
    lp.xValueAxis.valueSteps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    lp.xValueAxis.labelTextFormat = '%2.1f'
    lp.yValueAxis.valueMin = 0
    # lp.yValueAxis.valueMax = max_val
    # lp.yValueAxis.valueSteps = create_marks(max_val)
    lp.yValueAxis.valueMax = 100000000000
    lp.yValueAxis.valueSteps = create_marks(100000000000)
    drawing.add(lp)
    return drawing


def create_marks(data):
    data = int(round(data))
    result = []
    if(data > 100):
        result = range(int(round(data / 10)), data, int(round(data / 10)))
    elif data <= 10:
        result = range(1, data)
    real_result = []
    for item in result:
        real_result.append(item)
    return real_result
