# -*- coding: utf-8 -*-
import json, tempfile, zipfile
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / 'app'))
import main

def test_blank_lesson():
    l=main.blank_lesson(); assert l['lesson_title']==''; assert len(l['stages'])==11
    assert l['stages'][1]['kind']=='problem'; assert l['stages'][7]['kind']=='scrutiny'

def test_render_arabic_and_hypothesis():
    l=main.blank_lesson(); p=l['stages'][1]; p['hypotheses']=[{'text':'لا تعارض بين الإيمان والفلسفة','original_reason':'دليل عقلي'}]
    s=main.render_text(l); assert 'لا تعارض' in s; assert 'تمحيص الفرضيات' in s

def test_docx_real_zip():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'lesson.docx'; lesson=main.blank_lesson(); lesson['lesson_title']='الإيمان والفلسفة'; main.write_docx(p,'الإيمان والفلسفة\nسؤال وأجابة',lesson)
        assert zipfile.is_zipfile(p)
        with zipfile.ZipFile(p) as z:
            xml=z.read('word/document.xml').decode()
            assert 'word/document.xml' in z.namelist(); assert 'الإيمان' in xml; assert '<w:tbl>' in xml; assert '<w:tblBorders>' in xml; assert '<w:bidiVisual/>' in xml

def test_html_table_structure():
    l=main.blank_lesson(); h=main.html_doc(l); assert '<table>' in h; assert 'مراحل الدرس' in h; assert 'thead' in h; assert 'dir="rtl"' in h

def test_json_roundtrip():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'data.json'; obj={'lessons':[main.blank_lesson()], 'templates':[], 'settings':{}}
        p.write_text(json.dumps(obj,ensure_ascii=False),encoding='utf-8'); got=json.loads(p.read_text(encoding='utf-8')); assert got['lessons'][0]['stages'][0]['name']=='التقويم التشخيصي'

if __name__=='__main__':
    tests=[test_blank_lesson,test_render_arabic_and_hypothesis,test_docx_real_zip,test_html_table_structure,test_json_roundtrip]
    for t in tests: t(); print('PASS',t.__name__)
    print('ALL CORE TESTS PASSED')
