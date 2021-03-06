from Analysis import Analysis
from Analysis import FilterProps
import Pic_to_sin
import numpy as np

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

    def __init__(self, root, file):
        super().__init__()
        self.root = root

        self.var_refresh_checkbox = IntVar()
        self.var_iter_checkbox = IntVar()

        self.filter_props = FilterProps(gamma=2.4, gauss=1)
        self.test_alpha_button = Button(self, text="Alpha test", command=self.test_alpha)
        self.test_detectors_button = Button(self, text="Detectors test", command=self.test_detectors)
        self.test_width_button = Button(self, text="Width test", command=self.test_width)
        self.test_gamma_button = Button(self, text="Gamma test", command=self.test_gamma)
        self.test_gauss_button = Button(self, text="Gauss test", command=self.test_gauss)
        self.test_iter_button = Button(self, text="Iter test", command=self.test_iter)

        self.quit_button = Button(self, text="Quit", command=self.quit)
        self.browse_button = Button(self, text="Browse file", command=self.browse)
        self.refresh_button = Button(self, text="Refresh", command=self.refresh)
        self.refresh_checkbox = Checkbutton(self, text="Auto-refresh", variable=self.var_refresh_checkbox, command=self.auto_refresh)
        self.iter_checkbox = Checkbutton(self, text="Auto-iteration", variable=self.var_iter_checkbox, command=self.auto_refresh)
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

        self.test_alpha_button.place(x=100, y=20)
        self.test_detectors_button.place(x=196, y=20)
        self.test_width_button.place(x=300, y=20)
        self.test_gamma_button.place(x=100, y=50)
        self.test_gauss_button.place(x=199, y=50)
        self.test_iter_button.place(x=300, y=50)

        self.quit_button.place(x=1100, y=20)
        self.browse_button.place(x=1000, y=20)
        self.refresh_button.place(x=900, y=20)
        self.refresh_checkbox.place(x=790, y=20)
        self.iter_checkbox.place(x=670, y=20)

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

    def test_alpha(self):
        alphas = np.arange(2, 91, 2)
        x = []
        y = []
        self.pts_transformation.detectors_amount = 99
        self.pts_transformation.width = 180*2
        for i in alphas:
            self.pts_transformation.alpha = i
            self.refresh()
            mse = Analysis.mean_squared_error(self.input_picture, self.restored_picture)
            print("Alpha =", i, "error =", mse)
            self.root.update_idletasks()
            x.append(i)
            y.append(mse)
        Analysis.draw_plot(x, y, "Kąt α [°]", "Błąd średniokwadratowy", "alpha")

    def test_detectors(self):
        detectors = np.arange(3, 102, 4)
        x = []
        y = []
        self.pts_transformation.alpha = 2
        self.pts_transformation.width = 180*2
        for i in detectors:
            self.pts_transformation.detectors_amount = i
            self.refresh()
            mse = Analysis.mean_squared_error(self.input_picture, self.restored_picture)
            print("Detectors =", i, "error =", mse)
            self.root.update_idletasks()
            x.append(i)
            y.append(mse)
        Analysis.draw_plot(x, y, "Liczba detektorów", "Błąd średniokwadratowy", "detectors")

    def test_width(self):
        widths = np.arange(5, 181, 5)
        x = []
        y = []
        self.pts_transformation.alpha = 2
        self.pts_transformation.detectors_amount = 99
        for i in widths:
            self.pts_transformation.width = i*2
            self.refresh()
            mse = Analysis.mean_squared_error(self.input_picture, self.restored_picture)
            print("Width =", i, "error =", mse)
            self.root.update_idletasks()
            x.append(i)
            y.append(mse)
        Analysis.draw_plot(x, y, "Kąt rozwarcia stożka [°]", "Błąd średniokwadratowy", "width")

    def test_gamma(self):
        gammas = np.arange(0.2, 4.1, 0.2)
        x = []
        y = []
        self.pts_transformation.alpha = 2
        self.pts_transformation.detectors_amount = 99
        self.pts_transformation.width = 180 * 2
        for i in gammas:
            self.filter_props.gamma = i
            self.refresh()
            mse = Analysis.mean_squared_error(self.input_picture, self.restored_picture)
            print("Gamma =", i, "error =", mse)
            self.root.update_idletasks()
            x.append(i)
            y.append(mse)
        Analysis.draw_plot(x, y, "Wartość γ", "Błąd średniokwadratowy", "gamma")

    def test_gauss(self):
        gauss = np.arange(0, 3.1, 0.1)
        x = []
        y = []
        self.pts_transformation.alpha = 2
        self.pts_transformation.detectors_amount = 99
        self.pts_transformation.width = 180 * 2
        self.filter_props.gamma = 2.4
        for i in gauss:
            self.filter_props.gauss = i
            self.refresh()
            mse = Analysis.mean_squared_error(self.input_picture, self.restored_picture)
            print("Gauss =", i, "error =", mse)
            self.root.update_idletasks()
            x.append(i)
            y.append(mse)
        Analysis.draw_plot(x, y, "Odchylenie standardowe", "Błąd średniokwadratowy", "gauss")
        # odchylenie standardowe rozkładu normalnego, który został użyty do generacji maski

    def test_iter(self):
        x = []
        y = []
        self.var_iter_checkbox.set(True)

        self.pts_transformation.alpha = 2
        self.pts_transformation.detectors_amount = 99
        self.pts_transformation.width = 180 * 2
        self.filter_props.gamma = 2.4
        self.filter_props.gauss = 1.0
        self.pts_transformation.generate_all_positions(self.input_picture)

        is_end = False
        i = 0
        while not is_end:
            self.sinogram, is_end = self.pts_transformation.make_sinogram_iter(self.input_picture)
            self.display_picture(Image.fromarray(self.sinogram), 'sinogram')

            self.restored_picture = self.pts_transformation.restore_picture(self.sinogram, len(self.input_picture),
                                                                        self.filter_props)
            self.display_picture(Image.fromarray(self.restored_picture), 'output')
            self.root.update_idletasks()

            mse = Analysis.mean_squared_error(self.input_picture, self.restored_picture)
            x.append(i)
            y.append(mse)
            i += 1
            print("Iter =", i, "error =", mse)
        Analysis.draw_plot(x, y, "Iteracja", "Błąd średniokwadratowy", "iter")

    def center_window(self):
        w = 1200
        h = 700

        x = (self.master.winfo_screenwidth() - w) / 2
        y = (self.master.winfo_screenheight() - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def browse(self):
        file = filedialog.askopenfilename()
        if len(file) > 0:
            self.load_images(file)

    def auto_refresh(self):
        if self.var_refresh_checkbox.get():
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
        if self.var_refresh_checkbox.get():
            self.refresh()

    def refresh(self):
        self.pts_transformation.generate_all_positions(self.input_picture)
        if self.var_iter_checkbox.get():
            self.generate_iter()
        else:
            self.sinogram = self.pts_transformation.make_sinogram(self.input_picture)
            self.display_picture(Image.fromarray(self.sinogram), 'sinogram')

            self.restored_picture = self.pts_transformation.restore_picture(self.sinogram, len(self.input_picture),
                                                                            self.filter_props)
            self.display_picture(Image.fromarray(self.restored_picture), 'output')

    def generate_iter(self):
        self.sinogram, is_end = self.pts_transformation.make_sinogram_iter(self.input_picture)
        self.display_picture(Image.fromarray(self.sinogram), 'sinogram')

        self.restored_picture = self.pts_transformation.restore_picture(self.sinogram, len(self.input_picture),
                                                                        self.filter_props)
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
    app = MainWindow(root, "pictures/03.png")
    root.mainloop()
