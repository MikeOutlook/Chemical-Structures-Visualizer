"""Command-line interface for batch structure generation."""

import argparse
from pathlib import Path
import sys

from chemical_visualizer import __version__
from chemical_visualizer.core import CompoundProcessor, create_excel_with_images


def parse_image_size(value):
    """Parse a WxH image size string into an integer tuple."""

    # 允许用户通过命令行传入类似 `300x200` 的尺寸字符串。
    try:
        width_text, height_text = value.lower().split("x", 1)
        width = int(width_text)
        height = int(height_text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "Image size must be in WxH format, for example 300x200"
        ) from exc

    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("Image size values must be positive integers")

    return width, height


def build_parser():
    """Create the argument parser for the CLI."""

    parser = argparse.ArgumentParser(
        description="Generate 2D chemical structure images from SMILES strings."
    )
    parser.add_argument(
        "input",
        nargs="?",
        # 不传时默认回退到当前目录下的示例 CSV。
        help="Input CSV file. Defaults to chemical_structures_data.csv in the current directory.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="chemical_structures_with_images.xlsx",
        help="Output Excel file path.",
    )
    parser.add_argument(
        "-i",
        "--image-dir",
        default="chemical_images",
        help="Output directory for generated PNG files.",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=parse_image_size,
        default=(300, 200),
        help="Image size in WxH format, for example 300x200.",
    )
    parser.add_argument(
        "--version",
        action="version",
        # 复用包内版本号，避免 CLI 和包元数据不一致。
        version="%(prog)s {0}".format(__version__),
    )
    return parser


def main(argv=None):
    """Run the CLI and return a process exit code."""

    parser = build_parser()
    args = parser.parse_args(argv)

    input_path = Path(args.input) if args.input else Path("chemical_structures_data.csv")
    if not input_path.exists():
        print("Error: File not found: {0}".format(input_path), file=sys.stderr)
        return 1

    processor = CompoundProcessor(image_size=args.size)
    try:
        count = processor.load_csv(input_path)
    except Exception as exc:
        # 读取错误统一输出到标准错误，便于脚本环境捕获。
        print("Error: {0}".format(exc), file=sys.stderr)
        return 1

    if count == 0:
        print("Error: Input CSV contained no compounds", file=sys.stderr)
        return 1

    print("Loaded {0} compounds from {1}".format(count, input_path))
    print("Processing compounds...")
    success, fail = processor.process_all(args.image_dir)
    print("Processed: {0} successful, {1} failed".format(success, fail))

    output_path = Path(args.output)
    # 允许用户直接指定一个尚未创建的输出目录。
    output_path.parent.mkdir(parents=True, exist_ok=True)
    create_excel_with_images(processor, output_path)

    print("Excel saved to: {0}".format(output_path))
    print("Images saved to: {0}".format(Path(args.image_dir)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
