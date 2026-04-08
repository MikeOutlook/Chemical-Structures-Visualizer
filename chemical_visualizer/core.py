from dataclasses import dataclass
from pathlib import Path
import re
from typing import Callable, List, Optional

import openpyxl
import pandas as pd
from openpyxl.drawing.image import Image as OpenPyXLImage
from openpyxl.styles import Font
from rdkit import Chem
from rdkit.Chem import Draw


ProgressCallback = Callable[[int, int], None]


@dataclass
class CompoundRecord:
    """Represents one compound entry loaded from CSV or manual input."""

    index: object
    smiles: str
    status: str = "pending"
    image_path: Optional[str] = None
    error: Optional[str] = None


class CompoundProcessor:
    """Loads compounds, renders 2D structure images, and tracks results."""

    def __init__(self, image_size=(300, 200)):
        self.image_size = self._normalize_image_size(image_size)
        self.compounds = []  # type: List[CompoundRecord]

    @staticmethod
    def _normalize_image_size(image_size):
        width, height = image_size
        if width <= 0 or height <= 0:
            raise ValueError("Image size must use positive integers")
        return int(width), int(height)

    @staticmethod
    def _build_image_filename(index):
        safe_index = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(index)).strip("_")
        return "compound_{0}.png".format(safe_index or "item")

    def load_csv(self, filepath):
        """Load compounds from a CSV file."""

        dataframe = pd.read_csv(filepath)
        if "SMILES" not in dataframe.columns:
            raise ValueError("CSV must contain a 'SMILES' column")

        has_index_column = "Index" in dataframe.columns
        self.compounds = []

        for row_number, row in dataframe.iterrows():
            smiles = str(row["SMILES"]).strip()
            index = row["Index"] if has_index_column else row_number + 1
            self.compounds.append(CompoundRecord(index=index, smiles=smiles))

        return len(self.compounds)

    def add_smiles(self, smiles, index=None):
        """Add a single SMILES string after validating it with RDKit."""

        normalized_smiles = smiles.strip()
        if not normalized_smiles:
            return False

        molecule = Chem.MolFromSmiles(normalized_smiles)
        if molecule is None:
            return False

        compound_index = index if index is not None else len(self.compounds) + 1
        self.compounds.append(CompoundRecord(index=compound_index, smiles=normalized_smiles))
        return True

    def process_compound(self, compound, output_dir):
        """Render a single compound image and update its processing status."""

        molecule = Chem.MolFromSmiles(compound.smiles)
        if molecule is None:
            compound.status = "error"
            compound.error = "Invalid SMILES"
            compound.image_path = None
            return False

        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)

        image = Draw.MolToImage(molecule, size=self.image_size)
        image_path = output_dir_path / self._build_image_filename(compound.index)
        image.save(image_path)

        compound.status = "success"
        compound.error = None
        compound.image_path = str(image_path)
        return True

    def process_all(self, output_dir, progress_callback=None, only_pending=False):
        """Process all compounds or only those still marked as pending."""

        targets = self.compounds
        if only_pending:
            targets = [compound for compound in self.compounds if compound.status == "pending"]

        success_count = 0
        fail_count = 0
        total = len(targets)

        for current, compound in enumerate(targets, start=1):
            if self.process_compound(compound, output_dir):
                success_count += 1
            else:
                fail_count += 1

            if progress_callback is not None:
                progress_callback(current, total)

        return success_count, fail_count

    def clear(self):
        """Remove all loaded compounds."""

        self.compounds = []

    def get_compound(self, index):
        """Return the compound with the requested index, if present."""

        for compound in self.compounds:
            if compound.index == index:
                return compound
        return None

    def generate_preview_image(self, smiles, size=(400, 300)):
        """Generate a preview image for a SMILES string."""

        width, height = self._normalize_image_size(size)
        molecule = Chem.MolFromSmiles(smiles)
        if molecule is None:
            return None
        return Draw.MolToImage(molecule, size=(width, height))


def create_excel_with_images(processor, output_path, image_dir=None):
    """Create an Excel workbook that embeds generated structure images."""

    del image_dir  # Retained for backward compatibility with existing callers.

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Chemical Structures"
    worksheet.freeze_panes = "A2"

    headers = ("Index", "SMILES", "Structure")
    for column, value in enumerate(headers, start=1):
        cell = worksheet.cell(row=1, column=column, value=value)
        cell.font = Font(bold=True)

    for row_number, compound in enumerate(processor.compounds, start=2):
        worksheet.cell(row=row_number, column=1, value=compound.index)
        worksheet.cell(row=row_number, column=2, value=compound.smiles)

        if compound.status == "success" and compound.image_path and Path(compound.image_path).exists():
            image = OpenPyXLImage(compound.image_path)
            image.width = 150
            image.height = 100
            worksheet.add_image(image, "C{0}".format(row_number))
            worksheet.row_dimensions[row_number].height = 80

    worksheet.column_dimensions["A"].width = 12
    worksheet.column_dimensions["B"].width = 60
    worksheet.column_dimensions["C"].width = 24

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(output_path)
