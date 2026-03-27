# Chemical Structures Visualizer

Python tool for converting SMILES molecular formulas into beautiful chemical structure images

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![RDKit](https://img.shields.io/badge/RDKit-Latest-orange)

## Overview

This project reads compound SMILES (Simplified Molecular Input Line Entry System) from CSV files and automatically generates 2D chemical structure images using the RDKit cheminformatics library, exporting them to an Excel file with embedded structure images.

## Features

- Read SMILES molecular formulas from CSV
- Generate high-quality 2D chemical structure images
- Batch insert images into Excel (right of SMILES column)
- Support for 156+ compounds
- Export to editable Excel for further analysis

## Quick Start

### Requirements

- Python 3.8+
- Windows / macOS / Linux

### Install Dependencies

```bash
# Recommended: use rdkit-pypi for better compatibility
pip install rdkit-pypi pandas openpyxl Pillow
# or use requirements.txt
pip install -r requirements.txt
```

### Run the Script

```bash
python generate_chemical_images.py
```

The script will automatically:
1. Read `chemical_structures_data.csv`
2. Generate chemical structure images for each SMILES
3. Create Excel file with embedded images

### Output Files

- `chemical_structures_with_images.xlsx` - Excel file with images
- `chemical_images/` - Individual structure images (PNG)

## Data Format

### Input CSV

```csv
Index,SMILES
1,CN(Cc1ccccc1[N+](=O)[O-])Cc1cc(=O)oc2cc(O)ccc12
2,O=C(C=Cc1cc(Br)ccc1OC(F)F)Nc1ccc2c(c1)OCO2
```

### Output Excel

| Index | SMILES | Structure |
|-------|--------|-----------|
| 1 | CN(Cc1ccccc1[N+](=O)[O-])... | ![](images/compound_1.png) |
| 2 | O=C(C=Cc1cc(Br)ccc1OC(F)F)... | ![](images/compound_2.png) |

## Sample Images

Here are some generated chemical structure images:

| Compound | Description |
|---------|-------------|
| ![](chemical_images/compound_1.png) | Compound with nitro and benzene ring |
| ![](chemical_images/compound_2.png) | Aromatic compound with bromine and fluorine |
| ![](chemical_images/compound_3.png) | Compound with thiazole ring |

## Tech Stack

- **Python 3.11** - Programming language
- **RDKit** - Cheminformatics library
- **Pandas** - Data processing
- **OpenPyXL** - Excel file handling
- **Pillow (PIL)** - Image generation

## Project Structure

```
Third_work/
├── chemical_structures_data.csv   # Original SMILES data
├── generate_chemical_images.py     # Main script
├── chemical_structures_with_images.xlsx  # Output Excel file
├── chemical_images/                 # Generated images folder
│   ├── compound_1.png
│   ├── compound_2.png
│   └── ...
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore configuration
├── .github/workflows/ci.yml         # CI/CD automation
└── README.md                         # Project documentation
```

## CI/CD Automation

This project uses GitHub Actions for automated CI/CD:

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install RDKit
        run: |
          pip install --upgrade pip
          pip install rdkit-pypi
      - name: Install other dependencies
        run: pip install pandas openpyxl Pillow
      - name: Generate chemical images
        run: python generate_chemical_images.py
      - name: Verify output
        run: |
          test -f chemical_structures_with_images.xlsx
          test -d chemical_images
          echo "Files generated successfully!"
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: chemical-structures
          path: |
            chemical_structures_with_images.xlsx
            chemical_images/
```

On every `push` or `pull_request`:
1. Checkout code
2. Set up Python 3.11
3. Install dependencies
4. Run image generation script
5. Verify output files
6. Upload Excel and images as artifacts

## Extended Usage

### Custom Image Size

Modify the `size` parameter in the script:

```python
img = Draw.MolToImage(mol, size=(500, 300))  # Larger, clearer images
```

### Add More SMILES

Add new rows to `chemical_structures_data.csv`:

```csv
Index,SMILES
157,CCOc1ccc(NC(=O)c2ccco2)cc1
```

Re-run the script to generate new images.

## License

MIT License - Free to use, modify, and distribute

## Contributing

Feel free to submit Issues and Pull Requests!

---

Star this project if you found it helpful!
