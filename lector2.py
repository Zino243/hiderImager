from PIL import Image
imageName = 'resultado.png'
image = Image.open(imageName)
image = image.convert("RGB")
ancho, alto = image.size  

for x in range(ancho):
    for y in range(alto):
        pixel  = image.getpixel((x,y))
        print(pixel)