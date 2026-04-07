# -*- coding: utf-8 -*-
"""命令行接口"""
import argparse
import sys
import os

from chemical_visualizer.core import CompoundProcessor, create_excel_with_images


def main():
    parser = argparse.ArgumentParser(
        description='Chemical Structure Visualizer - Generate chemical structure images from SMILES'
    )
    parser.add_argument('input', nargs='?', help='Input CSV file (optional, can use stdin)')
    parser.add_argument('-o', '--output', default='chemical_structures_with_images.xlsx',
                    help='Output Excel file')
    parser.add_argument('-i', '--image-dir', default='chemical_images',
                    help='Output directory for images')
    parser.add_argument('-s', '--size', type=str, default='300x200',
                    help='Image size (WxH), e.g., 300x200')

    args = parser.parse_args()

    # 解析图像尺寸
    try:
        w, h = map(int, args.size.split('x'))
        image_size = (w, h)
    except:
        image_size = (300, 200)

    # 创建处理器
    processor = CompoundProcessor(image_size=image_size)

    # 加载输入
    if args.input:
        if not os.path.exists(args.input):
            print(f"Error: File not found: {args.input}")
            sys.exit(1)
        count = processor.load_csv(args.input)
        print(f"Loaded {count} compounds from {args.input}")
    else:
        # 尝试加载默认CSV
        default_csv = 'chemical_structures_data.csv'
        if os.path.exists(default_csv):
            count = processor.load_csv(default_csv)
            print(f"Loaded {count} compounds from {default_csv}")
        else:
            print("Error: No input file specified and default CSV not found")
            sys.exit(1)

    # 处理
    print(f"Processing compounds...")
    success, fail = processor.process_all(args.image_dir)
    print(f"Processed: {success} successful, {fail} failed")

    # 导出Excel
    create_excel_with_images(processor, args.output, args.image_dir)
    print(f"Excel saved to: {args.output}")
    print(f"Images saved to: {args.image_dir}")


if __name__ == '__main__':
    main()