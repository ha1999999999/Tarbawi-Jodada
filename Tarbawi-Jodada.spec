# -*- mode: python ; coding: utf-8 -*-



from PyInstaller.utils.hooks import collect_all



weasy_datas, weasy_binaries, weasy_hidden = collect_all('weasyprint')



analysis = Analysis(

    ['app\\main.py'],
    
    pathex=['.'],
    
    binaries=weasy_binaries,
    
    datas=weasy_datas,
    
    hiddenimports=weasy_hidden + ['weasyprint', 'weasyprint.text.ffi', 'cairocffi'],
    
    hookspath=[],
    
    hooksconfig={},
    
    runtime_hooks=[],
    
    excludes=[],
    
    noarchive=False,
    
)



pyz = PYZ(analysis.pure)

exe = EXE(

    pyz,
    
    analysis.scripts,
    
    analysis.binaries,
    
    analysis.datas,
    
    [],
    
    name='Tarbawi-Jodada',
    
    debug=False,
    
    bootloader_ignore_signals=False,
    
    strip=False,
    
    upx=False,
    
    console=False,
    
    disable_windowed_traceback=False,
    
)























