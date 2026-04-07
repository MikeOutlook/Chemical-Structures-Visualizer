# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import os
import tempfile
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Draw
try:
    from typing import Tuple, List, Optional
except ImportError:
    from typing import Tuple, List, Optional

try:
    unicode = unicode
except NameError:
    unicode = str


class CompoundProcessor:
    """化合物处理器 - 处理SMILES并生成结构图像"""

    def __init__(self, image_size=(300, 200)):
        self.image_size = image_size
        self.compounds = []

    def load_csv(self, filepath):
        """从CSV加载化合物数据"""
        df = pd.read_csv(filepath)
        self.compounds = []
        for idx, row in df.iterrows():
            self.compounds.append({
                'index': row.get('Index', idx + 1),
                'smiles': row['SMILES'],
                'status': 'pending',
                'image_path': None,
                'error': None
            })
        return len(self.compounds)

    def add_smiles(self, smiles, index=None):
        """添加单个SMILES"""
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return False
        idx = index or (len(self.compounds) + 1)
        self.compounds.append({
            'index': idx,
            'smiles': smiles,
            'status': 'pending',
            'image_path': None,
            'error': None
        })
        return True

    def process_compound(self, compound, output_dir):
        """处理单个化合物"""
        smiles = compound['smiles']
        mol = Chem.MolFromSmiles(smiles)

        if mol is None:
            compound['status'] = 'error'
            compound['error'] = 'Invalid SMILES'
            return False

        # 生成图像
        img = Draw.MolToImage(mol, size=self.image_size)
        img_filename = "compound_{}.png".format(compound['index'])
        img_path = os.path.join(output_dir, img_filename)
        img.save(img_path)

        compound['status'] = 'success'
        compound['image_path'] = img_path
        return True

    def process_all(self, output_dir, progress_callback=None):
        """处理所有化合物，返回 (成功数, 失败数)"""
        os.makedirs(output_dir, exist_ok=True)

        success_count = 0
        fail_count = 0

        for i, compound in enumerate(self.compounds):
            if self.process_compound(compound, output_dir):
                success_count += 1
            else:
                fail_count += 1

            if progress_callback:
                progress_callback(i + 1, len(self.compounds))

        return success_count, fail_count

    def clear(self):
        """清空所有化合物"""
        self.compounds = []

    def get_compound(self, index):
        """获取指定索引的化合物"""
        for c in self.compounds:
            if c['index'] == index:
                return c
        return None

    def generate_preview_image(self, smiles, size=(400, 300)):
        """生成预览图像（PIL Image对象，用于GUI显示）"""
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        return Draw.MolToImage(mol, size=size)


def create_excel_with_images(processor, output_path, image_dir):
    """创建包含嵌入式图像的Excel文件"""
    import openpyxl
    from openpyxl.drawing.image import Image

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Chemical Structures'

    # 写入表��
    ws['A1'] = 'Index'
    ws['B1'] = 'SMILES'
    ws['C1'] = 'Structure'

    # 写入数据
    for i, compound in enumerate(processor.compounds):
        row_num = i + 2
        ws.cell(row=row_num, column=1, value=compound['index'])
        ws.cell(row=row_num, column=2, value=compound['smiles'])

        # 添加图像
        if compound['status'] == 'success' and compound['image_path']:
            img = Image(compound['image_path'])
            img.width = 150
            img.height = 100
            ws.add_image(img, 'C{}'.format(row_num))

    # 调整列宽
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 60
    ws.column_dimensions['C'].width = 20

    wb.save(output_path)