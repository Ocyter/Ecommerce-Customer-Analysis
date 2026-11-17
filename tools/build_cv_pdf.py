"""Build the public PDF from resume.html. Original uploaded CV is not modified."""
from pathlib import Path
from html import unescape
from xml.sax.saxutils import escape
import re
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
FONT = Path('/usr/share/fonts/truetype/dejavu')

def markup(s):
    s = s.replace('<strong>', '<b>').replace('</strong>', '</b>')
    s = re.sub(r'<a href="([^"]+)">(.*?)</a>',
               r'<link href="\1" color="black"><u>\2</u></link>', s)
    return s.replace('<br>', '<br/>')

def plain(s):
    return unescape(re.sub(r'<[^>]+>', '', s))

def build():
    html = (ROOT / 'resume.html').read_text(encoding='utf-8')
    if (FONT / 'DejaVuSans.ttf').exists():
        pdfmetrics.registerFont(TTFont('CV', str(FONT / 'DejaVuSans.ttf')))
        pdfmetrics.registerFont(TTFont('CV-Bold', str(FONT / 'DejaVuSans-Bold.ttf')))
        pdfmetrics.registerFontFamily('CV', normal='CV', bold='CV-Bold', italic='CV', boldItalic='CV-Bold')
        normal, bold = 'CV', 'CV-Bold'
    else:
        normal, bold = 'Helvetica', 'Helvetica-Bold'
    common = dict(fontName=normal, textColor=colors.black, alignment=TA_LEFT)
    styles = {
        'name': ParagraphStyle('name', fontSize=25, leading=30, spaceAfter=3, fontName=bold, textColor=colors.black),
        'role': ParagraphStyle('role', fontSize=12, leading=17, spaceAfter=8, **common),
        'contact': ParagraphStyle('contact', fontSize=9.5, leading=14, spaceAfter=10, **common),
        'heading': ParagraphStyle('heading', fontSize=12, leading=16, spaceBefore=9, spaceAfter=6, keepWithNext=True, fontName=bold, textColor=colors.black),
        'body': ParagraphStyle('body', fontSize=10.3, leading=14, spaceAfter=5, **common),
        'job': ParagraphStyle('job', fontSize=10.5, leading=14, spaceAfter=3, keepWithNext=True, fontName=bold, textColor=colors.black),
        'detail': ParagraphStyle('detail', fontSize=10, leading=13.5, spaceAfter=5, **common),
        'bullet': ParagraphStyle('bullet', fontSize=10.1, leading=13.5, leftIndent=10, firstLineIndent=-10, spaceAfter=4, **common)
    }
    out = ROOT / 'downloads' / 'Osita_Nwaigwe_Portfolio_CV.pdf'
    out.parent.mkdir(exist_ok=True)
    document = SimpleDocTemplate(str(out), pagesize=A4,
        topMargin=13*mm, bottomMargin=14*mm, leftMargin=16*mm, rightMargin=16*mm,
        title='Osita Nwaigwe | Data Analyst | Portfolio CV', author='Osita Nwaigwe')
    story = [Paragraph('Osita Nwaigwe', styles['name']), Paragraph('Data Analyst', styles['role'])]
    contact = re.search(r'<div class="cv-contact">(.*?)</div>', html, re.S).group(1)
    contact_links = re.findall(r'<a href="[^"]+">.*?</a>', contact)
    story.append(Paragraph(' · '.join(markup(a) for a in contact_links), styles['contact']))
    for heading, section in re.findall(r'<section><h2>(.*?)</h2>(.*?)</section>', html, re.S):
        story.append(Paragraph(escape(plain(heading)), styles['heading']))
        if heading == 'Experience':
            for article in re.findall(r'<article class="cv-job">(.*?)</article>', section, re.S):
                employer = re.search(r'<h3>(.*?)</h3>', article, re.S).group(1)
                role = re.search(r'<p>(.*?)</p>', article, re.S).group(1)
                dates = re.search(r'<p class="cv-date">(.*?)</p>', article, re.S).group(1)
                job = [Paragraph(markup(employer), styles['job']),
                       Paragraph(markup(role)+' · '+markup(dates), styles['detail'])]
                for bullet in re.findall(r'<li>(.*?)</li>', article, re.S):
                    job.append(Paragraph('• '+markup(bullet), styles['bullet']))
                job.append(Spacer(1,5))
                story.append(KeepTogether(job))
        elif heading == 'Core skills':
            for bullet in re.findall(r'<li>(.*?)</li>', section, re.S):
                story.append(Paragraph('• '+markup(bullet), styles['bullet']))
        else:
            for paragraph in re.findall(r'<p>(.*?)</p>', section, re.S):
                paragraph=paragraph.replace('href="customer-behaviour.html"', 'href="https://ocyter.github.io/Ecommerce-Customer-Analysis/customer-behaviour.html"')
                story.append(Paragraph(markup(paragraph), styles['body']))

    def footer(canvas, doc):
        canvas.setFont(normal,8)
        canvas.setFillColor(colors.black)
        canvas.drawString(16*mm,9*mm,'Osita Nwaigwe · Data Analyst')
        canvas.drawRightString(A4[0]-16*mm,9*mm,str(doc.page))
    document.build(story,onFirstPage=footer,onLaterPages=footer)
    print('Built CV PDF:',out)

if __name__=='__main__':
    build()
