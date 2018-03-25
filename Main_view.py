import Pic_to_sin

from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Frame, Button, Label
from PIL import Image, ImageTk
from skimage import io
from skimage.color import rgb2gray


class MainWindow(Frame):
    detectors_amount = 70
    alpha = 10
    width = 180
    slider_length = 300
    progress = 5
    type = 0 # 0 not iter, 1 iter

    def __init__(self, root, file):
        super().__init__()
        self.root = root

        self.var_checkbox = IntVar()
        self.quit_button = Button(self, text="Quit", command=self.quit)
        self.browse_button = Button(self, text="Browse file", command=self.browse)
        self.refresh_button = Button(self, text="Refresh", command=self.refresh)
        self.checkbox = Checkbutton(self, text="Auto-refresh", variable=self.var_checkbox, command=self.auto_refresh)
        self.init_ui()

        self.pts_transformation = Pic_to_sin.Transform()
        self.pts_transformation.detectors_amount = MainWindow.detectors_amount
        self.pts_transformation.alpha = MainWindow.alpha
        self.pts_transformation.width = MainWindow.width * 2

        self.input_picture = rgb2gray(io.imread(file))
        self.display_picture(Image.fromarray(self.input_picture), 'input')

        self.sinogram = None
        self.restored_picture = None
        self.refresh()

    def init_ui(self):
        self.master.title("Tomograph")
        self.pack(fill=BOTH, expand=1)
        self.center_window()

        self.quit_button.place(x=1100, y=20)
        self.browse_button.place(x=1000, y=20)
        self.refresh_button.place(x=900, y=20)
        self.checkbox.place(x=790, y=20)

        detectors_slider = Scale(root, from_=1, to=100, length=MainWindow.slider_length, orient='horizontal',
                                 command=lambda value, name='detectors': self.change_parameters(name, value,
                                                                                                detectors_label))
        detectors_slider.set(MainWindow.detectors_amount)
        detectors_slider.place(x=100, y=200)
        detectors_label = Label(root, width=MainWindow.slider_length)
        detectors_label.place(x=100, y=200)

        alpha_slider = Scale(root, from_=1, to=180, length=MainWindow.slider_length, orient='horizontal',
                             command=lambda value, name='alpha': self.change_parameters(name, value, alpha_label))
        alpha_slider.set(MainWindow.alpha)
        alpha_slider.place(x=75 * 2 + MainWindow.slider_length, y=200)
        alpha_label = Label(root, width=MainWindow.slider_length)
        alpha_label.place(x=75 * 2 + MainWindow.slider_length, y=200)

        width_slider = Scale(root, from_=0, to=180, length=MainWindow.slider_length, orient='horizontal',
                             command=lambda value, name='width': self.change_parameters(name, value, width_label))
        width_slider.set(MainWindow.width)
        width_slider.place(x=200 + MainWindow.slider_length * 2, y=200)
        width_label = Label(root, width=MainWindow.slider_length)
        width_label.place(x=200 + MainWindow.slider_length * 2, y=200)

        progress_slider = Scale(root, from_=1, to=5, length=MainWindow.slider_length, orient='horizontal',
                                 command=lambda value, name='progress': self.change_parameters(name, value,
                                                                                                progress_label))
        progress_slider.set(MainWindow.progress)
        progress_slider.place(x=450, y=100)
        progress_label = Label(root, width=MainWindow.slider_length)
        progress_label.place(x=450, y=100)

    def center_window(self):
        w = 1200
        h = 800

        x = (self.master.winfo_screenwidth() - w) / 2
        y = (self.master.winfo_screenheight() - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def browse(self):
        file = filedialog.askopenfilename()
        if len(file) > 0:
            self.load_images(file)

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
            label.place(x=100, y=300)
        elif picture_type == 'sinogram':
            label.place(x=450, y=300)
        elif picture_type == 'output':
            label.place(x=800, y=300)

    def change_parameters(self, parameter_type, value, label):
        if parameter_type == 'detectors':
            self.pts_transformation.detectors_amount = int(value)
            label.config(text="Detectors amount = " + value)
        elif parameter_type == 'alpha':
            label.config(text="Alpha = " + value)
            self.pts_transformation.alpha = int(value)
        elif parameter_type == 'width':
            label.config(text="Width = " + value)
            self.pts_transformation.width = int(value) * 2
        elif parameter_type == 'progress':
            percent = int(int(value)/5 * 100)
            label.config(text="Progress = " + str(percent) + "%")
            self.pts_transformation.progress = int(value)
        if self.var_checkbox.get():
            self.refresh()

    def refresh(self):
        self.pts_transformation.generate_all_positions(self.input_picture)
        if MainWindow.type == 0:
            self.sinogram = self.pts_transformation.make_sinogram(self.input_picture)
            self.display_picture(Image.fromarray(self.sinogram), 'sinogram')

            self.restored_picture = self.pts_transformation.restore_picture(self.sinogram, len(self.input_picture))
            self.display_picture(Image.fromarray(self.restored_picture), 'output')
        else:
            self.generate_iter()

    def generate_iter(self):
        self.sinogram, is_end = self.pts_transformation.make_sinogram_iter(self.input_picture)
        self.display_picture(Image.fromarray(self.sinogram), 'sinogram')

        self.restored_picture = self.pts_transformation.restore_picture(self.sinogram, len(self.input_picture))
        self.display_picture(Image.fromarray(self.restored_picture), 'output')
        if not is_end:
            self.root.update_idletasks()
            self.root.after(0, self.generate_iter)

    def load_images(self, file):
        self.input_picture = rgb2gray(io.imread(file))
        self.display_picture(Image.fromarray(self.input_picture), 'input')
        self.refresh()


if __name__ == '__main__':
    root = Tk()
    app = MainWindow(root, "pictures/01.png")
    root.mainloop()
