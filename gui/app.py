# -*- coding: utf-8 -*-
"""
GUI 主窗口模块
"""
import customtkinter as ctk
from tkinter import PanedWindow
from tkinter import filedialog, messagebox
import os
import sys

from chemical_visualizer.core import CompoundProcessor, create_excel_with_images


class ChemicalVisualizerGUI(ctk.CTk):
    """化学结构可视化工具主窗口"""

    def __init__(self):
        super().__init__()

        # 配置窗口
        self.title("Chemical Structure Visualizer")
        self.geometry("900x700")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        # 数据
        self.processor = CompoundProcessor()
        self.temp_image_dir = None

        # 创建界面
        self.create_widgets()

        # 设置关闭行为
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # 创建临时目录
        self.create_temp_dir()

    def create_temp_dir(self):
        """创建临时图像目录"""
        import tempfile
        self.temp_image_dir = tempfile.mkdtemp(prefix="chem_")

    def create_widgets(self):
        """创建所有界面组件"""
        # 顶部工具栏
        self.toolbar = ctk.CTkFrame(self, fg_color="transparent")
        self.toolbar.pack(fill="x", padx=10, pady=10)

        # 导入按钮
        self.btn_import = ctk.CTkButton(
            self.toolbar,
            text="Import CSV",
            command=self.import_csv,
            width=120
        )
        self.btn_import.pack(side="left", padx=5)

        # 输入SMILES按钮
        self.btn_input = ctk.CTkButton(
            self.toolbar,
            text="Input SMILES",
            command=self.input_smiles,
            width=120
        )
        self.btn_input.pack(side="left", padx=5)

        # 清除按钮
        self.btn_clear = ctk.CTkButton(
            self.toolbar,
            text="Clear List",
            command=self.clear_list,
            width=120
        )
        self.btn_clear.pack(side="left", padx=5)

        # 分隔
        ctk.CTkLabel(self.toolbar, text="").pack(side="left", expand=True, fill="x")

        # 导出按钮
        self.btn_export_excel = ctk.CTkButton(
            self.toolbar,
            text="Export Excel",
            command=self.export_excel,
            fg_color="#217346",
            hover_color="#1e5e3a",
            width=120
        )
        self.btn_export_excel.pack(side="right", padx=5)

        self.btn_export_png = ctk.CTkButton(
            self.toolbar,
            text="Export PNG",
            command=self.export_png,
            width=120
        )
        self.btn_export_png.pack(side="right", padx=5)

        # 主内容区 - 使用PanedWindow分割
        self.main_paned = PanedWindow(self, orient="horizontal")
        self.main_paned.pack(fill="both", expand=True, padx=10, pady=5)

        # 左侧化合物列表
        self.create_list_panel()

        # 右侧预览区
        self.create_preview_panel()

        # 底部状态栏
        self.create_status_bar()

    def create_list_panel(self):
        """创建化合物列表面板"""
        self.list_frame = ctk.CTkFrame(self.main_paned)
        self.main_paned.add(self.list_frame, weight=3)

        # 标题
        ctk.CTkLabel(
            self.list_frame,
            text="Compound List",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=5)

        # 表头
        header_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10)

        ctk.CTkLabel(header_frame, text="#", width=40).pack(side="left")
        ctk.CTkLabel(header_frame, text="SMILES", width=200).pack(side="left", expand=True)
        ctk.CTkLabel(header_frame, text="Status", width=60).pack(side="right", padx=5)

        # 列表框（使用ScrollableFrame）
        self.list_scrollable = ctk.CTkScrollableFrame(
            self.list_frame,
            label_text=""
        )
        self.list_scrollable.pack(fill="both", expand=True, padx=10, pady=5)

    def create_preview_panel(self):
        """创建预览面板"""
        self.preview_frame = ctk.CTkFrame(self.main_paned)
        self.main_paned.add(self.preview_frame, weight=2)

        # 标题
        ctk.CTkLabel(
            self.preview_frame,
            text="Structure Preview",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=5)

        # 预览标签（用于显示图像）
        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="Select a compound to view structure",
            font=ctk.CTkFont(size=12)
        )
        self.preview_label.pack(fill="both", expand=True, padx=10, pady=10)

        # 化合物信息
        self.info_label = ctk.CTkLabel(
            self.preview_frame,
            text="",
            font=ctk.CTkFont(size=10)
        )
        self.info_label.pack(pady=5)

    def create_status_bar(self):
        """创建状态栏"""
        self.status_frame = ctk.CTkFrame(self, height=30)
        self.status_frame.pack(fill="x", padx=10, pady=5)

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready",
            anchor="w"
        )
        self.status_label.pack(side="left", padx=10)

        self.progress_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            anchor="e"
        )
        self.progress_label.pack(side="right", padx=10)

    def update_list(self):
        """更新化合物列表显示"""
        # 清空现有项
        for widget in self.list_scrollable.winfo_children():
            widget.destroy()

        # 重新添加项
        for compound in self.processor.compounds:
            self.add_list_item(compound)

        # 更新进度
        self.update_progress()

    def add_list_item(self, compound):
        """添加列表项"""
        item_frame = ctk.CTkFrame(self.list_scrollable, fg_color="transparent")
        item_frame.pack(fill="x", pady=2)

        # 索引
        ctk.CTkLabel(item_frame, text=str(compound['index']), width=40).pack(side="left")

        # SMILES（截断显示）
        smiles = compound['smiles']
        if len(smiles) > 30:
            smiles = smiles[:30] + "..."
        ctk.CTkLabel(item_frame, text=smiles, width=200).pack(side="left", expand=True, fill="x")

        # 状态
        status = compound['status']
        if status == 'success':
            status_text = "OK"
            color = "#28a745"
        elif status == 'error':
            status_text = "Error"
            color = "#dc3545"
        else:
            status_text = "Pending"
            color = "#ffc107"

        status_label = ctk.CTkLabel(
            item_frame,
            text=status_text,
            text_color=color,
            width=60
        )
        status_label.pack(side="right", padx=5)

        # 绑定点击事件
        item_frame.bind("<Button-1>", lambda e, c=compound: self.on_select_compound(c))

    def on_select_compound(self, compound):
        """选择化合物时更新预览"""
        smiles = compound['smiles']
        status = compound['status']

        if status == 'success' and compound['image_path']:
            # 显示图像
            from PIL import Image, ImageTk
            img = Image.open(compound['image_path'])
            img = img.resize((350, 250))
            photo = ImageTk.PhotoImage(img)
            self.preview_label.configure(image=photo, text="")
            self.preview_label.image = photo  # 保持引用
        elif status == 'error':
            self.preview_label.configure(image=None, text="Error: " + compound.get('error', 'Invalid SMILES'))
        else:
            # 实时生成预览
            img = self.processor.generate_preview_image(smiles, size=(350, 250))
            if img:
                from PIL import Image, ImageTk
                photo = ImageTk.PhotoImage(img)
                self.preview_label.configure(image=photo, text="")
                self.preview_label.image = photo
            else:
                self.preview_label.configure(image=None, text="Invalid SMILES")

        # 更新信息
        self.info_label.configure(text="#{}: {}...".format(compound['index'], compound['smiles'][:50]))

    def update_progress(self):
        """更新进度显示"""
        total = len(self.processor.compounds)
        if total == 0:
            self.progress_label.configure(text="")
            return

        success = sum(1 for c in self.processor.compounds if c['status'] == 'success')
        self.progress_label.configure(text="Processed: {}/{}".format(success, total))

    def set_status(self, text):
        """设置状态栏文本"""
        self.status_label.configure(text=text)
        self.update()

    def import_csv(self):
        """导入CSV文件"""
        filepath = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not filepath:
            return

        try:
            count = self.processor.load_csv(filepath)
            self.set_status("Imported {} compounds".format(count))
            self.update_list()
        except Exception as e:
            messagebox.showerror("Error", "Import failed: " + str(e))

    def input_smiles(self):
        """输入SMILES对话框"""
        # 创建对话框
        dialog = ctk.CTkToplevel(self)
        dialog.title("Input SMILES")
        dialog.geometry("500x300")
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Enter SMILES (one per line):").pack(pady=10)

        textbox = ctk.CTkTextbox(dialog, width=450, height=200)
        textbox.pack(pady=10, padx=10)

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=10)

        def add_compounds():
            content = textbox.get("1.0", "end").strip()
            if not content:
                messagebox.showwarning("Warning", "Please enter SMILES")
                return

            lines = content.split('\n')
            added = 0
            for line in lines:
                line = line.strip()
                if line:
                    if self.processor.add_smiles(line):
                        added += 1

            dialog.destroy()
            self.set_status("Added {} compounds".format(added))
            self.update_list()

        ctk.CTkButton(btn_frame, text="Add", command=add_compounds).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)

    def clear_list(self):
        """清除列表"""
        self.processor.clear()
        self.update_list()
        self.preview_label.configure(image=None, text="Select a compound to view structure")
        self.info_label.configure(text="")
        self.set_status("List cleared")

    def export_excel(self):
        """导出Excel"""
        if len(self.processor.compounds) == 0:
            messagebox.showwarning("Warning", "No compounds to export")
            return

        # 检查是否有成功处理的
        success = [c for c in self.processor.compounds if c['status'] == 'success']
        if not success:
            messagebox.showwarning("Warning", "No successfully processed compounds")
            return

        filepath = filedialog.asksaveasfilename(
            title="Save Excel File",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile="chemical_structures_with_images.xlsx"
        )

        if not filepath:
            return

        try:
            create_excel_with_images(self.processor, filepath, self.temp_image_dir)
            self.set_status("Exported Excel: " + filepath)
            messagebox.showinfo("Success", "Excel file saved to:\n" + filepath)
        except Exception as e:
            messagebox.showerror("Error", "Export failed: " + str(e))

    def export_png(self):
        """导出PNG图像"""
        if len(self.processor.compounds) == 0:
            messagebox.showwarning("Warning", "No compounds to export")
            return

        success = [c for c in self.processor.compounds if c['status'] == 'success']
        if not success:
            messagebox.showwarning("Warning", "No successfully processed compounds")
            return

        dirpath = filedialog.askdirectory(title="Select Output Directory")

        if not dirpath:
            return

        try:
            import shutil
            for compound in success:
                if compound['image_path']:
                    shutil.copy2(compound['image_path'], dirpath)

            self.set_status("Exported {} PNGs to: {}".format(len(success), dirpath))
            messagebox.showinfo("Success", "PNG files saved to:\n" + dirpath)
        except Exception as e:
            messagebox.showerror("Error", "Export failed: " + str(e))

    def on_close(self):
        """关闭时的清理"""
        import shutil
        if self.temp_image_dir and os.path.exists(self.temp_image_dir):
            shutil.rmtree(self.temp_image_dir)
        self.destroy()


def main():
    """主入口"""
    app = ChemicalVisualizerGUI()
    app.mainloop()


if __name__ == '__main__':
    main()