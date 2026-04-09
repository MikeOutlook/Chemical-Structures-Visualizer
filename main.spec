# PyInstaller 配置文件
# 使用方法: pyinstaller main.spec

from PyInstaller.utils.hooks import collect_all, collect_submodules
from PyInstaller.building.build_main import Analysis, EXE, PYZ

# 收集 RDKit 相关模块
# 这里集中声明 PyInstaller 在静态分析时可能漏掉的运行时依赖。
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

# 打包时把项目源码目录一起带上，确保运行时能找到本地模块。
datas = [
    ('chemical_visualizer', 'chemical_visualizer'),
    ('gui', 'gui'),
]

# Analysis 负责扫描入口脚本及其依赖关系。
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

# EXE 定义最终生成的可执行程序形态。
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
