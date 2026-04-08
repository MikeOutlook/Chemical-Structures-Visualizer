# Chemical Structures Visualizer

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
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python 3.10+">
  </a>
  <a href="https://www.rdkit.org/">
    <img src="https://img.shields.io/badge/RDKit-powered-orange?logo=python" alt="RDKit">
  </a>
</p>

Generate 2D chemical structure images from SMILES strings.

This project provides:

- a command-line workflow for batch processing CSV files
- a desktop GUI for importing and previewing compounds
- PNG image export and Excel workbook generation with embedded structure images

## Features

- Convert SMILES strings into 2D molecule images with RDKit
- Batch-process CSV input from the command line
- Export individual PNG files for each successfully parsed compound
- Generate `.xlsx` files with molecule images embedded next to source data
- Preview structures interactively in a CustomTkinter desktop application
- Includes a sample dataset with 156 compounds

## Requirements

- Python 3.10 or newer
- `pip`
- A platform supported by the listed dependencies

## Installation

The recommended installation method is an editable local install so the `chemviz` command is available.

```bash
git clone https://github.com/MikeOutlook/Chemical-Structures-Visualizer.git
cd Chemical-Structures-Visualizer

python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Install the package:

```bash
python -m pip install --upgrade pip
pip install -e .
```

If you only want the raw dependencies without installing the package entry point, you can use:

```bash
pip install -r requirements.txt
```

## Quick Start

### CLI

The CLI is the most complete workflow for repeatable batch processing.

```bash
chemviz chemical_structures_data.csv
```

This command will:

- read compounds from the CSV file
- generate PNG files in `chemical_images/`
- create `chemical_structures_with_images.xlsx`

You can also customize the output paths and image size:

```bash
chemviz chemical_structures_data.csv -o results.xlsx -i output_images -s 400x300
```

If you prefer not to install the entry point, run the module directly:

```bash
python -m chemical_visualizer.cli chemical_structures_data.csv
```

### Desktop App

Launch the GUI with:

```bash
python main.py
```

Current GUI workflow:

1. Import a CSV file or paste SMILES strings manually.
2. Browse the loaded compounds in the list view.
3. Click a compound to preview its 2D structure.

For automated runs and batch export, prefer the CLI.

## Input Format

CSV input must contain a `SMILES` column. An `Index` column is optional.

Example:

```csv
Index,SMILES
1,CN(Cc1ccccc1[N+](=O)[O-])Cc1cc(=O)oc2cc(O)ccc12
2,O=C(C=Cc1cc(Br)ccc1OC(F)F)Nc1ccc2c(c1)OCO2
```

Notes:

- `SMILES` is required.
- `Index` is used for file naming and Excel output when present.
- Invalid SMILES strings are reported during processing and skipped for image generation.

## Output

By default, the CLI creates:

- `chemical_images/` with one PNG per successfully parsed compound
- `chemical_structures_with_images.xlsx` with the original data and embedded structure images

Generated image files follow the naming pattern `compound_<index>.png`.

## Project Structure

```text
Chemical-Structures-Visualizer/
├── chemical_visualizer/
│   ├── __init__.py
│   ├── cli.py                  # Command-line entry point
│   └── core.py                 # CSV loading, image generation, Excel export
├── gui/
│   ├── __init__.py
│   └── app.py                  # CustomTkinter desktop GUI
├── chemical_structures_data.csv
├── generate_chemical_images.py # Standalone batch script
├── main.py                     # GUI launcher
├── pyproject.toml              # Package metadata and console script
├── requirements.txt
└── requirements-dev.txt
```

## Development

Install the development dependencies with:

```bash
pip install -e .[dev]
```

Run the test suite with:

```bash
pytest
```

Build a distributable package with:

```bash
python -m build
```

PyInstaller spec files are included in the repository for desktop packaging experiments.
See [CONTRIBUTING.md](CONTRIBUTING.md) for the local development workflow.

## Technology Stack

- Python
- RDKit
- Pandas
- Pillow
- OpenPyXL
- CustomTkinter

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make the change with a focused commit history.
4. Open a pull request with a clear description of the problem and solution.

If you are changing behavior, update the relevant documentation and examples in this README.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- [RDKit](https://www.rdkit.org/) for cheminformatics tooling
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the desktop UI framework
