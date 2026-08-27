from pathlib import Path
import re

html = Path('app/web/index.html').read_text(encoding='utf-8')
required = [
    'dir="rtl"', 'class="sidebar"', 'class="topbar"', 'class="card"',
    'function icon(', 'function moveStage(', 'function toggleDark(',
    'تمحيص الفرضيات', 'نسخ احتياطي', 'استرجاع نسخة', 'تصدير Word',
    'المعينات الديداكتيكية', 'مؤشرات التقويم', 'window.pywebview'
]
missing = [item for item in required if item not in html]
if missing:
    raise SystemExit('Missing UI markers: ' + ', '.join(missing))
if "doExport('pdf')" not in html:
    raise SystemExit('PDF export button missing from active HTML UI')
script = '\n'.join(re.findall(r'<script[^>]*>(.*?)</script>', html, re.S | re.I))
if not script.strip():
    raise SystemExit('No JavaScript found')
Path('/tmp/tarbawi_ui.js').write_text(script, encoding='utf-8')
print('PASS html_markers')
print('PASS rtl_and_svg')
print('PASS pdf_export_present')
print('PASS javascript_present')
print('HTML UI CHECK PASSED')
