from PIL import Image, ImageFilter

def applySharpenFilter(inputImage, outputImage):
    img = Image.open(inputImage)
    sharpenedImg = img.filter(ImageFilter.SHARPEN)
    sharpenedImg.save(outputImage)
    print(f"[{outputImage}]: Sharpen done")
    return outputImage

def applySepiaFilter(inputImage, outputImage):
    img = Image.open(inputImage)
    width, height = img.size
    sepiaImg = img.copy()

    for i in range(width):
        for j in range(height):
            r, g, b = img.getpixel((i, j))
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            tr = min(255, max(0, tr))
            tg = min(255, max(0, tg))
            tb = min(255, max(0, tb))

            sepiaImg.putpixel((i,j), (tr, tg, tb))
    sepiaImg.save(outputImage)
    print(f"[{outputImage}]: Sepia done")

    return outputImage

def applyRezise(inputImage, outputImage, size):
    img = Image.open(inputImage)
    resizedImg = img.resize(size)
    resizedImg.save(outputImage)
    print(f"[{outputImage}]: Resize {size[0]}x{size[1]} done")

