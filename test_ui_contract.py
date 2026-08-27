from pathlib import Path

root = Path(__file__).parent
html = (root / 'app' / 'web' / 'index.html').read_text(encoding='utf-8')
bridge = (root / 'app' / 'web_app.py').read_text(encoding='utf-8')
spec = (root / 'Tarbawi-Jodada.spec').read_text(encoding='utf-8')
bat = (root / 'BUILD-WINDOWS.bat').read_text(encoding='utf-8')
workflow = (root / '.github' / 'workflows' / 'windows-build.yml').read_text(encoding='utf-8')

checks = {
    'rtl': 'dir="rtl"' in html,
    'svg_icons': 'const SVG=' in html and 'function icon(' in html,
    'dark_mode': 'toggleDark' in html and 'tarbawi-dark' in html,
    'stage_reorder': 'function moveStage(step)' in html and 'data-tip="نقل المرحلة' in html,
    'hypothesis_scrutiny': 'function scrutiny' in html and 'current.stages.find(x=>x.kind===\'problem\')' in html,
    'windows_save_as': 'asksaveasfilename' in bridge,
    'windows_open_dialog': 'askopenfilename' in bridge,
    'word_export': "kind == 'docx'" in bridge,
    'html_export': "kind == 'docx'" in bridge and 'html_doc' in bridge,
    'no_pdf_active': not any(x in (html + bridge + spec + bat + workflow) for x in ('weasyprint', 'reportlab', 'export_pdf', '.pdf', 'تصدير PDF')),
    'active_entrypoint': "['app\\\\web_app.py']" in spec or "['app\\web_app.py']" in spec,
    'icon_packaged': 'tarbawi-icon.ico' in spec and 'tarbawi-icon.png' in spec,
    'double_click_build': 'PY_LAUNCHER=py -3' in bat and '-m venv' in bat and '>>>' not in bat,
    'requirements_file': 'requirements-build.txt' in bat,
}
for name, ok in checks.items():
    if not ok:
        raise SystemExit('FAIL ' + name)
    print('PASS', name)
print('ALL UI CONTRACT TESTS PASSED')
