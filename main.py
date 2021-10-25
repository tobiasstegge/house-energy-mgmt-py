from tkinter import *
from house import House

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = Tk()
    canvas = Canvas(root, width=300, height=300)
    canvas.pack()
    img = PhotoImage(file="smiley.png")
    canvas.create_image(10, 10, anchor=NW, image=img)
    house = House(file="./examples/Static_Data.csv")
    mainloop()




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
