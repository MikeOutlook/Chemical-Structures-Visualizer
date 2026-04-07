# Chemical Structures Visualizer 🧪

<p align="center">
  <a href="https://github.com/MikeOutlook/Chemical-Structures-Visualizer/releases">
    <img src="https://img.shields.io/github/v/release/MikeOutlook/Chemical-Structures-Visualizer?include_prereleases&label=Version" alt="Version">
  </a>
  <a href="https://github.com/MikeOutlook/Chemical-Structures-Visualizer/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/MikeOutlook/Chemical-Structures-Visualizer" alt="License">
  </a>
  <a href="https://github.com/MikeOutlook/Chemical-Structures-Visualizer/stargazers">
    <img src="https://img.shields.io/github/stars/MikeOutlook/Chemical-Structures-Visualizer" alt="Stars">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python" alt="Python">
  </a>
  <a href="https://www.rdkit.org/">
    <img src="https://img.shields.io/badge/RDKit-Latest-orange?logo=python" alt="RDKit">
  </a>
</p>

> Turn SMILES molecular formulas into beautiful 2D structure images with ease!

## ✨ Features

- 📥 **Easy Import** - Load compounds from CSV or paste SMILES directly
- 🎨 **Beautiful Images** - Generate high-quality 2D chemical structure images
- 📊 **Excel Export** - Create Excel files with embedded structure images
- 🖼️ **PNG Export** - Save individual structure images
- 🖥️ **Desktop App** - User-friendly GUI (Windows, macOS, Linux)
- ⚡ **CLI Support** - Command-line interface for automation

## 📸 Screenshots

| Desktop App | Structure Preview |
|------------|------------------|
| ![GUI](https://via.placeholder.com/400x300?text=Chemical+Visualizer+GUI) | ![Preview](chemical_images/compound_1.png) |

## 🚀 Quick Start

### Install

```bash
# Clone the repository
git clone https://github.com/MikeOutlook/Chemical-Structures-Visualizer.git
cd Chemical-Structures-Visualizer

# Install dependencies
pip install -r requirements.txt
```

### Run Desktop App

```bash
python main.py
```

### Run CLI

```bash
python -m chemical_visualizer.cli chemical_structures_data.csv
```

## 📖 Usage

### Desktop App

1. Click **Import CSV** to load your SMILES data
2. Or click **Input SMILES** to paste molecular formulas
3. Click on any compound in the list to preview its structure
4. Export to **Excel** or **PNG**

### Command Line

```bash
# Basic usage
chemviz input.csv

# Custom output
chemviz input.csv -o output.xlsx -i images/
```

## 📁 Project Structure

```
Chemical-Structures-Visualizer/
├── main.py                      # Desktop app entry point
├── chemical_visualizer/       # Core Python package
│   ├── core.py                 # Processing logic
│   └── cli.py                 # Command-line interface
├── gui/                       # GUI module
│   └── app.py                 # CustomTkinter app
├── chemical_structures_data.csv # Sample data (156 compounds)
├── chemical_images/            # Generated images
└── requirements.txt         # Dependencies
```

## 📋 Data Format

### Input CSV

```csv
Index,SMILES
1,CN(Cc1ccccc1[N+](=O)[O-])Cc1cc(=O)oc2cc(O)ccc12
2,O=C(C=Cc1cc(Br)ccc1OC(F)F)Nc1ccc2c(c1)OCO2
```

### SMILES Examples

| Compound | SMILES | Description |
|----------|-------|------------|
| Nitro compound | `CN(Cc1ccccc1[N+](=O)[O-])Cc1cc(=O)oc2cc(O)ccc12` | Benzene with nitro group |
| Brominated | `O=C(C=Cc1cc(Br)ccc1OC(F)F)Nc1ccc2c(c1)OCO2` | Aromatic with Br and F |

## 🛠️ Technology Stack

- **Python 3.8+** - Programming language
- **RDKit** - Cheminformatics library
- **CustomTkinter** - Modern GUI framework
- **Pandas** - Data processing
- **OpenPyXL** - Excel handling

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [RDKit](https://www.rdkit.org/) - Open source cheminformatics
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Beautiful Tkinter widgets

---

<p align="center">
  Made with ❤️ for chemistry enthusiasts
</p>