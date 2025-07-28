import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw

#class
class ShotChartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shot Chart")

        self.shot_result = tk.StringVar(value="make")
        self.shot_history = []

        self.load_image()
        if not self.original_image:
            return

        self.setup_ui()
        self.redraw_all_shots()

    def load_image(self):
        image_path = filedialog.askopenfilename(
            title="Select Court Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )

        if not image_path:
            messagebox.showerror("No Image", "You must select a court image.")
            self.root.quit()
            self.original_image = None
            return

        self.original_image = Image.open(image_path)
        scale = 2
        img_width, img_height = self.original_image.size
        new_size = (int(img_width * scale), int(img_height * scale))
        self.original_resized = self.original_image.resize(new_size, Image.Resampling.LANCZOS)
        self.working_image = self.original_resized.copy()

    def setup_ui(self):
        #canvas setup
        self.tk_image = ImageTk.PhotoImage(self.working_image)
        self.canvas = tk.Canvas(self.root, width=self.working_image.width, height=self.working_image.height)
        self.canvas.pack()
        self.canvas_image = self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)
        self.canvas.bind("<Button-1>", self.handle_click)

        #controls
        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        tk.Radiobutton(frame, text="Make", variable=self.shot_result, value="make").pack(side='left')
        tk.Radiobutton(frame, text="Miss", variable=self.shot_result, value="miss").pack(side='left')

        tk.Button(frame, text="Undo", command=self.undo_last_shot).pack(side='left', padx=10)
        tk.Button(frame, text="Reset", command=self.reset_chart).pack(side='left', padx=5)
        tk.Button(frame, text="Export", command=self.export_chart).pack(side='left', padx=10)

        #shot counter
        self.counter_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.counter_label.pack(pady=3)

    def handle_click(self, event):
        x, y = event.x, event.y
        shot_type = self.shot_result.get()
        self.shot_history.append((x, y, shot_type))
        self.redraw_all_shots()

    def redraw_all_shots(self):
        self.working_image = self.original_resized.copy()
        draw = ImageDraw.Draw(self.working_image)
        r = 9

        for x, y, shot_type in self.shot_history:
            if shot_type == "make":
                draw.ellipse([x - r, y - r, x + r, y + r], outline="lime", width=3)
            else:
                draw.line([x - r, y - r, x + r, y + r], fill='red', width=3)
                draw.line([x + r, y - r, x - r, y + r], fill='red', width=3)

        self.tk_image = ImageTk.PhotoImage(self.working_image)
        self.canvas.itemconfig(self.canvas_image, image=self.tk_image)

        self.update_shot_counter()

    def update_shot_counter(self):
        makes = sum(1 for _, _, s in self.shot_history if s == "make")
        total = len(self.shot_history)
        misses = total - makes

        if total == 0:
            fg_percent = "N/A"
        else:
            fg_percent = f"{(makes / total) * 100:.1f}%"

        self.counter_label.config(text=f"Makes: {makes} | Misses: {misses} | FG%: {fg_percent}")

    def undo_last_shot(self):
        if self.shot_history:
            self.shot_history.pop()
            self.redraw_all_shots()

    def reset_chart(self):
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the chart?"):
            self.shot_history.clear()
            self.redraw_all_shots()

    def export_chart(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save Shot Chart"
        )
        if file_path:
            self.working_image.save(file_path)
            messagebox.showinfo("Saved", f"Shot chart saved to:\n{file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ShotChartApp(root)
    root.mainloop()
