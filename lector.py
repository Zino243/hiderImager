from PIL import Image
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, default='', help='ruta de la imagen a modificar')
    parser.add_argument('-t', type=str, default='', help='ruta del texto o programa a convertir dentro de la imagen')
    parser.add_argument('-n', type=str, default='', help='nombre del producto final')
    args = parser.parse_args()
    
    convertImageWithData(args.i,args.t,args.n)
# funcion a devolver cuantos kb son modificables en la imagen
def howMuchKBtoImg(image):
    ancho, alto = image.size
    KBinImage = (ancho * alto) * 3           # cantidad de bits modificables
    KBinImage = (KBinImage / 8) / 1024       # cantidad de KB modificables
    return KBinImage
# codificador de texto a binario
def textToBin(input_file):
    with open(input_file, 'r') as file:                                     #guardamos el archivo en la variable file
        text = file.read()                                                  #
        binary_text = ''.join(format(ord(char), '08b') for char in text)    # lo convertimos en binario caracter a caracter
        output_file = 'outputfile.bin'                                      # creamos la variable con el nombre del futuro bin
        with open(output_file, 'wb') as bin_file:                           # creamos la variable donde escribiremos el binario
            bin_file.write(bytes(binary_text, 'utf-8'))                     # escribimos el binario
        return binary_text                                                  # retornamos el binario en crudo por si lo usamos   
# decodificador de binario a texto
def binToText(binary):
    with open(binary, 'rb') as binary:                                      # guardamos el binario en una variable binary
        bin_text = binary.read().decode('utf-8')                            # leemos y decodificamos en utf8
        text = ''.join(chr(int(bin_text[i:i+8], 2)) for i in range(0, len(bin_text), 8)) #dividimos el binario de 8 en 8 para ir byte por byte decodificanod 1 a 1 los char
        return text                                                         # retornamos text resuelto por si lo usamos
    
def convertImageWithData(imageName,textConvert,finalImageName):

    image = Image.open(imageName)
    image = image.convert("RGB")                         # pasamos a RGB para poder modificarla
    ancho, alto = image.size                             # guardamos en las variables su alto y ancho    
    dataBinInKB = len(binToText('outputfile.bin'))/8/1024

    if dataBinInKB > howMuchKBtoImg(image):
        print("el binario es mas grande que la imagen a modificar")
        print(f"""
    ->  el valor del binario {dataBinInKB} KB
    ->  el valor de la imagen es {howMuchKBtoImg(image)}""")
    else:

        h = 0
        binaries = textToBin(textConvert)
        while h < len(binaries):
            for x in range(ancho):
                for y in range(alto):
                    
                    pixel = image.getpixel((x, y))
                    new_pixel = ()
                    for i in range(3):
                        if h < len(binaries):
                            aux = format(pixel[i], '08b')
                            aux = aux[:7] + binaries[h]
                            new_pixel += tuple([int(aux,2)])
                            h += 1
                    if len(new_pixel) == 3:
                        image.putpixel((x,y), new_pixel)
                    if len(new_pixel) < 3:
                        len_pixel = len(new_pixel)
                        for _ in range(3 - len_pixel):
                            new_pixel = tuple(new_pixel + (0,))
                            
                    #print(f"{pixel}->{new_pixel}")
        print("done!")
        image.save(finalImageName + ".png")
        image.close()

if __name__ == "__main__":
    main()