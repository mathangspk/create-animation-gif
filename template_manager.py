import json
from tkinter import filedialog, messagebox

class TemplateManager:
    @staticmethod
    def save_template(images, duration, loop, resolution, custom_width="", custom_height=""):
        """
        Lưu template gồm danh sách hình ảnh, duration, loop, resolution, và custom resolution (nếu có).
        """
        template_data = {
            "images": images,
            "duration": duration,
            "loop": loop,
            "resolution": resolution,
            "custom_width": custom_width,
            "custom_height": custom_height
        }

        # Hộp thoại để lưu file
        save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if save_path:
            # Ghi thông tin vào file JSON
            with open(save_path, 'w') as file:
                json.dump(template_data, file)

            messagebox.showinfo("Success", f"Template saved successfully at {save_path}")

    @staticmethod
    def load_template():
        """
        Mở file JSON chứa template và trả về thông tin từ file.
        """
        # Hộp thoại để mở file template
        template_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if template_path:
            # Đọc dữ liệu từ file JSON
            with open(template_path, 'r') as file:
                template_data = json.load(file)
            return template_data
        return None
