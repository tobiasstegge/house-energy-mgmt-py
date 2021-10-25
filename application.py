import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkinter.messagebox import showinfo

window = tk.Tk()
window.title('Energy Management Project')
window.geometry('600x400')


class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.static_file = None
        self.dynamic_file = None

    def __open_static_file(self):
        file_path = askopenfile(mode='r', filetypes=[('CSV', '*csv')], initialdir='/')
        showinfo(
            title='Selected File',
            message=file_path
        )
        if file_path is not None:
            self.static_file = file_path

    def __open_dynamic_file(self):
        file_path = askopenfile(mode='r', filetypes=[('CSV', '*csv')], initialdir='/')
        showinfo(
            title='Selected File',
            message=file_path
        )
        if file_path is not None:
            self.dynamic_file = file_path


    open_button_static = ttk.Button(
        window,
        text='Open a Static File',
        command=__open_dynamic_file
    )

    open_button_dynamic = ttk.Button(
        window,
        text='Open a Dynamic File',
        command=__open_static_file
    )

    open_button_static.pack(expand=True)
    open_button_dynamic.pack(expand=True)

    canvas = tk.Canvas(
        window,
        width=400,
        height=400
    )
    canvas.pack()
    image = tk.PhotoImage(file='smiley.png')
    canvas.create_image(
        10,
        100,
        anchor=tk.CENTER,
        image=image
    )

    tk.mainloop()