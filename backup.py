from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from itertools import cycle
import os

# tk = Tk()
#
# img = ImageTk.PhotoImage(Image.open("tst.png"))
# b = Label(image=img)
# b.pack()
#
# tk.mainloop()

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
        self.get_images_list()
        self.current_image_index = self.image_list.index(self.image)
        # print(self.image_list, self.current_image_index)
        self.init_ui()
        self.draw_image(self.image)
        self.mainloop()

    def init_ui(self):
        self.title("Image Viewer")
        self.minsize(200, 200)
        self.geometry("900x700+500+150")
        self.config(menu=self.menu)
        self.menu_tab_file.add_command(label="Open", underline=0, command=self.open_image)
        self.menu_tab_file.add_separator()
        self.menu_tab_file.add_command(label="Exit", underline=1, command=self.on_exit)
        self.menu.add_cascade(label="File", underline=0, menu=self.menu_tab_file)

        self.field_image.config(width=100, height=100)
        self.field_button.config(width=100)
        self.button_next.config(text="Next", width=7,  command=self.choose_next)
        self.button_prev.config(text="Previous", width=7,  command=self.choose_prev)

        self.field_button.pack(side=BOTTOM)
        self.button_next.pack(side=RIGHT, padx=5, pady=1)
        self.button_prev.pack(side=LEFT, padx=5, pady=1)



    def draw_image(self, image):
        try:
            self.img = ImageTk.PhotoImage(Image.open(image))
        except Exception:
            pass
        self.canva_image = self.field_image.create_image(0, 0, anchor='nw', image=self.img)
        self.field_image.pack(fill=BOTH, expand=1)
        self.title(f"Image Viewer | {image}")

    def open_image(self):
        filepath = askopenfilename(filetypes=[("All files", "*"), ("Png files", "*.png"), ("Jpg files", "*.jpg"), ("Jpeg files", "*.jpeg"), ("GIF files", "*.gif")])
        if not filepath:
            return
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

    def get_images_list(self):
        self.image_list = []
        for item in os.listdir():
            for type_ in image_types:
                if type_ in item:
                    self.image_list.append(item)

    def on_exit(self):
        self.destroy()


def main():
    app = ImageViewer()


if __name__ == '__main__':
    main()
