
import os
import numpy as np
import time
from PIL import Image, ImageTk
import tkinter
import sys
from tkinter import messagebox
import pandas as pd
from PIL import Image, ImageTk
import tkinter
from extr import *
from back import *
from handlers import * 
'''
def images():
    im = []
    imagez = glob.glob("/Users/bartlomiejkos/Documents/ProgrammingNew/Python/show me your letters/clouds/*.jpg")
    for item in imagez:
        im.append(item)
    return sorted(im)
'''
store_df = pd.read_csv('/Users/bartlomiejkos/Documents/ProgrammingNew/Python/show me your letters/proj-letters-of-physics/db.csv')
store_df = store_df.sort_index()
msg = 'This time I prepared for you ' + str(len(store_df)) + ' summaries for Physics Today articles' + \
    '\n' + 'cool maps included'


class Application():
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry('600x1000')
        self.store_df = store_df
        self._images = images(self.store_df)
        self._titles = titles(self.store_df)
        self._summaries = summaries(self.store_df)
        self._numbers = numbers(self.store_df)
        
        
        self.position = 0
        self.root.title('letters of physics')

        self.root.bind("<Escape>", self.close)
        self.root.bind("<Left>", self.show_prev)
        self.root.bind("<Right>", self.show_next)

        self.start = messagebox.showinfo('Welcome', msg)

        self.next_button = tkinter.Button(self.root, text='next', command=self.show_next).pack()
        self.prev_button = tkinter.Button(self.root, text='previous', command=self.show_prev).pack()
        self.close_button = tkinter.Button(self.root, text='close', command=self.close).pack()
        self.run_back_button = tkinter.Button(self.root, text='run scraper', command=self.run_scraper).pack()

        self.nmbr = tkinter.StringVar()
        self.ttl = tkinter.StringVar()
        self.abstract = tkinter.StringVar()

        self.nmbr_lab = tkinter.Label(self.root, textvariable=self.nmbr).pack()
        self.ttl_lab = tkinter.Label(self.root, textvariable=self.ttl).pack()

        self.im_lab = tkinter.Label(self.root, image=None)
        self.im_lab.configure(borderwidth=0)
        self.im_lab.pack()
        
        self.sum_lab = tkinter.Label(self.root, textvariable=self.abstract, width=100, wraplength=500).pack()

        self.root.mainloop()



    # BUTTONS
    def run_scraper(self, ev=None):
        pages = scrape_em()
        for i in range(np.random.randint(10,20)):
            new = create_em(pages,i)
            m = make_precis(new[0])
            n = make_wdcld(new[0],i)
            self.store_df = to_df(self.store_df, i, new[1],n[1],m)
        self.store_df.to_csv('db.csv')
        l = len(self.store_df)
        msg = 'These are ' + str(l) +  ' the most fresh articles from Physics Today'
        self.msg = messagebox.showinfo('Info', msg)

    def close(self, ev=None):
        self.root.destroy()
    # IMAGES  

    def show_next(self, ev=None):
        fname = self.next_image()
        tname = self.next_title()
        sname = self.next_summary()
        nname = self.next_number()
        self.show_image(fname)        
        self.show_title(tname)
        self.show_summary(sname)
        self.show_number(nname)
        self.position += 1

    def show_prev(self, ev=None):
        fname = self.prev_image()
        tname = self.prev_title()
        sname = self.prev_summary()
        nname = self.prev_number()
        self.show_image(fname)        
        self.show_title(tname)
        self.show_summary(sname)
        self.show_number(nname)
        self.position -= 1

    def show_prev_image(self, ev=None):
        fname = self.prev_image()
        if not fname:
            return
        self.show_image(fname)

    def show_image(self, fname):
        self.original_image = Image.open(fname)
        self.place_image()

    def place_image(self):
        width, height = self.original_image.size
        self.image = self.original_image
        imgtoshow = ImageTk.PhotoImage(self.image)
        self.im_lab.configure(image=imgtoshow)
        self.im_lab.image = imgtoshow

    def next_image(self):
        if not self._images: 
            return None
        #self.position += 1
        self.position %= len(self._images)
        return self._images[self.position]

    def prev_image(self):
        if not self._images: 
            return None
        #self.position -= 1
        return self._images[self.position]
    # TITLES
    def show_next_title(self, ev=None):
        fname = self.next_title()
        if not fname:
            return
        self.show_title(fname)

    def show_prev_title(self, ev=None):
        fname = self.prev_title()
        if not fname:
            return
        self.show_title(fname)

    def next_title(self):
        if not self._titles: 
            return None
        #self.position += 1
        self.position %= len(self._titles)
        return self._titles[self.position]
    
    def prev_title(self):
        if not self._titles: 
            return None
        #self.position -= 1
        return self._titles[self.position]

    def show_title(self, fname):
        fname = self.clean_abstract(fname)
        self._title = fname
        self.place_title()

    def place_title(self):
        self.ttl.set(self._title)

    def show_next_number(self, ev=None):
        fname = self.next_number()
        if not fname:
            return
        self.show_number(fname)

    def show_prev_number(self, ev=None):
        fname = self.prev_number()
        if not fname:
            return
        self.show_number(fname)

    def next_number(self):
        if not self._numbers: 
            return None
        #self.position += 1
        self.position %= len(self._numbers)
        return self._numbers[self.position]
    
    def prev_number(self):
        if not self._numbers: 
            return None
        #self.position -= 1
        return self._numbers[self.position]

   

    def show_number(self, fname):
        self.num = fname
        self.place_number()

    def place_number(self):
        self.nmbr.set(self.num) 

    def clean_abstract(self, fname):
        fname = fname.replace('[', ' ')
        return fname
 

    def show_summary(self, fname):
        self._summary = fname
        #self._title = None
        self.place_summary()

    def place_summary(self):
        #titletoshow = self.title
        self.abstract.set(self._summary)
        #self.ttl_lab.configure(text=self._title)
        #self.ttl_lab.text = self._title

    def next_summary(self):
        if not self._summaries: 
            return None
        #self.position += 1
        self.position %= len(self._summaries)
        return self._summaries[self.position]
    
    def prev_summary(self):
        if not self._summaries: 
            return None
        #self.position -= 1
        return self._summaries[self.position]
    # SUMMARIES
   
if __name__ == '__main__': app=Application()