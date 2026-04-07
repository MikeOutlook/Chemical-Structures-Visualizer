# PyInstaller 配置文件
# 使用方法: pyinstaller main.spec

from PyInstaller.utils.hooks import collect_all, collect_submodules
from PyInstaller.building.build_main import Analysis, EXE, PYZ

# 收集 RDKit 相关模块
hiddenimports = [
    'rdkit',
    'rdkit.Chem',
    'rdkit.Chem.Draw',
    'rdkit.Chem.AllChem',
    'rdkit.RDLogger',
    'pandas',
    'openpyxl',
    'openpyxl.drawing.image',
    'PIL',
    'PIL.Image',
    'PIL.ImageTk',
    'customtkinter',
    'customtkinter',
    'customtkinter.tk',
    'tkinter',
    'tkinter.filedialog',
    'tkinter.messagebox',
]

datas = [
    ('chemical_visualizer', 'chemical_visualizer'),
    ('gui', 'gui'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
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
)