import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import ezdxf
import os
import re

class DXFGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("DXF Text Generator")
        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.master)
        frame.pack(padx=10, pady=10)

        ttk.Label(frame, text="Enter Text:").grid(row=0, column=0)
        self.text_input = ttk.Entry(frame, width=30)
        self.text_input.grid(row=0, column=1)

        ttk.Label(frame, text="Select Unit:").grid(row=1, column=0)
        self.unit_var = tk.StringVar()
        self.unit_dropdown = ttk.Combobox(frame, textvariable=self.unit_var, values=["inch", "mm"])
        self.unit_dropdown.grid(row=1, column=1)
        self.unit_dropdown.set("inch")

        ttk.Label(frame, text="Select Aspect Ratio:").grid(row=2, column=0)
        self.aspect_ratio_var = tk.StringVar()
        self.aspect_ratio_dropdown = ttk.Combobox(frame, textvariable=self.aspect_ratio_var, values=["2:1", "3:2"])
        self.aspect_ratio_dropdown.grid(row=2, column=1)
        self.aspect_ratio_dropdown.set("2:1")

        ttk.Label(frame, text="Enter Height:").grid(row=3, column=0)
        self.height_input = ttk.Entry(frame, width=30)
        self.height_input.grid(row=3, column=1)

        ttk.Label(frame, text="Output Directory:").grid(row=4, column=0)
        self.output_dir_label = ttk.Label(frame, text="No directory selected")
        self.output_dir_label.grid(row=4, column=1, sticky="w")
        self.output_dir_button = ttk.Button(frame, text="Choose Directory", command=self.select_output_directory)
        self.output_dir_button.grid(row=4, column=2)

        self.generate_button = ttk.Button(frame, text="Generate DXF", command=self.generate_dxf)
        self.generate_button.grid(row=5, columnspan=3)

        self.status_label = ttk.Label(frame, text="")
        self.status_label.grid(row=6, columnspan=3)

    @staticmethod
    def sanitize_filename(text):
        sanitized = re.sub(r'[\\/*?:"<>|]', "", text)
        sanitized = sanitized.replace(" ", "_")
        return sanitized

    def select_output_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_directory = directory
            self.output_dir_label.config(text=directory)

    def generate_dxf(self):
        if not (self.text_input.get() and self.unit_var.get() and self.aspect_ratio_var.get() and self.height_input.get()):
            self.status_label.config(text="All fields are required!", foreground="red")
            return

        if not hasattr(self, 'output_directory'):
            self.status_label.config(text="Output directory not selected!", foreground="red")
            return

        try:
            height = float(self.height_input.get())
            aspect_ratio = self.aspect_ratio_var.get()
            ratio_values = [int(r) for r in aspect_ratio.split(':')]
            width = height * ratio_values[1] / ratio_values[0]

            doc = ezdxf.new('R2010')
            msp = doc.modelspace()
            msp.add_text(self.text_input.get(), dxfattribs={
                'height': height,
                'width': width
            })

            filename = self.sanitize_filename(self.text_input.get())
            output_file = os.path.join(self.output_directory, f"{filename}.dxf")
            if os.path.exists(output_file):
                if not messagebox.askyesno("Overwrite File", "File already exists. Overwrite?"):
                    self.status_label.config(text="File not saved; user cancelled overwrite.", foreground="red")
                    return
            doc.saveas(output_file)
            self.status_label.config(text="DXF file generated successfully!", foreground="green")
        except Exception as e:
            self.status_label.config(text=str(e), foreground="red")

def run_app():
    root = tk.Tk()
    app = DXFGeneratorApp(root)
    root.mainloop()
    
run_app()
