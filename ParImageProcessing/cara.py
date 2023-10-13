import os
import cv2
import numpy as np
import threading
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showerror, showinfo
import time
from tkinter import filedialog

from Processing import *

def select_input_folder():
    input_folder_path = filedialog.askdirectory()
    input_folder.set(input_folder_path)

def select_output_folder():
    output_folder_path = filedialog.askdirectory()
    output_folder.set(output_folder_path)

def apply_filters():
    processImages(input_folder.get(), output_folder.get(), resize_var.get().split("x"), sharpen_var.get(), sepia_var.get())

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image Filter App") # title
    
    root['background'] = "gray" # default backround color
    root.resizable(False, False) # no windows resize
    
    my_font = ("Arial", 16) # default font

    input_output_frame = tk.Frame(root)
    input_output_frame.pack(pady=10)
    
    input_folder = tk.StringVar(value="img")
    input_label = tk.Label(input_output_frame, text="Input Folder")
    input_label.pack(side=tk.LEFT, padx=10)

    input_folder_entry = tk.Entry(input_output_frame, width=50, textvariable=input_folder)
    input_folder_entry.pack(side=tk.LEFT)

    input_button = tk.Button(input_output_frame, text="Browse", command=select_input_folder)
    input_button.pack(side=tk.LEFT, padx=10)
    
    output_folder = tk.StringVar(value="wow")
    output_label = tk.Label(input_output_frame, text="Output Folder")
    output_label.pack(side=tk.LEFT, padx=10)

    output_folder_entry = tk.Entry(input_output_frame, width=50, textvariable=output_folder)
    output_folder_entry.pack(side=tk.LEFT)

    output_button = tk.Button(input_output_frame, text="Browse", command=select_output_folder)
    output_button.pack(side=tk.LEFT, padx=10)

    filters_frame = tk.Frame(root)
    filters_frame.pack(pady=10)

    resize_var = tk.StringVar(value="700x700")
    resize_checkbox = tk.Label(input_output_frame, text="Resize")
    resize_checkbox.pack(side=tk.LEFT, padx=10)
    resize_entry = tk.Entry(filters_frame, textvariable=resize_var)
    resize_entry.pack()

    sharpen_var = tk.BooleanVar(value=True)
    sharpen_checkbox = tk.Checkbutton(filters_frame, text="Sharben", variable=sharpen_var)
    sharpen_checkbox.pack(side=tk.LEFT, padx=10)

    sepia_var = tk.BooleanVar(value=True)
    sepia_checkbox = tk.Checkbutton(filters_frame, text="Sepia", variable=sepia_var)
    sepia_checkbox.pack(side=tk.LEFT, padx=10)

    start_button = tk.Button(root, text="Start", command=apply_filters)
    start_button.pack(pady=10)
    
    root.mainloop()