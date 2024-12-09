import ttkbootstrap as ttk
from ttkbootstrap.constants import *

my_w = ttk.Window()
my_w.geometry("950x500")
#
my_themes = my_w.style.theme_names()  # List of available themes
my_str = ttk.StringVar(value=my_w.style.theme_use())  # default selection of theme
r, c = 0, 0  # row=0 and column =0
for values in my_themes:  # List of available themes
    b = ttk.Radiobutton(
        my_w, text=values, variable=my_str, value=values, command=lambda: my_upd()
    )  # Radio buttons with themes as values 
    b.grid(row=r, column=c, padx=5, pady=20)
    c = c + 1  # increase column by 1
    if c > 8:  # One line complete so change the row and column values
        r, c = r + 1, 0
c, r = 0, r + 1
for my_style in my_w.style.colors:  # List of styles
    b = ttk.Button(my_w, text=my_style, bootstyle=my_style)
    b.grid(row=r, column=c, padx=1, pady=20)
    b = ttk.Button(my_w, text=my_style, bootstyle=(my_style, OUTLINE))
    b.grid(row=r + 1, column=c, padx=1, pady=20)
    m1 = ttk.Meter(
        subtextstyle=my_style, metersize=100, amountused=65, bootstyle=my_style
    )
    m1.grid(row=r + 2, column=c)
    fg = ttk.Floodgauge(value=75, bootstyle=my_style)
    fg.grid(row=r + 3, column=c, padx=1, pady=20)
    # de=ttk.DateEntry(bootstyle=color)
    # de.grid(row=r+4,column=c,padx=1,pady=20)
    c = c + 1

def my_upd():
    my_w.style.theme_use(my_str.get())

my_w.mainloop()