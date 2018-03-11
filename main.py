from tkinter import Tk, BOTH
from tkinter.ttk import Frame, Button, Label
from PIL import Image, ImageTk

class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def centerWindow(self):
        w = 900
        h = 600

        x = (self.master.winfo_screenwidth() - w) / 2
        y = (self.master.winfo_screenheight() - h) / 2
        self.master.geometry('%dx%d+%d+%d' %(w, h, x, y))

    def initUI(self):
        self.master.title("Tomograph")
        self.pack(fill = BOTH, expand = 1)
        self.centerWindow()

        inputImage = ImageTk.PhotoImage(Image.open("example.jpg"))
        label1 = Label(self, image = inputImage)
        label1.image = inputImage
        label1.place(x = 100, y = 200)

        sinogramImage = ImageTk.PhotoImage(Image.open("example.jpg"))
        label1 = Label(self, image = sinogramImage)
        label1.image = sinogramImage
        label1.place(x = 350, y = 200)

        outputImage = ImageTk.PhotoImage(Image.open("example.jpg"))
        label1 = Label(self, image = outputImage)
        label1.image = outputImage
        label1.place(x = 600, y = 200)

        quitButton = Button(self, text = "Quit", command = self.quit)
        quitButton.place(x = 800, y = 20)

def main():
    root = Tk()
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()   
