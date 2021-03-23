from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.platypus import Spacer
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter, landscape
import io

pdfmetrics.registerFont(
    TTFont('Comfortaa', "fonts/Comfortaa/Comfortaa-VariableFont_wght.ttf"))

def create_title(text):
    styles = getSampleStyleSheet()
    title_style = styles['Heading2']
    title_style.alignment = 1
    title = Paragraph(text, title_style)
    return title

def create_paragraph(text):
    paragraph_style = ParagraphStyle(
        name='Normal',
        fontSize=18,
        leading=24,
        alignment=1,
        fontName="Comfortaa"
    )
    paragraph = Paragraph(text, paragraph_style)
    return paragraph

def create_name(text):
    paragraph_style = ParagraphStyle(
        name='Normal',
        fontSize=50,
        leading=55,
        alignment=1,
        fontName = "Comfortaa"
    )
    paragraph = Paragraph(text, paragraph_style)
    return paragraph

def create_assinatura(text, align):
    assinatura_style = ParagraphStyle(
        name='Normal',
        fontSize=12,
        alignment=align,
    )
    assinatura = Paragraph(text, assinatura_style)
    return assinatura


def create_line():
    line_style = ParagraphStyle(
        name='Normal',
        fontSize=12,
        leading=18,
    )
    line_style.alignment = 1
    line = Paragraph("_____________________________________________________________", line_style)
    return line

def create_qr_code(text):
    qrw = QrCodeWidget(text)
    b = qrw.getBounds()

    w = b[2] - b[0]
    h = b[3] - b[1]

    d = Drawing(45, 45, transform=[90. / w, 0, 0, 90. / h, 0, 0])
    d.add(qrw)
    return d


def pdf_generator(participant, data):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate("files/modelos/certificado.pdf",
                            pagesize=landscape(letter),
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=32,
                            bottomMargin=18,
                            title='Certificado')
    flowables = []
    # title = create_title("CERTIFICADO")
    name = create_name(str(participant).upper())
    description = create_paragraph('Pela participação como Avaliador(a) na I Feira de Ciências Virtual '
                                   'Sertão Ciência no dia '+str(int(data))+' de Dezembro de 2020 '
                                   'com carga horária de 08 horas.')

    flowables.append(Spacer(1, 0.1 * 600))
    flowables.append(Spacer(1, 0.1 * 1200))
    flowables.append(name)
    flowables.append(Spacer(1, 0.1 * 200))
    flowables.append(description)
    flowables.append(Spacer(1, 0.1 * 800))
    flowables.append(Spacer(1, 0.1 * 800))

    # flowables.append(assinatura)

    # flowables.append(Spacer(1, 0.1 * 800))
    # flowables.append(create_qr_code('123456890987654321'))
    doc.build(flowables)


def merge_pdf(path_file1, path_file2, path_output):

    file1 = PdfFileReader(open(path_file1, "rb"))
    output_file = PdfFileWriter()
    file2 = PdfFileReader(open(path_file2, "rb"))
    input_page = file2.getPage(0)
    input_page.mergePage(file1.getPage(0))
    output_file.addPage(input_page)

    with open(path_output, "wb") as outputStream:
        output_file.write(outputStream)