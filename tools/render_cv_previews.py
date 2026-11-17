"""Render each actual generated PDF page for visual review."""
from pathlib import Path
import base64
import fitz
ROOT=Path(__file__).resolve().parents[1]
document=fitz.open(ROOT/'downloads/Osita_Nwaigwe_Portfolio_CV.pdf')
for number,page in enumerate(document,1):
    pixels=page.get_pixmap(matrix=fitz.Matrix(1.15,1.15))
    data=pixels.tobytes('png')
    (ROOT/'downloads'/f'cv-page-{number}.png').write_bytes(data)
    print(f'CV_PREVIEW_BEGIN_{number}')
    print(base64.b64encode(data).decode('ascii'))
    print(f'CV_PREVIEW_END_{number}')
