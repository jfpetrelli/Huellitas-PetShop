from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
import io


def mail():
    pdf = generar_pdf()
    email = EmailMessage('Lista actualizada', 'el mensaje','seminarioe2etest@gmail.com', ['seminarioe2etest@gmail.com'])
    email.attach('ejemplo1.pdf', pdf)
    email.send()
    print('enviado')
    
def generar_pdf():
    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return p
