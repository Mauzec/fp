from Filters import *

import os
import time
from concurrent.futures import ProcessPoolExecutor

def combineImage(sharpenedImage, sepiaImage, outputFolder, nameImage):
    combinedPath = os.path.join(outputFolder, f"new_{nameImage}")

    sharpenedImage = Image.open(sharpenedImage)
    sepiaImage = Image.open(sepiaImage)
    combinedImage = Image.new("RGB", sepiaImage.size)

    combinedImage.paste(sharpenedImage, (0, 0))
    combinedImage.paste(sepiaImage, (0, 0))
    combinedImage.save(combinedPath)
    print(f"[{nameImage}]: combined")

def processImage(inputImage, outputFolder, size=(0,0), sharpened=False, sepia=False):
    nameImage = os.path.basename(inputImage)
    sharpenedOutput = os.path.join(outputFolder, f"sharpened_{nameImage}")
    sepiaOutput = os.path.join(outputFolder, f"sepia_{nameImage}")
    resizedOutput = os.path.join(outputFolder, f"resized_{nameImage}")

    if size[0] != 0:
        applyRezise(inputImage, resizedOutput, size)
    else:
        resizedOutput = inputImage

    # applySharpenFilter(resizedOutput, sharpenedOutput)
    # applySepiaFilter(resizedOutput, sepiaOutput)

    with ProcessPoolExecutor() as executor:
        sh = True
        if sharpened:
            sh = executor.submit(applySharpenFilter, resizedOutput, sharpenedOutput)

    with ProcessPoolExecutor() as executor:
        se = True
        if sepia:
            se = executor.submit(applySepiaFilter, resizedOutput, sepiaOutput)

    # combineImage(sharpenedOutput, sepiaOutput, outputFolder, nameImage)

    if sharpened and sepia:
        sh.result()
        se.result()
        combineImage(sharpenedOutput, sepiaOutput, outputFolder, nameImage)
    elif sharpened:
        sh.result()
        combineImage(sharpenedOutput, sharpenedOutput, outputFolder, nameImage)
    elif sepia:
        se.result()
        combineImage(sepiaOutput, sepiaOutput, outputFolder, nameImage)

def processImages(inputFolder, outputFolder, size = (0, 0), sharpened=False, sepia=False):
    os.makedirs(outputFolder, exist_ok=True)
    imageFiles = [os.path.join(inputFolder, file) for file in os.listdir(inputFolder) if file.endswith((".jpg", ".png"))]

    with ProcessPoolExecutor() as executor:
        for imageFile in imageFiles:
            executor.submit(processImage, imageFile, outputFolder, size, sharpened, sepia)

    # for imageFile in imageFiles:
    #     processImage(imageFile, outputFolder, size, sharpened, sepia)
        

    print("All done")

