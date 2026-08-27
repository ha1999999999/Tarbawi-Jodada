# -*- coding: utf-8 -*-
from pathlib import Path
import sys

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'app'))
import main

out = ROOT / 'tests' / 'sample_output'
out.mkdir(parents=True, exist_ok=True)
l = main.blank_lesson()
l['lesson_title'] = 'عينة فحص الإيمان والفلسفة'
l['level'] = 'الأولى باكالوريا'
l['school_year'] = '2026-2027'
l['institution'] = 'مؤسسة تجريب الفحص'
l['teacher'] = 'أستاذ التربية الإسلامية'
l['stages'][1]['problem'] = 'هل يمكن للعقل أن يصل إلى الحقيقة؟ هذا نص عربي طويل لفحص تعدد الصفحات. ' * 500
l['stages'][1]['hypotheses'] = [
    {'text': 'لا تعارض بين الإيمان والفلسفة', 'original_reason': 'كلاهما يطلب الحقيقة'}
    for _ in range(6)
]
l['stages'][8]['values'] = [
    {'name': 'التوحيد', 'evidence': 'دليل قرآني', 'explanation': 'شرح القيمة', 'behaviors': 'تجسيدها'}
    for _ in range(5)
]
(out / 'sample.docx').unlink(missing_ok=True)
(out / 'sample.html').unlink(missing_ok=True)
main.write_docx(out / 'sample.docx', main.render_text(l), l)
(out / 'sample.html').write_text(main.html_doc(l), encoding='utf-8')
print('DOCX_OK', (out / 'sample.docx').stat().st_size)
print('HTML_OK', (out / 'sample.html').stat().st_size)
