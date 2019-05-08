import glob
import os
import sys
import time
from PIL import Image, ImageTk
import tkinter

def images():
    im = []
    imagez = glob.glob("/Users/bartlomiejkos/Documents/ProgrammingNew/Python/show me your letters/clouds/*.jpg")
    for item in imagez:
        im.append(item)
    return sorted(im)

class Application():
    def __init__(self):
        self.root = tkinter.Tk()
        self._images = images()
        self.position = -1

        self.root.bind("<Escape>", self.close)
        self.root.bind("<Left>", self.show_prev_image)
        self.root.bind("<Right>", self.show_next_image)

        self.label = tkinter.Label(self.root, image=None)
        self.label.configure(borderwidth=0)
        self.label.pack()
        self.next_button = tkinter.Button(self.root, text='next', command=self.show_next_image).pack()
        self.prev_button = tkinter.Button(self.root, text='previous', command=self.show_prev_image).pack()
        self.close_button = tkinter.Button(self.root, text='close', command=self.close).pack()

        self.root.mainloop()


    def close(self, ev=None):
        self.root.destroy()

    def show_next_image(self, ev=None):
        fname = self.next_image()
        if not fname:
            return
        self.show_image(fname)

    def show_prev_image(self, ev=None):
        fname = self.prev_image()
        if not fname:
            return
        self.show_image(fname)

    def show_image(self, fname):
        self.original_image = Image.open(fname)
        self.image = None
        self.place_image()

    def place_image(self):
        width, height = self.original_image.size
        self.image = self.original_image
        imgtoshow = ImageTk.PhotoImage(self.image)
        self.label.configure(image=imgtoshow)
        self.label.image = imgtoshow

    def next_image(self):
        if not self._images: 
            return None
        self.position += 1
        self.position %= len(self._images)
        return self._images[self.position]

    def prev_image(self):
        if not self._images: 
            return None
        self.position -= 1
        return self._images[self.position]

if __name__ == '__main__': app=Application()