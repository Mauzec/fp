import os
import cv2
import numpy as np
import threading
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showerror, showinfo
import time

directory_input = ''
directory_output = ''
include_parametres = dict()

def is_error()->bool:
    global directory_output, directory_input
    if not directory_output or not directory_input:
        showerror(title="ошибка", message= "введите названия директорий")
        return 0
    elif sum(include_parametres.values()) == 0:
        showerror(title="ошибка", message="введите параметры")
        return 0
    elif not os.path.isdir(directory_input):
         showerror(title="ошибка", message=f"директория {directory_input} не найдена")
         return 0
    return 1
        
def safe_parametres():
    global directory_output, directory_input
    
    directory_input = Entry_input.get()
    directory_output = Entry_output.get()
    for line in include_column.keys():
        include_parametres[line] = int(include_column[line].get())
    
    showinfo(title="успешный успех", message="данные сохранены")
    
def generation_checkbutton(array_name)->dict:
    this_dict = dict()
    for line in array_name:
        this_dict[line] = tk.IntVar()
    return this_dict
# Функция для загрузки изображений из заданной директории
def load_images(directory):
    images = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            image = cv2.imread(image_path)
            images.append(image)
    return images

# Функция для разделения изображений на равные части
def split_image(image, num_parts):
    height, width, _ = image.shape
    part_width = (width // num_parts) + 1
    parts = []
    for i in range(num_parts):
        part = image[:, i * part_width:(i + 1) * part_width, :]
        parts.append(part)
    return parts

def process_image_part(k, image_part, filter_name, filtered_parts):
    if filter_name == "SHARPEN":
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        filtered_image_part = cv2.filter2D(image_part, -1, kernel)
    elif filter_name == "BLUR":
        filtered_image_part = cv2.GaussianBlur(image_part, (5, 5), 0)
    elif filter_name == "DECREASE":
        filtered_image_part = cv2.resize(image_part, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
    filtered_parts[k] = filtered_image_part

# Функция для сохранения обработанных изображений в новую директорию
def save_images(filtered_images, directory):
    name_file = os.listdir(directory_input)
    if not os.path.exists(directory):
        os.makedirs(directory)
    for i, image in enumerate(filtered_images):
        filename = f"{name_file[i][:name_file[i].find('.')]}_new{name_file[i][name_file[i].find('.'):]}"
        filepath = os.path.join(directory, filename)
        cv2.imwrite(filepath, image)

# Основная функция программы
def main():
    # Загрузка изображений из заданной директории
    if not is_error():
        showerror(title= "прерывание", message= "операция прервана")
        return

    # Разделение изображений на равные части для обработки каждым фильтром
    num_parts = 16
    image_parts = []
    for image in load_images(directory_input):
        parts = split_image(image, num_parts)
        image_parts.append(parts)

    # Создание фильтров
    filters = ["DECREASE", "SHARPEN", "BLUR"]
    translate = {
        "DECREASE": "Уменьшение",
        "SHARPEN": "Резкость",
        "BLUR": "Сглаживание"
    }
    for filter_name in filters:
        if (not include_parametres[translate[filter_name]]):
            continue
        filtered_images = []
        for parts in image_parts:
            threads = []
            filtered_parts = [0] * num_parts
            for i in range(0, num_parts):
                threads.append(threading.Thread(target=process_image_part, args=(i, parts[i], filter_name, filtered_parts)))
            for i in range(0, num_parts):
                threads[i].start()
            for i in range(0, num_parts):
                threads[i].join()
            threads.clear()
            filtered_images.append(filtered_parts.copy())
        image_parts = filtered_images.copy()
    filtered_images = []
    for image in image_parts:
            filtered_image = np.hstack(image)
            filtered_images.append(filtered_image)    
    save_images(filtered_images, directory_output)
    showinfo(title="успешный успех", message="изображения обработаны")
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("параллельная обработка изображений")
    
    root['background'] = "gray"
    root.resizable(False, False)
    
    my_font = ("Arial", 16) 
    
    style_frame = ttk.Style()
    style_frame.configure("CustomFrame.TFrame", background="white")
    style_way_frame = ttk.Style()
    style_way_frame.configure("Style.TFrame", background="gray")
    style_check_button = ttk.Style()
    style_check_button.configure("TCheckbutton", font=my_font, background="white", foreground="gray")
    style_button = ttk.Style()
    style_button.configure("TButton", font=my_font)
    style_label = ttk.Style()
    style_label.configure("TLabel", font=my_font, padding=10, foreground="white", background="gray")
    style_Entry = ttk.Style()
    style_Entry.configure("TEntry", padding=5, font=my_font, foreground="black", background="gray")
    
    main_menu = tk.Menu()


    obr = tk.Button(text="обработать изображения", command=main)
    obr.pack()
    sohr = tk.Button(text="сохранить параметры", command=safe_parametres)
    sohr.pack()
    
    write_name_file = ttk.Frame(root, style="Style.TFrame")
    write_name_file.pack()
    parametres = ttk.Frame(root, style="CustomFrame.TFrame")
    parametres.pack()
    name_check_button = ["Уменьшение", "Резкость", "Сглаживание"]
    include_column = generation_checkbutton(name_check_button)
    Check_button = {}
    filter_label = ttk.Label(parametres, style="TLabel", text="Выберите методы фильтрации")
    filter_label.grid(row=0, column=0)
    for line in name_check_button:
        Check_button[line] = ttk.Checkbutton(parametres, text=line, style="TCheckbutton", variable=include_column[line])
        Check_button[line].grid(sticky="w")
        
    label_in_out = ttk.Label(write_name_file, style="TLabel", text="Введите названия входных и выходных директорий")
    label_in_out.grid(row=0, column=0, columnspan=2)
    label_input = ttk.Label(write_name_file, style="TLabel", text="Директория ввода")
    label_input.grid(row=1, column=0)
    label_output = ttk.Label(write_name_file, style="TLabel", text="Директория вывода")
    label_output.grid(row=1, column=1)
    Entry_input = ttk.Entry(write_name_file, justify="center", width=30, style="TEntry")
    Entry_output = ttk.Entry(write_name_file, justify="center", width=30, style="TEntry")
    Entry_input.grid(row=2, column=0)
    Entry_output.grid(row=2, column=1)
  
    root.config(menu=main_menu)
    root.mainloop()