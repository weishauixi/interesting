import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import subprocess

try:
    from PIL import Image, ImageTk
except ImportError:
    import tkinter.messagebox
    root = tk.Tk()
    root.withdraw()
    tkinter.messagebox.showerror("缺少库", "请先安装图像处理库 Pillow。\n\n方法：在命令行输入 pip install Pillow")
    sys.exit()

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片一键处理工具")
        self.root.geometry("500x350")
        
        # 变量存储
        self.file_path = tk.StringVar()
        self.target_width = tk.DoubleVar(value=17.0) 
        self.target_dpi = tk.IntVar(value=300)       
        
        self.create_widgets()

    def create_widgets(self):

        file_frame = tk.LabelFrame(self.root, text="1. 选择图片文件", padx=10, pady=10)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Entry(file_frame, textvariable=self.file_path, width=40).pack(side="left", padx=5)
        tk.Button(file_frame, text="浏览...", command=self.select_file).pack(side="left")

        param_frame = tk.LabelFrame(self.root, text="2. 设置参数", padx=10, pady=10)
        param_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(param_frame, text="目标宽度 (cm):").grid(row=0, column=0, sticky="e", pady=5)
        width_entry = tk.Entry(param_frame, textvariable=self.target_width, width=10)
        width_entry.grid(row=0, column=1, sticky="w", pady=5)
        
        tk.Label(param_frame, text="目标 DPI:").grid(row=1, column=0, sticky="e", pady=5)
        dpi_entry = tk.Entry(param_frame, textvariable=self.target_dpi, width=10)
        dpi_entry.grid(row=1, column=1, sticky="w", pady=5)

        btn_frame = tk.Frame(self.root, pady=20)
        btn_frame.pack()
        
        self.process_btn = tk.Button(btn_frame, text="开始处理并生成 TIFF 与 JPG", 
                                     command=self.run_process, 
                                     bg="#007bff", fg="black", 
                                     font=("Arial", 12, "bold"), padx=20, pady=5)
        self.process_btn.pack()
        
        self.status_label = tk.Label(self.root, text="准备就绪", fg="gray")
        self.status_label.pack(side="bottom", pady=5)

    def select_file(self):
        filename = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.tiff *.bmp"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)

    def run_process(self):
        input_path = self.file_path.get()
        if not input_path or not os.path.exists(input_path):
            messagebox.showerror("错误", "请先选择一个有效的图片文件！")
            return
            
        try:
            width_cm = self.target_width.get()
            dpi = self.target_dpi.get()
            
            self.status_label.config(text="正在处理中...", fg="blue")
            self.root.update() 
            
            output_files = self.process_image(input_path, width_cm, dpi)
            
            self.status_label.config(text="处理完成！", fg="green")
            
            msg = f"成功生成以下文件：\n\n1. {os.path.basename(output_files[0])}\n2. {os.path.basename(output_files[1])}\n\n是否打开文件夹查看？"
            if messagebox.askyesno("完成", msg):
                self.open_file_folder(output_files[0])
                
        except ValueError:
             messagebox.showerror("错误", "宽度或 DPI 必须是数字！")
        except Exception as e:
            messagebox.showerror("处理出错", str(e))
            self.status_label.config(text="出错", fg="red")

    def process_image(self, input_path, output_width_cm, target_dpi):
        """核心图像处理逻辑 (与之前相同，但适配 GUI)"""
        with Image.open(input_path) as img:

            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P': img = img.convert('RGBA')
                background.paste(img, mask=img.split()[3])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            target_width_px = int((output_width_cm / 2.54) * target_dpi)
            aspect_ratio = img.height / img.width
            target_height_px = int(target_width_px * aspect_ratio)

            resized_img = img.resize((target_width_px, target_height_px), resample=Image.Resampling.LANCZOS)

            dir_name, file_name_ext = os.path.split(input_path)
            file_name, _ = os.path.splitext(file_name_ext)
            
            output_tiff = os.path.join(dir_name, f"Prossessed_{file_name}.tiff")
            output_jpg = os.path.join(dir_name, f"Prossessed_{file_name}.jpg")

            resized_img.save(output_tiff, dpi=(target_dpi, target_dpi), compression="tiff_lzw_no_prediction")
            resized_img.save(output_jpg, dpi=(target_dpi, target_dpi), quality=95, subsampling=0)
            
            return [output_tiff, output_jpg]

    def open_file_folder(self, path):

        folder_path = os.path.dirname(path)
        if sys.platform == 'win32':
            subprocess.Popen(['explorer', '/select,', os.path.normpath(path)])
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', folder_path])
        else:
            subprocess.Popen(['xdg-open', folder_path])

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()