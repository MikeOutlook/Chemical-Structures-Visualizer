# -*- mode: python ; coding: utf-8 -*-

# 旧模板里保留该变量，便于统一传给 Analysis / PYZ。
block_cipher = None

# Analysis 负责解析入口脚本并收集打包所需资源。
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('chemical_visualizer', 'chemical_visualizer'),
        ('gui', 'gui'),
    ],
    hiddenimports=[
        'rdkit',
        'rdkit.Chem',
        'rdkit.Chem.Draw',
        'pandas',
        'openpyxl',
        'PIL',
        'customtkinter',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, block_cipher)

# EXE 负责描述最终 GUI 可执行文件的打包参数。
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ChemicalStructureVisualizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
