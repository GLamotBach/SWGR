import tkinter as tk
# from PIL import Image, ImageTk
# Pillow not yet installed


def test_function():
    appraise_text.set("loading")


# Beginning of window object
root = tk.Tk()

# Window size and grid shape
canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=3, rowspan=3)

# # Logo - placeholder
# # Open image file
# logo = Image.open('logo.png')
# # Convert to Tk Image
# logo = ImageTk.PhotoImage(logo)
# # Create a logo widget
# logo_label = tk.Label(image=logo)
# logo_label.image = logo
# logo_label.grid(column=1, row=0)

# Entry box
entry = tk.Entry(root)
canvas.create_window(300, 200, window=entry)

# Instructions
instructions = tk.Label(root, text="Podaj link do ogłoszenia które chcesz wycenić.", font="Raleway")
instructions.grid(columnspan=3, column=0, row=1)

# "Wyceń" button
appraise_text = tk.StringVar()
appraise_btn = tk.Button(root, textvariable=appraise_text, command=lambda:test_function(), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
appraise_text.set("Wyceń")
appraise_btn.grid(column=1, row=2)

# End of Window object
root.mainloop()
