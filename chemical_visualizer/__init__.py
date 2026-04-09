"""Chemical Structure Visualizer package."""

from chemical_visualizer.core import CompoundProcessor, CompoundRecord, create_excel_with_images

# 版本号供 CLI 和打包流程统一读取，避免多个地方各写一份。
__version__ = "3.0.0"
# 这些对象是包最常用的公开接口，方便外部直接从根包导入。
__all__ = ["CompoundProcessor", "CompoundRecord", "create_excel_with_images"]
