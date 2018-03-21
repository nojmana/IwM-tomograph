import Pic_to_sin

from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Frame, Button, Label
from PIL import Image, ImageTk
from skimage import io
from skimage.color import rgb2gray


class MainWindow(Frame):

    def __init__(self, file):
        super().__init__()
        self.var_checkbox = IntVar()
        self.init_ui()

        self.input_picture = rgb2gray(io.imread(file))
        self.display_picture(Image.fromarray(self.input_picture), 'input')

        self.pts_transformation = Pic_to_sin.Transform()
        self.sinogram = self.pts_transformation.make_sinogram(self.input_picture)
        self.display_picture(Image.fromarray(self.sinogram), 'sinogram')

    def center_window(self):
        w = 1200
        h = 800

        x = (self.master.winfo_screenwidth() - w) / 2
        y = (self.master.winfo_screenheight() - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def browse(self):
        file = filedialog.askopenfilename()
        self.load_images(file)

    def init_ui(self):
        self.master.title("Tomograph")
        self.pack(fill=BOTH, expand=1)
        self.center_window()

        self.quit_button = Button(self, text="Quit", command=self.quit)
        self.quit_button.place(x=1100, y=20)

        self.browse_button = Button(self, text="Browse file", command=self.browse)
        self.browse_button.place(x=1000, y=20)

        self.refresh_button = Button(self, text="Refresh", command=self.refresh)
        self.refresh_button.place(x=900, y=20)

        self.checkbox = Checkbutton(self, text="Auto-refresh", variable=self.var_checkbox, command=self.auto_refresh)
        self.checkbox.place(x=790, y=20)

    def auto_refresh(self):
        if self.var_checkbox.get():
            self.refresh()
            self.refresh_button['state'] = 'disabled'
        else:
            self.refresh_button['state'] = 'normal'

    def display_picture(self, picture, picture_type):
        width = 300
        width_percent = width/float(picture.size[0])
        height = int((float(picture.size[0] * float(width_percent))))
        resized_picture = picture.resize((width, height), Image.ANTIALIAS)
        resized_picture = ImageTk.PhotoImage(resized_picture)
        label = Label(self, image=resized_picture)
        label.image = resized_picture
        if picture_type == 'input':
            label.place(x=100, y=200)
        elif picture_type == 'sinogram':
            label.place(x=450, y=200)
        elif picture_type == 'output':
            label.place(x=800, y=200)

    def change_parameters(self, parameter_type, value, label):
        if parameter_type == 'detectors':
            self.pts_transformation.detectors_amount=int(value)
            label.config(text="Detectors amount = " + value)
        elif parameter_type == 'alpha':
            label.config(text="Alpha = " + value)
            self.pts_transformation.alpha=int(value)
        elif parameter_type == 'width':
            label.config(text="Width = " + value)
            self.pts_transformation.width = int(value)
        if self.var_checkbox.get():
            self.refresh()

    def refresh(self):
        self.sinogram = self.pts_transformation.make_sinogram(self.input_picture)
        self.display_picture(Image.fromarray(self.sinogram), 'sinogram')

    def load_images(self, file):
        self.input_picture = rgb2gray(io.imread(file))
        self.display_picture(Image.fromarray(self.input_picture), 'input')
        self.refresh()


if __name__ == '__main__':
    root = Tk()
    app = MainWindow("pictures/01.png")
    slider_length = 300

    detectors_slider = Scale(root, from_=1, to=100, length=slider_length, orient='horizontal',
                             command=lambda value, name='detectors': app.change_parameters(name, value, detectors_label))
    detectors_slider.set(70)
    detectors_slider.place(x=75, y=100)
    detectors_label = Label(root, width=slider_length)
    detectors_label.place(x=75, y=100)

    alpha_slider = Scale(root, from_=1, to=180, length=slider_length, orient='horizontal',
                         command=lambda value, name='alpha': app.change_parameters(name, value, alpha_label))
    alpha_slider.set(10)
    alpha_slider.place(x=75*2+slider_length, y=100)
    alpha_label = Label(root, width=slider_length)
    alpha_label.place(x=75*2+slider_length, y=100)

    width_slider = Scale(root, from_=0, to=360, length=slider_length, orient='horizontal',
                         command=lambda value, name='width': app.change_parameters(name, value, width_label))
    width_slider.set(360)
    width_slider.place(x=75*3+slider_length*2, y=100)
    width_label = Label(root, width=slider_length)
    width_label.place(x=75*3+slider_length*2, y=100)

    root.mainloop()
