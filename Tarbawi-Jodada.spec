# -*- mode: python ; coding: utf-8 -*-

analysis = Analysis(
    ['app\\web_app.py'],
    pathex=['app', '.'],
    binaries=[],
    datas=[
        ('app\\web', 'web'),
        ('app\\assets\\Amiri-Regular.ttf', 'assets'),
        ('app\\assets\\Amiri-Bold.ttf', 'assets'),
        ('tarbawi-icon.png', '.'),
    ],
    hiddenimports=[
        'webview',
        'webview.platforms.winforms',
        'webview.platforms.edgechromium',
        'reportlab.pdfbase._fontdata',
        'arabic_reshaper',
        'bidi',
    ],
    hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=['weasyprint'], noarchive=False,
)

pyz = PYZ(analysis.pure)
exe = EXE(
    pyz, analysis.scripts, analysis.binaries, analysis.datas, [],
    name='Tarbawi-Jodada', debug=False, bootloader_ignore_signals=False,
    strip=False, upx=False, console=False, icon='tarbawi-icon.ico',
    disable_windowed_traceback=False,
)
