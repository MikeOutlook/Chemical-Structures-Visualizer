# -*- coding: utf-8 -*-
"""
Chemical Structure Visualizer - 桌面应用入口
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.app import main

if __name__ == '__main__':
    main()