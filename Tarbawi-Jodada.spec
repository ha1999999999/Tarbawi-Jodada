# -*- mode: python ; coding: utf-8 -*-

analysis = Analysis(
    ['app\\web_app.py'],
    pathex=['app', '.'],
    binaries=[],
    datas=[
        ('app\\web', 'web'),
        ('tarbawi-icon.png', '.'),
    ],
    hiddenimports=[
        'webview',
        'webview.platforms.winforms',
        'webview.platforms.edgechromium',
    ],
    hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=[], noarchive=False,
)

pyz = PYZ(analysis.pure)
exe = EXE(
    pyz, analysis.scripts, analysis.binaries, analysis.datas, [],
    name='Tarbawi-Jodada', debug=False, bootloader_ignore_signals=False,
    strip=False, upx=False, console=False, icon='tarbawi-icon.ico',
    disable_windowed_traceback=False,
)
