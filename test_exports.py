# -*- coding: utf-8 -*-
import tempfile, zipfile, subprocess
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
        rows=main.stage_activity(lesson)
        assert all(row[2] and row[3] and row[4] for row in rows), 'automatic pedagogical fields must not be empty'
        docx=out/'lesson.docx'; main.write_docx(docx,text,lesson); assert zipfile.is_zipfile(docx)
        with zipfile.ZipFile(docx) as z:
            xml=z.read('word/document.xml').decode('utf-8')
            assert '<w:tbl>' in xml and '<w:tblHeader/>' in xml
            assert 'استحضار المكتسبات السابقة' in xml and 'مؤشرات التقويم' in xml
        html=out/'lesson.html'; html.write_text(main.html_doc(lesson),encoding='utf-8'); assert 'dir="rtl"' in html.read_text(encoding='utf-8')
        pdf=out/'lesson.pdf'; main.write_pdf(pdf,lesson); assert pdf.exists() and pdf.stat().st_size > 10000
        info=subprocess.run(['pdfinfo',str(pdf)],capture_output=True,text=True,check=True).stdout
        assert 'Pages:' in info and 'Page size:' in info and '841.89 x 595.276 pts (A4)' in info
    print('PASS export_long_arabic')

if __name__=='__main__': main_test(); print('ALL EXPORT TESTS PASSED')
