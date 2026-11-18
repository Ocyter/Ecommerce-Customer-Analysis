"""Meaningful publication checks; not a Career Coach or accessibility score."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import json
import re

ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.links=[]; self.h1=0
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if 'id' in d:self.ids.append(d['id'])
        if tag=='a' and 'href' in d:self.links.append(d['href'])
        if tag=='h1':self.h1+=1

pages={}
for path in ROOT.rglob('*.html'):
    if '.git' in path.parts:continue
    parser=Page(); text=path.read_text(encoding='utf-8'); parser.feed(text)
    assert parser.h1==1,(path,'H1 count')
    assert len(parser.ids)==len(set(parser.ids)),(path,'Duplicate IDs')
    assert '—' not in text,(path,'Em dash')
    pages[path.resolve()]=parser
for path,parser in pages.items():
    for href in parser.links:
        u=urlparse(href)
        if u.scheme or u.netloc:continue
        destination=(path.parent/unquote(u.path)).resolve() if u.path else path
        if destination.is_dir():destination=destination/'index.html'
        assert destination.is_file(),(path,href,'Missing destination')
        if u.fragment:
            assert destination in pages and unquote(u.fragment) in pages[destination].ids,(path,href,'Missing fragment')
cv=(ROOT/'resume.html').read_text()
jobs=re.findall(r'<article class="cv-job">(.*?)</article>',cv,re.S)
assert len(jobs)==4
for job in jobs:assert len(re.findall(r'<li>',job))>=3
expected=(
'Genesys Upskill','Genesys','AtlasCapture','National Assembly',
'Sep 2026 to Present','Dec 2025 to Aug 2026','Dec 2025 to Jun 2026',
'May 2025 to Apr 2026','BSc Computer Science'
)
from pypdf import PdfReader
reader=PdfReader(ROOT/'downloads/Osita_Nwaigwe_Portfolio_CV.pdf')
text='\n'.join(page.extract_text() for page in reader.pages)
for term in expected:assert term in text,term
uris=set()
for page in reader.pages:
    for annotation in page.get('/Annots',[]):
        action=annotation.get_object().get('/A',{})
        if '/URI' in action:uris.add(str(action['/URI']))
for uri in [
'tel:+2349035379801','mailto:nwaigweaustin96@gmail.com',
'https://www.linkedin.com/in/osita-nwaigwe-a2288b394',
'https://ocyter.github.io/','https://github.com/Ocyter'
]: assert uri in uris,uri
assert 'Selected Role Alignment' not in text
import fitz
pdf=fitz.open(ROOT/'downloads/Osita_Nwaigwe_Portfolio_CV.pdf')
for page in pdf:
    spans=[s for b in page.get_text('dict')['blocks'] if 'lines' in b for line in b['lines'] for s in line['spans']]
    assert spans
    for span in spans:
        assert span['color']==0,span
        assert not re.search('italic|oblique',span['font'],re.I),span
        x0,y0,x1,y1=span['bbox']
        assert 0<=x0<x1<=page.rect.width and 0<=y0<y1<=page.rect.height,span
verification=json.loads((ROOT/'case-studies/sql-data-quality/outputs/verification.json').read_text())
assert verification['raw_order_rows']==12
assert verification['quarantined_order_rows']==7
assert verification['reported_amount_ngn']==52000
assert verification['row_reconciliation_difference']==0
assert verification['known_amount_reconciliation_difference_ngn']==0
print(f'PASS: {len(pages)} page structures, local links/fragments, four CV roles, dates, PDF links, black non-italic text, PDF text bounds, and SQL fixture expectations.')
print('PDF_PAGES',len(reader.pages))
print('Not checked: live desktop/mobile interactions, Power BI execution or identity of the historical customer file.')
