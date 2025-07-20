import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw

# main window
root = tk.Tk()
root.title("shot chart")

# pick image
image_path = filedialog.askopenfilename(
    title="select court image",
    filetypes=[("image files", "*.png *.jpg *.jpeg *.bmp")]
)

if not image_path:
    messagebox.showerror("no image", "you must select a court image.")
    root.destroy()
    exit()

# load and resize
original_image = Image.open(image_path)
scale = 2
img_width, img_height = original_image.size
new_size = (int(img_width * scale), int(img_height * scale))
original_resized = original_image.resize(new_size, Image.Resampling.LANCZOS)
working_image = original_resized.copy()

# canvas setup
shot_result = tk.StringVar(value="make")
tk_image = ImageTk.PhotoImage(working_image)
canvas = tk.Canvas(root, width=working_image.width, height=working_image.height)
canvas.pack()
canvas_image = canvas.create_image(0, 0, anchor='nw', image=tk_image)

# shot history
shot_history = []

# export
def finish_and_export():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("png files", "*.png")],
        title="save shot chart"
    )
    if file_path:
        working_image.save(file_path)
        messagebox.showinfo("done", f"saved to:\n{file_path}")

# draw shot
def handle_click(event):
    global working_image, tk_image
    x, y = event.x, event.y
    shot_type = shot_result.get()
    shot_history.append((x, y, shot_type))
    redraw_all_shots()

def redraw_all_shots():
    global working_image, tk_image
    working_image = original_resized.copy()
    draw = ImageDraw.Draw(working_image)
    r = 9

    for x, y, shot_type in shot_history:
        if shot_type == "make":
            draw.ellipse([x - r, y - r, x + r, y + r], outline="lime", width=3)  # using named bright green
        else:
            draw.line([x - r, y - r, x + r, y + r], fill='red', width=3)
            draw.line([x + r, y - r, x - r, y + r], fill='red', width=3)

    tk_image = ImageTk.PhotoImage(working_image)
    canvas.itemconfig(canvas_image, image=tk_image)

# undo
def undo_last_shot():
    if shot_history:
        shot_history.pop()
        redraw_all_shots()

# reset
def reset_chart():
    shot_history.clear()
    redraw_all_shots()

# buttons
frame = tk.Frame(root)
frame.pack(pady=5)
tk.Radiobutton(frame, text="Make", variable=shot_result, value="make").pack(side='left')
tk.Radiobutton(frame, text="Miss", variable=shot_result, value="miss").pack(side='left')
tk.Button(frame, text="Undo", command=undo_last_shot).pack(side='left', padx=10)
tk.Button(frame, text="Reset", command=reset_chart).pack(side='left', padx=5)
tk.Button(frame, text="Export", command=finish_and_export).pack(side='left', padx=10)

# bind click
canvas.bind("<Button-1>", handle_click)

root.mainloop()
