import tkinter as tk
from PIL import Image, ImageTk

from user_interface import appraise_offer_approx


def button_function():
    """Functionality of the GUI, appraise (pol:'Wyceń') button."""
    url = entry.get()
    price = appraise_offer_approx(url)
    message_lable['text'] = f"Auto warte jest {price}zł"


# Beginning of window object
root = tk.Tk()

# Window size and grid shape
canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=3, rowspan=4)

# Logo - placeholder
# Open image file
logo = Image.open('swgr_logo.png')
# Convert to Tk Image
logo = ImageTk.PhotoImage(logo)
# Create a logo widget
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)

# Instructions
message = "Podaj link do ogłoszenia z otomoto.pl które chcesz wycenić."
message_lable = tk.Label(root, text=message, font="Raleway")
message_lable.grid(columnspan=3, column=0, row=1)

# Entry box
entry = tk.Entry(root, width=75)
entry.grid(columnspan=3, column=0, row=2,)
offer_url = entry.get()

# "Wyceń" button
appraise_text = tk.StringVar()
appraise_btn = tk.Button(root,
                         textvariable=appraise_text,
                         command=button_function,
                         font="Raleway",
                         bg="#c2121b",
                         fg="white",
                         height=1,
                         width=15)
appraise_text.set("Wyceń")
appraise_btn.grid(column=1, row=3)

# End of Window object
root.mainloop()
