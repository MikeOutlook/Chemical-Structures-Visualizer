import pytest


pytest.importorskip("customtkinter")

from gui.app import ChemicalVisualizerGUI, main


def test_gui_module_imports():
    assert ChemicalVisualizerGUI.__name__ == "ChemicalVisualizerGUI"
    assert callable(main)
