from pathlib import Path

import openpyxl
import pytest

from chemical_visualizer.core import CompoundProcessor, create_excel_with_images


def write_csv(path, content):
    path.write_text(content, encoding="utf-8")


def test_load_csv_requires_smiles_column(tmp_path):
    csv_path = tmp_path / "invalid.csv"
    write_csv(csv_path, "Index,Name\n1,Example\n")

    processor = CompoundProcessor()
    with pytest.raises(ValueError, match="SMILES"):
        processor.load_csv(csv_path)


def test_add_smiles_rejects_invalid_input():
    processor = CompoundProcessor()

    assert processor.add_smiles("CCO") is True
    assert processor.add_smiles("not-a-smiles") is False
    assert processor.add_smiles("   ") is False
    assert len(processor.compounds) == 1
    assert processor.compounds[0].smiles == "CCO"


def test_process_all_creates_images_and_excel(tmp_path):
    csv_path = tmp_path / "compounds.csv"
    write_csv(
        csv_path,
        "Index,SMILES\n1,CCO\n2,invalid_smiles\n",
    )

    processor = CompoundProcessor(image_size=(220, 160))
    count = processor.load_csv(csv_path)
    assert count == 2

    events = []
    image_dir = tmp_path / "images"
    success, fail = processor.process_all(
        image_dir,
        progress_callback=lambda current, total: events.append((current, total)),
    )

    assert success == 1
    assert fail == 1
    assert events == [(1, 2), (2, 2)]

    first, second = processor.compounds
    assert first.status == "success"
    assert first.image_path is not None
    assert Path(first.image_path).exists()
    assert second.status == "error"
    assert second.error == "Invalid SMILES"

    excel_path = tmp_path / "output.xlsx"
    create_excel_with_images(processor, excel_path)

    workbook = openpyxl.load_workbook(excel_path)
    worksheet = workbook.active
    assert worksheet.title == "Chemical Structures"
    assert worksheet["A1"].value == "Index"
    assert worksheet["B1"].value == "SMILES"
    assert worksheet["C1"].value == "Structure"
    assert worksheet["A2"].value == 1
    assert worksheet["B2"].value == "CCO"


def test_process_all_only_pending_skips_processed_rows(tmp_path):
    processor = CompoundProcessor()
    processor.add_smiles("CCO", index=1)
    processor.add_smiles("CCN", index=2)

    image_dir = tmp_path / "images"
    success, fail = processor.process_all(image_dir, only_pending=True)
    assert (success, fail) == (2, 0)

    first_image = processor.compounds[0].image_path
    second_image = processor.compounds[1].image_path

    success, fail = processor.process_all(image_dir, only_pending=True)
    assert (success, fail) == (0, 0)
    assert processor.compounds[0].image_path == first_image
    assert processor.compounds[1].image_path == second_image
