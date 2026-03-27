# Chemical Structures Visualizer

将 SMILES 分子式转换为精美化学结构图像的 Python 工具

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![RDKit](https://img.shields.io/badge/RDKit-Latest-orange)

## 项目简介

本项目从 CSV 文件读取化合物的 SMILES（Simplified Molecular Input Line Entry System）分子式，利用 RDKit 化学信息学库自动生成对应的 2D 化学结构图像，并导出为带有结构图片的 Excel 文件。

## 功能特点

- 读取 SMILES 格式的化学分子式
- 自动生成高质量 2D 化学结构图像
- 将图像批量插入 Excel（SMILES 右侧单元格）
- 支持 156+ 化合物的批量处理
- 输出可编辑的 Excel 文件，方便进一步分析

## 快速开始

### 环境要求

- Python 3.8+
- Windows / macOS / Linux

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python generate_chemical_images.py
```

程序将自动：
1. 读取 `chemical_structures_data.csv` 文件
2. 为每个 SMILES 生成化学结构图像
3. 创建包含结构图像的 Excel 文件

### 输出文件

- `chemical_structures_with_images.xlsx` - 带图像的 Excel 文件
- `chemical_images/` - 单独的结构图像（PNG 格式）

## 数据格式

### 输入 CSV 格式

```csv
Index,SMILES
1,CN(Cc1ccccc1[N+](=O)[O-])Cc1cc(=O)oc2cc(O)ccc12
2,O=C(C=Cc1cc(Br)ccc1OC(F)F)Nc1ccc2c(c1)OCO2
```

### 输出 Excel 格式

| Index | SMILES | Structure |
|-------|--------|-----------|
| 1 | CN(Cc1ccccc1[N+](=O)[O-])... | ![](images/compound_1.png) |
| 2 | O=C(C=Cc1cc(Br)ccc1OC(F)F)... | ![](images/compound_2.png) |

## 示例图像

以下是部分生成的化学结构图像：

| 化合物示例 | 描述 |
|-----------|------|
| ![](chemical_images/compound_1.png) | 含有硝基和苯环的化合物 |
| ![](chemical_images/compound_2.png) | 含溴和氟的芳香化合物 |
| ![](chemical_images/compound_3.png) | 含噻唑环的化合物 |

## 技术栈

- **Python 3.11** - 编程语言
- **RDKit** - 化学信息学库（分子结构处理）
- **Pandas** - 数据处理
- **OpenPyXL** - Excel 文件操作
- **Pillow (PIL)** - 图像生成

## 项目结构

```
Third_work/
├── chemical_structures_data.csv   # 原始 SMILES 数据
├── generate_chemical_images.py     # 主程序脚本
├── chemical_structures_with_images.xlsx  # 输出的 Excel 文件
├── chemical_images/                 # 生成的图像文件夹
│   ├── compound_1.png
│   ├── compound_2.png
│   └── ...
├── requirements.txt                  # Python 依赖
└── README.md                         # 项目文档
```

## 扩展使用

### 自定义图像大小

修改脚本中的 `size` 参数：

```python
img = Draw.MolToImage(mol, size=(500, 300))  # 更大更清晰的图像
```

### 添加更多 SMILES 数据

在 `chemical_structures_data.csv` 中添加新行，遵循以下格式：

```csv
Index,SMILES
157,CCOc1ccc(NC(=O)c2ccco2)cc1
```

重新运行脚本即可生成新图像。

## 许可证

MIT License - 自由使用、修改和分发

## 贡献指南

欢迎提交 Issue 和 Pull Request！

---

⭐ 如果这个项目对你有帮助，请 star 支持一下！