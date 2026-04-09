import pytest


# 如果当前环境没有安装 GUI 依赖，就跳过这个导入测试。
pytest.importorskip("customtkinter")

from gui.app import ChemicalVisualizerGUI, main


def test_gui_module_imports():
    # 这里只验证 GUI 入口能被导入，不启动真正的界面主循环。
    assert ChemicalVisualizerGUI.__name__ == "ChemicalVisualizerGUI"
    assert callable(main)
