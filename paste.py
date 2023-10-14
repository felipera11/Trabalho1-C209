import cv2
import numpy as np
from PIL import Image
import numpy as np
import os

def convert(backgroundDIR, personDIR):

    #define o diretório das imagens
    imageDir = personDIR
    imageBackgroundDir = backgroundDIR

    #pega o tamanho da imagem
    with Image.open(imageDir) as img:
        xres, yres = img.size

    #armazena a imagem em uma variável
    image = cv2.imread(imageDir)

    #adiciona um canal alpha caso a imagem nao tiver
    if image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    #faz um clone da imagem sem canal alpha para ser usado no grabcut
    image_grabcut = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    #faz uma máscara de zeros do tamanho da imagem
    mask = np.zeros(image.shape[:2], np.uint8)

    #cria os arrays de background e foreground
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)

    #define o retângulo de onde o grabcut vai pegar a imagem
    rect = (1,1,xres-1,yres-1)

    #aplica o grabcut na imagem
    cv2.grabCut(image_grabcut, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    #cria uma mascara com o background em 0 e o foreground em 1
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')

    #o canal alpha da imagem recebe a mascara e seta o background como transparente
    image[...,3] = mask2 * 255

    #salva o resultado
    cv2.imwrite('output.png', image)

    imagePersonDir = 'output.png'

    #abre as novas imagens
    cropImg = Image.open(imagePersonDir)
    backG = Image.open(imageBackgroundDir)

    #pega o tamanho do background
    bXres, bYres = backG.size

    #a imagem de pessoa é convertida para um array numpy
    personArray = np.array(cropImg)

    #pega o tamanho do array
    pYres, pXres, pCres = personArray.shape

    #calcula a escala da imagem de pessoa para ficar com 70% do tamanho do background
    scale = (bYres/pYres)*0.7

    #cria uma nova imagem da pessoa escalonada
    imgEscalonada = np.zeros(shape=(int(pYres * scale), int(pXres * scale), pCres), dtype=np.uint8)

    for i in range(int(pYres*scale)):
        for j in range(int(pXres*scale)):
            new_y = int(np.floor(i * (pYres / (int(pYres*scale)))))
            new_x = int(np.floor(j * (pXres / (int(pXres*scale)))))
            
            imgEscalonada[i, j] = personArray[new_y, new_x]

    #o array é convertido de volta em uma imagem
    pessoaFinal = Image.fromarray(imgEscalonada)

    #pega o tamanho da imagem escalonada
    finalXres, finalYres = pessoaFinal.size

    #cola a imagem escalonada no centro do background
    backG.paste(pessoaFinal, (int((bXres/2)-(finalXres/2)), bYres-finalYres), pessoaFinal)
    
    #salva o resultado final
    backG.save('result.png')
    os.remove('output.png')
