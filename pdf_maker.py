from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def make_pdf(type_of_bacteria, duration, temp, acidity, nutrient, hum):
       c = canvas.Canvas("simulador.pdf", pagesize=A4)
       c.setFont('Helvetica', 12)

       c.drawString(30, 810, 'Reporte - Simulador de bacterias')
       c.line(30, 800, 550, 800)
       c.drawImage('transcurso.png', 140, 550, width=313, height=235)

       c.drawString(45, 530, '- Bacteria seleccionada: {}'.format(type_of_bacteria))
       c.drawString(45, 510, '- Duracion total: {}s'.format(duration))
       c.drawString(45, 490, '- Temperatura inicial: {}C'.format(temp))
       c.drawString(45, 470, '- Acidez inicial: {}ph'.format(acidity))
       c.drawString(45, 450, '- Nutriente inicial: {}'.format(nutrient))
       c.drawString(45, 430, '- Humedad inicial: {}'.format(hum))

       c.drawImage('initialbacteria.jpeg', 125, 262, width=150, height=150)
       c.drawImage('maxbacteria.jpeg', 325, 262, width=150, height=150)
       c.drawString(150, 250, 'Bacterias iniciales')
       c.drawString(345, 250, 'Maximo N Bacterias')

       c.save()



