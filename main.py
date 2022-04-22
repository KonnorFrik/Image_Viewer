from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from os import listdir, getcwd
from sys import argv

image_types = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]


class ImageViewer(Tk):
    def __init__(self, image="tst.png"):
        super().__init__()
        self.canva_image = None
        self.img = None

        self.image = image

        self.menu = Menu(self)
        self.menu_tab_file = Menu(self.menu)
        self.field_image = Canvas(self)
        self.field_button = Frame(self)
        self.button_next = Button(self.field_button)
        self.button_prev = Button(self.field_button)

        self.image_list = []
        self.get_images_list(getcwd())
        try:
            self.current_image_index = self.image_list.index(self.image)
        except ValueError:
            self.current_image_index = 0
        self.init_ui()
        self.draw_image(self.image)
        self.mainloop()

    def init_ui(self):
        self.title("Image Viewer")
        self.minsize(200, 200)
        self.geometry("900x700+500+150")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.config(menu=self.menu)
        self.menu_tab_file.add_command(label="Open", underline=0, command=self.open_image)
        self.menu_tab_file.add_separator()
        self.menu_tab_file.add_command(label="Exit", underline=1, command=self.on_exit)
        self.menu.add_cascade(label="File", underline=0, menu=self.menu_tab_file)

        self.field_image.config(width=200, height=200)
        self.field_button.config(width=100)
        self.button_next.config(text="Next", width=7, command=self.choose_next)
        self.button_prev.config(text="Previous", width=7, command=self.choose_prev)

        # self.field_button.pack(side=BOTTOM)
        self.field_button.grid(row=1, column=0, sticky=S)
        self.button_next.pack(side=RIGHT, padx=5, pady=1)
        self.button_prev.pack(side=LEFT, padx=5, pady=1)
        self.field_image.grid(row=0, column=0)


    def draw_image(self, image):
        self.field_image.delete("img")
        try:
            self.img = ImageTk.PhotoImage(Image.open(image))
        except Exception:
            pass
        self.canva_image = self.field_image.create_image(0, 0, anchor=NW, image=self.img)
        self.field_image.addtag_all("img")
        self.resize()
        # self.field_image.pack(fill=BOTH, expand=1)
        self.title(f"Image Viewer | {image}")

    def resize(self):
        x1, y1, x2, y2 = self.field_image.bbox("img")
        self.field_image.config(width=x2, height=y2)

    def open_image(self):
        filepath = askopenfilename(
            filetypes=[("All files", "*"), ("Png files", "*.png"), ("Jpg files", "*.jpg"), ("Jpeg files", "*.jpeg"),
                       ("GIF files", "*.gif"), ("BMP files", "*.bmp")])
        if not filepath:
            return

        self.get_images_list(self.clear_path(filepath))
        try:
            self.current_image_index = self.image_list.index(filepath)
        except ValueError:
            self.current_image_index = 0
        self.draw_image(filepath)

    def choose_next(self):
        try:
            self.current_image_index += 1
            new_image = self.image_list[self.current_image_index]
        except IndexError:
            self.current_image_index = 0
            new_image = self.image_list[self.current_image_index]
        self.draw_image(new_image)

    def choose_prev(self):
        try:
            self.current_image_index -= 1
            new_image = self.image_list[self.current_image_index]
        except IndexError:
            self.current_image_index = len(self.image_list) - 1
            new_image = self.image_list[self.current_image_index]
        self.draw_image(new_image)

    def clear_path(self, path):
        buf = path.split("/")
        buf.pop()
        path = "/".join(buf)
        return path

    def get_images_list(self, dirpath):
        self.image_list = []
        for item in listdir(dirpath):
            for type_ in image_types:
                if type_ in item:
                    self.image_list.append(dirpath + '/' + item)

    def on_exit(self):
        self.destroy()


def main():
    img_name = " "
    if len(argv) > 1:
        img_name = argv[1]
    # app = ImageViewer(img_name)
    app = ImageViewer("tst.jpg")


if __name__ == '__main__':
    main()
