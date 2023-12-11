
'''
for output
'''
from matplotlib import pyplot as plt 
import tkinter as tk 
from tkinter import filedialog

'''
skimage to work with the image
'''
from skimage import io
from skimage.color import rgb2gray
from skimage.feature import blob_log
from skimage.segmentation import felzenszwalb, mark_boundaries
import numpy as np
from multiprocessing import Pool

from PIL import Image, ImageDraw

import time

def count_stars_for(image_path: str, part: int) -> (int, list):
    img = io.imread(image_path)
    image_gray = rgb2gray(img) # convert the image to black and white for its simplicity
    print('gray got', part)

    segments = felzenszwalb(image_gray, scale=200, sigma=.5, min_size=100)
    segments_ids = np.unique(segments)
    print(segments_ids)

    dict_seg = {}
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            seg = segments[i, j]
            if seg not in dict_seg.keys():
                dict_seg[seg] = 1
                continue
            dict_seg[seg] += 1

    max_l = max(dict_seg, key=dict_seg.get)
    print(max_l)
    blobs_log = blob_log(image_gray, max_sigma=30, num_sigma=10, threshold=.05)    

    stars_count = 0
    xyr = []
    for blob in blobs_log:
        y, x, r = blob
        

        if segments[int(y), int(x)] == max_l:
            stars_count += 1
            xyr.append((x,y,r*2))
      
    return (stars_count, xyr)

class ImageProcessorApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Image Processor')

        self.image_path = None

        self.browse_button = tk.Button(self.master, text='Browse Image', command=self.browse_image)
        self.browse_button.pack(pady=10)

        self.image_label = tk.Label(self.master)
        self.image_label.pack()

        self.start_button = tk.Button(self.master, text='Start', command=self.process_image)
        self.start_button.pack(pady=10)

        self.result_label = tk.Label(self.master, text='')
        self.result_label.pack()

    def browse_image(self):

        self.image_path = filedialog.askopenfilename()
  

    def process_image(self):
        start_time = time.time()
        if self.image_path:
            image_path = self.image_path
            original_image = Image.open(image_path)

            width, height = original_image.size

            region_width = width//4
            region_height = height//2
        
            args = []
            for i in range(2):
                for j in range(4):
                    left = j * region_width
                    top = i * region_height
                    right = left + region_width
                    bottom = top + region_height

                    part = original_image.crop((left, top, right, bottom))
                    part.save(f'Part{i*4 + j + 1}.png', quality=100, format='PNG')
                    args.append( (f'Part{i*4 + j + 1}.png', i*4 + j + 1) )
        
            stars_count = 0
            
            xyr = list()
            with Pool(processes=2) as pool:
                results = pool.starmap(count_stars_for, args)

                for result in results:
                    stars_count += result[0]
                    xyr.append(result[1])
                    
            print(stars_count)

            combined_image = Image.new("RGB", (region_width * 4, region_height * 2))
            for i in range(2):
                for j in range(4):
                    left = j * region_width
                    top = i * region_height
                    combined_image.paste(Image.open(args[i * 4 + j][0]), (left, top))
            for i in range(2):
                for j in range(4):
                    left = j * region_width
                    top = i * region_height
                    
                    for x,y,r in xyr[i * 4 + j]:
                        x += left
                        y += top
                        draw = ImageDraw.Draw(combined_image)
                        draw.ellipse([ (x - r, y - r), (x + r, y + r) ], outline=(255,255,255))
            
            print('TIME:', time.time() - start_time)
                
            combined_image.save("combined.png", quality=100, format='PNG')

            self.result_label.config(text=f'Result: {stars_count}')

            photo = tk.PhotoImage(file="combined.png")
            self.image_label.config(image=photo)
            self.image_label.image = photo




if __name__ == '__main__':
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()

 


