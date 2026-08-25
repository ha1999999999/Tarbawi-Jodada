# -*- coding: utf-8 -*-
import tempfile, zipfile
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / 'app'))
import main

def main_test():
    with tempfile.TemporaryDirectory() as d:
        out=Path(d)
        lesson=main.blank_lesson(); lesson['lesson_title']='جذاذة طويلة للاختبار'; lesson['level']='الأولى باكالوريا'
        lesson['stages'][1]['problem']='هذا نص عربي طويل للاختبار. '*100
        lesson['stages'][1]['hypotheses']=[{'text':'فرضية أولى','original_reason':'تعليل أصلي'} for _ in range(8)]
        lesson['stages'][8]['values']=[{'name':'التوحيد','evidence':'دليل','explanation':'شرح القيمة','behaviors':'سلوك'} for _ in range(5)]
        text=main.render_text(lesson); assert len(text)>1000
        docx=out/'lesson.docx'; main.write_docx(docx,text); assert zipfile.is_zipfile(docx)
        html=out/'lesson.html'; html.write_text(main.html_doc(lesson),encoding='utf-8'); assert 'dir="rtl"' in html.read_text(encoding='utf-8')
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        pdf=out/'lesson.pdf'; p=canvas.Canvas(str(pdf),pagesize=A4); p.drawString(50,800,'اختبار'); p.save(); assert pdf.stat().st_size>0
    print('PASS export_long_arabic')

if __name__=='__main__': main_test(); print('ALL EXPORT TESTS PASSED')
