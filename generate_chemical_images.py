"""Convenience script for generating sample outputs from the bundled dataset."""

from pathlib import Path

from chemical_visualizer.core import CompoundProcessor, create_excel_with_images


def main():
    csv_path = Path("chemical_structures_data.csv")
    if not csv_path.exists():
        raise SystemExit("Sample CSV not found: {0}".format(csv_path))

    processor = CompoundProcessor()
    count = processor.load_csv(csv_path)

    image_dir = Path("chemical_images")
    excel_path = Path("chemical_structures_with_images.xlsx")

    print("Loaded {0} compounds from {1}".format(count, csv_path))
    success, fail = processor.process_all(image_dir)
    print("Processed: {0} successful, {1} failed".format(success, fail))

    create_excel_with_images(processor, excel_path)
    print("Excel file saved to: {0}".format(excel_path))
    print("Images saved to: {0}".format(image_dir))


if __name__ == "__main__":
    main()
