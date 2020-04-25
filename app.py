# Credits to The Come Up for the tutorial!  Follow her original video here:  https://youtu.be/IrZ58M8BgcA

import os
import random

import tkinter as tk
from PIL import Image, ImageTk
from playsound import playsound


WINDOW_TITLE = 'My Wardrobe'
WINDOW_HEIGHT = 650
WINDOW_WIDTH = 220
IMG_WIDTH = 250
IMG_HEIGHT = 250
SOUND_EFFECT_FILE_PATH = ""

# store all the Tops into a file we can access.
# Compile a list of 'tops' images in this section.
ALL_TOPS = [str('images/tops/') + imagefile for imagefile in os.listdir('images/tops/') if not imagefile.startswith('.')]
ALL_BOTTOMS = [str('images/bottoms/') + imagefile for imagefile in os.listdir('images/bottoms/') if not imagefile.startswith('.')]


class WardrobeApp:
    def __init__(self, root):
        self.root = root

        # show top and bottom images in the window
        self.top_images = ALL_TOPS
        self.bottom_images = ALL_BOTTOMS

        # display single top and bottom
        self.top_image_path = self.top_images[0]
        self.bottom_image_path = self.bottom_images[0]

        # create and add top and bottom images into Frame
        self.tops_frame = tk.Frame(self.root)
        self.top_image_label = self.create_photo(self.top_image_path, self.tops_frame)

        self.bottom_frame = tk.Frame(self.root)
        self.bottom_image_label = self.create_photo(self.bottom_image_path, self.bottom_frame)

        # add it to pack
        self.top_image_label.pack(side=tk.TOP)
        self.bottom_image_label.pack(side=tk.TOP)

        # create background
        self.create_background()

    def create_background(self):

        # add title to window and change the size of the window
        self.root.title(WINDOW_TITLE)
        self.root.geometry('{0}x{1}'.format(WINDOW_WIDTH, WINDOW_HEIGHT))

        # add all buttons
        self.create_buttons()

        # add clothing
        self.tops_frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.bottom_frame.pack(fill=tk.BOTH, expand=tk.YES)


    def create_buttons(self):
        top_prev_button = tk.Button(self.tops_frame, text='Prev', command=self.get_next_top)
        top_prev_button.pack(side=tk.LEFT)

        top_next_button = tk.Button(self.tops_frame, text='Next', command=self.get_prev_top)
        top_next_button.pack(side=tk.RIGHT)

        bottom_prev_button = tk.Button(self.bottom_frame, text='Prev', command=self.get_next_bottom)
        bottom_prev_button.pack(side=tk.LEFT)

        bottom_next_button = tk.Button(self.bottom_frame, text='Next', command=self.get_prev_bottom)
        bottom_next_button.pack(side=tk.RIGHT)

        create_outfit_button = tk.Button(self.bottom_frame, text='Create Outfit', command=self.create_outfit)
        create_outfit_button.pack(side=tk.RIGHT)

    # general function that will allow us to move front and back
    def _get_next_item(self, current_item, category, increment = True):

        # if we know where the current item index is in a category, then we can find the pic before/after current index
        item_index = category.index(current_item)
        final_index = len(category) -1
        next_index = 0

        # consider the edge cases
        if increment and item_index==final_index:
            # add the end, and need to up, cycle back to beginning
            next_index = 0
        elif not increment and item_index==0:
            # cycle back to end
            next_index = final_index
        else:
            # regular up and down
            # based on increment
            increment = 0 if increment else -1
            next_index =item_index + increment

        next_image = category[next_index]

        # reset and update the image based on next_image path
        if current_item in self.top_images:
            image_label = self.top_image_label
            self.top_image_path = next_image

        else:
            image_label = self.bottom_image_label
            self.bottom_image_path = next_image

        # use update function to change the image
        self.update_image(next_image, image_label)


    def update_image(self, new_image_path, image_label):
        # use pillow to change the image to a way tkinter can understand
        image_file = Image.open(new_image_path)
        image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
        tk_photo = ImageTk.PhotoImage(image_resized)

        # instead of using new label, update the label using 'configure'
        image_label.configure(image=tk_photo)

        # weird tkinter quirk
        image_label.image = tk_photo


    def get_next_top(self):
        self._get_next_item(self.top_image_path, self.top_images)

    def get_prev_top(self):
        self._get_next_item(self.top_image_path, self.top_images, increment=False)

    def get_next_bottom(self):
        self._get_next_item(self.bottom_image_path, self.bottom_images)

    def get_prev_bottom(self):
        self._get_next_item(self.bottom_image_path, self.bottom_images, increment=False)



    # function that allows you to add image
    def create_photo(self, image_path, frame):
        image_file = Image.open(image_path)
        image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
        tk_photo = ImageTk.PhotoImage(image_resized)
        image_label = tk.Label(frame, image=tk_photo, anchor=tk.CENTER)

        # weird tkinter quirk
        image_label.image = tk_photo

        return image_label

    def create_outfit(self):
        # random selecting top and bottom
        new_top_index = random.randint(0,len(self.top_images))
        new_bottom_index = random.randint(0,len(self.bottom_images))

        # update clothes onto screen
        self.update_image(self.top_images[new_top_index], self.top_image_label)
        self.update_image(self.bottom_images[new_bottom_index], self.bottom_image_label)

        # add sound
        playsound(SOUND_EFFECT_FILE_PATH)


root = tk.Tk()
print(ALL_TOPS)
app = WardrobeApp(root)
root.mainloop()