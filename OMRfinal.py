# ----------------------------------------------------------------------------------------------------
# -------------------------------------- DISENIO EXAMEN ----------------------------------------------

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import math 

# para dibujar las opciones 
def drawOptions(vecOpciones, x1, y1, radio, x2, y2, fuente, tamFuente, espX):
    for txtOpc in vecOpciones:
        c.setFont(fuente, tamFuente)
        c.circle(x1, y1, radio)
        c.drawString(x2, y2, txtOpc)
        x1+= radio*2+espX
        x2+= radio*2+espX
    return 0 


# para crear un pdf
nombrePDF = "hoja_respuestas_diseno.pdf"
w, h = A4
c = canvas.Canvas(nombrePDF, pagesize=A4)
margenL = 15

# ------------------ SECCION SUPERIOR - TITULO Y CI  
fuente = "Courier"
# fuente = "Times-Roman"
# fuente = "Helvetica-Bold"

# titulo
titulo = "HOJA DE RESPUESTAS"
tamanio_titulo = c.stringWidth(titulo, fuente, 20)
n = (w-tamanio_titulo)/2
c.setFont(fuente, 20)
c.drawString(n, h-30, titulo)

# ci
c.setFont(fuente, 15)
c.drawString(20, h-60, "CI: ")
#recuadro ci 
c.rect(margenL, h - 65, w-(margenL*2), 20)


# ------------------ SECCION INFERIOR - OPCIONES  
# 1. A B C D ... 
tamFuenteNro = 10
nroPreguntas = 100   #nro de preguntas a escribir 
tamFuenteOpc = 11
txtNro = "xxx."
tamanio_txtNro = c.stringWidth(txtNro, fuente, tamFuenteNro)
vecOpciones = ["A", "B", "C", "D"]
nroOpciones = len(vecOpciones)     #opciones A B C D E 
radio = 7           # radio de la burbuja 
espX = 5
espY = 5
# h1 -> linea intermedia entre las secciones 
h1 = (h*0.11) - radio-radio//2-espY
# h2 -> linea donde inicia la primera linea de opciones 
h2 = h - (h*0.11)
# calculamos el espacio (ancho y alto) que ocupara cada opcion 
WeidthBoxPregunta = tamanio_txtNro+nroOpciones*(radio*2+espX)
HighBoxPregunta = radio*2
#dibujar box question 
# c.rect(margenL, h2-radio/2, WeidthBoxPregunta, HighBoxPregunta)
nroPreguntas_x_columna = int(h2 // (HighBoxPregunta + espY))
nroColumnsMax = math.floor((w-(margenL*2))/WeidthBoxPregunta)
nroColumns = math.ceil(nroPreguntas / nroPreguntas_x_columna) 
if nroColumns > nroColumnsMax: 
    print("Nro de preguntas por hoja superado... ")
    nroColumns = nroColumnsMax
# reformulamos el margenL para centrar las columnas 
margenL_old = margenL
margenL = (w-(WeidthBoxPregunta+espX)*nroColumns)/2

# espX1 espY1 para circle
# espX2 espY2 para string
# espX3 espY3 para nro
espY1 = h2+radio/2
espY2 = h2
espY3 = h2
espX1 = margenL+tamanio_txtNro+espX+radio       # para el circulo 
espX2 = margenL+tamanio_txtNro+espX+radio/2     # para texto del circulo 
espX3 = margenL                                 # para el nro 

z=1
n2 = 0 
for n in range (1, nroPreguntas+1):
    c.setFont(fuente, tamFuenteNro)
    txtNro = str(n)+"."
    c.drawString(espX3, espY3, txtNro)
    espY3-= espY + radio*2 
    drawOptions(vecOpciones, espX1, espY1, radio, espX2, espY2, fuente, tamFuenteOpc, espX)
    espY1 -= espY+radio*2  
    espY2 -= espY+radio*2
    if (n==nroPreguntas_x_columna*z):
        z+=1
        espY3 = h2
        espX3+= WeidthBoxPregunta + espX 
        espY1 = h2+radio/2
        espY2 = h2
        espX1+= WeidthBoxPregunta + espX 
        espX2+= WeidthBoxPregunta + espX 
    if (n == (nroPreguntas_x_columna*nroColumns)):
        n2 = n
        break
c.showPage()
c.save()

# ----------------------------------------------------------------------------------------------------
# -------------------------------------- DE PDF A JPEG----------------------------------------------
from pdf2image import convert_from_path 
import os 
import cv2

# es necesario importar la libreria de esta manera 
poppler_path = r"C:\Users\mayra\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
pdf_path = r"C:\Users\mayra\OneDrive\Escritorio\RECONOCIMIENTO_EXAMENES\OMR\marcado.pdf"

images = convert_from_path(pdf_path=pdf_path, poppler_path=poppler_path, dpi=300)
folder = r"C:\Users\mayra\OneDrive\Escritorio\RECONOCIMIENTO_EXAMENES\OMR"
for i, img in enumerate(images): 
    img_name = f"img-{i}.jpeg"
    img.save(os.path.join(folder, img_name), "JPEG")

# ----------------------------------------------------------------------------------------------------
# -------------------------------------- RESIZE ----------------------------------------------

img = cv2.imread(r"C:\Users\mayra\OneDrive\Escritorio\RECONOCIMIENTO_EXAMENES\OMR\img-0.jpeg")
# img = cv2.resize(img, None, fx=0.2, fy=0.2) 
# cv2.imshow("img", img)
# cv2.waitKey(0)
w_copy = w
h_copy = h
h, w = img.shape[:2]

# cacular en porcentaje cuan grande o mas pequenio es esta imagen respecto a la imagen de disenio 
porcentaje = (100*h/h_copy)/100
margenL_porcentaje = margenL*porcentaje
margenL_porcentaje=round(margenL*porcentaje)
WeidthBoxPregunta_porcentaje = round(WeidthBoxPregunta*porcentaje)
HighBoxPregunta_porcentaje = round(HighBoxPregunta*porcentaje)
espX_porcentaje = round(espX*porcentaje)
espY_porcentaje = round(espY*porcentaje)

xTop = int(h1 * porcentaje)
xBottom = int(h-(margenL_old * porcentaje)-(espY*porcentaje))
# recortar la parte superior e inferior 
img = img[xTop:xBottom, :w]
# cv2.imshow("imagen recortada con porcentaje", img) 
# cv2.waitKey(0)
h, w = img.shape[:2]

# ----------------------------------------------------------------------------------------------------
# -------------------------------------- ANALISIS OMR ----------------------------------------------

import cv2
import respuestascorrectas 

def designarOpcion(matPuntos, limites):
    if len(matPuntos)==0:
        return -2   #significa no hay respuesta, -2 resp vacia 
    elif len(matPuntos)>1: 
        return -1   #significa que hay mas de una opc marcada, -1 error, preg descalificada
    else:  
        pt = matPuntos[0][0]
        for i in range(0, len(limites)-1):
            if limites[i] <= pt and pt <= limites[i+1]:
                return (i+1) 
        return -1   #posicion no valida, -1 preg descalificada


def obtenerRespuesta(img, limites):
    centers = []
    contornos = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contornos = contornos[0] if len(contornos) == 2 else contornos[1]

    # m00 area 
    # m10 coordenadas x
    # m01 coordenadas y
    for cntr in contornos:
        M = cv2.moments(cntr)
        if (M["m00"]>100 ):
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            pt = (cx,cy)
            centers.append(pt)
            # cv2.circle(img, (cx, cy), 20, (255, 255, 255 ), -1)
            # cv2.putText(img, "x: "+ str(cx) +" y: "+str(cy), (cx, cy), 1,1,(0,0,0), 1)
            # cv2.imshow("imagen con punto encontrado", img)
            # cv2.waitKey(0)
    # print("CENTERS", centers)
    return designarOpcion(centers, limites)


# filtrar colores de la iamgen 
colorMin = (0, 0, 0)
colorMax = (10, 10, 10)
thresh = cv2.inRange(img, colorMin, colorMax)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
# cerrar los circulos
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
# eliminar el ruido 
morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
img = morph

# cv2.imshow("thresh", thresh)
# cv2.imshow("morph", morph)

# vector de limites 
limites = []
j = (tamanio_txtNro+espX)*porcentaje
for i in range(0,nroOpciones+1):
    limites.append(j)
    j += (radio*2 + espX)*porcentaje

# segmentar la imagen en columnas  
vecImg = [] 
for f in range (margenL_porcentaje, w-margenL_porcentaje-10, WeidthBoxPregunta_porcentaje+espX_porcentaje):
    newimg = img[:h, f:f+WeidthBoxPregunta_porcentaje+espX_porcentaje]
    # cv2.imshow("columnas recortes", newimg)
    # cv2.waitKey(0)
    vecImg.append(newimg)

# segmentar cada columna en filas 
respuestas = [] 
count = 0
for k in vecImg:
    for f in range (espY_porcentaje,h+1,HighBoxPregunta_porcentaje+espY_porcentaje):
        count+=1
        newimg = k[f:f+HighBoxPregunta_porcentaje+espY_porcentaje, :w]
        # cv2.imshow("img", newimg)
        # cv2.waitKey(0) 
        # ahora ingresa a la funcion para obtener la coordenada y recibir que opcion es
        resp = obtenerRespuesta(newimg, limites)
        respuestas.append(resp)
        if (count == nroPreguntas): 
            break

print(respuestas)
# comparamos con la matriz de respuestas correctas
resultados=[]
i=0
for x in respuestas:
    if x > 0:
        if respuestascorrectas.respCorrectas[i][x] == 1:
            resultados.append(1)
        else:
            resultados.append(0)
    else: 
        resultados.append(0)
    i+=1

respT=resultados.count(1)
respF=resultados.count(0)
print(f"Total: {respT}/{respT+respF}")
cv2.waitKey(0)
