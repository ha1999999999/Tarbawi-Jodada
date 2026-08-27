# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

weasy_datas, weasy_binaries, weasy_hidden = collect_all('weasyprint')

analysis = Analysis(
    ['app\\web_app.py'],
    pathex=['app', '.'],
    binaries=weasy_binaries,
    datas=[
        ('app\\web', 'web'),
        ('tarbawi-icon.png', '.'),
        *weasy_datas,
    ],
    hiddenimports=[
        'webview',
        'webview.platforms.winforms',
        'webview.platforms.edgechromium',
        'weasyprint',
        *weasy_hidden,
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
