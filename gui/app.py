"""Desktop GUI for the Chemical Structures Visualizer."""

from pathlib import Path
import shutil
import tempfile
from tkinter import PanedWindow, filedialog, messagebox

import customtkinter as ctk

from chemical_visualizer.core import CompoundProcessor, create_excel_with_images


class ChemicalVisualizerGUI(ctk.CTk):
    """Simple desktop interface for loading, previewing, and exporting molecules."""

    def __init__(self):
        super().__init__()

        self.title("Chemical Structure Visualizer")
        self.geometry("900x700")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.processor = CompoundProcessor()
        self.temp_image_dir = None

        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.create_temp_dir()

    def create_temp_dir(self):
        """Create a temporary directory used for generated GUI images."""

        self.temp_image_dir = Path(tempfile.mkdtemp(prefix="chem_"))

    def reset_temp_dir(self):
        """Reset the temporary image directory to remove stale images."""

        if self.temp_image_dir and self.temp_image_dir.exists():
            shutil.rmtree(self.temp_image_dir)
        self.create_temp_dir()

    def create_widgets(self):
        """Create the application layout."""

        self.toolbar = ctk.CTkFrame(self, fg_color="transparent")
        self.toolbar.pack(fill="x", padx=10, pady=10)

        self.btn_import = ctk.CTkButton(
            self.toolbar,
            text="Import CSV",
            command=self.import_csv,
            width=120,
        )
        self.btn_import.pack(side="left", padx=5)

        self.btn_input = ctk.CTkButton(
            self.toolbar,
            text="Input SMILES",
            command=self.input_smiles,
            width=120,
        )
        self.btn_input.pack(side="left", padx=5)

        self.btn_clear = ctk.CTkButton(
            self.toolbar,
            text="Clear List",
            command=self.clear_list,
            width=120,
        )
        self.btn_clear.pack(side="left", padx=5)

        ctk.CTkLabel(self.toolbar, text="").pack(side="left", expand=True, fill="x")

        self.btn_export_excel = ctk.CTkButton(
            self.toolbar,
            text="Export Excel",
            command=self.export_excel,
            fg_color="#217346",
            hover_color="#1e5e3a",
            width=120,
        )
        self.btn_export_excel.pack(side="right", padx=5)

        self.btn_export_png = ctk.CTkButton(
            self.toolbar,
            text="Export PNG",
            command=self.export_png,
            width=120,
        )
        self.btn_export_png.pack(side="right", padx=5)

        self.main_paned = PanedWindow(self, orient="horizontal")
        self.main_paned.pack(fill="both", expand=True, padx=10, pady=5)

        self.create_list_panel()
        self.create_preview_panel()
        self.create_status_bar()

    def create_list_panel(self):
        """Create the compound list panel."""

        self.list_frame = ctk.CTkFrame(self.main_paned)
        self.main_paned.add(self.list_frame, weight=3)

        ctk.CTkLabel(
            self.list_frame,
            text="Compound List",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(pady=5)

        header_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10)

        ctk.CTkLabel(header_frame, text="#", width=40).pack(side="left")
        ctk.CTkLabel(header_frame, text="SMILES", width=200).pack(side="left", expand=True)
        ctk.CTkLabel(header_frame, text="Status", width=60).pack(side="right", padx=5)

        self.list_scrollable = ctk.CTkScrollableFrame(self.list_frame, label_text="")
        self.list_scrollable.pack(fill="both", expand=True, padx=10, pady=5)

    def create_preview_panel(self):
        """Create the structure preview panel."""

        self.preview_frame = ctk.CTkFrame(self.main_paned)
        self.main_paned.add(self.preview_frame, weight=2)

        ctk.CTkLabel(
            self.preview_frame,
            text="Structure Preview",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(pady=5)

        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="Select a compound to view structure",
            font=ctk.CTkFont(size=12),
        )
        self.preview_label.pack(fill="both", expand=True, padx=10, pady=10)

        self.info_label = ctk.CTkLabel(
            self.preview_frame,
            text="",
            font=ctk.CTkFont(size=10),
        )
        self.info_label.pack(pady=5)

    def create_status_bar(self):
        """Create the bottom status bar."""

        self.status_frame = ctk.CTkFrame(self, height=30)
        self.status_frame.pack(fill="x", padx=10, pady=5)

        self.status_label = ctk.CTkLabel(self.status_frame, text="Ready", anchor="w")
        self.status_label.pack(side="left", padx=10)

        self.progress_label = ctk.CTkLabel(self.status_frame, text="", anchor="e")
        self.progress_label.pack(side="right", padx=10)

    def update_list(self):
        """Refresh the compound list UI."""

        for widget in self.list_scrollable.winfo_children():
            widget.destroy()

        for compound in self.processor.compounds:
            self.add_list_item(compound)

        self.update_progress()

    def add_list_item(self, compound):
        """Render one compound row in the list."""

        item_frame = ctk.CTkFrame(self.list_scrollable, fg_color="transparent")
        item_frame.pack(fill="x", pady=2)

        smiles_preview = compound.smiles
        if len(smiles_preview) > 30:
            smiles_preview = smiles_preview[:30] + "..."

        if compound.status == "success":
            status_text = "OK"
            color = "#28a745"
        elif compound.status == "error":
            status_text = "Error"
            color = "#dc3545"
        else:
            status_text = "Pending"
            color = "#ffc107"

        index_label = ctk.CTkLabel(item_frame, text=str(compound.index), width=40)
        index_label.pack(side="left")

        smiles_label = ctk.CTkLabel(item_frame, text=smiles_preview, width=200)
        smiles_label.pack(side="left", expand=True, fill="x")

        status_label = ctk.CTkLabel(
            item_frame,
            text=status_text,
            text_color=color,
            width=60,
        )
        status_label.pack(side="right", padx=5)

        for widget in (item_frame, index_label, smiles_label, status_label):
            widget.bind("<Button-1>", lambda _event, c=compound: self.on_select_compound(c))

    def on_select_compound(self, compound):
        """Update the preview panel for the selected compound."""

        from PIL import Image, ImageTk

        if compound.status == "success" and compound.image_path and Path(compound.image_path).exists():
            preview_image = Image.open(compound.image_path)
            preview_image.thumbnail((350, 250))
            photo = ImageTk.PhotoImage(preview_image)
            self.preview_label.configure(image=photo, text="")
            self.preview_label.image = photo
        elif compound.status == "error":
            self.preview_label.configure(image=None, text="Error: {0}".format(compound.error or "Invalid SMILES"))
            self.preview_label.image = None
        else:
            preview_image = self.processor.generate_preview_image(compound.smiles, size=(350, 250))
            if preview_image is None:
                self.preview_label.configure(image=None, text="Invalid SMILES")
                self.preview_label.image = None
            else:
                photo = ImageTk.PhotoImage(preview_image)
                self.preview_label.configure(image=photo, text="")
                self.preview_label.image = photo

        self.info_label.configure(text="#{0}: {1}".format(compound.index, compound.smiles[:80]))

    def update_processing_progress(self, current, total):
        """Display progress while pending compounds are rendered."""

        self.progress_label.configure(text="Processing: {0}/{1}".format(current, total))
        self.update_idletasks()

    def update_progress(self):
        """Display the number of successfully processed compounds."""

        total = len(self.processor.compounds)
        if total == 0:
            self.progress_label.configure(text="")
            return

        success = sum(1 for compound in self.processor.compounds if compound.status == "success")
        self.progress_label.configure(text="Processed: {0}/{1}".format(success, total))

    def set_status(self, text):
        """Set the status bar text."""

        self.status_label.configure(text=text)
        self.update_idletasks()

    def process_pending_compounds(self):
        """Render all compounds that have not been processed yet."""

        pending_count = sum(1 for compound in self.processor.compounds if compound.status == "pending")
        if pending_count == 0:
            self.update_list()
            return 0, 0

        self.set_status("Processing {0} compounds...".format(pending_count))
        success, fail = self.processor.process_all(
            self.temp_image_dir,
            progress_callback=self.update_processing_progress,
            only_pending=True,
        )
        self.update_list()
        self.set_status("Processed {0} compounds, {1} failed".format(success, fail))
        return success, fail

    def import_csv(self):
        """Import compounds from a CSV file and process them."""

        filepath = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not filepath:
            return

        try:
            self.reset_temp_dir()
            count = self.processor.load_csv(filepath)
            self.update_list()
            self.process_pending_compounds()
            self.set_status("Imported {0} compounds from {1}".format(count, Path(filepath).name))
        except Exception as exc:
            messagebox.showerror("Error", "Import failed: {0}".format(exc))

    def input_smiles(self):
        """Open a dialog for entering SMILES strings manually."""

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

            added = 0
            skipped = 0
            for line in content.splitlines():
                if self.processor.add_smiles(line):
                    added += 1
                elif line.strip():
                    skipped += 1

            dialog.destroy()
            self.update_list()
            self.process_pending_compounds()
            self.set_status("Added {0} compounds, skipped {1} invalid entries".format(added, skipped))

        ctk.CTkButton(btn_frame, text="Add", command=add_compounds).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)

    def clear_list(self):
        """Clear all loaded compounds and reset the preview."""

        self.processor.clear()
        self.reset_temp_dir()
        self.update_list()
        self.preview_label.configure(image=None, text="Select a compound to view structure")
        self.preview_label.image = None
        self.info_label.configure(text="")
        self.set_status("List cleared")

    def export_excel(self):
        """Export the current compounds to an Excel workbook."""

        if not self.processor.compounds:
            messagebox.showwarning("Warning", "No compounds to export")
            return

        self.process_pending_compounds()
        success = [compound for compound in self.processor.compounds if compound.status == "success"]
        if not success:
            messagebox.showwarning("Warning", "No successfully processed compounds")
            return

        filepath = filedialog.asksaveasfilename(
            title="Save Excel File",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile="chemical_structures_with_images.xlsx",
        )
        if not filepath:
            return

        try:
            create_excel_with_images(self.processor, filepath)
            self.set_status("Exported Excel: {0}".format(filepath))
            messagebox.showinfo("Success", "Excel file saved to:\n{0}".format(filepath))
        except Exception as exc:
            messagebox.showerror("Error", "Export failed: {0}".format(exc))

    def export_png(self):
        """Export generated PNG files for successful compounds."""

        if not self.processor.compounds:
            messagebox.showwarning("Warning", "No compounds to export")
            return

        self.process_pending_compounds()
        success = [compound for compound in self.processor.compounds if compound.status == "success"]
        if not success:
            messagebox.showwarning("Warning", "No successfully processed compounds")
            return

        dirpath = filedialog.askdirectory(title="Select Output Directory")
        if not dirpath:
            return

        try:
            destination = Path(dirpath)
            for compound in success:
                if compound.image_path:
                    shutil.copy2(compound.image_path, destination / Path(compound.image_path).name)

            self.set_status("Exported {0} PNGs to: {1}".format(len(success), destination))
            messagebox.showinfo("Success", "PNG files saved to:\n{0}".format(destination))
        except Exception as exc:
            messagebox.showerror("Error", "Export failed: {0}".format(exc))

    def on_close(self):
        """Clean up temporary files when the application closes."""

        if self.temp_image_dir and self.temp_image_dir.exists():
            shutil.rmtree(self.temp_image_dir)
        self.destroy()


def main():
    """Launch the desktop application."""

    app = ChemicalVisualizerGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
