import Pic_to_sin

from tkinter import Tk, BOTH
from tkinter.ttk import Frame, Button, Label
from PIL import Image, ImageTk
from skimage import data, io
from skimage.color import rgb2gray


class Example(Frame):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def center_window(self):
        w = 900
        h = 600

        x = (self.master.winfo_screenwidth() - w) / 2
        y = (self.master.winfo_screenheight() - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def init_ui(self):
        self.master.title("Tomograph")
        self.pack(fill = BOTH, expand=1)
        self.center_window()

        quit_button = Button(self, text="Quit", command=self.quit)
        quit_button.place(x=800, y=20)

    def display_picture(self, picture, picture_type):
        image = ImageTk.PhotoImage(picture)
        label1 = Label(self, image=image)
        label1.image = image
        if picture_type == 'input':
            label1.place(x=100, y=200)
        elif picture_type == 'sinogram':
            label1.place(x=350, y=200)
        elif picture_type == 'output':
            label1.place(x=600, y=200)


if __name__ == '__main__':
    root = Tk()
    app = Example()

    pic = Pic_to_sin.Picture
    pic.input_picture = rgb2gray(io.imread("pictures/01.png"))
    app.display_picture(Image.fromarray(pic.input_picture), 'input')

    pts = Pic_to_sin.Transform()
    pts.make_sinogram(pic.input_picture)

    root.mainloop()




